# Corpus hỏi đáp quy định HCMUS — 4 tài liệu

Phiên bản hiện tại: `multi_document_v2`, cập nhật 01/11/2026. Mở rộng phạm vi corpus từ một quy chế sang nhiều văn bản. Chưa thu thập syllabus.

## Bộ tài liệu gốc đã tải

| Mã | Chủ đề và phiên bản | File gốc | Số trang PDF |
|---|---|---|---:|
| D01 | Quy chế đào tạo, QĐ3087 ngày 29/09/2026; có Điều 19 về điều kiện tốt nghiệp và Điều 27 về chuyển tiếp | [Mở PDF](raw/D01_quy_che_dao_tao_2026.pdf) | 21 |
| D02 | Điểm rèn luyện: quy chế 2020 kèm quyết định sửa đổi 2739 ngày 12/12/2023; PDF ghép gồm cả phụ lục | [Mở PDF](raw/D02_quy_che_diem_ren_luyen_2020_sua_2023.pdf) | 16 |
| D03 | Học phí 2026–2027, QĐ3317 ngày 14/10/2026, chính quy đại trà khóa 2022–2026 | [Mở PDF](raw/D03_hoc_phi_2026_2027_K2022_ve_sau.pdf) | 5 |
| D04 | Ngoại ngữ trong quá trình học và khi tốt nghiệp, QĐ2464 ngày 11/08/2026, đại trà/tài năng từ khóa 2022 | [Mở PDF](raw/D04_chuan_ngoai_ngu_tot_nghiep_2026.pdf) | 9 |
| **Tổng** | **4 file PDF gốc, giữ nguyên đầy đủ** | | **51** |

Nguồn công bố chính thức:

- D01: https://hcmus.edu.vn/quy-che-dao-tao-trinh-do-dai-hoc-nam-2026/
- D02: https://hcmus.edu.vn/quy-che-danh-gia-ket-qua-ren-luyen-sinh-vien-he-chinh-quy/
- D03: https://hcmus.edu.vn/thong-bao-nop-hoc-phi-hoc-ky-1-2026-2027-chuong-trinh-dai-tra/
- D04: https://hcmus.edu.vn/quy-dinh-ve-viec-hoc-ngoai-ngu-va-chuan-trinh-do-ngoai-ngu-khi-tot-nghiep-dai-hoc/

Metadata, URL PDF gốc, ngày truy cập, SHA-256 và phạm vi áp dụng được lưu trong [sources.json](sources.json).

## Phân biệt thư viện gốc và corpus sạch

**51 trang là dung lượng bốn PDF gốc, không phải 51 trang đã được chép sạch toàn văn.**

Corpus dùng được ngay cho bộ câu hỏi hiện tại là bản trích chọn nội dung từ **25 trang nguồn** của bốn tài liệu. Không phải toàn bộ nội dung của cả 25 trang đều được giữ: có trang chỉ trích một số khoản, có bảng được chuyển sang Markdown. Tất cả phần được giữ đều có mốc trang PDF và mô tả điều/khoản. Bản gốc đầy đủ vẫn có trong `raw/` để mở rộng tiếp nếu cần.

| Mã | Trang PDF có nội dung trích chọn | Nội dung sạch |
|---|---|---|
| D01 | 4, 5, 6, 7, 8, 17, 18, 21 | [Học vụ](processed/D01_corpus.md), [điều kiện tốt nghiệp](processed/D01_tot_nghiep.md) |
| D02 | 3, 5, 6, 7, 14, 15, 16 | [Điểm rèn luyện và sửa đổi](processed/D02_corpus.md) |
| D03 | 1–5 | [Học phí và toàn bộ bảng 27 ngành](processed/D03_corpus.md) |
| D04 | 1, 5, 6, 7, 8 | [Chuẩn ngoại ngữ và hồ sơ](processed/D04_corpus.md) |

- Đọc gộp: [corpus_all.md](processed/corpus_all.md).
- Đầu vào đề xuất cho Task 3: [corpus_pages.json](processed/corpus_pages.json), gồm `doc_id`, `pdf_page`, `section`, `text` và URL nguồn.
- Thống kê có thể đọc bằng chương trình: [corpus_manifest.json](corpus_manifest.json).
- Tệp `D01_corpus.txt` vẫn chỉ là phần học vụ cũ, **không phải corpus đầy đủ của phiên bản bốn nguồn**.

## Bộ câu hỏi đi kèm

[questions.md](questions.md) / [questions.json](questions.json) hiện chứa **20 câu hỏi bao phủ cả bốn tài liệu**, có đáp án chuẩn, ý cần có và 30 đoạn bằng chứng. Có câu hỏi kết hợp hai tài liệu, câu hỏi về bảng học phí và phép tính minh họa.

Bộ cũ một tài liệu được giữ trong `archive/single_document_v1/`. ID Q01–Q20 của hai phiên bản không có cùng nội dung; chỉ dùng bộ câu hỏi với đúng `corpus_version` của nó. Không đưa thư mục archive hoặc câu hỏi/đáp án vào chỉ mục.

