# CHƯƠNG 1 TỔNG QUAN VỀ ĐỀ TÀI

---

Chương này nhằm:

Phân tích bối cảnh ứng dụng Trí tuệ nhân tạo trong ngành du lịch.

Xác định khoảng trống của các hệ thống trợ lý du lịch hiện nay.

Làm rõ bài toán nghiên cứu đối với miền dữ liệu địa phương Quy Nhơn – Bình Định.

Biện minh cho các lựa chọn kiến trúc và công nghệ được sử dụng trong đề tài.

Trình bày các đóng góp chính của hệ thống đề xuất.

Chương này đóng vai trò nền tảng lý luận cho các chương thiết kế và triển khai ở phía sau.


## 1.1 Bối cảnh nghiên cứu

### 1.1.1 Xu hướng ứng dụng AI trong ngành du lịch

Trong thập niên gần đây, sự phát triển nhanh chóng của Trí tuệ nhân tạo (AI) và đặc biệt là các Mô hình Ngôn ngữ Lớn (Large Language Models – LLM) đã tạo ra sự chuyển dịch căn bản trong cách thức cung cấp và tiêu thụ thông tin du lịch. Thay vì mô hình tra cứu tĩnh dựa trên từ khóa (keyword-based search), hệ sinh thái du lịch đang chuyển sang mô hình tương tác hội thoại thông minh (Conversational AI), nơi người dùng có thể đặt câu hỏi tự nhiên và nhận được phản hồi được tổng hợp theo ngữ cảnh [13].

Các nghiên cứu gần đây chỉ ra rằng việc tích hợp AI vào hệ thống du lịch thông minh (Smart Tourism Systems) giúp cải thiện đáng kể trải nghiệm người dùng thông qua cá nhân hóa, lập kế hoạch tự động và tối ưu hóa quyết định [14]. Tuy nhiên, phần lớn các hệ thống hiện tại vẫn tồn tại sự tách rời giữa năng lực sinh ngôn ngữ tự nhiên và khả năng truy xuất dữ liệu thực tế, đặc biệt trong bối cảnh thông tin địa phương cần độ chính xác cao và cập nhật liên tục.

Sự xuất hiện của kiến trúc đa tác tử (Multi-Agent Systems – MAS) kết hợp với LLM mở ra một hướng tiếp cận mới: phân tách chức năng suy luận, truy xuất dữ liệu và sinh phản hồi thành các thành phần độc lập nhưng phối hợp chặt chẽ [15]. Cách tiếp cận này được xem là bước tiến quan trọng để giảm thiểu hiện tượng “hallucination” vốn phổ biến trong các hệ thống LLM thuần túy [3].

---

### 1.1.2 Tiềm năng phát triển du lịch Quy Nhơn – Bình Định

Quy Nhơn – Bình Định đang nổi lên như một điểm đến chiến lược của khu vực duyên hải Nam Trung Bộ, với lợi thế về tài nguyên biển đảo, di sản văn hóa Chăm Pa và hệ sinh thái ẩm thực đặc thù. Sự gia tăng nhanh chóng về lượng khách du lịch kéo theo nhu cầu tiếp cận thông tin bản địa đa chiều: từ ẩm thực, lưu trú, dịch vụ, đến điều kiện thời tiết và phương án di chuyển.

Tuy nhiên, dữ liệu du lịch địa phương hiện nay còn phân mảnh trên nhiều nền tảng không đồng bộ (mạng xã hội, blog cá nhân, bản đồ trực tuyến). Điều này làm giảm tính tin cậy và gây khó khăn cho du khách trong việc tổng hợp thông tin để ra quyết định. Khoảng trống này đặt ra yêu cầu xây dựng một hệ thống tập trung, có khả năng kiểm soát dữ liệu và bảo đảm tính xác thực.

---

### 1.1.3 Thách thức cung cấp thông tin địa phương đa domain

Một chuyến du lịch thực tế là bài toán đa miền (multi-domain problem), bao gồm ít nhất các khía cạnh: ẩm thực, khách sạn, điểm đến, dịch vụ phụ trợ và yếu tố thời tiết. Hệ thống hỗ trợ thông minh phải xử lý chính xác từng miền dữ liệu nhưng vẫn duy trì được tính liên kết ngữ cảnh xuyên suốt.

