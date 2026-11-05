# RAG embedding trên Kaggle

Mở **S07_RAG_Embedding_Kaggle.ipynb** bằng Kaggle → Code → New Notebook → File → Import Notebook. Add Input → Your Datasets → **S07 HCMUS RAG Corpus**. Chọn GPU T4/P100 trong Settings, bật Internet và Run All. Notebook đọc Dataset trong `/kaggle/input`, không cần API key. Cài các thư viện trước khi import; nếu chạy trong session đã import Transformers phiên bản khác, restart session trước.

Notebook đã được tạo trong tài khoản Kaggle: [S07 RAG Embedding HCMUS](https://www.kaggle.com/code/tunlnh/s07-rag-embedding-hcmus/edit). Quyền xem phụ thuộc cài đặt của chủ notebook.

Dataset: [S07 HCMUS RAG Corpus](https://www.kaggle.com/datasets/tunlnh/s07-hcmus-rag-corpus), version 1, chế độ Private, snapshot commit `8bba55c`. Gồm 162 chunks, 20 câu hỏi/30 bằng chứng, corpus 51 trang, nguồn, 4 PDF gốc, README và SHA256SUMS (10 files). Notebook kiểm tra checksum của ba file đầu vào; chỉ embedding chunks, không embedding đáp án. Khi có nhiều Dataset cùng cấu trúc, đặt `DATA_ROOT` để chọn rõ thư mục thay vì tự đoán.

Pipeline dùng `BAAI/bge-m3` để tạo dense embeddings chuẩn hóa L2. Tìm kiếm cosine chính xác bằng NumPy phù hợp corpus 162 chunks. `Qwen/Qwen2.5-1.5B-Instruct` nhận câu hỏi và các đoạn top-k để sinh đáp án tiếng Việt, trích dẫn bằng `[chunk_id]`. Không fine-tune, không đưa đáp án/câu hỏi đánh giá vào index.

Generator mặc định FP32 + SDPA. Khi kiểm tra trên môi trường Kaggle T4 hiện tại, FP16 + eager đã sinh chuỗi dấu `!`; FP32 khắc phục được trong kiểm tra thực tế. Notebook dừng nếu logits chứa NaN/Inf hoặc đáp án không có chữ, tránh lưu lỗi số học như một đáp án hợp lệ. Embedding vẫn dùng FP16 trên GPU, vector lưu FP32. FP32 generator cần khoảng 6,2 GB riêng cho trọng số, cộng bộ nhớ chạy; không giữ encoder GPU khi nạp LLM.

## Chạy và hỏi thêm

- Mặc định `EVAL_LIMIT=None`, `RUN_GENERATION=True`: đo retrieval trên 20 câu, sinh 20 cặp đáp án không RAG/có RAG, rồi trả lời `CUSTOM_QUESTION`.
- Chạy thử nhanh: `EVAL_LIMIT=2`. Kết quả này chỉ đại diện hai câu, không phải benchmark 20 câu.
- Sau Run All: `result = ask("Câu hỏi của bạn", k=5)` rồi `print(result["answer"])`. Trường `sources` chứa tên tài liệu, trang và URL. Query mới nạp lại encoder trên CPU để không tranh GPU với LLM.
- Đổi `GENERATION_TOP_K` để thử số chunk khác. Không diễn giải cosine score thành xác suất câu trả lời đúng.
- Model nhỏ là baseline tiết kiệm bộ nhớ; chất lượng trả lời phải kiểm tra bằng chứng, không được suy ra chỉ từ retrieval score.

## Output `/kaggle/working/s07_rag/`

| File | Nội dung |
|---|---|
| `embeddings.npy`, `index_manifest.json` | Vector và model revision, fingerprint, ID theo thứ tự; cache không dùng lại khi corpus/model thay đổi. |
| `query_embeddings.npy`, `retrieval_hits.json` | Query vector và đoạn truy hồi kèm score, metadata. |
| `gold_alignment.json` | Ánh xạ 30 bằng chứng sang chunk bằng nguyên văn + tài liệu + trang. |
| `retrieval_per_question.csv`, `retrieval_summary.csv` | Hit, Evidence Recall, All Evidence Hit, Chunk Recall, MRR ở k=1/3/5. |
| `answers_comparison.json` | Đáp án baseline/RAG, prompt thực tế, nguồn đã đưa vào, đoạn bị bỏ do hết ngân sách, thời gian/token. Lưu sau mỗi câu. |
| `custom_answer.json` | Đáp án câu hỏi demo tùy chỉnh. |
| `manual_review.csv` | Mẫu chấm thủ công 1–5; điểm để trống. |
| `run_manifest.json` | SHA dữ liệu, model revision, cấu hình, môi trường, số câu đã hoàn thành. |

Nhấn **Save Version → Save & Run All** để giữ output trên Kaggle. Embedding/chunk không được cắt ngầm theo tokenizer. Khi prompt hết ngân sách, notebook chỉ giữ các chunk nguyên vẹn theo thứ tự rank và ghi `omitted_context_ids`.

Cell cuối tạo `s07_rag_results.zip` (không chứa model weights). Tải bằng sidebar Output → làm mới thư mục → More actions của file ZIP → Download.

## Cách đọc đánh giá

Hit@k chỉ cần một bằng chứng; Evidence Recall@k đo tỷ lệ bằng chứng cần thiết; All Evidence Hit@k yêu cầu đủ tất cả. Chunk Recall@k dùng tập chunk được ánh xạ; nhiều chunk chứa cùng bằng chứng có thể làm chỉ số này khác Evidence Recall. MRR@k là nghịch đảo hạng relevant đầu tiên trong k kết quả. Tổng hợp là trung bình trên câu hỏi.

`relevant_chunk_ids` trong file gốc đang rỗng nên không dùng trực tiếp. Notebook tạo nhãn tạm bằng đối chiếu quote trong phần thân nguồn (`body_char_start:`), loại phần ngữ cảnh biên tập. Không có match thì dừng, không bỏ câu khỏi mẫu số. Nhóm cần duyệt lại nhãn. OCR và bộ đáp án đều còn chờ kiểm tra độc lập. Citation audit chỉ xác nhận ID thuộc context, không xác nhận nội dung trả lời được nguồn hỗ trợ. Điểm sinh câu trả lời cần chấm thủ công sau khi đối chiếu PDF.

Generator nhỏ có thể bỏ qua yêu cầu citation dù đã nhận đúng đoạn nguồn. Output vẫn giữ `sources`, `context_ids` và cờ `has_citation`; bảng nguồn của câu demo hiển thị riêng. Không tự gán citation cho câu trả lời rồi coi đó là bằng chứng model đã trích dẫn đúng.

## Phát triển và tái tạo notebook

Helper: `experiment/rag_embedding.py`; builder: `experiment/scripts/build_kaggle_notebook.py`. Dùng môi trường có NumPy/Pandas:

```bash
python experiment/scripts/build_kaggle_notebook.py
python -m unittest discover -s experiment/tests -v
```

Khi thay corpus, chạy `python experiment/scripts/package_kaggle_dataset.py`, upload ZIP trong `experiment/outputs/` thành version mới của Dataset và chọn đúng version trong notebook Input. Cập nhật data commit trong builder cho đúng snapshot mới rồi tạo lại notebook. Helper được chép vào notebook tự động. File requirements RAG riêng với requirements chunking; giữ Torch/CUDA có sẵn của Kaggle. Tái hiện một run bằng cách dùng lại Dataset version, các SHA model trong `run_manifest.json` và cùng cấu hình/phần cứng; kết quả float có thể khác nhẹ theo môi trường.

Tham khảo chính thức: [BGE-M3](https://huggingface.co/BAAI/bge-m3), [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct), [Sentence Transformers](https://sbert.net/docs/package_reference/sentence_transformer/SentenceTransformer.html), [Transformers generation](https://huggingface.co/docs/transformers/main_classes/text_generation).
