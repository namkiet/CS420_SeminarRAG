# Benchmark RAG ngày 08/11/2026

Đã chạy **TF-IDF, BM25 và BGE-M3** trên 162 chunk, 20 câu hỏi và 30 nhóm bằng chứng. Kaggle bản 1 sinh đủ **60 đáp án** trên Tesla T4. [Notebook Kaggle](https://www.kaggle.com/code/tunlnh/s07-rag-retrieval-methods-benchmark)

Cả ba dùng cùng revision Qwen2.5-1.5B-Instruct, FP32 + SDPA, cùng system prompt, greedy decoding, tối đa 5 chunk và 384 token sinh. Điểm retrieval được tính ở k = 1, 3 và 5. Nhãn bằng chứng gồm phần thân và chú giải lặp đã đối chiếu vị trí nguồn trong trang PDF. Chỉ mục của ba retriever được xây từ nội dung corpus. [Cấu hình và SHA của lần chạy](manifest.json)

## Retrieval

| Phương pháp | Evidence Recall@1 | Evidence Recall@3 | Evidence Recall@5 | Hit@5 | Đủ bằng chứng@5 | MRR@5 |
|---|---:|---:|---:|---:|---:|---:|
| TF-IDF | 70,83% | 82,50% | 82,50% | 90% | 15/20 | 0,8250 |
| BM25 | **80,00%** | **84,17%** | 84,17% | 90% | **16/20** | **0,8667** |
| BGE-M3 | 65,00% | 81,67% | **89,17%** | **95%** | **16/20** | 0,7867 |

Evidence Recall là trung bình theo câu của tỷ lệ nhóm bằng chứng tìm thấy. Hit cần ít nhất một nhóm, còn “Đủ bằng chứng” yêu cầu mọi nhóm. MRR đo thứ hạng của bằng chứng đầu tiên trong top-k. [Bảng chỉ số đầy đủ](retrieval_summary.csv)

BM25 dẫn ở k=1 và k=3. BGE-M3 dẫn về coverage ở k=5, với 19/20 câu có ít nhất một bằng chứng. BM25 và BGE-M3 đều lấy đủ bằng chứng cho 16/20 câu, nhưng thiếu ở những câu khác nhau. [Từng câu và danh sách chunk](retrieval_per_question.csv) · [Thứ hạng và score](retrieval_hits.json)

## Đáp án sinh ra

| Phương pháp | Đúng ý chính | Một phần | Sai | Chỉ sinh placeholder | Có ID hợp lệ dạng `[chunk_id]` |
|---|---:|---:|---:|---:|---:|
| TF-IDF | **11/20** | 2 | 7 | 0 | 0/20 |
| BM25 | 10/20 | 2 | 7 | 1 | 0/20 |
| BGE-M3 | 9/20 | 3 | 7 | 1 | 0/20 |

Codex đọc 60 đáp án và chấm sơ bộ dựa trên nội dung tham chiếu. “Đúng ý chính” xét kết luận và các ý trọng yếu, “Một phần” dành cho câu có ý đúng nhưng thiếu vế hoặc điều kiện, “Sai” dành cho kết luận trọng yếu sai. Nội dung và định dạng citation được chấm riêng. Nhãn nguồn và điểm nội dung cần nhóm chấm chéo trước khi báo cáo chính thức.

Có đáp án nhắc ID dưới dạng `[chunk_id: D01_regulation_article_19_01]`. Cột citation chỉ tính dạng `[D01_regulation_article_19_01]` với ID nằm trong context. Model dùng toàn bộ các chunk đã chọn trong cả 60 lượt. BGE-M3 ở Q03 chạm giới hạn 384 token sinh. [Đáp án nguyên gốc, prompt, ID nguồn, token và thời gian](answers.json)

| Câu | TF-IDF | BM25 | BGE-M3 |
|---|---|---|---|
| Q01 | Sai | Sai | Đúng ý chính |
| Q02 | Đúng ý chính | Đúng ý chính | Đúng ý chính |
| Q03 | Một phần | Một phần | Sai |
| Q04 | Sai | Sai | Sai |
| Q05 | Một phần | Sai | Placeholder |
| Q06 | Đúng ý chính | Đúng ý chính | Đúng ý chính |
| Q07 | Sai | Sai | Sai |
| Q08 | Sai | Đúng ý chính | Một phần |
| Q09 | Đúng ý chính | Đúng ý chính | Đúng ý chính |
| Q10 | Đúng ý chính | Đúng ý chính | Đúng ý chính |
| Q11 | Đúng ý chính | Một phần | Một phần |
| Q12 | Sai | Đúng ý chính | Sai |
| Q13 | Sai | Sai | Sai |
| Q14 | Đúng ý chính | Đúng ý chính | Một phần |
| Q15 | Đúng ý chính | Đúng ý chính | Đúng ý chính |
| Q16 | Sai | Sai | Sai |
| Q17 | Đúng ý chính | Placeholder | Đúng ý chính |
| Q18 | Đúng ý chính | Đúng ý chính | Đúng ý chính |
| Q19 | Đúng ý chính | Sai | Sai |
| Q20 | Đúng ý chính | Đúng ý chính | Đúng ý chính |

## Các câu cho thấy khác biệt giữa phương pháp

- **Q01.** Cả ba xếp đoạn định nghĩa đúng hạng 1. TF-IDF và BM25 đưa đoạn về Anh văn vào hạng 2, và hai đáp án chuyển sang quy định Anh văn. BGE-M3 trả đúng khác biệt giữa học phần tiên quyết và học phần học trước. Điểm cosine hạng 1 của BGE-M3 trong lần chạy này là 0,6271.
- **Q03.** BM25 lấy đúng 12–25 tín chỉ nhưng trả nhầm ngoại lệ vượt mức tối đa cho vế hỏi ngoại lệ tối thiểu. TF-IDF lấy được mức tối thiểu 12 nhưng thiếu mức tối đa và cũng nhầm ngoại lệ. BGE-M3 trả sai mức thông thường và chạm giới hạn sinh.
- **Q07.** Cả ba đều bỏ sót ngưỡng 65–79 điểm ở top-5 và trả lời theo điều khoản 50 điểm. Trong phép xếp hạng lại trên toàn bộ corpus cục bộ, đoạn đúng ở hạng 12 với TF-IDF, 7 với BM25 và 11 với BGE-M3.
- **Q12.** Cả ba nhận đủ bảng và chú giải. BM25 trả đúng 1.014.000 đồng. TF-IDF trả 488.000 đồng và BGE-M3 trả 734.000 đồng.
- **Q13.** Cả ba nhận đủ bảng và chú giải. Chênh lệch đúng là 40.000 đồng. TF-IDF trả 0, BM25 trả 126.000 và BGE-M3 trả 230.000 đồng.
- **Q14.** TF-IDF và BM25 thiếu đoạn trích tham chiếu theo tiêu chí khớp quote. Prompt vẫn chứa metadata phạm vi 2022–2026, đủ để trả đúng rằng khóa 2020 nằm ngoài phạm vi bảng. BGE-M3 trả đúng cho khóa 2020 nhưng mở rộng phạm vi thành “2022 trở lên”.
- **Q15 và Q16.** BM25 lấy đủ ba nhóm bằng chứng của Q15. Cả ba trả đúng ý chính Q15, nhưng đều bỏ sót đoạn IELTS 5.0 của Q16 và trả sai mức của chương trình tài năng.
- **Q19.** TF-IDF trả đủ thời hạn hai năm và hai mốc thời gian. BM25 lạc sang thủ tục nộp chứng chỉ. BGE-M3 trả khoản cho trường hợp chứng chỉ có ghi hiệu lực.

Chênh lệch giữa 11, 10 và 9 câu đúng chỉ mô tả bộ 20 câu và generator này. Kết quả cho thấy một retriever có coverage tốt hơn vẫn có thể đưa vào các đoạn làm model chọn sai điều kiện. Cần đối chiếu thêm nội dung đầu ra và chất lượng nguồn khi so sánh pipeline.

## Tái tạo

Đóng gói notebook cùng metadata cho dataset Kaggle hiện tại. [Script benchmark](../../scripts/benchmark_rag.py)

```powershell
python experiment/scripts/benchmark_rag.py --package-kaggle --output experiment/outputs/kaggle-benchmark
kaggle kernels push -p experiment/outputs/kaggle-benchmark --accelerator NvidiaTeslaT4 --timeout 3600
```

Lần chạy tham chiếu dùng namespace Kaggle `tunlnh`. Chỉnh `id` trong metadata nếu chạy bằng tài khoản khác có quyền vào dataset. [Hướng dẫn Kaggle CLI](https://github.com/Kaggle/kaggle-cli/blob/main/docs/kernels.md)

Có thể kiểm tra retrieval trên CPU bằng ZIP vector của lần chạy BGE-M3 trước, với đúng corpus và thứ tự câu hỏi.

```powershell
python experiment/scripts/benchmark_rag.py --data-dir experiment/data --retrieval-only --dense-cache experiment/outputs/s07_rag_results.zip --output experiment/outputs/benchmark-local
```

Đã đối chiếu SHA của dữ liệu và code đã chạy, số lượng 60 đáp án, 180 dòng retrieval và context của từng lượt. Retrieval cục bộ khớp bảng tổng hợp Kaggle. 20 đáp án BGE-M3 tái tạo đúng chuỗi đáp án của lần chạy 05/11. 26 bài kiểm thử có sẵn đều qua.