Thách thức cốt lõi không nằm ở việc sinh văn bản tự nhiên, mà ở khả năng định tuyến chính xác truy vấn đến nguồn dữ liệu tương ứng. Nếu thiếu cơ chế phân tách ý định (intent disambiguation) rõ ràng, hệ thống dễ rơi vào trạng thái nhiễu ngữ cảnh (context contamination), làm giảm độ tin cậy tổng thể [15].

---

## 1.2 Tổng quan các hệ thống AI hỗ trợ du lịch hiện có

### 1.2.1 Chatbot du lịch truyền thống (rule-based)

Các chatbot dựa trên luật (rule-based) vận hành theo cây quyết định hoặc kịch bản rẽ nhánh. Ưu điểm của mô hình này là tính kiểm soát cao và khả năng dự đoán hành vi hệ thống. Tuy nhiên, chúng không đủ linh hoạt trước các biến thể ngôn ngữ tự nhiên và không thể xử lý truy vấn phức hợp ngoài kịch bản định trước [16].

Khi số lượng kịch bản tăng, chi phí bảo trì tăng theo cấp số nhân, trong khi khả năng mở rộng (scalability) bị giới hạn nghiêm trọng.

---

### 1.2.2 Hệ thống hỏi-đáp dựa trên LLM

LLM thuần túy giải quyết hiệu quả bài toán hiểu ngôn ngữ và sinh phản hồi mạch lạc. Tuy nhiên, do kiến thức của mô hình bị “đóng băng” tại thời điểm huấn luyện, các hệ thống này thường phát sinh thông tin không chính xác khi được yêu cầu cung cấp dữ liệu địa phương cụ thể [3].

Hiện tượng hallucination không chỉ làm giảm độ tin cậy mà còn gây rủi ro thực tiễn khi thông tin sai lệch liên quan đến giá cả, địa chỉ hoặc điều kiện thời tiết.

---

### 1.2.3 Kiến trúc Multi-Agent trong bài toán trợ lý du lịch

Multi-Agent Systems (MAS) phân chia hệ thống thành các tác tử chuyên biệt với nhiệm vụ rõ ràng: điều phối, truy xuất, lập kế hoạch, hoặc sinh phản hồi. Các nghiên cứu gần đây cho thấy MAS cải thiện đáng kể độ chính xác trong các bài toán chuyên miền (domain-specific QA) so với LLM đơn lẻ [15], [17].

Việc tách biệt tầng điều phối (Orchestrator) khỏi tầng sinh văn bản giúp giảm tải context window và tăng tính kiểm chứng của pipeline.

---

### 1.2.4 So sánh và định vị đề tài

Đề tài này không lựa chọn mô hình chatbot nguyên khối hay RAG truyền thống dựa trên vector database. Thay vào đó, hệ thống được định vị theo hướng:

* Điều phối tập trung bằng Orchestrator Pattern
* Truy xuất dữ liệu cấu trúc từ PostgreSQL
* Tính tương đồng chuỗi ở mức lexical thay vì semantic embedding
* Ép LLM xuất JSON hợp lệ và xác thực bằng Pydantic

Cách tiếp cận này ưu tiên tính xác định (determinism) và khả năng kiểm chứng hơn là tối đa hóa khả năng suy diễn ngữ nghĩa.

---

## 1.3 Phân tích vấn đề và đề xuất giải pháp

### 1.3.1 Hạn chế của chatbot một khối (monolithic)

Trong kiến trúc monolithic, một tác tử duy nhất phải thực hiện đồng thời phân loại ý định, quyết định gọi công cụ và sinh phản hồi. Khi số lượng công cụ tăng, xác suất chọn sai công cụ cũng tăng theo, gây ra lỗi dây chuyền trong pipeline.

Hiện tượng này được ghi nhận trong các nghiên cứu về tool-augmented LLM khi thiếu tầng kiểm chứng trung gian [17].

---

### 1.3.2 Lý do chọn kiến trúc Multi-Agent với Orchestrator Pattern

