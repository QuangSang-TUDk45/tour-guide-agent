import streamlit as st
import requests

# ==========================================
# WEB INTERFACE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Quy Nhơn AI Tour Guide",
    page_icon="🏝️",
    layout="centered"
)

st.title("🏝️ Trợ Lý Du Lịch Quy Nhơn")
st.markdown("Xin chào! Mình là AI Tour Guide. Mình có thể giúp bạn tìm kiếm món ăn, nhà hàng, điểm tham quan và lên lịch trình chi tiết tại Quy Nhơn.")

# ==========================================
# MAIN FASTAPI CALL FUNCTION
# ==========================================
def call_fastapi(user_message):
    """
    This function sends the user's question to FastAPI and receives the response.
    """
    api_url = "http://localhost:8000/api/chat"
    
    # Payload matching the Pydantic model (ChatRequest) in FastAPI
    payload = {
        "user_prompt": user_message
    }
    
    try:
        # Send POST request to API with a timeout to prevent long app hangs
        response = requests.post(api_url, json=payload, timeout=60)
        
        # Check if the API returned an HTTP error code (e.g., 404, 500)
        response.raise_for_status()
        
        # Parse JSON response and extract the "data" field
        result = response.json()
        return result.get("data", "Xin lỗi, mình không nhận được dữ liệu phản hồi từ hệ thống.")
        
    except requests.exceptions.ConnectionError:
        return "Lỗi kết nối: Không thể kết nối đến máy chủ. Bạn hãy kiểm tra xem FastAPI đã được chạy chưa nhé."
    except requests.exceptions.Timeout:
        return "Lỗi thời gian chờ: Hệ thống đang xử lý quá lâu, vui lòng thử lại sau."
    except Exception as e:
        return f"Đã xảy ra lỗi hệ thống: {str(e)}"

# ==========================================
# CHAT HISTORY MANAGEMENT (SESSION STATE)
# ==========================================
# Check if chat history exists; if not, initialize with a greeting
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Chào bạn! Rất vui khi được gặp bạn, mình có thể hỗ trợ cho bạn những gì về du lịch Quy Nhơn nhỉ?"}
    ]

# Re-render all previous messages whenever the app reloads
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# USER INPUT HANDLING
# ==========================================
if user_input := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
    
    # Display user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display loading state and execute the actual API call
    with st.chat_message("assistant"):
        with st.spinner("Đang phân tích yêu cầu và tìm kiếm thông tin..."):
            
            # CALL FASTAPI HERE
            bot_response = call_fastapi(user_input)
            
            # Display result
            st.markdown(bot_response)
            
    # Save AI message to history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})