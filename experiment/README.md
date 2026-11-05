# Dữ liệu thực nghiệm RAG

Corpus gồm **4 tài liệu, 51 trang**, chia thành **162 chunks với trần 800 token** theo tokenizer `cl100k_base`. Trần tính cả ngữ cảnh và tiêu đề bảng được lặp lại trong trường `text`.

## Các file cần dùng

| File | Công dụng |
|---|---|
| [chunks_by_structure.json](data/chunks/chunks_by_structure.json) | Chunks để tạo embedding/index từ `chunks[*].text`; giữ metadata để trích dẫn. |
| [corpus_pages.json](data/processed/corpus_pages.json) | Văn bản đầy đủ theo trang để kiểm tra và tạo lại chunks. |
| [questions.json](data/questions.json) | 20 câu hỏi đánh giá, đáp án chuẩn và 30 đoạn bằng chứng. Không đưa vào chỉ mục tìm kiếm. |
| [sources.json](data/sources.json) | Link nguồn, số quyết định, phạm vi áp dụng và SHA-256 của PDF. |
| `data/raw/*.pdf` | 4 PDF gốc để đối chiếu. |
| [chunk_by_structure.py](scripts/chunk_by_structure.py) | Script chia theo cấu trúc rồi tách phần dài theo trần token. |
| [requirements.txt](requirements.txt) | Phiên bản `tiktoken` dùng để tái tạo kết quả. |

Đây là dữ liệu cho pipeline RAG: chunking → embedding → retrieval → sinh câu trả lời. Bộ câu hỏi hiện dùng để đánh giá, chưa phải dữ liệu fine-tuning.

## Notebook RAG trên Kaggle

