# MỤC LỤC BÁO CÁO KHOA HỌC
## **Hệ Thống Trợ Lý Du Lịch Ảo Quy Nhơn Sử Dụng Kiến Trúc Multi-Agent và Mô Hình Ngôn Ngữ Lớn**

Trước khi vào mục lục, đây là toàn bộ stack công nghệ **thực sự tồn tại** trong code:

| Thành phần | Công nghệ thực tế | File nguồn |
|---|---|---|
| LLM | `Qwen/Qwen2.5-7B-Instruct:together` qua HuggingFace Router | `agents/*.py` |
| LLM Client | `openai.OpenAI` (OpenAI-compatible API) | `agents/*.py` |
| Agent 1 | `Orchestrator_Agent` – Intent Classification + JSON routing | `agents/Orchestrator_Agent.py` |
| Agent 2 | `Response_Agent` – General Q&A Chat | `agents/Response_Agent.py` |
| Agent 3 | `Planning_Agent` – Itinerary Generation | `agents/Planning_Agent.py` |
| Schema validation | `pydantic.BaseModel`, `ValidationError`, `model_post_init` | `agents/Orchestrator_Agent.py` |
| Similarity search | `difflib.SequenceMatcher` | `tools/get_food.py`, `tools/get_restaurant.py`, `tools/get_destination.py` |
| Database | PostgreSQL (`BinhDinh_TourGuide`) – **5 bảng** (`food`, `restaurant`, `destination`, `hotel`, `service`) | `script_init_database/`, `tools/*.py` |
| ORM | `SQLAlchemy` + `psycopg2-binary` | `tools/*.py` |
| Data processing | `pandas`, `openpyxl` | `tools/*.py`, `script_init_database/` |
| Backend API | `FastAPI` + `uvicorn` | `main.py` |
| Request model | `pydantic.BaseModel` (`ChatRequest`) | `main.py` |
| Frontend | `Streamlit` | `app.py` |
| Env config | `python-dotenv` | `agents/*.py`, `tools/*.py` |
| Orchestration | Custom pipeline `get_context()` + `get_response()` | `main.py` |
| Weather API | Open-Meteo (HTTP GET không cần API key) | `tools/weather_tool.py` |

> **Ghi chú cấu trúc:** Báo cáo được tổ chức thành **5 chương** theo yêu cầu bắt buộc (đã gộp các nội dung phân tích + prompt/validation và cài đặt + kiểm thử/đánh giá).

---

## TRANG PHỤ BÌA

## LỜI CAM ĐOAN

## LỜI CẢM ƠN

## TÓM TẮT

> Hệ thống trợ lý du lịch ảo Quy Nhơn được xây dựng theo kiến trúc Multi-Agent với **3 agents**, **6 tools** tra cứu dữ liệu, cơ sở dữ liệu PostgreSQL `BinhDinh_TourGuide` gồm **5 bảng**, sử dụng mô hình ngôn ngữ `Qwen/Qwen2.5-7B-Instruct:together` qua HuggingFace Router, giao diện Streamlit và REST API FastAPI.

## DANH MỤC HÌNH ẢNH

## DANH MỤC BẢNG BIỂU

## DANH MỤC TỪ VIẾT TẮT

> LLM, API, NLP, JSON, ORM, SQL, HTTP, AI, HF (HuggingFace), NCKH, GPS, RAG.

---
## PHẦN MỞ ĐẦU *(~8 trang)*

**1. Lý do chọn đề tài** ✓  
> Nhu cầu du lịch Quy Nhơn – Bình Định tăng cao; khoảng trống ứng dụng AI địa phương; tính khả thi của LLM mã nguồn mở qua API router.

**2. Mục tiêu nghiên cứu** ✓  
> - Xây dựng hệ thống hỏi-đáp du lịch tự động với **8 loại intent**.
> - Triển khai kiến trúc Multi-Agent phân tầng: Orchestrator → Tool Layer → Response/Planning.
> - Tích hợp dữ liệu thực tế **5 bảng** về ẩm thực, nhà hàng, địa điểm, khách sạn, dịch vụ.
> - Hỗ trợ thêm tư vấn thời tiết thời gian thực.

**3. Đối tượng và phạm vi nghiên cứu** ✓  
> - **Đối tượng**: LLM, Multi-Agent, Prompt Engineering, Pydantic Validation, Text Similarity.
> - **Phạm vi**: Du lịch Quy Nhơn – Bình Định với 8 domain intent hiện có trong code.

**4. Phương pháp nghiên cứu** ✓  
> Nghiên cứu lý thuyết; thiết kế kiến trúc; triển khai thực nghiệm; đánh giá định tính và định lượng.