## Quy tắc phiên bản và phạm vi

- D01: cần đọc Điều 27 khi hỏi về khóa 2025 trở về trước. Không mặc định mọi quy định mới áp dụng nguyên trạng cho khóa cũ.
- D02: đây là **snapshot PDF 2020 + sửa đổi 2023**, không khẳng định là mọi quy định hiện hành mới nhất năm 2026. Website Sổ tay sinh viên có bài [trích lược theo Thông tư 40/2026](https://stsv.hcmus.edu.vn/quy-che-diem-ren-luyen) có ngưỡng phân loại khác; chưa đưa bài đó vào corpus. Câu hỏi D02 phải ghi rõ phiên bản. Trong phạm vi snapshot, phần sửa đổi 2023 thay thế các khoản tương ứng của bản 2020; bản sạch đã dùng nội dung sửa đổi ở các khoản được chọn.
- D02: văn bản sửa đổi ghi số quyết định gốc 1208, khác số 1028 trên trang đầu file. Đã ghi nhận khác biệt nguồn; không tự chỉnh bản PDF hoặc suy đoán số đúng.
- D03: chỉ năm học 2026–2027 và các khóa/chương trình ghi trong văn bản. **Tín chỉ học phí** dựa trên số tiết, khác cách hiểu thông thường về tín chỉ học tập. Định mức bốn năm trong bảng được tính tại năm học nêu trong nguồn, không bảo đảm mọi đơn giá bất biến bốn năm.
- D04: phân biệt chuẩn trong quá trình học với chuẩn đầu ra. Tách chương trình đại trà/tài năng và khóa tuyển; không dùng cho chương trình có quyết định ngoại ngữ riêng.

## Công việc tiếp theo

1. Mở bốn PDF gốc để hiểu cấu trúc và phiên bản.
2. Đọc corpus sạch, kiểm tra các đoạn nguồn quan trọng; đối chiếu cả tiêu đề cột khi kiểm tra học phí.
3. Kiểm tra 20 câu hỏi và các đáp án, sau đó cập nhật `human_review_status` khi nhóm tự kiểm chứng.
4. Bàn giao `corpus_pages.json`, `sources.json` và `questions.json` cho Task 3–4.

Mọi trường `human_review_status` hiện là `pending`: đã có trợ lý đọc ảnh và kiểm tra tính nhất quán, chưa ghi nhận thành viên nhóm tự kiểm chứng độc lập. `verified: true` không có nghĩa là đã xác minh mọi văn bản là quy định mới nhất đang có hiệu lực.

## Lưu ý cho Task 3–4

- Chỉ index nội dung corpus sạch đã chọn. Giữ `doc_id`, trang PDF, điều/khoản và phiên bản trong metadata của mỗi chunk.
- Bảng học phí dùng ký hiệu C1–C7: khi chia chunks phải mang theo chú giải cột. Nếu chỉ lấy dòng số mà thiếu tiêu đề cột thì không đủ bằng chứng xác định loại đơn giá.
- Không index README, tài liệu bàn giao, archive, bộ câu hỏi hoặc đáp án chuẩn.
- Gán `relevant_chunk_ids` riêng theo từng cấu hình chunking. Hiện để rỗng vì Task 3 chưa tạo chunks.
- Dùng Hit@k hoặc Recall@k ở cấp chunk/đoạn; với câu cần nhiều bằng chứng hoặc nhiều tài liệu, báo cáo thêm việc có đủ toàn bộ bằng chứng. Có một chunk đúng không đồng nghĩa đủ trả lời.
- Chưa có code retrieval, kết quả Recall@k hay đánh giá sinh câu trả lời trong phần Task 1–2 này.

## Tái tạo dữ liệu

Chạy tại thư mục experiment/: `python scripts/build_multi_document_dataset.py` (cần PyMuPDF).

Script đọc các bản chép sạch Markdown và dữ liệu bản đầu đã lưu, kiểm tra quote trên đúng trang, tạo lại metadata, JSON corpus và bộ câu hỏi. Nó không tải nguồn hoặc tự OCR toàn bộ PDF. Chạy lại sẽ ghi đè các output JSON/câu hỏi; nếu sửa đáp án bằng tay cần cập nhật script tương ứng trước khi chạy lại.

## Quy mô so với đề seminar

Với phạm vi mở rộng, thư viện gốc hiện lớn hơn quy mô khoảng 5–10 trang trong đề. Bộ 4 tài liệu có thể dùng cho hướng thực nghiệm mở rộng. Nếu nhóm muốn có thêm một cấu hình nhỏ đúng quy mô gợi ý của đề, cần chọn rõ tập con 5–10 trang và dùng bộ câu hỏi có bằng chứng trong đúng tập con đó; không báo cáo 51 trang là corpus 5–10 trang.
