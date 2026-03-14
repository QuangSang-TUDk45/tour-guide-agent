# agents/Response_Agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==========================================
# LLM SETUP AND CONFIGURATION
# ==========================================
# Initialize the OpenAI client pointing to Hugging Face's router
HF_TOKEN = os.getenv("HF_TOKEN")
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# ==========================================
# PROMPT LOADING
# ==========================================
# Load the system prompt for the general Response Agent
# This prompt defines the AI's persona and tone as a local guide
with open(r"prompts\response_agent.txt", 'r', encoding='utf-8') as file:
    system_prompt = file.read()

# ==========================================
# CORE LOGIC FUNCTION
# ==========================================
def get_agent_response(user_prompt):
    """
    Sends the user prompt and context to the LLM for general chat interaction.
    Suitable for Q&A, greetings, and simple travel recommendations.
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
        
        # Extract and return the AI's response content
        agent_response = completion.choices[0].message.content
        return agent_response
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu của bạn. Vui lòng thử lại sau."
    return agent_response