# Thực nghiệm RAG — corpus toàn bộ 51 trang

Phần chuẩn bị dữ liệu và bộ câu hỏi cho G2 Task 1–2.

## Sản phẩm hiện tại

| Tài liệu | Trang gốc | Trang có trong corpus |
|---|---:|---:|
| D01 — Quy chế đào tạo, gồm điều kiện tốt nghiệp | 21 | 21 |
| D02 — Điểm rèn luyện, phụ lục và sửa đổi 2023 | 16 | 16 |
| D03 — Học phí 2026–2027 | 5 | 5 |
| D04 — Học ngoại ngữ và chuẩn ngoại ngữ tốt nghiệp | 9 | 9 |
| **Tổng** | **51** | **51** |

- [Danh sách nguồn và phạm vi corpus](data/CORPUS_4_TAI_LIEU.md).
- [Corpus toàn bộ để đọc](data/processed/corpus_all.md).
- [Corpus theo trang để index](data/processed/corpus_pages.json).
- [Kiểm tra thiếu/trùng trang và chất lượng](data/coverage_report.json).
- [20 câu hỏi kèm đáp án và bằng chứng](data/questions.md).

**Độ phủ đủ 51/51 trang; chất lượng OCR chưa được kiểm chứng hoàn toàn.** Có 22 trang đã chép/khôi phục bảng từ ảnh và 29 trang OCR cần kiểm tra độc lập. Mọi trang vẫn giữ trạng thái nhóm tự kiểm chứng là `pending`. Đã phục hồi các bảng/công thức quan trọng mà OCR tự động làm mất hoặc lệch, không chỉ tạo 51 mục metadata rỗng.

## Quy trình chuẩn bị

1. Giữ nguyên bốn PDF gốc và metadata nguồn, phiên bản, phạm vi áp dụng, SHA-256.
2. OCR mọi trang với Tesseract Việt/Anh chạy cục bộ qua PyMuPDF; không bỏ trang theo câu hỏi.
3. Giữ bản OCR nguyên trạng trong `data/extracted/`; chép lại các bảng khó và sửa các đoạn đã đối chiếu trong bản Markdown.
4. Giữ mốc trang, thứ tự điều, căn cứ, phụ lục, công thức và cả bản gốc lẫn sửa đổi. Metadata `revision_role` phân biệt vùng 2020/2023 của D02.
5. Tạo JSON theo trang, corpus gộp, báo cáo độ phủ và bộ câu hỏi. Script kiểm tra đủ 21+16+5+9 trang, không trùng/thiếu và mọi đoạn bằng chứng còn trong corpus.
6. Nhóm kiểm chứng tiếp các trang OCR và các số liệu quan trọng trước khi dùng làm kết luận nghiên cứu.

## Chạy script build

Từ thư mục gốc repo:

```powershell
python -m pip install -r experiment/requirements.txt
python experiment/scripts/build_multi_document_dataset.py
```

Script này không phải hệ thống RAG. Nó tái tạo output từ bản Markdown toàn văn và các đầu vào độc lập:

- `data/source_catalog.json`: nguồn tài liệu.
- `data/page_review.json`: trạng thái OCR/kiểm chứng từng trang.
- `data/questions.reference.json`: câu hỏi, đáp án và bằng chứng tham chiếu.
- `data/processed/D01_corpus.md` đến `D04_corpus.md`: văn bản toàn bộ, là đầu vào có thể chỉnh sửa.
- `data/extracted/*_ocr_pages.json`: bản OCR gốc để xác minh nguồn trích xuất.

Script không gọi mạng/LLM, không cần model OCR. Nếu sửa câu hỏi, sửa `questions.reference.json`; nếu sửa văn bản, sửa đúng Markdown và cập nhật trạng thái trang, rồi build. Không chỉ sửa các JSON output vì chạy lại sẽ ghi đè chúng.

## Chạy lại OCR (tùy chọn)

