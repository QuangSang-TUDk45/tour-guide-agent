TRANG PHỤ BÌA

BỘ GIÁO DỤC VÀ ĐÀO TẠO
TRƯỜNG ĐẠI HỌC [TÊN TRƯỜNG]
KHOA [TÊN KHOA]
---------------

BÁO CÁO NGHIÊN CỨU KHOA HỌC / ĐỒ ÁN TỐT NGHIỆP

ĐỀ TÀI:
HỆ THỐNG TRỢ LÝ DU LỊCH ẢO QUY NHƠN
SỬ DỤNG KIẾN TRÚC MULTI-AGENT
VÀ MÔ HÌNH NGÔN NGỮ LỚN

Giảng viên hướng dẫn: [Học hàm, Học vị, Tên Giảng viên]
Nhóm sinh viên thực hiện: [Danh sách thành viên]
Mã số sinh viên: [MSSV từng thành viên]
Lớp/Khóa: [Tên lớp – Khóa]

[Tên Thành phố], Tháng [X] Năm 202…

---

LỜI CAM ĐOAN

Nhóm nghiên cứu cam đoan rằng đề tài “Hệ thống trợ lý du lịch ảo Quy Nhơn sử dụng kiến trúc Multi-Agent và mô hình ngôn ngữ lớn” là công trình nghiên cứu do nhóm thực hiện dưới sự hướng dẫn khoa học của [Tên Giảng viên hướng dẫn].

Toàn bộ dữ liệu, kết quả và nội dung trình bày trong báo cáo được xây dựng từ quá trình khảo sát, thiết kế, lập trình và kiểm thử hệ thống thực nghiệm. Các tài liệu tham khảo, bài báo khoa học, nguồn dữ liệu và mã nguồn mở được sử dụng trong quá trình nghiên cứu đều được trích dẫn đầy đủ theo đúng quy định học thuật.

Nhóm nghiên cứu hoàn toàn chịu trách nhiệm trước Nhà trường và Khoa về tính trung thực, tính chính xác và quyền sở hữu trí tuệ của công trình này.

[Tên Thành phố], ngày … tháng … năm …
ĐẠI DIỆN NHÓM SINH VIÊN
(Ký và ghi rõ họ tên)

---

LỜI CẢM ƠN

Nhóm nghiên cứu xin trân trọng cảm ơn Ban Giám hiệu Trường [Tên Trường] và toàn thể giảng viên Khoa [Tên Khoa] đã cung cấp nền tảng kiến thức chuyên môn, phương pháp nghiên cứu khoa học và môi trường học thuật thuận lợi trong suốt quá trình học tập.

Nhóm xin bày tỏ lòng biết ơn sâu sắc tới [Học hàm, Học vị, Tên Giảng viên hướng dẫn], người đã định hướng đề tài, góp ý chuyên môn và hỗ trợ nhóm trong toàn bộ quá trình triển khai nghiên cứu. Những nhận xét và phản biện khoa học của Thầy/Cô là cơ sở quan trọng giúp đề tài được hoàn thiện về cả mặt lý thuyết lẫn thực nghiệm.

Nhóm cũng xin cảm ơn gia đình và bạn bè đã luôn động viên, hỗ trợ tinh thần và tham gia trải nghiệm thử nghiệm hệ thống trong giai đoạn đánh giá.

Do giới hạn về thời gian và nguồn lực, báo cáo khó tránh khỏi những thiếu sót nhất định. Nhóm nghiên cứu mong nhận được những ý kiến đóng góp từ Hội đồng để tiếp tục hoàn thiện và phát triển hệ thống trong các nghiên cứu tiếp theo.

Xin trân trọng cảm ơn.

---

TÓM TẮT

Sự phát triển nhanh chóng của Trí tuệ Nhân tạo (AI), đặc biệt là các Mô hình Ngôn ngữ Lớn (LLM), đã mở ra nhiều hướng tiếp cận mới trong việc xây dựng các hệ thống trợ lý thông minh theo miền chuyên biệt. Trong bối cảnh ngành du lịch địa phương đang thúc đẩy chuyển đổi số, việc ứng dụng LLM vào cung cấp thông tin và hỗ trợ du khách theo thời gian thực là một hướng nghiên cứu có tính thực tiễn cao.

Báo cáo này trình bày quá trình nghiên cứu, thiết kế và triển khai hệ thống trợ lý du lịch ảo cho khu vực Quy Nhơn – Bình Định. Hệ thống được xây dựng nhằm giải quyết các bài toán phân loại ý định người dùng, truy xuất dữ liệu thực tế và sinh phản hồi phù hợp với ngữ cảnh truy vấn.

