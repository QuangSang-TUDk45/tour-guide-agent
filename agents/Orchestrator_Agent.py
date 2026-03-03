# agents/Orchestrator Agent
import os
import json
from typing import Optional, Union, Literal
from pydantic import BaseModel, ValidationError, RootModel

from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# LLM SETUP AND CONFIGURATION
# ==========================================
HF_TOKEN = os.getenv("HF_TOKEN")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# ===============================
# SCHEMA DEFINITIONS
# ===============================

class FoodModel(BaseModel):
    type_of_food: Optional[Literal["món chính", "món phụ", "đồ ăn vặt", "đồ tráng miệng", "đồ uống"]] = None
    filter_tags: str

class RestaurantModel(BaseModel):
    filter_tags: str

class DestinationModel(BaseModel):
    filter_tags: str

class PlanningModel(BaseModel):
    time: Optional[str] = None
    budget: Optional[str] = None
    prefer: Optional[str] = None

class WeatherModel(BaseModel):
    location: str

class HotelModel(BaseModel):
    location: Optional[str] = None
    max_price: Optional[int] = None

class ServiceModel(BaseModel):
    location: str
    filter_tags: Optional[str] = None

class ChatModel(BaseModel):
    pass


# Root schema – EXACTLY ONE key allowed
class OrchestratorOutput(BaseModel):
    food: Optional[FoodModel] = None
    restaurant: Optional[RestaurantModel] = None
    destination: Optional[DestinationModel] = None
    planning: Optional[PlanningModel] = None
    weather: Optional[WeatherModel] = None
    hotel: Optional[HotelModel] = None
    service: Optional[ServiceModel] = None
    chat: Optional[ChatModel] = None

    def model_post_init(self, __context):
        # Count how many intents are not None
        fields = [
            self.food,
            self.restaurant,
            self.destination,
            self.planning,
            self.weather,
            self.hotel,
            self.service,
            self.chat
        ]
        if sum(f is not None for f in fields) != 1:
            raise ValueError("Response must contain EXACTLY ONE top-level key.")

# ==========================================
# PROMPT LOADING
# ==========================================
# Read the system prompt from the specified text file
with open(r"prompts\orchestrator_agent.txt", 'r', encoding='utf-8') as file:
    system_prompt = file.read()

# ==========================================
# CORE LOGIC FUNCTIONS
# ==========================================
def get_route_json(user_prompt):
    """
    Sends the user's prompt to the LLM and retrieves the raw content response.
    """
    completion = client.chat.completions.create(
        model="Qwen/Qwen2.5-7B-Instruct:together",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
    )
    agent_response = completion.choices[0].message.content
    return agent_response

def validate_route_json(agent_response, current_prompt):
    try:
        # Validate full orchestrator schema
        OrchestratorOutput.model_validate_json(agent_response)

        return {
            "res": "successfully"
        }

    except ValidationError as e:
        new_prompt = current_prompt + f"\nLưu ý đừng mắc lỗi sau nhé:\n{e}"
        return {
            "res": "failed",
            "user_prompt": new_prompt
        }

    except Exception as e:
        new_prompt = current_prompt + f"\nLưu ý đừng mắc lỗi sau nhé:\n{e}"
        return {
            "res": "failed",
            "user_prompt": new_prompt
        }
    
def get_routing_from_orchestrator(user_prompt: str):
    """
    Main entry point for the Orchestrator. 
    Includes a retry mechanism to handle schema validation failures.
    """
    max_retries = 1
    for attempt in range(max_retries):
        # 1. Fetch raw JSON response from LLM
        agent_response = get_route_json(user_prompt)
        
        # 2. Validate response against schema
        valid_status = validate_route_json(agent_response, current_prompt=user_prompt)
        
        # 3. Check validation results
        if valid_status["res"] == "successfully":
            return agent_response # Return correct JSON immediately
        else:
            # If validation fails, update prompt with error and retry
            user_prompt = valid_status["user_prompt"]

    # If retries are exhausted, return the last generated response as a fallback
    return agent_response

# Example usage:
# print(get_routing_from_orchestrator(user_prompt="Bạn có thể đề xuất cho tôi các món ăn trưa ở Qui Nhơn không?"))