Tải `vie.traineddata` và `eng.traineddata` từ kho chính thức [tesseract-ocr/tessdata_best](https://github.com/tesseract-ocr/tessdata_best) vào một thư mục ngoài dữ liệu index, sau đó:

```powershell
python experiment/scripts/extract_full_pdf_ocr.py --tessdata C:/path/to/tessdata --workers 3
```

Đây là đường dẫn mẫu, phải thay bằng thư mục model thật. Output OCR thô nằm trong `experiment/tmp/full_ocr/`, không tự ghi đè bản đã chỉnh sửa. Cần đối chiếu ảnh và hợp nhất sửa lỗi trước khi cập nhật Markdown. Các file model và ảnh kiểm tra tạm không cần push lên Git.

## Bàn giao Task 3–4

Chỉ index trường `text` trong `data/processed/corpus_pages.json`. Giữ `doc_id`, `pdf_page`, `section`, phiên bản, `revision_role` và trạng thái chất lượng ở metadata.

- Không index câu hỏi/đáp án, các bản OCR thô hoặc bản sửa bảng riêng lần nữa.
- Bảng phải mang theo tiêu đề cột; câu nối qua trang cần được giữ ngữ cảnh.
- Giữ cả bản cũ và sửa đổi để bảo toàn tài liệu, nhưng khi trả lời theo bản sau sửa đổi phải ưu tiên đúng văn bản; tránh trả lời bằng khoản đã bị thay thế.
- `relevant_chunk_ids` đang rỗng vì chưa chia chunks; cần gán theo mỗi cấu hình trước khi tính Recall@k.
- 20 câu hỏi hiện có vẫn có đủ bằng chứng nhưng chưa bao phủ toàn bộ 51 trang.

## Giới hạn và công việc tiếp theo

- Chưa có retrieval, bảng Recall@k hoặc kết quả sinh câu trả lời.
- Đủ trang không đồng nghĩa OCR đúng mọi chữ/số; cần đọc lại 29 trang còn gắn nhãn OCR và kiểm chứng độc lập toàn bộ dữ liệu theo yêu cầu môn học.
- Bộ bốn PDF không được mặc định là mọi quy định mới nhất của Trường: D02 là bản 2020 kèm sửa đổi 2023, và các văn bản khác có khóa/năm học/chương trình riêng.
- Bản đầy đủ lớn hơn gợi ý 5–10 trang của đề; báo cáo đúng quy mô thực tế, không gọi 51 trang là corpus 5–10 trang.
- Bộ nhỏ do nhóm xây dựng chưa đủ chứng minh RAG loại bỏ hallucination trong mọi tình huống.

## Mô tả tham khảo cho báo cáo

> Nhóm thu thập bốn tệp PDF từ các trang công bố chính thức của HCMUS, gồm 51 trang về quy chế đào tạo, đánh giá điểm rèn luyện, học phí và ngoại ngữ tốt nghiệp. Toàn bộ trang được đưa vào quy trình trích xuất, giữ điều khoản, phụ lục và các văn bản sửa đổi. Văn bản được OCR cục bộ bằng model Việt/Anh, kết hợp bản chép và khôi phục bảng từ ảnh; trạng thái kiểm chứng được lưu riêng theo trang. Bộ 20 câu hỏi tham chiếu kèm 30 đoạn bằng chứng được giữ để đánh giá, đồng thời kiểm tra lại vị trí bằng chứng trong corpus toàn bộ. Nhóm phân biệt độ phủ trang với độ chính xác nhận dạng và cần kiểm chứng độc lập dữ liệu trước khi báo cáo kết quả thực nghiệm.

Chỉnh đoạn này đúng với công việc nhóm thực sự đã thực hiện và khai báo công cụ AI theo đề.

## Prompt tái sử dụng

[Yêu cầu trích xuất đầy đủ, không tóm tắt hoặc chọn bỏ điều](docs/FULL_CORPUS_PROMPT.md).
