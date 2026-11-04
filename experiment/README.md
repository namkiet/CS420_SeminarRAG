# Dữ liệu thực nghiệm RAG

Corpus gồm **4 tài liệu, tổng cộng 51 trang**, đã chia thành **80 chunks theo cấu trúc tài liệu**.

## Các file cần dùng

| File | Công dụng |
|---|---|
| [chunks_by_structure.json](data/chunks/chunks_by_structure.json) | Chunks để tạo embedding và chỉ mục tìm kiếm. Đọc `chunks[*].text`, giữ metadata để trích dẫn. |
| [corpus_pages.json](data/processed/corpus_pages.json) | Văn bản đầy đủ theo trang, dùng để kiểm tra và tạo lại chunks. |
| [questions.json](data/questions.json) | 20 câu hỏi đánh giá, đáp án chuẩn và 30 đoạn bằng chứng. Không đưa vào chỉ mục tìm kiếm. |
| [sources.json](data/sources.json) | Link nguồn, số quyết định, phạm vi áp dụng và SHA-256 của PDF. |
| `data/raw/*.pdf` | 4 PDF gốc để đối chiếu văn bản, số liệu và bảng. |
| [chunk_by_structure.py](scripts/chunk_by_structure.py) | Script tạo lại chunks, chỉ dùng thư viện chuẩn Python. |

Đây là dữ liệu cho pipeline RAG: chia tài liệu → embedding → retrieval → sinh câu trả lời. Bộ câu hỏi hiện dùng để đánh giá, chưa phải bộ dữ liệu fine-tuning.

## Nguyên tắc chia

Ví dụ: tài liệu có 3 chương, mỗi chương 4 mục, mỗi mục 5 gạch đầu dòng → **12 chunks**. Mỗi chunk giữ đủ 5 gạch đầu dòng của một mục; chương được lưu làm ngữ cảnh.

Với các quy chế trong corpus, cấp tương ứng là **Điều**:

- Mỗi điều là một chunk, chứa toàn bộ các khoản, điểm a/b/c, gạch đầu dòng và bảng bên trong. Không chia mỗi khoản thành một chunk.
- Phụ lục điểm rèn luyện chia theo 6 mục lớn. Các mục con và bảng thuộc mục nào được giữ trong mục đó.
- Phụ lục học phí chia thành 3 mục. Mục bảng học phí giữ nguyên chú giải C1–C7 và đủ 27 dòng, kể cả khi kéo dài từ trang PDF 2 đến 5.
- Không cắt theo số trang hoặc giới hạn 400/800 token; không gom hai điều ngắn để đạt độ dài mục tiêu; không tạo overlap.
- Chương là metadata và tiêu đề chương được giữ cùng điều đầu tiên của chương. Phần mở đầu của mỗi văn bản đi cùng điều/mục đầu tiên.
- Quyết định ban hành, quy chế kèm theo, phụ lục và văn bản sửa đổi được phân biệt bằng `instrument`. D02 giữ riêng vai trò bản gốc và sửa đổi bằng `revision_role`.

Script nhận diện cả chữ OCR `Điêu` như một tiêu đề điều, nhưng giữ nguyên văn bản nguồn. Ranh giới giữa các văn bản kèm trong 4 PDF được khai báo trong hàm `instrument()`; nếu thay bộ PDF, cần kiểm tra lại quy tắc này.

## Kết quả

| Tài liệu | Trang | Chunks |
|---|---:|---:|
| D01 — Quy chế đào tạo | 21 | 30 |
| D02 — Điểm rèn luyện, gồm sửa đổi | 16 | 25 |
| D03 — Học phí | 5 | 7 |
| D04 — Ngoại ngữ | 9 | 18 |
| **Tổng** | **51** | **80** |

Số chunks bao gồm các điều trong quyết định ban hành và các mục phụ lục. Có 30 chunks đi qua nhiều trang. Chunk dài nhất có 5.486 ký tự; đây là số ký tự, không phải số token.

Đếm riêng trường `text` bằng tokenizer `cl100k_base`: trung bình khoảng **675 token/chunk**, trung vị **564**, ngắn nhất **27**, dài nhất **2.572**. Đây là thống kê tham khảo; script chia cấu trúc không phụ thuộc tokenizer. Cần đếm lại bằng tokenizer của mô hình embedding được chọn.

Script kiểm tra mọi ký tự nguồn đều được giữ đúng một lần trong `source_spans`, không lẫn tài liệu/văn bản/phiên bản, và có thể dựng lại văn bản từ các vị trí nguồn. Kiểm tra độc lập xác nhận ví dụ 3 × 4 mục tạo đúng 12 chunks, đủ 27 dòng bảng học phí và 30/30 đoạn bằng chứng nằm trọn trong chunk tương ứng. Đây chưa phải kết quả đo retrieval.

## Chạy lại

Từ thư mục gốc repo `CS420_SeminarRAG`, chạy:

```powershell
python experiment/scripts/chunk_by_structure.py
```

Không cần cài thêm package. Script chỉ đọc `corpus_pages.json` và `sources.json`, không dùng câu hỏi/đáp án để quyết định ranh giới. Output ghi vào `experiment/data/chunks/chunks_by_structure.json`. Hai bộ chunks 400/800 token cũ đã được thay bằng file này.

## Đọc chunks

```python
import json
from pathlib import Path

payload = json.loads(
    Path("experiment/data/chunks/chunks_by_structure.json").read_text(encoding="utf-8")
)
chunks = payload["chunks"]
texts = [chunk["text"] for chunk in chunks]
```

Output có `config`, `statistics`, `chunks`. Mỗi chunk có `chunk_id`, `doc_id`, `instrument`, `revision_role`, `chapter`, `section`, `section_number`, `pdf_pages`, `text`, `char_count`, URL nguồn và trạng thái kiểm tra.

`source_spans` lưu `pdf_page`, `char_start`, `char_end`: vị trí ký tự trong `text` của trang nguồn, bắt đầu từ 0, kết thúc không bao gồm ký tự ở `char_end`. Văn bản giữ nguyên, chỉ thêm hai dấu xuống dòng khi nối trang; metadata không được tự chèn vào trường `text`.

## Việc tiếp theo

- Chọn mô hình embedding và kiểm tra số token từng chunk bằng tokenizer của mô hình đó. Cách chia hiện tại không đặt trần token; cần kiểm tra giới hạn đầu vào trước khi index để tránh bị cắt mất nội dung.
- Tạo embedding/index từ `chunks[*].text`; khi cần, bổ sung tên tài liệu, chương và điều từ metadata vào đầu vào embedding. Không index thêm bản theo trang hoặc bộ câu hỏi vào cùng chỉ mục.
- Gán và kiểm tra `relevant_chunk_ids` trong bộ câu hỏi trước khi đo Recall@k; các trường này hiện vẫn rỗng. ID chunks đã thay đổi theo cách chia mới.
- D02 phải đọc bản gốc cùng sửa đổi 2023; lưu ý phạm vi áp dụng, năm học và khóa tuyển của từng tài liệu.
- Chất lượng văn bản: 22 trang có bản chép/khôi phục bảng từ ảnh; 29 trang OCR còn cần đối chiếu độc lập. Mọi trang vẫn có `human_review_status: pending`. Bao phủ 51 trang không có nghĩa OCR đã hoàn toàn chính xác.