Kiến trúc hệ thống được tổ chức theo mô hình Multi-Agent, bao gồm ba thành phần chính: Orchestrator Agent đảm nhiệm phân loại intent và định tuyến xử lý; Response Agent chịu trách nhiệm sinh phản hồi hội thoại chung; Planning Agent thực hiện xây dựng lịch trình du lịch có cấu trúc. Để hạn chế hiện tượng sinh thông tin sai lệch, hệ thống tích hợp sáu công cụ truy xuất dữ liệu động kết nối trực tiếp với cơ sở dữ liệu quan hệ PostgreSQL mang tên BinhDinh_TourGuide, bao gồm năm bảng dữ liệu về ẩm thực, nhà hàng, điểm tham quan, khách sạn và dịch vụ du lịch.

Lõi xử lý ngôn ngữ tự nhiên sử dụng mô hình Qwen/Qwen2.5-7B-Instruct:together thông qua HuggingFace Router và giao diện lập trình OpenAI-compatible API. Backend được triển khai bằng FastAPI, trong khi giao diện người dùng được xây dựng bằng Streamlit theo kiến trúc client–server.

Kết quả thực nghiệm cho thấy kiến trúc Multi-Agent kết hợp xác thực dữ liệu bằng Pydantic và cơ chế truy xuất có kiểm soát giúp nâng cao độ chính xác phân loại intent, cải thiện tính nhất quán của phản hồi và đảm bảo tính ổn định của hệ thống. Đề tài đóng góp một mô hình triển khai thực tiễn cho ứng dụng LLM trong lĩnh vực du lịch địa phương, đồng thời tạo tiền đề cho các hướng mở rộng như tích hợp truy xuất ngữ nghĩa và triển khai trên môi trường điện toán đám mây.

Từ khóa: Trợ lý du lịch ảo, Multi-Agent System, Large Language Model (LLM), Intent Classification, Prompt Engineering, Pydantic Validation, PostgreSQL, FastAPI, Streamlit, Quy Nhơn, Bình Định.


---

DANH MỤC HÌNH ẢNH

Hình 1.1. Sơ đồ luồng hoạt động tổng quan của hệ thống trợ lý du lịch ảo ........ [Trang]
Hình 2.1. Kiến trúc Multi-Agent với 3 Agents và 6 Tools ................................. [Trang]
Hình 3.1. Sơ đồ quan hệ thực thể (ERD) của cơ sở dữ liệu BinhDinh_TourGuide ... [Trang]
Hình 4.1. Giao diện tương tác người dùng xây dựng bằng Streamlit ............... [Trang]
Hình 4.2. Kết quả trả về JSON từ Orchestrator Agent ................................. [Trang]
Hình 5.1. Ví dụ chức năng sinh lịch trình du lịch tự động ............................. [Trang]

---

DANH MỤC BẢNG BIỂU

Bảng 2.1. Mô tả chức năng của năm bảng trong cơ sở dữ liệu BinhDinh_TourGuide ... [Trang]
Bảng 3.1. Định nghĩa các Intent và cấu trúc schema Pydantic tương ứng ........ [Trang]
Bảng 4.1. Các endpoint của hệ thống REST API FastAPI .............................. [Trang]
Bảng 5.1. Kết quả kiểm thử độ chính xác của các Agent .............................. [Trang]

---

DANH MỤC TỪ VIẾT TẮT

AI – Artificial Intelligence – Trí tuệ nhân tạo
API – Application Programming Interface – Giao diện lập trình ứng dụng
GPS – Global Positioning System – Hệ thống định vị toàn cầu
HF – HuggingFace – Nền tảng cung cấp và phân phối mô hình học máy
HTTP – HyperText Transfer Protocol – Giao thức truyền tải siêu văn bản
JSON – JavaScript Object Notation – Định dạng trao đổi dữ liệu
LLM – Large Language Model – Mô hình ngôn ngữ lớn
NCKH – Nghiên cứu khoa học
NLP – Natural Language Processing – Xử lý ngôn ngữ tự nhiên
ORM – Object-Relational Mapping – Ánh xạ đối tượng – quan hệ
RAG – Retrieval-Augmented Generation – Sinh văn bản tăng cường truy xuất
SQL – Structured Query Language – Ngôn ngữ truy vấn cơ sở dữ liệu
