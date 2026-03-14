# main.py
from agents.Orchestrator_Agent import *
from agents.Response_Agent import *
from agents.Planning_Agent import *
from tools.get_food import *
from tools.get_restaurant import *
from tools.get_destination import *
from tools.weather_tool import get_weather
from tools.get_hotel import get_hotel
from tools.get_service import get_service
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Initialize the FastAPI application
app = FastAPI(title="Quy Nhon AI Tour Guide API", description="API cho trợ lý du lịch ảo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/chat-planner", StaticFiles(directory="frontend/chat-planner", html=True), name="chat_planner")

@app.get("/")
def redirect_to_chat_planner():
    return RedirectResponse(url="/chat-planner")

class ChatRequest(BaseModel):
    user_prompt: str

# ==========================================
# LOGIC FUNCTIONS
# ==========================================
def get_context(user_prompt):
    """
    Identifies the user's intent and gathers relevant data from tools 
    to build the context for the response agent.
    """
    planning_flag = False
    routing_json_string = get_routing_from_orchestrator(user_prompt)
    print("Orchestrator Routing:", routing_json_string)

    try:
        routing_dict = json.loads(routing_json_string)
    except json.JSONDecodeError:
        print("Error: The routing JSON string is not valid. Please check the format!")
        routing_dict = {}

    context = ""

    # If do not need to call tools
    if "chat" in routing_dict:
        return {"planning_flag": False, "context": ""}
    
    # Check for 'food' intent and fetch relevant data
    if "food" in routing_dict:
        food_data = routing_dict.get("food", {}) 
        type_of_food = food_data.get("type_of_food")
        filter_tags = food_data.get("filter_tags")
        food_context = get_food_list(type_of_food, filter_tags)
        context += f"\nThông tin về món ăn:\n{food_context}\n"

    # Check for 'restaurant' intent and fetch relevant data
    if "restaurant" in routing_dict:
        restaurant_data = routing_dict.get("restaurant", {})
        filter_tags = restaurant_data.get("filter_tags")
        restaurant_context = get_restaurant(filter_tags)
        context += f"\nThông tin về nhà hàng:\n{restaurant_context}\n"

    # Check for 'destination' intent and fetch relevant data
    if "destination" in routing_dict:
        destination_data = routing_dict.get("destination", {})
        filter_tags = destination_data.get("filter_tags")
        destination_context = get_destination(filter_tags)
        context += f"\nThông tin về địa điểm:\n{destination_context}\n"

    # Check for 'weather' intent and fetch weather data
    if "weather" in routing_dict:
        weather_data = routing_dict.get("weather", {})
        location = weather_data.get("location")

        df_destination = get_destination(location)

        if not df_destination.empty:
            row = df_destination.iloc[0]
            lat = row["gps_lat"]
            lon = row["gps_lon"]

            weather = get_weather(lat, lon)

            if "error" not in weather:
                context += (
                    f"\nThông tin thời tiết tại {row['name']}:\n"
                    f"- Nhiệt độ: {weather['temperature']}°C\n"
                    f"- Tốc độ gió: {weather['windspeed']} km/h\n"
                )
            else:
                context += "\nKhông thể lấy thông tin thời tiết hiện tại.\n"
        else:
            context += "\nKhông tìm thấy địa điểm để kiểm tra thời tiết.\n"

    # Check for 'planning' intent (itinerary generation)
    if "hotel" in routing_dict:
        hotel_data = routing_dict["hotel"]

        location = hotel_data.get("location")
        max_price = hotel_data.get("max_price")

        df_result = get_hotel(location=location, max_price=max_price)

        if df_result.empty:
            context += "\nKhông tìm thấy khách sạn phù hợp.\n"
        else:
            context += "\nKhách sạn gần nhất:\n"
            context += df_result.to_string(index=False)

    # Check for 'service' intent and fetch relevant data
    if "service" in routing_dict:
        service_data = routing_dict.get("service", {})
        location = service_data.get("location")
        filter_tags = service_data.get("filter_tags")

        service_result = get_service(location=location, filter_tags=filter_tags)

        if service_result["status"] == "not_found":
            context += f"\n{service_result['message']}\n"

        elif service_result["status"] == "empty":
            context += f"\nKhông tìm thấy dịch vụ phù hợp tại {location}.\n"

        else:
            context += f"\nThông tin dịch vụ tại {location}:\n"
            for s in service_result["services"]:
                context += (
                    f"- {s['name']} | Giá: {s['price']} VNĐ\n"
                    f"  {s['description']}\n"
                )

        # Check for 'hotel' intent and fetch relevant data
    if "planning" in routing_dict:
        planning_flag = True
        planning_data = routing_dict.get("planning", {})
        
        # Set default values if not provided
        time = planning_data.get("time") or "3 ngày"
        budget = planning_data.get("budget") or "5 triệu"
        prefer = planning_data.get("prefer") or "hải sản, biển"

        destination_context = get_destination(prefer)
        restaurant_context = get_restaurant(prefer)
        
        # Build structured context for the Planning Agent
        context += f"\n=========================================\n"
        context += f"YÊU CẦU LẬP LỊCH TRÌNH:\n"
        context += f"- Thời gian: {time}\n"
        context += f"- Ngân sách: {budget}\n"
        context += f"- Ưu tiên/Phong cách: {prefer}\n\n"
        context += f"NGUYÊN LIỆU GỢI Ý (Chỉ dùng các dữ liệu dưới đây để xếp lịch):\n\n"
        context += f"[1. ĐỊA ĐIỂM THAM QUAN]\n{destination_context}\n\n"
        context += f"[2. NHÀ HÀNG / QUÁN ĂN]\n{restaurant_context}\n\n"
        context += f"=========================================\n"
    
    return {"planning_flag" : planning_flag, "context" : context}

def get_response(user_prompt: str, context: dict):
    """
    Routes the prompt to either the general Response Agent or the Planning Agent
    based on the planning_flag.
    """
    end_context = context["context"]
    final_user_prompt = user_prompt + f"\nSau đây là các thông tin liên quan cho bạn tham khảo:\n{end_context}"
    
    if context["planning_flag"] == False:
        # Standard chat response
        end_response = get_agent_response(final_user_prompt)
    else:
        # Itinerary generation response
        end_response = get_planning_agent_response(final_user_prompt)

    return {"agent_response" : end_response}

# if __name__ == "__main__":
#     test_prompt = "Gợi ý quán hải sản ngon ở Quy Nhơn"
#     context = get_context(test_prompt)
#     response = get_response(test_prompt, context)
#     print(response)

# ==========================================
# API ENDPOINTS
# ==========================================
@app.post("/api/chat")
def api_get_answer(request: ChatRequest):
    """
    Primary endpoint for processing user chat requests and returning AI-generated answers.
    """
    try:
        # 1. Fetch context based on intent
        ctx = get_context(request.user_prompt)
        
        # 2. Generate final response from agents
        result = get_response(request.user_prompt, ctx)
        
        return {
            "status": "success",
            "data": result["agent_response"]
        }
        
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(status_code=500, detail=f"System error: {str(e)}")