**5. Cấu trúc báo cáo** ✓

---

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI *(~14 trang)*

**1.1 Bối cảnh nghiên cứu** ✓  
> - 1.1.1 Xu hướng ứng dụng AI trong ngành du lịch.
> - 1.1.2 Tiềm năng phát triển du lịch Quy Nhơn – Bình Định.
> - 1.1.3 Thách thức cung cấp thông tin địa phương đa domain.

**1.2 Tổng quan các hệ thống AI hỗ trợ du lịch hiện có** ✓  
> - 1.2.1 Chatbot du lịch truyền thống (rule-based).
> - 1.2.2 Hệ thống hỏi-đáp dựa trên LLM.
> - 1.2.3 Kiến trúc Multi-Agent trong bài toán trợ lý du lịch.
> - 1.2.4 So sánh và định vị đề tài.

**1.3 Phân tích vấn đề và đề xuất giải pháp** ✓  
> - 1.3.1 Hạn chế của chatbot một khối (monolithic).
> - 1.3.2 Lý do chọn kiến trúc Multi-Agent với Orchestrator Pattern.
> - 1.3.3 Lý do chọn model `Qwen/Qwen2.5-7B-Instruct:together`.
> - 1.3.4 Lý do chọn PostgreSQL + `difflib.SequenceMatcher` thay vì vector database.
> - 1.3.5 Lý do tích hợp Open-Meteo API cho intent thời tiết.
> - 1.3.6 Bối cảnh thay đổi địa giới hành chính Việt Nam từ 01/07/2025 (mô hình 2 cấp: Tỉnh – Xã) và tác động tới dữ liệu địa chỉ du lịch.

**1.4 Những đóng góp của đề tài** ✓  
> - 1.4.1 Đóng góp kỹ thuật: routing JSON + Pydantic validation + retry.
> - 1.4.2 Đóng góp thực tiễn: dữ liệu địa phương Quy Nhơn – Bình Định.

**1.5 Tóm tắt chương** ✓

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT *(~38 trang)*

### 2.1 Mô hình ngôn ngữ lớn (LLM) ✓ *(~10 trang)*
- 2.1.1 Tổng quan LLM và tiến hoá từ n-gram → Transformer.
- 2.1.2 Transformer: self-attention, multi-head attention, positional encoding.
- 2.1.3 Instruct-tuned model và ý nghĩa trong tác vụ sinh JSON.
- 2.1.4 Mô hình sử dụng thực tế: `Qwen/Qwen2.5-7B-Instruct:together`.

### 2.2 OpenAI-compatible API và HuggingFace Router ✓ *(~6 trang)*
- 2.2.1 Kiến trúc Router và lợi ích không cần GPU cục bộ.
- 2.2.2 `openai.OpenAI` với `base_url` custom.
- 2.2.3 Quản lý `HF_TOKEN` bằng `python-dotenv`.

### 2.3 Kiến trúc Multi-Agent và Orchestrator Pattern ✓ *(~8 trang)*
- 2.3.1 Khái niệm Agent và Multi-Agent System.
- 2.3.2 Tách vai trò: Orchestrator / Response / Planning.
- 2.3.3 Intent classification trong NLP.
- 2.3.4 8 intents thực tế trong hệ thống.
- 2.3.5 Routing bằng JSON có cấu trúc.

### 2.4 Pydantic v2 và xác thực dữ liệu có cấu trúc ✓ *(~6 trang)*
- 2.4.1 Schema-first validation với `BaseModel`, `Literal`, `Optional`.
- 2.4.2 9 models trong Orchestrator (`8 leaf + 1 root`).
- 2.4.3 `model_post_init` cho ràng buộc exactly-one-intent.
- 2.4.4 `ValidationError` feedback loop và `max_retries=1`.

### 2.5 Truy xuất tương đồng văn bản với `difflib.SequenceMatcher` ✓ *(~4 trang)*
- 2.5.1 Nguyên lý lexical similarity và `.ratio()`.
- 2.5.2 Chiến lược `filter_tags`.
- 2.5.3 Top-K retrieval: food top-5, restaurant top-10, destination top-10.

### 2.6 Cơ sở dữ liệu và kiến trúc web ✓ *(~4 trang)*
- 2.6.1 PostgreSQL + SQLAlchemy + Pandas pipeline.
- 2.6.2 FastAPI (`/api/chat`) + Streamlit client-server architecture.
- 2.6.3 Request validation với `ChatRequest(BaseModel)`.

**2.7 Tóm tắt chương** ✓

---

## CHƯƠNG 3: PHÂN TÍCH, THIẾT KẾ HỆ THỐNG VÀ THIẾT KẾ PROMPT/VALIDATION *(~50 trang)*

