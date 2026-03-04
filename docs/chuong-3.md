# CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG ĐA TÁC NHÂN

Chương này đóng vai trò là cầu nối giữa các cơ sở lý thuyết đã trình bày ở Chương 2 và quá trình lập trình thực tế sẽ được thảo luận ở Chương 4. Nội dung của chương tập trung vào việc áp dụng các nguyên lý kỹ thuật phần mềm (Software Engineering) để phân tích yêu cầu, từ đó thiết kế kiến trúc hệ thống, quy hoạch cơ sở dữ liệu, và đặc biệt là thiết kế cấu trúc tác nhân (Agent) thông qua kỹ thuật Prompt Engineering và Pydantic Validation.

---

## 3.1 Đặc tả yêu cầu hệ thống

Phân tích yêu cầu là bước khởi đầu và mang tính quyết định trong vòng đời phát triển phần mềm (Software Development Life Cycle – SDLC). Theo Sommerville [7], mục tiêu cốt lõi của giai đoạn này là xác định một cách chính xác và không mơ hồ những gì hệ thống phải thực hiện (Functional Requirements) cũng như các tiêu chuẩn chất lượng mà hệ thống phải đáp ứng (Non-functional Requirements).

Đối với hệ thống **Trợ lý Du lịch Ảo Quy Nhơn – Bình Định**, yêu cầu được phân chia thành hai nhóm chính:

* **Yêu cầu chức năng (Functional Requirements)** – mô tả các Use Case (UC) cụ thể mà hệ thống phải thực hiện.
* **Yêu cầu phi chức năng (Non-functional Requirements)** – mô tả các ràng buộc về hiệu năng, độ ổn định, tính xác định và khả năng mở rộng của kiến trúc đa tác tử.

Hệ thống được thiết kế theo kiến trúc Multi-Agent, trong đó Orchestrator Agent chịu trách nhiệm định tuyến (routing) và xuất JSON có cấu trúc — một yêu cầu quan trọng đối với các hệ thống sử dụng LLM hiện đại [9].

---

# 3.1.1 Yêu cầu chức năng

Hệ thống phải xử lý chính xác **8 Use Case (UC)** tương ứng với 8 intent được định nghĩa trong schema của Orchestrator Agent.

![Hình 3.1 - Luồng chức năng tổng quát cho 8 Use Case](images/hinh_3_1_luong_chuc_nang_uc.svg)

---

## UC-01: Tra cứu món ăn theo loại và sở thích (Food Intent)

**Mục tiêu:**
Cung cấp danh sách tối đa 5 món ăn phù hợp với loại món và sở thích người dùng.

**Tham số bắt buộc trích xuất:**

* `type_of_food`: chỉ được thuộc tập giá trị chuẩn hóa gồm:
  `"món chính"`, `"món phụ"`, `"đồ ăn vặt"`, `"đồ tráng miệng"`, `"đồ uống"`.
* `filter_tags`: chuỗi từ khóa mô tả sở thích (không bao gồm tên tỉnh/thành).

**Luồng xử lý kỹ thuật:**

1. Orchestrator Agent phân loại intent `food`.
2. Xuất JSON hợp lệ dạng:

   ```json
   {"food": {"type_of_food": "...", "filter_tags": "..."}}
   ```
3. Tool Layer gọi `get_food_list(type_of_food, filter_tags)`.
4. Truy vấn bảng `food` bằng câu lệnh SQL có tham số hóa (parameterized query) nhằm ngăn chặn SQL Injection.
5. Tính điểm tương đồng bằng `difflib.SequenceMatcher`.
6. Trả về **Top-5** bản ghi có similarity score cao nhất.

Việc sử dụng truy vấn có tham số và kiểm soát dữ liệu đầu vào tuân theo nguyên lý thiết kế phần mềm an toàn được khuyến nghị trong kỹ nghệ phần mềm hiện đại [7].

---

## UC-02: Tra cứu nhà hàng theo phong cách (Restaurant Intent)

**Tham số trích xuất:**

* `filter_tags` (ví dụ: “quán nhậu bình dân”, “ăn chay”, “kiểu Pháp”).

**Luồng xử lý:**

1. Orchestrator → intent `restaurant`.
2. Tool `get_restaurant(filter_tags)` truy vấn toàn bộ bảng `restaurant`.
3. So khớp chuỗi giữa `filter_tags` và trường `category`.
4. Trả về **Top-10** nhà hàng có điểm tương đồng cao nhất.

