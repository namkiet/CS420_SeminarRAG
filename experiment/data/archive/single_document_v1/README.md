# Dữ liệu thực nghiệm RAG — G2 Task 1–2

## Phạm vi

- G2 Task 1: corpus khoảng 5–10 trang tài liệu công khai hoặc được cấp phép phù hợp, có nguồn xác minh được.
- G2 Task 2: 15–20 câu hỏi, mỗi câu có đáp án chuẩn và nguồn hỗ trợ.
- Nguồn corpus đã chọn: website chính thức HCMUS (`https://hcmus.edu.vn/`).
- Phạm vi đã thực hiện: hỏi đáp về học phần, tín chỉ, thời gian đào tạo, tổ chức đào tạo và đăng ký học tập theo Quy chế 2026.
- Nguồn: [Quy chế đào tạo trình độ đại học năm 2026](https://hcmus.edu.vn/quy-che-dao-tao-trinh-do-dai-hoc-nam-2026/), đăng ngày 16/10/2026; QĐ3087/QĐ-KHTN ngày 29/09/2026.
- Đã tải PDF gốc 21 trang và chọn **6 trang nguồn: PDF 4–8 và 21**, tương ứng trang in 3–7 và 20.
- Đã tạo **20 câu hỏi**: 5 tra cứu trực tiếp, 7 diễn đạt lại, 8 kết hợp nhiều đoạn bằng chứng. Có tổng cộng 29 đoạn trích hỗ trợ.
- Điều 27 được giữ trong corpus để làm rõ chuyển tiếp: không mặc định mọi quy định mới áp dụng nguyên trạng cho khóa 2025 trở về trước.

## Cấu trúc

- `raw/D01_quy_che_dao_tao_2026.pdf`: PDF gốc 21 trang, dùng đối chiếu nguồn; **không index toàn bộ file này** trong thí nghiệm corpus 6 trang.
- `processed/D01_corpus.md`: bản chép sạch có mốc trang, dễ đọc và kiểm tra.
- `processed/D01_corpus.txt`: văn bản liên tục để chia chunks, đã nối hai câu qua ranh giới trang.
- `processed/D01_pages.json`: văn bản theo trang, phù hợp nếu cần giữ metadata khi chia chunks. Cần xử lý nối câu ở trang 5–6 và 7–8.
- `sources.json`: metadata của nguồn D01, URL gốc, trang đã chọn, SHA-256 của PDF.
- `questions.json`: 20 câu hỏi, đáp án, các ý cần có, evidence và vị trí nguồn; dùng để đánh giá, **không đưa vào chỉ mục retrieval**.
- `questions.md`: bản đọc của bộ câu hỏi và bằng chứng, có link đến PDF gốc.
- `BAN_GIAO.md`: ghi chú phương pháp, giới hạn và cách bàn giao cho Task 3–4.
- `templates/`: mẫu cấu trúc, không phải dữ liệu dùng đánh giá.

Tạo lại các file JSON, TXT và bản câu hỏi Markdown từ bản chép sạch: `python scripts/build_huy_dataset.py` (chạy tại thư mục Seminar, cần PyMuPDF). Script kiểm tra mọi đoạn evidence đều có trong đúng trang corpus. Kiểm tra này không thay thế việc đọc ảnh PDF gốc.

## Thứ tự làm

1. Chốt chủ đề và phạm vi tài liệu với nhóm.
2. Tìm nguồn gốc, kiểm tra quyền sử dụng và phiên bản áp dụng; chọn tổng cộng khoảng 5–10 trang.
3. Lưu bản gốc vào `raw/`, ghi thông tin vào `sources.json`.
4. Tạo văn bản sạch trong `processed/`; đối chiếu bản gốc, đặc biệt bảng và các điều kiện/ngoại lệ.
5. Soạn 15–20 câu hỏi trong `questions.json`, dựa trên corpus đã chốt.
6. Kiểm tra từng đáp án với đoạn bằng chứng, ghi đủ các đoạn nếu cần kết hợp nhiều nguồn.
7. Bàn giao cho người làm Task 3–4; ánh xạ các đoạn bằng chứng sang chunk_id khi có kết quả chia chunks.

## Quy ước đề xuất

- Tài liệu: `D01`, `D02`, ...; câu hỏi: `Q01`, `Q02`, ...
- `pdf_page`: số trang của file PDF, bắt đầu từ 1. Dùng `null` cho nguồn không có trang PDF.
- `printed_page`: số trang in trên tài liệu, nếu có; tránh nhầm với số trang PDF.
- `section`: tên mục/điều/khoản hoặc tiêu đề trên trang web.
- `quote`: đoạn trích hỗ trợ trực tiếp đáp án; kiểm tra từ nguồn gốc.
- `verified: true`: trợ lý đã đọc ảnh trang PDF và đối chiếu nội dung; xem `verification_method` trong mỗi câu hỏi. **Không có nghĩa là thành viên nhóm đã kiểm chứng độc lập.**
- `human_review_status: pending`: nhóm cần tự đọc lại, sửa thành `reviewed` sau khi hoàn tất. Không chạy lại script sinh dữ liệu sau khi sửa tay mà chưa lưu thay đổi vào script.
- Khi chưa có chunks, giữ `relevant_chunk_ids` là danh sách rỗng. Mỗi cấu hình chunking có thể tạo ID khác nhau; giữ evidence theo trang/mục làm tham chiếu ổn định.

## Điều kiện bàn giao

- [x] Corpus có phạm vi rõ ràng: 6 trang nguồn.
- [x] Tài liệu có URL nguồn, ngày/phiên bản, ghi nhận cách sử dụng và checksum.
- [x] Văn bản sạch được trợ lý đối chiếu ảnh PDF gốc.
- [x] Có 20 câu hỏi và đáp án tham chiếu.
- [x] Mỗi câu hỏi có bằng chứng theo trang/điều/khoản; các đoạn trích đã qua kiểm tra tự động.
- [ ] Nhóm tự kiểm chứng độc lập trước khi nộp.
- [ ] Ánh xạ evidence sang chunk_id theo từng cấu hình ở Task 3–4.

Độ đa dạng câu hỏi (tra cứu trực tiếp, diễn đạt lại, kết hợp nhiều đoạn) là gợi ý thiết kế. Đề không quy định tỷ lệ từng loại.
