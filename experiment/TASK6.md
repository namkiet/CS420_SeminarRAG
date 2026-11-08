# G2 Task 6 — So sánh câu trả lời có và không retrieval

## Hiện trạng repo

BM25 đã có từ commit `246851c`: code, top-k và đánh giá Task 3–4. Hiện cả ba retriever **TF-IDF, BM25 và BGE-M3 embedding** đều có kết quả trên cùng 162 chunks và 20 câu hỏi.

Lần chạy embedding ngày 05/11 có 20 cặp đáp án Qwen không/có RAG và bản phân tích sơ bộ. Khi chuẩn bị notebook này, TF-IDF/BM25 mới có kết quả retrieval. Lần chạy cũ có system prompt khác giữa hai điều kiện và từng bị cắt output ở 384 token. Giữ nguyên kết quả cũ làm lần thí nghiệm trước, không dùng lẫn với kết quả mới.

Repo cũng đã có [benchmark ba retriever ngày 08/11](results/rag_methods_2026-11-08/README.md), sinh 60 đáp án với giới hạn 384 token. Đây là bộ chạy riêng với bộ bốn nhánh 80 đáp án/768 token dưới đây; không gộp số liệu hoặc dùng kết luận của bộ này thay cho bộ kia.

**Cập nhật 08/11/2026:** đã nhận ZIP Kaggle có đủ 80 đáp án thật, xác minh dữ liệu/cấu hình/prompt và chấm AI sơ bộ. Xem [kết quả Task 6](results/task6_4way/README.md): TF-IDF và embedding cùng đúng chính 10/20, BM25 9/20, baseline 0/20; 0/60 citation-ID hợp lệ. Điểm cần nhóm kiểm tra độc lập, không phải accuracy đã được con người duyệt. Các bước bên dưới vẫn dùng để tái chạy hoặc điều chỉnh điểm.

## So sánh như thế nào là đủ?

| Nhánh | Đầu vào Qwen |
|---|---|
| `baseline` — không RAG | Câu hỏi, không có tài liệu |
| `tfidf` — RAG TF-IDF | Cùng câu hỏi + top-5 TF-IDF |
| `bm25` — RAG BM25 | Cùng câu hỏi + top-5 BM25 |
| `embedding` — RAG BGE-M3 | Cùng câu hỏi + top-5 embedding |

**20 câu × 4 nhánh = 80 câu trả lời.** Một baseline được dùng đối chiếu ba retriever. Không cần thêm hybrid hoặc lặp generation ở cả k=1/3/5 để hoàn thành Task 6; ảnh hưởng của k đã thuộc Task 4. So sánh bốn nhánh này đủ để phân biệt lợi ích của cung cấp tài liệu và ảnh hưởng của cách chọn tài liệu trong phạm vi bộ thử nhỏ.

Khóa điều kiện trước khi chạy:

- Cùng 162 chunks, cùng 20 câu hỏi và thứ tự chunk đã xác minh SHA-256.
- Cùng `Qwen/Qwen2.5-1.5B-Instruct`, revision `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`.
- Cùng system prompt cho cả bốn nhánh; cùng định dạng user message, chỉ thay phần evidence. Prompt yêu cầu dùng nguồn khi có nguồn; không có nguồn thì dựa kiến thức sẵn có và không bịa.
- Cùng greedy decoding (`do_sample=False`), seed 42, FP32 + SDPA, input budget 8.192 và output budget **768 token**.
- Mỗi câu/nhánh có messages mới; không truyền đáp án hoặc lịch sử câu trước. Reference answer chỉ dùng lúc chấm, không đưa vào prompt LLM.
- Các nhánh RAG đều lấy top-5. Nếu vượt ngân sách input, chỉ bỏ nguyên chunk cuối và ghi `omitted_context_ids`, không cắt ngầm văn bản.
- Không chỉnh prompt/tham số riêng cho từng câu để đạt đáp án chuẩn. Có thể đổi cấu hình cho thí nghiệm mới, nhưng phải chạy lại đồng bộ và dùng output directory mới.

## Vì sao không cần chạy embedding lại?

Notebook khóa thứ hạng của Task 3–4 hiện có. TF-IDF/BM25 lấy top-5 từ `evaluation_details.json`; embedding lấy danh sách `context_ids` theo thứ tự trong output cũ, đã xác nhận đủ 5 và không bỏ chunk. Hash corpus, câu hỏi và nguồn khớp, nên có thể tái sử dụng thứ hạng này. **Không tái sử dụng đáp án Qwen cũ.** Điều này tiết kiệm bộ nhớ/thời gian và giữ biến can thiệp chính là evidence được đưa cho cùng generator.

Nếu thay corpus hoặc chạy retriever với tham số khác, phải tạo lại retrieval results và notebook. Builder sẽ từ chối hash/ranking không khớp; không tự tìm gold chunks để thay vào thứ hạng.

## Các bước bạn cần làm

### 1. Mở notebook

File: [S07_Task6_RAG_Comparison.ipynb](notebooks/S07_Task6_RAG_Comparison.ipynb).

Vào Kaggle → tạo Notebook → File → Import Notebook → chọn file trên. Add Input → gắn **S07 HCMUS RAG Corpus** đang dùng của nhóm. Bật **Internet** và **GPU T4/P100**. Notebook không cần API key hoặc BGE-M3 weights; chỉ tải Qwen. Không nâng cấp torch của Kaggle.

Notebook kiểm tra hash đầu vào trước khi chạy. Nếu báo nhiều Dataset cùng cấu trúc, đặt `DATA_ROOT` trong cell cấu hình đến đúng thư mục Dataset của nhóm.

### 2. Chạy thử rồi chạy đủ