Hệ thống đề xuất sử dụng Orchestrator Agent làm lớp điều phối độc lập. Tác tử này chỉ thực hiện một nhiệm vụ duy nhất: ánh xạ truy vấn người dùng thành một cấu trúc JSON chứa đúng một intent.

Cách thiết kế này đảm bảo:

* Phân tách trách nhiệm (Separation of Concerns)
* Tăng tính xác định trong định tuyến
* Giảm khả năng hallucination ở tầng sinh văn bản

---

### 1.3.3 Lý do chọn model `Qwen/Qwen2.5-7B-Instruct:together`

Mô hình `Qwen/Qwen2.5-7B-Instruct:together` được lựa chọn do khả năng tuân thủ chỉ thị cao và năng lực sinh cấu trúc JSON ổn định. Việc truy cập thông qua HuggingFace Router giúp tận dụng hạ tầng suy luận từ xa mà không cần triển khai GPU cục bộ, tối ưu chi phí và khả năng triển khai thực tế.

---

### 1.3.4 Lý do chọn PostgreSQL + `difflib.SequenceMatcher`

Trong bối cảnh dữ liệu du lịch có cấu trúc và số lượng không quá lớn, việc sử dụng vector database có thể tạo ra sai lệch ngữ nghĩa không mong muốn đối với danh từ riêng địa phương.

Chiến lược kết hợp PostgreSQL và `difflib.SequenceMatcher` cho phép:

* Truy vấn có tham số hóa
* Tính điểm tương đồng minh bạch
* Duy trì toàn vẹn dữ liệu cấu trúc

Cách tiếp cận này phù hợp với nguyên tắc “lightweight yet reliable” trong các hệ thống chuyên miền quy mô vừa.

---

### 1.3.5 Lý do tích hợp Open-Meteo API

LLM không thể cung cấp dữ liệu thời gian thực. Do đó, việc tích hợp Open-Meteo API giúp tách biệt hoàn toàn lớp dữ liệu động khỏi lớp suy luận.

Hệ thống sử dụng tọa độ GPS từ cơ sở dữ liệu nội bộ để truy vấn API, đảm bảo tính chính xác và không phụ thuộc vào khả năng suy diễn địa lý của LLM.

---

### 1.3.6 Bối cảnh thay đổi địa giới hành chính Việt Nam từ 01/07/2025

Việc chuẩn hóa lại đơn vị hành chính theo mô hình hai cấp (Tỉnh – Xã) tạo ra thách thức lớn cho các hệ thống dựa trên dữ liệu cũ. Nếu phụ thuộc hoàn toàn vào tri thức huấn luyện của LLM, hệ thống có nguy cơ cung cấp địa chỉ không còn hợp lệ.

Thiết kế dựa trên cơ sở dữ liệu quan hệ cho phép cập nhật tập trung và điều chỉnh đồng loạt thông tin địa chỉ mà không cần huấn luyện lại mô hình, bảo đảm tính thích ứng cao trước thay đổi chính sách.

---

## 1.4 Những đóng góp của đề tài

### 1.4.1 Đóng góp kỹ thuật

* Xây dựng pipeline định tuyến JSON có tính xác định cao.
* Áp dụng Pydantic validation để kiểm tra đầu ra LLM.
* Triển khai cơ chế retry với self-correction dựa trên thông báo lỗi.

Cách tiếp cận này góp phần giải quyết bài toán structured output reliability trong hệ thống LLM.

---

### 1.4.2 Đóng góp thực tiễn

* Số hóa cơ sở dữ liệu du lịch Quy Nhơn – Bình Định với 5 bảng chuyên biệt.
* Xây dựng hệ thống trợ lý du lịch có khả năng vận hành thực tế.
* Giảm thiểu hiện tượng hallucination trong môi trường địa phương hóa cao.

---

## 1.5 Tóm tắt chương

Chương 1 đã phân tích bối cảnh phát triển AI trong du lịch, xác định khoảng trống trong các hệ thống hiện tại và đề xuất một kiến trúc đa tác tử có tính xác định cao. Lựa chọn thiết kế được biện minh dựa trên yêu cầu thực tiễn của dữ liệu địa phương và yêu cầu kiểm soát hallucination trong hệ thống LLM.

---

> Nguồn tham khảo của chương này được quản lý tập trung tại file `docs/REFERENCES`.
