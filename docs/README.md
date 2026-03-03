# Tài liệu báo cáo khoa học – Quy Nhon Virtual Travel Assistant

Thư mục `docs/` là không gian làm việc tập trung để biên soạn báo cáo khoa học/đồ án tốt nghiệp cho đề tài **Hệ thống trợ lý du lịch ảo Quy Nhơn sử dụng kiến trúc Multi-Agent và mô hình ngôn ngữ lớn**.

Mục tiêu của thư mục này:
- Chuẩn hóa cấu trúc nội dung báo cáo theo định dạng học thuật.
- Đồng bộ nội dung viết với hiện trạng triển khai thực tế trong codebase.
- Hỗ trợ quy trình viết theo từng phần/chương một cách có hệ thống.

---

## 1) Cấu trúc tài liệu trong thư mục `docs/`

### Tài liệu điều hướng chính
- `MUC_LUC_BAO_CAO_CAP_NHAT.md`  
  Mục lục tổng thể (master TOC), bao gồm cấu trúc 5 chương, các phần đầu báo cáo, phụ lục, và các ghi chú kỹ thuật quan trọng.

- `README.md` (file này)  
  Hướng dẫn tổ chức tài liệu, quy tắc cập nhật, và lộ trình biên soạn.

### Tài liệu phần đầu báo cáo
- `PHAN_DAU_BAO_CAO.md`  
  Bao gồm: Trang phụ bìa, Lời cam đoan, Lời cảm ơn, Tóm tắt, Danh mục hình ảnh, Danh mục bảng biểu, Danh mục từ viết tắt.

- `PHAN_MO_DAU.md`  
  Nội dung Phần mở đầu: lý do chọn đề tài, mục tiêu, đối tượng/phạm vi, phương pháp nghiên cứu, cấu trúc báo cáo.

### Tài liệu theo chương
- `chuong-1.md` đến `chuong-5.md`  
  Nội dung chi tiết từng chương (soạn và cập nhật dần theo master TOC).

### Tài liệu tham khảo/phụ trợ
- `REFERENCES`  
  Danh sách tài liệu tham khảo dùng xuyên suốt báo cáo.

- `phu-luc.md`  
  Nội dung phụ lục: prompt, schema, script dữ liệu, hướng dẫn cài đặt/chạy, tài liệu đối chiếu hành chính.

---

## 2) Nguyên tắc biên soạn

Để đảm bảo tính nhất quán và khả năng nghiệm thu học thuật, khi cập nhật tài liệu cần tuân thủ:

1. **Bám sát code thực tế**
   - Mọi mô tả kiến trúc/chức năng cần đối chiếu từ source code hiện tại.
   - Tránh ghi nhận các tính năng chưa triển khai.

2. **Ưu tiên tính truy vết (traceability)**
   - Nội dung trong chương nên tham chiếu rõ tới file/module liên quan trong repo (agents, tools, main.py, app.py, script_init_database, prompts).

3. **Phân tách rõ “đã làm” và “hướng phát triển”**
   - Những nội dung chưa hoàn thiện phải đặt ở phần hạn chế/hướng phát triển, không mô tả như chức năng đã chạy ổn định.

4. **Thống nhất thuật ngữ**
   - Dùng nhất quán thuật ngữ: Intent, Multi-Agent, Orchestrator, Tool Layer, Pydantic Validation, Routing JSON, v.v.

---

## 3) Quy trình làm việc đề xuất theo từng vòng

Mỗi vòng cập nhật báo cáo nên đi theo trình tự:

1. Cập nhật/đối chiếu lại `MUC_LUC_BAO_CAO_CAP_NHAT.md` nếu có thay đổi phạm vi.
2. Soạn nội dung chi tiết cho 1 chương đích (`chuong-x.md`).
3. Đồng bộ lại phần trích dẫn trong `REFERENCES` (nếu phát sinh nguồn mới).
4. Rà soát chéo với các phần đã viết để tránh mâu thuẫn số liệu/thuật ngữ.
5. Chốt phiên bản bằng commit riêng cho từng chương để dễ theo dõi lịch sử.

---

## 4) Mapping nhanh giữa nội dung báo cáo và mã nguồn

- **Kiến trúc & điều phối pipeline**: `main.py`
- **Orchestrator/Response/Planning Agents**: `agents/`
- **Tool truy xuất dữ liệu và thời tiết**: `tools/`
- **Prompt hệ thống**: `prompts/`
- **Khởi tạo & nạp dữ liệu PostgreSQL**: `script_init_database/`
- **Giao diện người dùng**: `app.py`
- **Phụ thuộc môi trường**: `requirements.txt`

---

## 5) Lưu ý chất lượng tài liệu

- Ưu tiên viết ngắn gọn, chính xác, có số liệu và dẫn chứng.
- Mỗi chương nên có: mục tiêu chương → nội dung chính → tóm tắt chương.
- Các bảng/hình trong báo cáo cần đồng bộ với danh mục hình ảnh/bảng biểu đã khai báo ở phần đầu.
- Khi có thay đổi lớn về cấu trúc chương, cập nhật lại `MUC_LUC_BAO_CAO_CAP_NHAT.md` trước.

---

## 6) Trạng thái hiện tại

Thư mục `docs/` hiện đã có:
- Bộ khung đầy đủ cho phần đầu báo cáo.
- Master TOC chi tiết theo cấu trúc 5 chương.
- File nguồn tham khảo (`REFERENCES`).
- Placeholder cho các chương và phụ lục để triển khai nội dung chi tiết ở các phiên tiếp theo.
