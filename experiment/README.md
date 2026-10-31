# Thực nghiệm RAG — corpus và bộ câu hỏi tham chiếu (G2 Task 1–2)

## Bắt đầu đọc

- [Danh sách bốn tài liệu, link nguồn và phạm vi corpus](data/CORPUS_4_TAI_LIEU.md).
- [Corpus sạch gộp](data/processed/corpus_all.md).
- [20 câu hỏi, đáp án chuẩn và bằng chứng](data/questions.md).

## Dữ liệu hiện có

| Phần | Vị trí | Nội dung |
|---|---|---|
| PDF gốc | `data/raw/` | 4 PDF, tổng 51 trang: đào tạo/tốt nghiệp, điểm rèn luyện, học phí, ngoại ngữ tốt nghiệp |
| Corpus sạch | `data/processed/corpus_pages.json` | Trích chọn nội dung từ 25 trang nguồn; không phải toàn văn 51 trang |
| Nguồn | `data/sources.json` | URL, phiên bản, đối tượng áp dụng, vị trí file và SHA-256 |
| Bộ đánh giá | `data/questions.json` | 20 câu hỏi và 30 đoạn bằng chứng, phiên bản `multi_document_v2` |
| Thống kê | `data/corpus_manifest.json` | Số tài liệu, trang nguồn và bằng chứng |
| Bản đầu | `data/archive/single_document_v1/` | Dữ liệu một nguồn cũ; script sử dụng làm đầu vào tái tạo, không index |

Phần sạch hiện tại là **bản trích chọn**. Mong muốn dùng toàn bộ nội dung có ý nghĩa của 51 trang vẫn cần bước chép sạch/kiểm chứng bổ sung. Việc copy vào repo không thay đổi mức độ hoàn thiện này.

## Tái tạo output

Từ thư mục gốc repo:

```powershell
python -m pip install -r experiment/requirements.txt
python experiment/scripts/build_multi_document_dataset.py
```

Script xác định thư mục dữ liệu theo vị trí của chính nó, nên không phụ thuộc working directory. Nó dùng PDF và Markdown đã có trong repo, không cần gọi mạng hay LLM để chạy. Script ghi lại `sources.json`, các JSON theo trang, corpus gộp và bộ câu hỏi; nếu sửa thủ công output thì cần cập nhật đầu vào/script trước khi chạy lại.

## Quy trình chuẩn bị và bàn giao

1. **Chọn miền dữ liệu:** hỏi đáp quy định sinh viên HCMUS với bốn văn bản về đào tạo/tốt nghiệp, điểm rèn luyện, học phí và ngoại ngữ tốt nghiệp.
2. **Thu thập:** theo liên kết công bố trên website HCMUS; lưu đủ PDF gốc, URL, phiên bản và checksum.
3. **Kiểm tra phiên bản:** ghi năm học, khóa tuyển và chương trình áp dụng. Trong D02, phân biệt quy chế 2020 với sửa đổi 2023; không xem cả bốn tài liệu là một bộ quy định đồng nhất mới nhất.
4. **Chuẩn hóa:** trích chọn các phần đã đối chiếu ảnh PDF; giữ số liệu, điều kiện và ngoại lệ, chuyển bảng học phí thành Markdown. Bản gốc được giữ nguyên.
5. **Tạo tham chiếu:** soạn 20 câu hỏi, đáp án chuẩn, các ý cần có và đoạn bằng chứng. Các phép tính minh họa được ghi rõ là do nhóm xây dựng.
6. **Kiểm tra:** script xác nhận mọi đoạn bằng chứng tồn tại trên đúng trang của bản sạch; ảnh PDF được trợ lý đọc riêng. Nhóm cần tự kiểm chứng trước khi nộp và khai báo công cụ AI theo yêu cầu môn học.
7. **Bàn giao Task 3–4:** dùng `data/processed/corpus_pages.json` làm đầu vào retrieval và giữ `data/questions.json` ở phía đánh giá. Gán nhãn chunks sau khi đã xác định cách chia tài liệu.