Cách tiếp cận này phù hợp với các hệ thống truy vấn dựa trên từ khóa có cấu trúc dữ liệu rõ ràng [7].

---

## UC-03: Tra cứu địa điểm tham quan theo loại hình (Destination Intent)

**Tham số trích xuất:**

* `filter_tags` (ví dụ: “bãi biển”, “di tích lịch sử”, “khu vui chơi”).

**Luồng xử lý:**

1. Orchestrator → intent `destination`.
2. Gọi `get_destination(filter_tags)`.
3. Truy vấn bảng `destination`.
4. Tính similarity score dựa trên trường `category`.
5. Trả về **Top-10** địa điểm kèm:

   * địa chỉ
   * mô tả
   * `gps_lat`, `gps_lon`

Dữ liệu GPS là tiền đề bắt buộc cho UC-05 (Weather).

---

## UC-04: Lập lịch trình du lịch (Planning Intent)

Đây là Use Case phức tạp nhất và yêu cầu phối hợp nhiều Agent.

**Tham số trích xuất:**

* `time` (mặc định: “3 ngày”)
* `budget` (mặc định: “5 triệu”)
* `prefer` (mặc định: “hải sản, biển”)

**Luồng xử lý kỹ thuật:**

1. Orchestrator xuất JSON dạng:

   ```json
   {"planning": {"time": "...", "budget": "...", "prefer": "..."}}
   ```
2. Kích hoạt `planning_flag = True`.
3. Gọi đồng thời:

   * `get_destination(prefer)`
   * `get_restaurant(prefer)`
   * `get_hotel(prefer)`
   * `get_food_list(...)`
4. Tổng hợp thành một structured context.
5. Chuyển sang Planning Agent.

Planning Agent bắt buộc sinh lịch trình có cấu trúc rõ ràng gồm:

* Mở đầu
* Lịch trình theo ngày/buổi
* Bảng ngân sách tham khảo
* Kết luận

Theo nghiên cứu về Retrieval-Augmented Generation (RAG), việc ép LLM sinh nội dung dựa hoàn toàn trên context đã truy xuất giúp giảm hallucination đáng kể [8].

---

## UC-05: Hỏi thời tiết tại địa điểm cụ thể (Weather Intent)

**Tham số trích xuất:**

* `location` (giữ nguyên dấu, không suy diễn).

**Luồng xử lý hai bước:**

1. Truy vấn bảng `destination` để lấy `gps_lat`, `gps_lon`.
2. Gọi API Open-Meteo:

   ```
   https://api.open-meteo.com/v1/forecast?latitude=...&longitude=...&current_weather=true
   ```

Hệ thống chỉ bổ sung dữ liệu thời tiết vào context, không cho phép LLM tự suy đoán thông tin ngoài dữ liệu API — nguyên tắc kiểm soát tri thức ngoại vi trong hệ thống LLM kết hợp công cụ [8].

---

## UC-06: Tìm khách sạn theo vị trí và mức giá (Hotel Intent)

**Tham số:**

* `location`
* `max_price` (chuẩn hóa về số nguyên VNĐ).

**Luồng xử lý:**

1. Chuyển đổi chuỗi giá sang `price_numeric`.
2. Lọc theo điều kiện `price_numeric <= max_price`.
3. Nếu rỗng → kích hoạt **nearest-price fallback**:

   ```
   ORDER BY ABS(price_numeric - max_price)
   ```
4. Trả về **Top-5** sắp xếp tăng dần theo giá.

---

## UC-07: Tra cứu dịch vụ tại điểm du lịch (Service Intent)

**Tham số:**

* `location` (bắt buộc)
* `filter_tags` (tùy chọn)

**Luồng xử lý hai giai đoạn:**

1. Tìm `destination_id`.
2. Truy vấn bảng `service` theo ID.
3. Nếu có `filter_tags` → áp dụng điều kiện `ILIKE`.
4. Nếu không tìm thấy địa điểm → trả trạng thái `"not_found"`.

---

## UC-08: Hội thoại chung (Chat Intent)

Intent `chat` được xử lý trực tiếp bởi Response Agent mà không gọi Tool Layer.

JSON bắt buộc:

```json
{"chat": {}}
```

Không được chứa free-text ngoài JSON — yêu cầu này dựa trên nguyên tắc ép LLM sinh structured output nhằm bảo đảm tính xác định [9].

