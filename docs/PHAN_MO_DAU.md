## PHẦN MỞ ĐẦU

### 1. Lý do chọn đề tài

Trong những năm gần đây, ngành du lịch tại khu vực Quy Nhơn – Bình Định ghi nhận tốc độ tăng trưởng ổn định và đóng vai trò quan trọng trong chiến lược phát triển kinh tế – xã hội của địa phương [1]. Sự gia tăng lượng khách du lịch kéo theo nhu cầu tiếp cận thông tin nhanh chóng, chính xác và có tính cá nhân hóa cao. Tuy nhiên, phần lớn thông tin về điểm tham quan, ẩm thực, khách sạn và dịch vụ vẫn phân tán trên nhiều nền tảng khác nhau, gây khó khăn cho du khách trong quá trình tìm kiếm và ra quyết định.

Các hệ thống hỗ trợ du lịch truyền thống chủ yếu dựa trên cơ chế tìm kiếm từ khóa hoặc chatbot kịch bản (rule-based chatbot), vốn hạn chế về khả năng hiểu ngôn ngữ tự nhiên và khó xử lý các truy vấn phức tạp [4]. Sự xuất hiện của các Mô hình Ngôn ngữ Lớn (Large Language Models – LLM) đã tạo ra bước đột phá trong xử lý ngôn ngữ tự nhiên nhờ kiến trúc Transformer [6] và các năng lực suy luận nổi bật khi mở rộng quy mô mô hình [2]. Những tiến bộ này cho phép xây dựng các hệ thống hội thoại có khả năng hiểu ngữ cảnh và thực hiện tác vụ đa bước.

Tuy nhiên, một trong những thách thức lớn khi ứng dụng LLM vào các miền chuyên biệt là hiện tượng “hallucination” – mô hình sinh ra thông tin không chính xác hoặc không có thật [3]. Điều này đặc biệt nghiêm trọng trong lĩnh vực du lịch địa phương, nơi tính xác thực của dữ liệu (giá cả, địa điểm, dịch vụ) có ảnh hưởng trực tiếp đến trải nghiệm người dùng. Do đó, việc kết hợp LLM với cơ chế truy xuất dữ liệu có kiểm soát và xác thực đầu ra trở thành yêu cầu thiết yếu.

Bên cạnh đó, xu hướng tích hợp các hệ thống AI đa tác vụ và cộng tác nhiều tác tử (multi-agent collaboration) đang được xem là hướng tiếp cận hiệu quả để phân tách chức năng và tăng tính kiểm soát hệ thống [5]. Đồng thời, việc khai thác LLM mã nguồn mở thông qua API Router giúp giảm yêu cầu về hạ tầng tính toán, tăng tính khả thi trong triển khai thực tế ở quy mô địa phương.

Từ những cơ sở trên, đề tài “Hệ thống trợ lý du lịch ảo Quy Nhơn sử dụng kiến trúc Multi-Agent và mô hình ngôn ngữ lớn” được đề xuất nhằm xây dựng một hệ thống hội thoại thông minh, định hướng dữ liệu và có khả năng mở rộng, góp phần thúc đẩy chuyển đổi số trong lĩnh vực du lịch địa phương.

---

### 2. Mục tiêu nghiên cứu

Nghiên cứu này hướng đến các mục tiêu cụ thể sau:

Thứ nhất, xây dựng hệ thống hỏi – đáp du lịch tự động có khả năng phân loại và xử lý chính xác 8 loại ý định (intent) của người dùng, bao gồm: giao tiếp thông thường, ẩm thực, nhà hàng, điểm đến, khách sạn, dịch vụ, thời tiết và lập lịch trình.

Thứ hai, triển khai kiến trúc Multi-Agent phân tầng gồm ba thành phần chính:

* Orchestrator Agent thực hiện phân loại intent và trích xuất tham số.
* Tool Layer kết nối cơ sở dữ liệu và dịch vụ bên ngoài.
* Response Agent và Planning Agent chịu trách nhiệm sinh phản hồi tự nhiên và xây dựng lịch trình đa bước.

Thứ ba, tích hợp cơ sở dữ liệu thực tế gồm 5 bảng (food, restaurant, destination, hotel, service) trong hệ quản trị PostgreSQL nhằm hạn chế hallucination và tăng tính xác thực của hệ thống [3].

Thứ tư, bổ sung chức năng tư vấn thời tiết thời gian thực thông qua API bên ngoài, nâng cao tính thực tiễn trong hỗ trợ ra quyết định của du khách.

---

### 3. Đối tượng và phạm vi nghiên cứu

**Đối tượng nghiên cứu** bao gồm:

* Mô hình Ngôn ngữ Lớn (LLM) và cơ chế khai thác thông qua API Router.
* Kiến trúc Multi-Agent và cơ chế điều phối tác vụ.
* Kỹ thuật Prompt Engineering nhằm tối ưu hóa đầu ra của mô hình [2].
* Cơ chế xác thực dữ liệu bằng Pydantic Validation.
* Phương pháp tính toán độ tương đồng văn bản phục vụ truy xuất dữ liệu.

**Phạm vi nghiên cứu** giới hạn trong miền dữ liệu du lịch khu vực Quy Nhơn – Bình Định và 8 domain intent đã được định nghĩa sẵn trong hệ thống. Đề tài không mở rộng sang các chức năng giao dịch tài chính hoặc thương mại điện tử.

---

### 4. Phương pháp nghiên cứu

Nghiên cứu áp dụng phương pháp kết hợp giữa lý thuyết và thực nghiệm.

Về lý thuyết, nhóm nghiên cứu tổng hợp các công trình liên quan đến kiến trúc Transformer [6], năng lực mở rộng của LLM [2], và các nghiên cứu về hiện tượng hallucination [3]. Đồng thời, các tài liệu về chuyển đổi số trong du lịch cũng được tham khảo để xác định bối cảnh ứng dụng [4].

Về thực nghiệm, hệ thống được thiết kế theo kiến trúc client–server với backend FastAPI, frontend Streamlit và cơ sở dữ liệu PostgreSQL. Kỹ thuật Few-shot Prompting được sử dụng để hướng dẫn mô hình sinh JSON có cấu trúc.

Về đánh giá, hệ thống được kiểm thử theo cả phương pháp định tính (độ tự nhiên và hữu ích của phản hồi) và định lượng (tỷ lệ phân loại intent chính xác, độ trễ phản hồi API).

---

### 5. Cấu trúc báo cáo

Phần còn lại của báo cáo được tổ chức như sau:

Chương 1 trình bày tổng quan đề tài và các nghiên cứu liên quan.
Chương 2 cung cấp cơ sở lý thuyết về LLM, Multi-Agent và kỹ thuật truy xuất dữ liệu.
Chương 3 trình bày phân tích và thiết kế hệ thống.
Chương 4 mô tả quá trình triển khai và đánh giá thực nghiệm.
Chương 5 đưa ra kết luận và hướng phát triển trong tương lai.

---