- Muốn smoke test: `EVAL_LIMIT=2`, đổi `OUTPUT` thành `/kaggle/working/s07_task6_smoke`; dự kiến 8 đáp án.
- Chạy chính thức: `EVAL_LIMIT=None`, `OUTPUT=/kaggle/working/s07_task6_4way`; dự kiến **80 đáp án**.
- Run All; đợi dòng `Completed: 80 / 80`. Dùng Save Version → Save & Run All để lưu output.
- Mỗi đáp án được checkpoint. Nếu chạy lại cùng cấu hình và output còn tồn tại, các đáp án đã xong được bỏ qua. Không dùng chung thư mục giữa smoke/full hoặc hai cấu hình khác nhau.

FP32 weights cần hơn 4 GB VRAM, nên GPU laptop 4 GB hiện tại không phù hợp cấu hình đã khóa. Hướng chạy được chuẩn bị là Kaggle GPU. Máy cục bộ cũng chưa có torch/transformers trong `.venv`; không coi kiểm thử CPU/mock là đã chạy LLM thật.

### 3. Tải output

Cell cuối hiển thị file `s07_task6_4way_results.zip`. Tải ZIP về, giải nén vào `experiment/results/task6_4way/`:

| File | Dùng để làm gì? |
|---|---|
| `answers_comparison.json` | 20 câu × 4 nhánh: đáp án, prompt thực tế, context, token, thời gian và cờ cắt output. |
| `retrieval_plan.json` | Thứ hạng top-5 đã khóa và provenance/hash. |
| `run_manifest.json` | Model revision, cấu hình, môi trường và số đáp án đã hoàn tất. |
| `generation_summary.csv` | Token/thời gian/cắt output/citation-ID; **không phải accuracy**. |
| `manual_review.csv` | 80 hàng để chấm nội dung và mức độ được nguồn hỗ trợ. |

### 4. Chấm 80 đáp án

Mở `manual_review.csv` bằng Excel/editor hỗ trợ UTF-8, đối chiếu `reference_answer`, `expected_key_points`, evidence và PDF gốc. Ghi lý do/nguồn cho mỗi đánh giá, ưu tiên một người khác kiểm tra chéo; không chỉ nhờ cùng generator tự chấm.

| Cột | Quy ước |
|---|---|
| `answered` | `yes`: có đáp án thực chất; `no`: từ chối/placeholder/không trả lời. |
| `correctness` | `2`: đúng nội dung trọng yếu và điều kiện; `1`: đúng một phần, thiếu ý hoặc có lỗi; `0`: sai trọng yếu/không trả lời. |
| `completeness` | `2`: đủ các ý cần thiết; `1`: thiếu một phần; `0`: thiếu phần lớn/không trả lời. |
| `unsupported_claim` | `1`: có khẳng định đáng kể sai hoặc không được tài liệu hỗ trợ; `0`: không thấy khẳng định như vậy. Dùng nguồn gốc làm chuẩn cho cả baseline và RAG. |
| `citation_support` | RAG: `2` các khẳng định cần nguồn được dẫn và hỗ trợ đầy đủ; `1` một phần; `0` thiếu/sai citation; `na` nếu không có kết luận cần dẫn, như từ chối hoàn toàn. Baseline luôn `na`, không phạt vì không có nguồn để trích. |
| `reviewer` | Người chấm, bắt buộc điền. |
| `notes` | Lý do + điều/khoản/chunk/ý chuẩn dùng để chấm, bắt buộc điền. |

Tất cả 20 câu hiện có đều có đáp án tham chiếu: từ chối không tính là đúng, dù từ chối có thể tốt hơn bịa thông tin. Có thể gặp một đáp án đúng nhưng không grounded; correctness và unsupported/citation được chấm riêng. ID citation hợp lệ không đồng nghĩa trích dẫn hỗ trợ nội dung.

### 5. Tổng hợp và viết kết luận

Từ thư mục gốc repo, chạy (chỉ dùng Python chuẩn, không cần torch):

```powershell
python experiment/task6_comparison.py summarize --run-dir experiment/results/task6_4way
```

Lệnh từ chối chấm khi còn ô điểm trống hoặc điểm không hợp lệ, không tự bịa accuracy. Khi đủ điểm, tạo:

- `answer_quality_summary.csv`: tỷ lệ đúng đầy đủ, đúng một phần, completeness trung bình, tỷ lệ khẳng định ngoài/sai nguồn, tỷ lệ từ chối và citation support.
- `TASK6_REPORT.md`: bảng so sánh để viết báo cáo; cần bổ sung phần nhận xét của bạn.

Nhận xét nên trả lời: RAG có cải thiện so với baseline không? Ba cách retrieval khác nhau ở những câu nào? Có câu lấy đủ nguồn nhưng LLM vẫn sai không? Tăng độ phủ retrieval có chuyển thành câu trả lời đúng không? Chọn 2–3 cặp ví dụ minh họa từ output thật. Không kết luận phương pháp tốt nhất nói chung từ 20 câu, và không dùng Hit@5/Recall@5 làm độ chính xác câu trả lời.

## Tái tạo notebook và kiểm tra

```powershell
python experiment/scripts/build_task6_notebook.py
python -B -m unittest discover -s experiment/tests -p test_task6_comparison.py -v
```

Builder/helper dùng thư viện chuẩn, không cần tải mô hình. Unit test dùng generator giả để kiểm tra đủ 80 điều kiện, prompt chung, checkpoint, kiểm tra hash, ngân sách, citation audit và tính điểm; không đo chất lượng Qwen.

Tham khảo cách gọi model: [Qwen2.5 trên Transformers](https://qwen.readthedocs.io/en/v2.5/inference/chat.html) và [cấu hình generation của Transformers](https://huggingface.co/docs/transformers/v4.57.0/llm_tutorial).
