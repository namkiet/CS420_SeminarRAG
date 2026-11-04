# Dữ liệu thực nghiệm RAG

Thư mục này chỉ giữ bộ dữ liệu dùng trực tiếp và PDF gốc để đối chiếu. Không cần chạy script tạo dữ liệu.

## Cấu trúc

```text
experiment/
├── README.md
└── data/
    ├── processed/
    │   └── corpus_pages.json
    ├── questions.json
    ├── sources.json
    └── raw/
        ├── D01_quy_che_dao_tao_2026.pdf
        ├── D02_quy_che_diem_ren_luyen_2020_sua_2023.pdf
        ├── D03_hoc_phi_2026_2027_K2022_ve_sau.pdf
        └── D04_chuan_ngoai_ngu_tot_nghiep_2026.pdf
```

## File nào dùng để làm gì?

| File | Mục đích |
|---|---|
| [corpus_pages.json](data/processed/corpus_pages.json) | Dữ liệu chính: 51 trang của 4 tài liệu. Chia chunks và tạo chỉ mục retrieval từ trường `text`; giữ metadata nguồn/trang/phiên bản. |
| [questions.json](data/questions.json) | 20 câu hỏi đánh giá, đáp án chuẩn và 30 đoạn bằng chứng. Giữ riêng để chấm kết quả, không đưa vào corpus tìm kiếm. |
| [sources.json](data/sources.json) | Link tài liệu gốc, số quyết định, ngày, phạm vi áp dụng và SHA-256. |
| `data/raw/*.pdf` | 4 PDF nguyên bản để kiểm tra lại số liệu, điều khoản và bảng. |

Với seminar RAG, bước tiếp theo là tạo chỉ mục tìm kiếm từ corpus; bộ dữ liệu này không phải dữ liệu fine-tuning mô hình đã gán nhãn sẵn.

## Đọc dữ liệu

Chạy Python từ thư mục gốc repo:

```python
import json
from pathlib import Path

data = Path("experiment/data")
pages = json.loads((data / "processed/corpus_pages.json").read_text(encoding="utf-8"))
questions = json.loads((data / "questions.json").read_text(encoding="utf-8"))
```

Mỗi trang có `doc_id`, `pdf_page`, `printed_page`, `section`, `text`, URL và trạng thái kiểm chứng. Corpus đủ D01: 21, D02: 16, D03: 5, D04: 9 trang. Có thể sửa văn bản trực tiếp trong JSON này, không cần đồng bộ nhiều bản Markdown/TXT khác.

## Khi sử dụng

- Chỉ index `corpus_pages.json`; không index đáp án chuẩn hoặc PDF thêm lần nữa cùng corpus.
- Chưa có chunks và nhãn `relevant_chunk_ids`; cần gán theo từng cấu hình trước khi đo Recall@k.
- Bảng học phí phải giữ ý nghĩa cột C1–C7. D02 giữ cả quy chế gốc và sửa đổi 2023; dùng `revision_role` và phạm vi nguồn để tránh trả lời bằng khoản đã bị thay thế.
- Đủ 51/51 trang không có nghĩa mọi ký tự OCR đã chính xác: 22 trang đã có bản chép/khôi phục bảng theo ảnh, 29 trang OCR còn cần kiểm tra độc lập. Mọi trang vẫn có `human_review_status: pending`.
- 20 câu hỏi chưa bao phủ mọi điều khoản của 51 trang. Năm học, khóa tuyển và chương trình áp dụng phải được giữ khi trả lời.