### 3.1 Đặc tả yêu cầu hệ thống *(~5 trang)*
**3.1.1 Yêu cầu chức năng** ✓  
> - UC-01: Tra cứu món ăn theo loại và sở thích.
> - UC-02: Tra cứu nhà hàng theo phong cách.
> - UC-03: Tra cứu địa điểm tham quan theo loại hình.
> - UC-04: Lập lịch trình du lịch theo thời gian/ngân sách/sở thích.
> - UC-05: Hỏi thời tiết tại địa điểm cụ thể.
> - UC-06: Tìm khách sạn theo vị trí và mức giá.
> - UC-07: Tra cứu dịch vụ tại điểm du lịch.
> - UC-08: Hội thoại chung.

**3.1.2 Yêu cầu phi chức năng** ✓  
> Thời gian phản hồi, độ ổn định API, khả năng mở rộng thêm tool/intent, tính xác định trong routing.

### 3.2 Thiết kế kiến trúc tổng thể *(~8 trang)*
- 3.2.1 Sơ đồ tổng thể 3 tầng: Presentation / Application / Data.
- 3.2.2 Luồng dữ liệu: Streamlit → FastAPI → Orchestrator → Tools → Agent.
- 3.2.3 Thiết kế pipeline `get_context()` + `get_response()`.
- 3.2.4 Cấu trúc thư mục dự án.

### 3.3 Thiết kế chi tiết các Agent *(~10 trang)*
- 3.3.1 Orchestrator Agent: phân loại intent + trích xuất tham số.
- 3.3.2 Response Agent: sinh phản hồi chung từ context.
- 3.3.3 Planning Agent: sinh lịch trình có cấu trúc.
- 3.3.4 Cơ chế chọn agent theo `planning_flag`.

### 3.4 Thiết kế Tool Layer *(~10 trang)*
- 3.4.1 `get_food_list()`: validation category + SQL parameterized + top-5.
- 3.4.2 `get_restaurant()`: similarity từ `category` + top-10.
- 3.4.3 `get_destination()`: similarity từ `category` + top-10.
- 3.4.4 `get_weather()`: GPS → Open-Meteo current weather.
- 3.4.5 `get_hotel()`: filter location + max_price + nearest-price fallback.
- 3.4.6 `get_service()`: tra cứu theo `destination_id` và `filter_tags`.

### 3.5 Thiết kế Prompt và Orchestrator JSON Schema *(~9 trang)*
- 3.5.1 Prompt Orchestrator cho 8 intents.
- 3.5.2 Quy tắc JSON-only output (không markdown fence, không hội thoại).
- 3.5.3 Phân tích 16 few-shot examples.
- 3.5.4 Quy tắc Forced Single Intent khi truy vấn đa ý định.

### 3.6 Thiết kế Validation Pipeline với Pydantic *(~5 trang)*
- 3.6.1 8 leaf models: `Food/Restaurant/Destination/Planning/Weather/Hotel/Service/Chat`.
- 3.6.2 Root model `OrchestratorOutput` và `model_post_init()`.
- 3.6.3 Hàm `validate_route_json()` + retry loop + fallback.

### 3.7 Thiết kế API, Frontend và CSDL *(~3 trang)*
- 3.7.1 API endpoint `POST /api/chat`.
- 3.7.2 Streamlit session state, call API timeout 60s.
- 3.7.3 Thiết kế dữ liệu 5 bảng và scripts ETL.

### 3.8 Vấn đề dữ liệu địa chỉ hành chính sau sáp nhập 2025 *(~4 trang)*
- 3.8.1 Mốc thời gian triển khai đề tài (22/09/2025) và hiện trạng dữ liệu nguồn ban đầu.
- 3.8.2 Thực tế dữ liệu địa chỉ trên Google Maps vẫn mang đơn vị hành chính cũ tại nhiều điểm.
- 3.8.3 Rủi ro sai lệch khi đối chiếu địa chỉ cũ/mới trong truy vấn và hiển thị kết quả.
- 3.8.4 Quy trình chuẩn hoá thủ công: tra cứu GG Maps + đối chiếu văn bản pháp lý/nguồn tra cứu sáp nhập.
- 3.8.5 Nguyên tắc ghi nhận trong CSDL: lưu địa chỉ gốc, địa chỉ chuẩn hoá, nguồn đối chiếu, thời điểm cập nhật.

**3.9 Tóm tắt chương** ✓

---

## CHƯƠNG 4: CÀI ĐẶT, TRIỂN KHAI, KIỂM THỬ VÀ ĐÁNH GIÁ *(~32 trang)*

