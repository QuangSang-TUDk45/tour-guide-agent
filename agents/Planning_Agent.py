# agents/Planning Agent
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# LLM SETUP AND CONFIGURATION
# ==========================================
# Initialize the OpenAI client using Hugging Face's router
HF_TOKEN = os.getenv("HF_TOKEN")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# ==========================================
# PROMPT LOADING
# ==========================================
# Read the specialized system prompt for the Planning Agent
# This prompt defines how the agent should structure itineraries
with open(r"prompts\planning_agent.txt", 'r', encoding='utf-8') as file:
    system_prompt = file.read()

# ==========================================
# CORE LOGIC FUNCTION
# ==========================================
def get_planning_agent_response(user_prompt):
    """
    Sends the user's itinerary request and gathered context to the LLM.
    Returns a detailed, structured travel plan for Quy Nhon.
    """
    try:
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
        
        # Extract the AI-generated response content
        agent_response = completion.choices[0].message.content
        return agent_response
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return "Xin lỗi, có lỗi xảy ra khi tạo lịch trình. Vui lòng thử lại sau."
    return agent_response