## Dùng cho Task 3–4

Chỉ index nội dung trường `text` trong `data/processed/corpus_pages.json`, giữ metadata `doc_id`, `pdf_page`, `section` và phiên bản. Không quét index toàn bộ thư mục `data/` vì có đáp án chuẩn, archive và tài liệu hướng dẫn.

`relevant_chunk_ids` đang rỗng vì chưa chia chunks. Cần ánh xạ bằng chứng sang chunk ID theo từng cấu hình rồi mới tính Recall@k. Với bảng học phí, mỗi chunk phải có tiêu đề/ý nghĩa cột.

## Giới hạn và kiểm chứng

- Chưa có retrieval, bảng Recall@k hoặc kết quả sinh câu trả lời.
- `human_review_status: pending`: chưa ghi nhận thành viên nhóm tự kiểm chứng độc lập.
- Điểm rèn luyện D02 cố định ở PDF 2020 kèm sửa đổi 2023, không khẳng định đây là toàn bộ quy định mới nhất năm 2026.
- Năm học, khóa tuyển và chương trình áp dụng phải được giữ khi trả lời.
- Bộ mở rộng này lớn hơn gợi ý corpus khoảng 5–10 trang trong đề; cần ghi đúng phạm vi thực nghiệm của nhóm.
- Bộ câu hỏi hiện đều có bằng chứng; chưa có bộ câu hỏi không có đáp án để đánh giá khả năng từ chối.
- Kết quả từ bộ dữ liệu nhỏ này không đủ chứng minh RAG loại bỏ hallucination trong mọi tình huống.
- Đạt điều kiện riêng như ngoại ngữ không đồng nghĩa đã đủ mọi điều kiện tốt nghiệp trong quy chế đào tạo.

## Nội dung tham khảo cho báo cáo

> Nhóm xây dựng thư viện tài liệu hỏi đáp về các quy định sinh viên tại Trường Đại học Khoa học tự nhiên, ĐHQG-HCM, gồm bốn tệp PDF gốc với tổng cộng 51 trang. Các tài liệu bao phủ quy chế đào tạo và điều kiện tốt nghiệp, đánh giá điểm rèn luyện, học phí năm học 2026–2027 và chuẩn ngoại ngữ tốt nghiệp. Từ thư viện này, nhóm chuẩn bị corpus sạch bằng cách trích chọn nội dung từ 25 trang nguồn, giữ thông tin mã tài liệu, trang PDF, điều/khoản và phạm vi áp dụng. Nhóm xây dựng bộ 20 câu hỏi có đáp án tham chiếu và 30 đoạn bằng chứng. Các văn bản có phiên bản và đối tượng áp dụng khác nhau được ghi rõ trong metadata và câu hỏi; riêng tài liệu điểm rèn luyện cố định ở bản PDF 2020 kèm sửa đổi 2023. Việc đánh giá retrieval và chất lượng sinh câu trả lời được thực hiện riêng ở bước thực nghiệm tiếp theo.

Đoạn này mô tả sản phẩm đã chuẩn bị với trợ lý AI. Khi đưa vào báo cáo, cần điều chỉnh theo công việc nhóm thực sự thực hiện; không ghi đã tự kiểm chứng nếu chưa hoàn tất.

## Công việc tiếp theo

- Tự kiểm tra nguồn và đáp án; cập nhật `human_review_status` khi hoàn tất.
- Thống nhất metadata, cách xử lý bảng và nhãn chunk liên quan với người thực hiện Task 3–4.
- Hoàn thiện bản sạch toàn văn nếu dùng toàn bộ nội dung có ý nghĩa của 51 trang.
- Chuẩn bị giải thích cách chọn bốn nguồn và phân biệt thư viện gốc với corpus sạch.
- Chuẩn bị một ví dụ tìm bằng chứng đúng và một ví dụ dễ nhầm do phiên bản, chương trình hoặc tiêu đề cột.
