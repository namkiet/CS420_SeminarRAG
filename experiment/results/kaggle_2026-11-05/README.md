# Kết quả chạy Kaggle — 05/11/2026

**Cập nhật đánh giá 07/11:** đã đọc 20 cặp đáp án, phân loại lỗi nội dung và kiểm tra context. Xem [đánh giá chi tiết](OUTPUT_REVIEW_2026-11-07.md). Nội dung RAG đúng chính 9/20 theo đánh giá sơ bộ, không phải độ chính xác 95%. Q12/Q13 thực tế đã có chú giải bảng trong context; audit bổ sung phân biệt điều này với metric phần thân bên dưới.

Xem thêm [phân tích lỗi theo từng bước và thứ tự cải thiện](ERROR_ANALYSIS_AND_IMPROVEMENT_2026-11-07.md): 6/8 câu lỗi nặng đã đủ bằng chứng trong prompt; có thứ hạng các nguồn bị bỏ và kiểm tra giới hạn của validator hiện tại.

Đã chạy trên Tesla T4: 162 chunks → 162 vector BGE-M3 (1024 chiều), 20 câu hỏi đánh giá và một câu demo. Cùng Qwen2.5-1.5B-Instruct sinh đủ **20 cặp đáp án không RAG/có RAG**, greedy, tối đa 384 output token. Generator dùng FP32 + SDPA; embedding dùng FP16 trên GPU. Dataset version 1 đọc từ `/kaggle/input/datasets/tunlnh/s07-hcmus-rag-corpus`.

- [Dataset Kaggle](https://www.kaggle.com/datasets/tunlnh/s07-hcmus-rag-corpus) — Private, 10 files, gồm JSON và 4 PDF gốc.
- [Notebook Kaggle](https://www.kaggle.com/code/tunlnh/s07-rag-embedding-hcmus) — đã lưu version 2 cùng output hiển thị.
- [Cấu hình, SHA model, SHA dữ liệu và phiên bản thư viện](run_manifest.json).

## Retrieval

| k | Hit@k | Evidence Recall@k | All Evidence Hit@k | Chunk Recall@k | MRR@k |
|---:|---:|---:|---:|---:|---:|
| 1 | 70% | 60,83% | 50% | 59,17% | 0,7000 |
| 3 | 85% | 77,50% | 65% | 75,83% | 0,7667 |
| 5 | 95% | 85,00% | 70% | 83,33% | 0,7867 |

Đây là trung bình trên 20 câu. Nhãn tạm được ánh xạ từ 30 quote nguyên văn theo tài liệu, trang và phần thân chunk; mọi bằng chứng đều có match. Nhãn và OCR vẫn cần người duyệt. **Hit@5 95% không phải độ chính xác câu trả lời 95%.**

Kiểm tra độc lập từ ZIP tải về đã tái tạo toàn bộ thứ hạng top-5 và các chỉ số từ vector NumPy. Đã kiểm tra vector hữu hạn, chuẩn hóa L2, checksum index và fingerprint khớp corpus/model revision. SHA của ba file đầu vào trên Kaggle khớp dữ liệu repo commit `8bba55c`. Không có chunk nào bị bỏ khỏi prompt do ngân sách token trong 20 câu này.

## Giới hạn và ca lỗi quan sát được

| Câu | Quan sát có thể kiểm tra trong output | Ý nghĩa |
|---|---|---|
| Q07 | Hit@5 = 0, Evidence Recall@5 = 0 | Không truy hồi được bằng chứng tham chiếu trong top-5. |
| Q12 | Hit@5 = 1 nhưng Evidence Recall@5 phần thân = 0,5 | Chú giải C5 đã có trong context lặp; generator đọc sai cột. Xem audit toàn context ngày 07/11. |
| Q19 | Generator dẫn `[chunk_id]`, không phải ID từ context | Có context không đảm bảo model tuân thủ trích dẫn. |
| Q03 | Đạt giới hạn 384 output token | Đáp án có thể chưa hoàn tất; trường `reached_token_limit` ghi nhận điều này. |

15/20 đáp án RAG không có ID trích dẫn theo mẫu ngoặc vuông; 5 đáp án có ID ngoài context (Q03, Q05, Q11, Q13, Q19). Trường `sources` luôn giữ danh sách nguồn đã cung cấp cho model; danh sách đó không chứng minh mọi kết luận của model đúng. Chưa chấm độ đúng, đầy đủ hay mức độ được bằng chứng hỗ trợ: các điểm trong `manual_review.csv` cố ý để trống.

Lần thử FP16 + eager trước đó sinh chuỗi dấu `!`; kết quả lỗi đó không dùng cho bảng này. Đã đổi FP32 + SDPA và chạy lại cả 20 cặp. Notebook có chặn logits NaN/Inf và đầu ra không chứa chữ.

## File để nhóm phân tích

- `retrieval_per_question.csv`, `retrieval_summary.csv`: chỉ số chi tiết/tổng hợp.
- `gold_alignment.json`: nhãn tạm để nhóm đối chiếu PDF.
- `answers_comparison.json`: đáp án, reference, prompt, context IDs, nguồn, citation audit, token và thời gian.
- `manual_review.csv`: 40 hàng để chấm baseline/RAG.
- `custom_answer.json`: câu demo và nguồn thực tế đã cung cấp.
- `index_manifest.json`, `run_manifest.json`: dấu vết cấu hình và dữ liệu.

Vector và danh sách đoạn truy hồi đầy đủ nằm trong `s07_rag_results.zip` ở Output của Kaggle. Không đưa weights hoặc vector cache vào Git.
