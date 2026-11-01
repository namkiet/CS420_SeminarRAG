# Prompt trích xuất toàn bộ corpus

```text
Đọc đủ 4 PDF gốc trong experiment/data/raw/: D01 21 trang, D02 16 trang,
D03 5 trang, D04 9 trang. Chuyển toàn bộ nội dung có ý nghĩa của đủ 51/51
trang thành văn bản dùng cho RAG. Không tóm tắt, không chỉ lấy phần trả lời
được bộ câu hỏi hiện có, không tự chọn bỏ điều/khoản/phụ lục/căn cứ.

Yêu cầu:
1. Giữ thứ tự từng tài liệu và từng trang. Mỗi trang có doc_id, pdf_page,
   printed_page nếu có, điều/mục và văn bản; phân biệt số trang PDF với số in.
2. PDF scan hoặc lớp chữ lỗi phải OCR tiếng Việt/Anh; không đoán nội dung
   bị mờ. Gắn nhãn phần cần kiểm tra, đối chiếu với ảnh gốc.
3. Giữ bảng, tiêu đề cột, đơn vị, ô gộp, công thức, số liệu, điều kiện và
   ngoại lệ. Không thay bảng bằng một đoạn diễn giải làm mất hàng/cột.
4. Giữ cả quy chế gốc và quyết định sửa đổi. Ghi rõ vùng nào là bản gốc,
   vùng nào sửa đổi/thay thế. Không tự tạo văn bản hợp nhất hoặc sửa các
   mâu thuẫn nguồn nếu chưa có căn cứ.
5. Giữ PDF gốc, URL, ngày/phiên bản, phạm vi áp dụng và checksum.
6. Xuất Markdown toàn bộ từng tài liệu, JSON theo trang, corpus gộp và
   báo cáo độ phủ. Kiểm tra chính xác D01=21, D02=16, D03=5, D04=9,
   tổng=51, không thiếu/trùng/trang rỗng. Đếm metadata đủ 51 không thay
   thế việc kiểm tra nội dung, đặc biệt bảng/công thức OCR dễ bỏ sót.
7. Phân biệt độ phủ với độ chính xác: không tuyên bố sạch hoàn toàn hoặc
   đã được người dùng kiểm chứng nếu mới chạy OCR. Lưu trạng thái từng trang.
8. Script build chỉ dùng các đầu vào hiện tại, không đưa đáp án chuẩn vào chỉ mục.
   Mọi câu hỏi tham chiếu phải kiểm tra lại bằng chứng sau khi đổi corpus.
9. Báo cáo rõ những gì hoàn thành, các lỗi OCR chưa được kiểm tra và các
   phần cần đối chiếu tiếp. Không bịa nội dung để đạt đủ số trang.
```