Đã có [notebook Kaggle](notebooks/S07_RAG_Embedding_Kaggle.ipynb) dùng BGE-M3 embeddings, cosine retrieval và Qwen2.5 sinh câu trả lời kèm nguồn. Gắn [Dataset S07 HCMUS RAG Corpus](https://www.kaggle.com/datasets/tunlnh/s07-hcmus-rag-corpus) vào Input. Xem [hướng dẫn chạy và đọc kết quả](notebooks/README.md). Notebook có đánh giá retrieval k=1/3/5 và so sánh cùng LLM có/không RAG trên 20 câu hỏi; điểm chất lượng câu trả lời cần chấm thủ công.

## Nguyên tắc chia

1. Nhận diện **điều** trong quy chế/quyết định và **mục lớn** trong phụ lục. Corpus có 80 điều/mục cha.
2. Nếu toàn bộ điều/mục cùng ngữ cảnh không vượt 800 token, giữ thành một chunk. Không ghép hai điều ngắn để đạt độ dài mục tiêu.
3. Nếu vượt trần, ưu tiên giữ các khoản nguyên vẹn và gom những khoản liên tiếp cùng điều khi vừa giới hạn. Khoản riêng lẻ quá dài được tách tiếp theo đoạn, gạch đầu dòng, câu, rồi khoảng trắng; trường hợp chuỗi liền quá dài mới dùng ranh giới ký tự Unicode.
4. Bảng trong phần vượt trần được chia theo nhóm hàng; không cắt ngang một hàng. Các nhóm sau lặp tiêu đề cột. Bảng học phí lặp đầy đủ chú giải C1–C7, đơn vị và thời gian đào tạo từ nguồn. Nếu một hàng cộng ngữ cảnh vượt trần, script báo lỗi thay vì âm thầm cắt hàng.
5. Mỗi chunk có ngữ cảnh tên tài liệu, loại văn bản và điều/mục. Phần thân nguồn không tạo overlap; tiêu đề/ngữ cảnh có thể lặp lại. Không trộn tài liệu, điều/mục hoặc bản gốc và sửa đổi.

`section_id` là ID của điều/mục cha; `chunk_id` là ID của mảnh sau khi chia. Ví dụ một điều dài có thể tạo `D01_regulation_article_3_01`, `D01_regulation_article_3_02`, cùng `section_id: D01_regulation_article_3`.

Tiêu đề chương được giữ cùng điều đầu tiên của chương và lưu trong metadata. Phần mở đầu văn bản được giữ trong điều đầu tiên trước khi chia tiếp. Script chấp nhận OCR `Điêu` như tiêu đề điều, giữ nguyên nội dung nguồn; chỉ coi “Chương” kèm số La Mã/chữ số là tiêu đề, tránh nhầm “chương trình…”. Ranh giới văn bản kèm trong 4 PDF được khai báo ở `instrument()`; cần kiểm tra lại nếu thay corpus.

## Kết quả cấu hình 800 token

| Tài liệu | Trang | Điều/mục cha | Chunks |
|---|---:|---:|---:|
| D01 — Quy chế đào tạo | 21 | 30 | 58 |
| D02 — Điểm rèn luyện và sửa đổi | 16 | 25 | 54 |
| D03 — Học phí | 5 | 7 | 22 |
| D04 — Ngoại ngữ | 9 | 18 | 28 |
| **Tổng** | **51** | **80** | **162** |

Có 29 điều/mục phải tách thành nhiều chunks; 51 điều/mục còn lại giữ nguyên một chunk.

| Thống kê token trong `text` | Giá trị |
|---|---:|
| Trung bình | 441,3 |
| Trung vị | 380,5 |
| Ngắn nhất | 96 |
| Dài nhất | 788 |
| Từ 1–500 token | 95 chunks |
| Từ 501–800 token | 67 chunks |
| Trên 800 token | **0 chunks** |

Giới hạn 800 là trần, không phải độ dài bắt buộc. Phần ngữ cảnh lặp cũng được tính vào số token nên tổng token của các chunks lớn hơn corpus ban đầu.

Script kiểm tra tất cả ký tự nguồn của 51 trang được giữ đúng một lần trong phần thân, không lẫn văn bản/phiên bản. Kiểm tra độc lập xác nhận các dòng bảng không bị cắt, đủ 27 dòng học phí và 30/30 đoạn bằng chứng nằm nguyên trong chunk tương ứng. Đây là kiểm tra dữ liệu, chưa phải đánh giá retrieval.

## Chạy lại

Từ thư mục gốc `CS420_SeminarRAG`, chạy PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r experiment/requirements.txt
.\.venv\Scripts\python.exe experiment/scripts/chunk_by_structure.py --max-tokens 800
```

Hai lệnh đầu chỉ cần khi chuẩn bị môi trường. Nếu đã có `.venv` và `tiktoken`, chỉ chạy lệnh cuối. Lần đầu tokenizer có thể tải từ vựng công khai; không gửi corpus đi. Cache mặc định trong `experiment/tmp/`, đã được Git bỏ qua; có thể đổi bằng `TIKTOKEN_CACHE_DIR`.

Script chỉ đọc corpus và nguồn, không dùng câu hỏi/đáp án để chọn ranh giới. Output vẫn là `data/chunks/chunks_by_structure.json`, thay thế bản 80 chunks trước đó, không tạo thêm các file dữ liệu trùng nhau.

## Cấu trúc output

```python
import json
from pathlib import Path

payload = json.loads(
    Path("experiment/data/chunks/chunks_by_structure.json").read_text(encoding="utf-8")
)
chunks = payload["chunks"]
texts = [chunk["text"] for chunk in chunks]
```

Output có `config`, `statistics`, `chunks`. Mỗi chunk có:

| Trường | Ý nghĩa |
|---|---|
| `doc_id`, `section_id`, `chunk_id` | Tài liệu, điều/mục cha và chunk duy nhất. |
| `section`, `chapter`, `instrument`, `revision_role` | Tiêu đề và phạm vi văn bản/phiên bản. |
| `chunk_index`, `chunks_in_section` | Thứ tự mảnh và tổng số mảnh trong điều/mục. |
| `text` | Ngữ cảnh cộng văn bản nguồn, dùng để embedding. |
| `word_count` | Số đơn vị cách nhau bởi khoảng trắng trong toàn bộ `text`; không phải phân đoạn từ tiếng Việt. |
| `token_count` | Số token `cl100k_base` trong toàn bộ `text`, tối đa 800. |
| `pdf_pages`, URL nguồn | Nguồn phần thân để trích dẫn. |
| `source_spans` | Vị trí nguồn phần thân theo trang: `char_start` bắt đầu từ 0, `char_end` không bao gồm ký tự cuối. |
| `body_char_start` | Phần thân nguồn là `text[body_char_start:]`; phần trước là ngữ cảnh thêm/lặp. |
| `context_source_spans` | Vị trí nguồn của tiêu đề bảng/chú giải lặp. Tên tài liệu và tiêu đề điều được lấy từ metadata. |
| `context_is_derived` | Ngữ cảnh có thêm nhãn biên tập, không coi toàn bộ ngữ cảnh là trích dẫn nguyên văn. |

Phần thân giữ nguyên văn bản nguồn, chỉ nối các trang bằng hai dấu xuống dòng. Các ID đã thay đổi so với bản 80 chunks; cần tạo lại index khi dùng bản này.

## Việc tiếp theo

- Chọn mô hình embedding và kiểm tra lại đầu vào bằng tokenizer của chính mô hình. Trần 800 `cl100k_base` không đảm bảo vừa giới hạn của mọi mô hình. Nếu thêm nội dung vào `text`, cần đếm lại.
- Gán và kiểm tra `relevant_chunk_ids` trước khi đo Recall@k; các trường này trong bộ câu hỏi vẫn rỗng. Không index câu hỏi/đáp án vào corpus.
- D02 phải đọc bản gốc cùng sửa đổi 2023; lưu ý năm học, khóa tuyển và phạm vi áp dụng của từng tài liệu.
- 22 trang có bản chép/khôi phục bảng từ ảnh; 29 trang OCR còn cần đối chiếu độc lập. Mọi trang vẫn có `human_review_status: pending`. Đủ 51 trang không có nghĩa OCR hoàn toàn chính xác.