### 4.1 Cài đặt môi trường và dependencies *(~4 trang)*
- 4.1.1 Cài đặt từ `requirements.txt`.
- 4.1.2 Cấu hình `.env` với `HF_TOKEN`, `DB_URL`.
- 4.1.3 Chuẩn bị dữ liệu Excel đầu vào.

### 4.2 Triển khai backend, agents và tools *(~8 trang)*
- 4.2.1 Cấu hình FastAPI trong `main.py`.
- 4.2.2 Triển khai 3 agents trong `agents/`.
- 4.2.3 Triển khai 6 tools trong `tools/`.

### 4.3 Triển khai cơ sở dữ liệu và frontend *(~5 trang)*
- 4.3.1 Tạo database `BinhDinh_TourGuide`.
- 4.3.2 Nạp dữ liệu từ Excel sang PostgreSQL.
- 4.3.3 Chạy giao diện Streamlit và kết nối API.

### 4.4 Kịch bản vận hành end-to-end *(~3 trang)*
- 4.4.1 Luồng user query cho từng intent.
- 4.4.2 Luồng planning itinerary.
- 4.4.3 Luồng weather/hotel/service.

### 4.5 Kiểm thử hệ thống *(~7 trang)*
- 4.5.1 Unit test theo từng module agent/tool.
- 4.5.2 Integration test pipeline `get_context()` → `get_response()`.
- 4.5.3 End-to-end test Streamlit ↔ FastAPI.
- 4.5.4 Kiểm thử negative cases: JSON invalid, empty DataFrame, location not found.
- 4.5.5 Kiểm thử đối chiếu địa chỉ hành chính cũ/mới sau sáp nhập (mẫu địa điểm tại Quy Nhơn).

### 4.6 Đánh giá và thảo luận kết quả *(~5 trang)*
- 4.6.1 Đánh giá chất lượng phân loại intent.
- 4.6.2 Đánh giá chất lượng truy xuất dữ liệu.
- 4.6.3 Đánh giá chất lượng phản hồi và mức độ hữu ích.
- 4.6.4 Đánh giá hiệu năng, độ ổn định, giới hạn hiện tại.
- 4.6.5 Đánh giá chi phí vận hành khi phải chuẩn hoá địa chỉ thủ công.

**4.7 Tóm tắt chương** ✓

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN *(~8 trang)*

### 5.1 Kết luận
- 5.1.1 Tổng kết kết quả đạt được.
- 5.1.2 Mức độ đáp ứng mục tiêu nghiên cứu.

### 5.2 Hạn chế hiện tại
- 5.2.1 `difflib` là lexical matching, chưa semantic.
- 5.2.2 Chưa có memory đa lượt hội thoại.
- 5.2.3 Retry hiện tại còn ngắn (`max_retries=1`).
- 5.2.4 Chưa tối ưu production (pooling/monitoring).
- 5.2.5 Dữ liệu địa chỉ mới sau cải cách hành chính chưa đồng bộ trên nguồn công khai, cần cập nhật tay theo đợt.

### 5.3 Hướng phát triển
- 5.3.1 Nâng cấp semantic retrieval/RAG.
- 5.3.2 Bổ sung conversational memory.
- 5.3.3 Mở rộng domain dữ liệu du lịch.
- 5.3.4 Docker + cloud deployment + observability.
- 5.3.5 Xây dựng pipeline bán tự động chuẩn hoá địa chỉ hành chính theo danh mục mới (Tỉnh – Xã).

---

## TÀI LIỆU THAM KHẢO

---

## PHỤ LỤC

**Phụ lục A: Nội dung System Prompt Orchestrator Agent** (`prompts/orchestrator_agent.txt`)

**Phụ lục B: Prompt của Response Agent và Planning Agent** (`prompts/response_agent.txt`, `prompts/planning_agent.txt`)

**Phụ lục C: Schema Pydantic đầy đủ và logic routing** (`agents/Orchestrator_Agent.py`)

**Phụ lục D: Danh sách toàn bộ thư viện** (`requirements.txt`)

**Phụ lục E: Scripts khởi tạo và migrate dữ liệu PostgreSQL** (`script_init_database/`)

**Phụ lục F: Hướng dẫn cài đặt và chạy hệ thống** (`readme.md`)

**Phụ lục G: Nguồn đối chiếu địa giới hành chính sau sáp nhập** (Thư Viện Pháp Luật: bài viết Quy Nhơn sau sáp nhập, công cụ tra cứu sáp nhập tỉnh)

**Phụ lục H: Quy trình chuẩn hoá thủ công địa chỉ cũ → địa chỉ mới cho dữ liệu du lịch**