---


# 3.1.2 Yêu cầu phi chức năng

Theo tiêu chuẩn ISO/IEC 25010 [10], các yêu cầu phi chức năng mô tả các thuộc tính chất lượng mà hệ thống phải đảm bảo bên cạnh tính đúng đắn chức năng.

---

**Thời gian phản hồi (Latency / Performance Efficiency).**

Do LLM sinh văn bản theo cơ chế tự hồi quy (auto-regressive generation), mỗi token được tạo ra tuần tự theo phân phối xác suất:

[
P(w_t \mid w_{<t})
]

Quá trình này khiến thời gian suy luận dài hơn so với API truyền thống. Do đó, hệ thống thiết lập ngưỡng thời gian phản hồi tối đa là **60 giây** cho toàn bộ chu trình từ lúc người dùng gửi yêu cầu đến khi hiển thị kết quả trên giao diện. Giới hạn này nhằm đảm bảo trải nghiệm người dùng theo khuyến nghị về tương tác người–AI [7].

---

**Tính xác định trong phân loại ý định (Determinism & Reliability).**

LLM vốn hoạt động theo cơ chế xác suất, do đó đầu ra mang tính ngẫu nhiên (stochastic). Tuy nhiên, nghiệp vụ định tuyến của hệ thống yêu cầu tính tất định (deterministic routing). Vì vậy:

* Orchestrator Agent phải trả về đúng một đối tượng JSON hợp lệ.
* Chỉ chứa duy nhất một khóa cấp cao nhất (exactly-one-key constraint).
* Không sinh thêm văn bản tự do.

Yêu cầu này nhằm đảm bảo quy trình phân tích cú pháp (JSON parsing) không bị lỗi và toàn bộ pipeline hoạt động ổn định.

---

**Khả năng xử lý lỗi mềm mại (Graceful Degradation / Fault Tolerance).**

Trong kiến trúc phụ thuộc Cloud API, các lỗi như:

* Mất kết nối mạng,
* Vượt giới hạn API (rate limit),
* Lỗi máy chủ (HTTP 500),

là điều không thể tránh khỏi. Theo Knight [11], hệ thống phần mềm phải đảm bảo cơ chế xử lý lỗi an toàn, đặc biệt khi tích hợp thành phần bên ngoài. Do đó, hệ thống phải:

* Bắt ngoại lệ tại tầng Backend.
* Không để lộ stack-trace kỹ thuật ra giao diện người dùng.
* Trả về thông báo xin lỗi thân thiện và đề nghị thử lại.

---


### 3.1.3. Ràng buộc thiết kế (Design Constraints) 

Ràng buộc thiết kế giới hạn không gian giải pháp kỹ thuật của hệ thống và được xác định ngay từ đầu để đảm bảo tính khả thi triển khai.

---

**Ràng buộc về Hạ tầng và Triển khai.**

Hệ thống được thiết kế để hoạt động trong môi trường không có GPU chuyên dụng. Vì vậy:

* Cấm tải trực tiếp trọng số mô hình tại máy chủ cục bộ.
* Toàn bộ suy luận phải thông qua Cloud API (HuggingFace Inference Router).
* Giao tiếp sử dụng giao thức HTTP chuẩn hóa theo OpenAI-compatible API.

Ràng buộc này giúp giảm chi phí phần cứng và phù hợp với kiến trúc prediction-serving phân tán được đề xuất trong các hệ thống phục vụ mô hình học máy hiện đại [12].

---

**Ràng buộc về Không gian Dữ liệu (Data Scope Constraints).**

Để ngăn chặn hiện tượng “ảo giác” (hallucination), hệ thống bị giới hạn chặt chẽ trong phạm vi địa lý Quy Nhơn – Bình Định. Điều này đồng nghĩa:

* Chỉ được phép sử dụng dữ liệu đã lưu trữ trong cơ sở dữ liệu nội bộ.
* Nếu người dùng yêu cầu nội dung ngoài phạm vi (ví dụ: Đà Nẵng, Nha Trang, Đà Lạt), hệ thống phải từ chối thay vì tự động sinh nội dung dựa trên tri thức tổng quát của LLM.

Ràng buộc này đảm bảo tính chính xác của thông tin và duy trì tính nhất quán của hệ thống.

---

> Nguồn tham khảo của chương này được quản lý tập trung tại file `docs/REFERENCES`.
