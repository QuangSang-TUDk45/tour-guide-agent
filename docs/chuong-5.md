# CHƯƠNG 5

# KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

Chương này tổng hợp các kết quả chính đạt được trong quá trình thực hiện đề tài, đồng thời đánh giá mức độ đáp ứng các mục tiêu nghiên cứu đã đề ra. Bên cạnh việc khẳng định các đóng góp về mặt kỹ thuật và thực tiễn, chương cũng phân tích một cách khách quan những hạn chế còn tồn tại của hệ thống. Trên cơ sở đó, các định hướng phát triển trong giai đoạn tiếp theo được đề xuất nhằm nâng cao độ chính xác ngữ nghĩa, khả năng mở rộng hệ thống và mức độ sẵn sàng triển khai trong môi trường thực tế.

Nội dung chương được tổ chức thành ba phần chính: (i) kết luận và tổng hợp kết quả đạt được, (ii) các hạn chế hiện tại của hệ thống, và (iii) các hướng phát triển tiềm năng trong tương lai.

---

# 5.1 Kết luận

## 5.1.1 Tổng kết kết quả đạt được

Từ góc độ kỹ thuật, đề tài đã xây dựng thành công một hệ thống trợ lý du lịch dựa trên kiến trúc **Multi-Agent**, có khả năng vận hành hoàn chỉnh theo chu trình xử lý từ đầu vào đến đầu ra (end-to-end) trong môi trường thực nghiệm. Hệ thống bao gồm các thành phần cốt lõi sau:

* **Orchestrator Agent** thực hiện phân loại ý định (intent classification) và định tuyến truy vấn thông qua cấu trúc JSON chuẩn hóa.
* **Response Agent** chịu trách nhiệm sinh phản hồi hội thoại cho các truy vấn tra cứu thông tin thông thường.
* **Planning Agent** xử lý các yêu cầu phức tạp liên quan đến việc xây dựng lịch trình du lịch nhiều ngày.
* **Tool Layer** đóng vai trò trung gian kết nối với các nguồn dữ liệu, bao gồm cơ sở dữ liệu quan hệ và các dịch vụ ngoại vi như API thời tiết, nhằm cung cấp ngữ cảnh dữ liệu có kiểm chứng.

Một trong những điểm mạnh quan trọng của hệ thống là cách tiếp cận kết hợp giữa **năng lực sinh ngôn ngữ của mô hình ngôn ngữ lớn (LLM)** và **cơ chế truy xuất dữ liệu có kiểm soát**. Thay vì cho phép mô hình suy luận tự do dựa trên tri thức huấn luyện, hệ thống áp dụng chu trình xử lý gồm các bước:

**route → retrieve → inject → generate**

Quy trình này giúp đảm bảo rằng nội dung phản hồi của hệ thống được xây dựng dựa trên dữ liệu thực tế được truy xuất từ các nguồn đáng tin cậy, từ đó giảm đáng kể hiện tượng **hallucination** thường gặp trong các hệ thống sinh ngôn ngữ tự động [8], [22].

Ngoài ra, việc sử dụng thư viện **Pydantic** để kiểm chứng cấu trúc dữ liệu đầu ra của Orchestrator Agent, cùng với ràng buộc *exactly-one-intent*, đã tạo ra một cơ chế định tuyến có tính xác định cao. Điều này giúp đảm bảo mỗi truy vấn chỉ được ánh xạ tới một intent duy nhất, qua đó tăng độ ổn định của toàn bộ pipeline xử lý [9], [10].

---

## 5.1.2 Mức độ đáp ứng mục tiêu nghiên cứu

Đối chiếu với các mục tiêu đã được xác định trong phần mở đầu của đề tài, có thể nhận thấy rằng hệ thống đã đạt được các kết quả chính sau:

**Thứ nhất, về mục tiêu chức năng**, hệ thống đã triển khai thành công tám loại intent khác nhau, bao phủ các nhu cầu thông tin phổ biến của người dùng khi tìm kiếm hỗ trợ du lịch địa phương, bao gồm tra cứu ẩm thực, nhà hàng, địa điểm tham quan, khách sạn, dịch vụ, thời tiết, thông tin tổng quát và lập lịch trình du lịch.

**Thứ hai, về mặt kiến trúc**, đề tài đã hiện thực hóa thành công mô hình **Multi-Agent phân tầng**, trong đó các chức năng điều phối, truy xuất dữ liệu và sinh phản hồi được tách biệt rõ ràng. Cách tiếp cận này giúp giảm độ phức tạp của từng thành phần và tạo điều kiện thuận lợi cho việc mở rộng hệ thống trong tương lai.

**Thứ ba, về mặt dữ liệu**, hệ thống đã tích hợp cơ sở dữ liệu PostgreSQL với các bảng chuyên biệt theo miền thông tin du lịch, bao gồm dữ liệu về ẩm thực, nhà hàng, địa điểm tham quan, khách sạn và dịch vụ địa phương. Các dữ liệu này được thu thập và chuẩn hóa từ nhiều nguồn thực tế.

**Thứ tư, về khả năng vận hành**, hệ thống đã được triển khai với backend sử dụng FastAPI và giao diện người dùng xây dựng bằng Streamlit. Ngoài ra, hệ thống cũng đã tích hợp cơ chế xử lý lỗi cơ bản và quản lý phiên hội thoại ở mức tối thiểu, đủ để phục vụ các thử nghiệm tương tác với người dùng.

Tổng thể, hệ thống đạt mức **“proof-of-practice”**, tức là không chỉ dừng lại ở việc đề xuất mô hình lý thuyết mà còn triển khai được một nguyên mẫu hoạt động thực tế trong bối cảnh dữ liệu du lịch địa phương.

---

# 5.2 Hạn chế hiện tại

Mặc dù hệ thống đạt được nhiều kết quả tích cực, vẫn tồn tại một số hạn chế cần được ghi nhận nhằm đảm bảo tính khách quan và minh bạch của nghiên cứu.

## 5.2.1 Giới hạn của phương pháp truy xuất lexical

Cơ chế truy xuất hiện tại của hệ thống chủ yếu dựa trên phương pháp so khớp chuỗi thông qua thuật toán `difflib.SequenceMatcher`. Phương pháp này có ưu điểm là nhẹ, dễ triển khai và không yêu cầu hạ tầng tính toán phức tạp. Tuy nhiên, bản chất của nó vẫn là **so khớp bề mặt chuỗi (lexical matching)**.

Do đó, trong một số trường hợp, hệ thống có thể không nhận diện được các truy vấn có cách diễn đạt khác nhau nhưng mang ý nghĩa ngữ nghĩa tương tự, dẫn đến khả năng bỏ sót kết quả phù hợp.

---

## 5.2.2 Thiếu bộ nhớ hội thoại đa lượt

Các agent trong hệ thống hiện được thiết kế theo mô hình **stateless**, nghĩa là mỗi truy vấn được xử lý độc lập và không duy trì ngữ cảnh dài hạn giữa các lượt hội thoại.

Điều này làm giảm khả năng duy trì mạch hội thoại liên tục khi người dùng thực hiện chuỗi truy vấn liên quan, chẳng hạn như khi họ muốn điều chỉnh dần các ràng buộc về ngân sách, thời gian hoặc sở thích cá nhân trong quá trình lập kế hoạch du lịch.

---

## 5.2.3 Cơ chế tự sửa lỗi còn hạn chế

Mặc dù Orchestrator Agent đã được trang bị cơ chế **retry loop** để xử lý các trường hợp mô hình sinh ra JSON sai cấu trúc, giá trị `max_retries` hiện vẫn còn thấp. Trong một số tình huống hiếm gặp khi mô hình liên tục sinh đầu ra không hợp lệ, khả năng tự phục hồi của hệ thống vẫn chưa đủ mạnh.

---

## 5.2.4 Hạ tầng vận hành chưa đạt mức production

Hệ thống hiện đang ở mức **triển khai thử nghiệm** phục vụ mục tiêu nghiên cứu học thuật. Một số thành phần quan trọng của môi trường production vẫn chưa được triển khai đầy đủ, chẳng hạn như:

* cơ chế connection pooling nâng cao,
* hệ thống giám sát và logging tập trung,
* pipeline CI/CD cho vòng đời phát triển phần mềm.

Những yếu tố này đóng vai trò quan trọng trong việc đảm bảo độ ổn định và khả năng vận hành lâu dài của hệ thống trong môi trường thực tế [11], [12].

---

## 5.2.5 Thách thức về dữ liệu hành chính trong giai đoạn chuyển tiếp

Một yếu tố thực tiễn ảnh hưởng đến hệ thống là sự thay đổi trong cấu trúc đơn vị hành chính của Việt Nam từ năm 2025. Trong giai đoạn chuyển tiếp này, dữ liệu địa chỉ trên các nền tảng công khai vẫn chưa hoàn toàn đồng bộ.

Điều này khiến quá trình chuẩn hóa thông tin địa chỉ trong cơ sở dữ liệu đôi khi phải thực hiện bán thủ công, đặc biệt đối với các địa điểm du lịch mới hoặc các đơn vị hành chính vừa được điều chỉnh [29], [30], [31], [32].

---

# 5.3 Hướng phát triển

Các hướng phát triển trong tương lai tập trung vào ba mục tiêu chính: nâng cao chất lượng truy xuất tri thức, cải thiện khả năng hội thoại đa lượt và tăng độ ổn định của hạ tầng triển khai.

![Hình 5.1 - Lộ trình phát triển hệ thống giai đoạn tiếp theo](images/hinh_5_1_lo_trinh_phat_trien.svg)

---

## 5.3.1 Nâng cấp semantic retrieval / RAG

Trong các phiên bản tiếp theo, hệ thống có thể được nâng cấp bằng cách bổ sung lớp **semantic retrieval dựa trên embedding** song song với cơ chế lexical retrieval hiện tại.

Phương pháp **hybrid retrieval** kết hợp cả hai cơ chế sẽ giúp hệ thống hiểu tốt hơn các truy vấn có cách diễn đạt đa dạng nhưng mang ý nghĩa tương tự, đồng thời vẫn giữ được khả năng kiểm chứng dữ liệu truy xuất [8], [20].

---

## 5.3.2 Bổ sung cơ chế conversational memory

Một hướng cải tiến quan trọng là xây dựng lớp **quản lý bộ nhớ hội thoại nhiều lượt (conversation memory)**. Thành phần này cho phép hệ thống ghi nhớ các thông tin mà người dùng đã cung cấp trước đó, chẳng hạn như:

* ngân sách,
* thời gian chuyến đi,
* sở thích ẩm thực,
* khu vực ưu tiên.

Việc duy trì các ràng buộc này giúp hệ thống đưa ra các gợi ý phù hợp hơn trong các lượt hội thoại tiếp theo, từ đó cải thiện đáng kể trải nghiệm người dùng.

---

## 5.3.3 Mở rộng domain dữ liệu du lịch

Ngoài năm bảng dữ liệu hiện tại, hệ thống có thể được mở rộng sang các miền thông tin du lịch khác như:

* phương tiện di chuyển,
* sự kiện và lễ hội theo mùa,
* thông tin vé tham quan và khung giờ mở cửa,
* dữ liệu đánh giá cộng đồng đã được kiểm chứng.

Việc mở rộng domain dữ liệu sẽ tăng đáng kể độ bao phủ thông tin của hệ thống, tuy nhiên cũng đòi hỏi các quy trình quản trị dữ liệu chặt chẽ hơn để đảm bảo chất lượng dữ liệu đầu vào.

---

## 5.3.4 Production hóa hạ tầng triển khai

Để chuyển hệ thống từ mức thử nghiệm sang vận hành thực tế, cần thực hiện một số bước nâng cấp hạ tầng như:

* đóng gói toàn bộ hệ thống bằng **Docker**,
* triển khai theo mô hình nhiều môi trường (**development – staging – production**),
* bổ sung hệ thống **logging, monitoring và alerting**,
* xây dựng quy trình **sao lưu và phục hồi dữ liệu**.

Những cải tiến này sẽ giúp nâng cao độ tin cậy của hệ thống khi triển khai trong môi trường vận hành dài hạn.

---

## 5.3.5 Chuẩn hóa địa chỉ hành chính bán tự động

Để thích ứng với các thay đổi trong hệ thống đơn vị hành chính, cần xây dựng một pipeline chuẩn hóa địa chỉ bán tự động gồm các bước:

1. nhận diện các địa chỉ theo chuẩn cũ,
2. đối chiếu với danh mục hành chính mới,
3. lưu trữ địa chỉ chuẩn hóa kèm theo nguồn và thời gian cập nhật,
4. đồng bộ dữ liệu vào cơ sở dữ liệu nghiệp vụ.

Cách tiếp cận này giúp giảm đáng kể khối lượng công việc thủ công trong quá trình cập nhật dữ liệu và đảm bảo tính nhất quán của thông tin địa chỉ khi các chính sách hành chính tiếp tục thay đổi.

---

# 5.4 Tóm tắt chương

Chương 5 đã tổng hợp các kết quả chính của đề tài, khẳng định rằng hệ thống đề xuất đáp ứng được các mục tiêu cốt lõi về kiến trúc và chức năng đối với bài toán trợ lý du lịch địa phương dựa trên mô hình **Multi-Agent kết hợp LLM**.

Bên cạnh những đóng góp đạt được, chương cũng phân tích rõ các hạn chế hiện tại của hệ thống liên quan đến phương pháp truy xuất ngữ nghĩa, cơ chế quản lý ngữ cảnh hội thoại và mức độ hoàn thiện của hạ tầng triển khai.

Trên cơ sở đó, các hướng phát triển được đề xuất theo ba trục chính:

* **nâng cao chất lượng truy xuất tri thức**,
* **cải thiện năng lực hội thoại đa lượt**,
* **tăng độ tin cậy của hạ tầng triển khai**.

Những định hướng này tạo nền tảng cho việc tiếp tục phát triển hệ thống từ một nguyên mẫu nghiên cứu sang một nền tảng có khả năng ứng dụng rộng rãi hơn trong quá trình chuyển đổi số của ngành du lịch địa phương.

---
