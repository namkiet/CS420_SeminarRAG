# G3 Task 3 - Note kiểm tra report và slides

**Rà lần đầu:** 11:59 ngày 08/11/2026. **Cập nhật:** 09/11/2026.

**Kết luận:** Report khớp các công thức và bảng số liệu chính. Outline còn lỗi cần sửa trước khi làm deck. Note này ghi kết quả kiểm tra; report, outline và log gốc được giữ nguyên.

Phạm vi: [report PDF](S07_Bao_Cao_RAG_HCMUS.pdf), [outline](../slides/OUTLINE.md), [đề S07](../docs/S07_Seminar_RAG.pdf), papers và các log bên dưới. Các nhận xét áp dụng cho bản report/outline đã rà ngày 08/11; kiểm lại nếu file thay đổi. `P1`: sửa trước khi trình bày; `P2`: làm rõ/bổ sung nguồn.

## 1. Report: kết quả và việc cần bổ sung

Đã kiểm tra: 8 trang nội dung A4 + 1 trang references; 14 mục tham khảo có link nhúng; hình/bảng không bị cắt trong bản render. Công thức khớp Lewis; ví dụ số **Sequence = 0,5280**, **Token = 0,4692**. Corpus, retrieval, bảng điểm Task 6 và các ca lỗi mới khớp log. Report đã phân biệt citation do nhóm bổ sung với output thật của model.

| ID | Trạng thái | Vị trí | Note |
|---|---|---|---|
| R03 | P2 | Trang 4, Hình 1 | Nên ghi “Nhóm tự vẽ, phỏng theo pipeline RAG và triển khai của nhóm” để rõ nguồn hình. |
| R04 | P2 | Trang 5 | Viết rõ baseline nhận **cùng system prompt + câu hỏi + NGUỒN rỗng**; các nhánh RAG nhận thêm top-5. |
| R05 | P2 | Trang 9, [8]-[10] | Ngoài link PDF snapshot GitHub, nên có link công bố HCMUS/ngày truy cập; giữ phạm vi phiên bản, nhất là D02. |
| R06 | P2 | Trang 9, [3], [4] | Publisher bị timeout/403 trong công cụ rà, chưa đọc được toàn văn. Đây không phải bằng chứng DOI sai. Có thể thêm tài liệu scikit-learn/Lucene cho cấu hình triển khai. |
| R07 | P2 | Trang 9, [14] | Ghi rõ AI hỗ trợ soạn/rà/chấm và bước nhóm xác minh; không tự điền model ID nếu không lưu được. |

## 2. Outline slides: các lỗi cần sửa

| ID | Mức | Vị trí | Sửa thành / lưu ý |
|---|---|---|---|
| S01 | P1 | Slide 5 | Bốn tài liệu là **đào tạo, rèn luyện, học phí, ngoại ngữ**; không phải CT tiên tiến/CT tài năng. |
| S02 | P1 | Slide 6 | Thay bảng metric sai/trộn body-only với context lặp bằng bảng thống nhất ở mục 4. Ghi rõ k của MRR. |
| S03 | P1 | Slide 7 và timeline | Cosine Q01 đúng là **0,6271 / 0,5813 / 0,5704**, không phải 0,8412 / 0,7245 / 0,7103. Hạng 3 là mảnh khác của Điều 3. |
| S04 | P1 | Slide 8 và timeline | Không nói model tạo citation chuẩn/đúng 100%. Dùng output thật; citation thêm sau phải ghi **nhóm bổ sung**. Quote baseline “cả hai phải thi đạt trên trung bình” không có trong log đang dẫn. |
| S05 | P1 | Slide 9 | Q12=734.000, Q19 placeholder, Q03 cắt 384 thuộc lần cũ. Dùng ca mới ở Bảng 6 report hoặc ghi rõ run cũ. |
| S06 | P1 | Slide 9 | “6/8” chỉ thuộc 8 câu **sai trọng yếu/không có đáp án** của lần cũ, không gồm mọi câu một phần. Truncation không giải thích lỗi đã xuất hiện đầu đáp án; lần mới không chạm trần. |
| S07 | P1 | Slide 10 | Bỏ “RAG loại bỏ ảo giác bịa đặt”. Viết: **RAG cải thiện một số câu nhưng vẫn có khẳng định sai/ngoài nguồn và citation thiếu/sai**. Chưa chứng minh quan hệ nhân quả hay “loại ảo giác mới”. |
| S08 | P2 | Slide 4 | Thống nhất ví dụ report: trọng số **0,70/0,30**, Sequence **0,5280**, Token **0,4692**. Cosine/BM25 score không tự động là xác suất. |
| S09 | P2 | Slide 5, 7 | “Đủ evidence Q01” nghĩa là đủ 2 quote tham chiếu trong chunk; không suy thành accuracy chung 100%. Ghi đúng nguồn và phạm vi kiểm tra. |
| S10 | P2 | Slide 2, 10-12 | Thêm nguồn cho RAGTruth/lost-in-the-middle nếu giữ; dùng phát biểu có điều kiện về fine-tuning/context dài, không suy kết luận tổng quát từ 20 câu. |
| S11 | P2 | Slide 11 | Verification loop, hybrid, reranker k=15 và cập nhật index là **đề xuất**, chưa chứng minh đã triển khai/cải thiện. Không hứa bảo đảm đúng 100%. |
| S12 | P2 | Toàn bộ | Hiện chỉ có outline. Khi có PPTX/PDF, kiểm lại font, hình, bảng, citation và thời lượng thực tế; timeline chưa thay cho chạy thử. |

## 3. Nguồn Task 5 dẫn sang slides cũng cần sửa

Đối chiếu [research/G2_TASK_5.md](../research/G2_TASK_5.md):

| ID | Vị trí | Nội dung sửa |
|---|---|---|
| T01 | Bảng 4.1/note | Thay cosine bằng log thật ở mục 4, hoặc bỏ score và giữ đúng rank/ID. |
| T02 | Mục 5, 8 | Model thực tế là **Qwen2.5-1.5B-Instruct**, không phải 7B. Nếu nói lần 7B riêng phải có log riêng. |
| T03 | Mục 6.2/bảng attribution | Tách đáp án nguyên gốc và bản nhóm thêm citation; không gọi bản biên tập là model output. |
| T04 | Bảng 4.1/prompt | `D01_regulation_article_18_02` ở **trang PDF 16**, nói về chứng chỉ GDĐH/công nhận-chuyển đổi tín chỉ. Điều 10 mới là đánh giá học phần. |
| T05 | Cuối mục 8 | Một Q01 đúng chưa “chứng minh Cross-Attention lọc nhiễu tốt”; chỉ kết luận đúng cho ví dụ/lần chạy đó. |

## 4. Số liệu đúng để dùng chung

**Corpus:** D01 đào tạo 21 trang; D02 rèn luyện 16; D03 học phí 5; D04 ngoại ngữ 9. Tổng **51 trang, 80 điều/mục, 162 chunks, 20 câu/30 nhóm evidence**. Trần 800 token gồm ngữ cảnh lặp; chunk dài nhất lưu trong bộ là 788 token.

### Retrieval cho slide 6

Gold gồm phần thân + chú giải lặp có nguồn; macro trên 20 câu. Đã tính lại từ ranking, khớp [CSV benchmark](../experiment/results/rag_methods_2026-11-08/retrieval_summary.csv).

| Retriever | k | Hit Rate@k | Evidence Recall@k | All Evidence Hit@k | MRR@k |
|---|---:|---:|---:|---:|---:|
| TF-IDF | 1 | 75,00% | 70,83% | 65,00% | 0,7500 |
| TF-IDF | 3 | 90,00% | 82,50% | 75,00% | 0,8250 |
| TF-IDF | 5 | 90,00% | 82,50% | 75,00% | 0,8250 |
| BM25 | 1 | 85,00% | 80,00% | 75,00% | 0,8500 |
| BM25 | 3 | 90,00% | 84,17% | 80,00% | 0,8667 |
| BM25 | 5 | 90,00% | 84,17% | 80,00% | 0,8667 |
| BGE-M3 | 1 | 70,00% | 65,00% | 60,00% | 0,7000 |
| BGE-M3 | 3 | 85,00% | 81,67% | 75,00% | 0,7667 |
| BGE-M3 | 5 | 95,00% | 89,17% | 80,00% | 0,7867 |

BM25 dẫn Evidence Recall ở k=1/3; BGE-M3 dẫn coverage ở k=5. **Hit@5=95% không phải answer accuracy 95%.**

### Q01 cho slide 7-8

Nguồn: [ranking Q01.bge_m3](../experiment/results/rag_methods_2026-11-08/retrieval_hits.json).

| Hạng | Chunk ID | Cosine | Trang PDF |
|---|---|---:|---:|
| 1 | `D01_regulation_article_3_03` | 0,6271 | 4 |
| 2 | `D01_regulation_article_27_01` | 0,5813 | 21 |
| 3 | `D01_regulation_article_3_02` | 0,5704 | 3 |
| 4 | `D01_regulation_article_6_02` | 0,5643 | 7 |
| 5 | `D01_regulation_article_18_02` | 0,5540 | 16 |

Đáp án embedding thật phân biệt đúng **tiên quyết: học và thi đạt** với **học trước: hoàn thành quá trình học tập**, nhưng không có citation. Nếu thêm ID trên slide, ghi là nhóm bổ sung khi đối chiếu. Nguồn: [80 đáp án/prompt](../experiment/results/task6_4way/answers_comparison.json), `Q01.answers`.

Giữ cách nói “định nghĩa học trước không ghi điều kiện thi đạt như tiên quyết”; không mở rộng thành môn đó không bao giờ phải thi đạt để tích lũy/tốt nghiệp.

### Task 6 cho phần thảo luận

| Nhánh | Đúng chính | Một phần | Sai/không trả lời | Có khẳng định sai/ngoài nguồn |
|---|---:|---:|---:|---:|
| Không RAG | 0/20 | 3/20 | 17/20 | 15/20 |
| RAG TF-IDF | 10/20 | 5/20 | 5/20 | 8/20 |
| RAG BM25 | 9/20 | 6/20 | 5/20 | 7/20 |
| RAG embedding | 10/20 | 6/20 | 4/20 | 6/20 |

Nguồn: [bảng chấm Task 6](../experiment/results/task6_4way/manual_review.csv). Điểm có nguồn gốc từ lượt chấm GPT; **cả 60 đáp án RAG thiếu citation-ID hợp lệ**. Embedding và TF-IDF đồng hạng về tỷ lệ đúng.

## 5. Không trộn các lần chạy

| Bộ kết quả | Phạm vi/trần output | Dùng cho |
|---|---|---|
| [05/11](../experiment/results/kaggle_2026-11-05/README.md) | 40 đáp án: baseline + embedding; 384 token | Phân tích cũ: Q03 bị cắt, Q05 placeholder, Q12 sai giá. System prompt baseline/RAG khác nhau. |
| [Benchmark 08/11](../experiment/results/rag_methods_2026-11-08/README.md) | 60 đáp án: 3 retriever; 384 token | Bảng retrieval report [11]; nếu dùng đáp án phải ghi đúng run. |
| [Task 6 bốn nhánh](../experiment/results/task6_4way/README.md) | 80 đáp án; 768 token | Bảng điểm/failure cases mới report [12]; không có chunk bị bỏ hoặc output chạm trần. |

Không ghép accuracy 11/20-10/20-9/20 của benchmark 60 đáp án vào bảng Task 6 80 đáp án. Q12 sai ở lần cũ nhưng đúng ở embedding lần mới; không sửa log để ép chúng giống nhau.

## 6. Nguồn đối chiếu và việc chốt

- **Lewis:** [paper local](../docs/RAG.pdf), mục 2.1/trang PDF 3 cho công thức, Table 1/trang PDF 6 cho các số NQ/WQ trong report. Đã đối chiếu đúng.
- **GenXAI:** [paper local](../docs/GenXAI.pdf), mục 3.3/trang PDF 12-13 và [DOI Springer](https://doi.org/10.1007/s10462-024-10916-x). Verification loop là cách nhóm vận dụng, không phải kết quả đã được paper xác nhận cho HCMUS.
- **Triển khai:** [scikit-learn](https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), [Lucene BM25](https://svn.apache.org/repos/infra/sites/lucene/core/9_12_0/core/org/apache/lucene/search/similarities/BM25Similarity.html), [M3-Embedding](https://arxiv.org/abs/2402.03216), [Qwen2.5](https://arxiv.org/abs/2412.15115). Nhóm chọn k1=1.5/b=0.75, không gọi đó là mọi mặc định Lucene.
- **Bổ sung nếu giữ trên slides:** [RAGTruth](https://aclanthology.org/2024.acl-long.585/), [Lost in the Middle](https://aclanthology.org/2024.tacl-1.9/). Không coi các paper này là bằng chứng nhóm đã thử mọi cơ chế được nêu.
- **Corpus:** [sources.json](../experiment/data/sources.json) và [corpus](../experiment/data/processed/corpus_pages.json). Đã đối chiếu hash/số trang 4 PDF. Giữ đúng snapshot và lưu ý khác biệt số 1028/1208 của D02 như note nguồn, không tự sửa nguyên văn.

- [x] Rà report, công thức/ví dụ số, bảng, caption, references và log.
- [ ] Sửa P1 ở outline và nguồn Task 5, sau đó các mục P2.
- [ ] Rà deck PPTX/PDF khi có bản hoàn chỉnh.

**Huy ưu tiên slide 5-8:** gửi các sửa corpus/metric/cosine/citation cho Kiệt; trao đổi các note report và phạm vi failure cases với Lĩnh. Đây là note Task 3, chưa thay thế nghiệm thu toàn bộ sản phẩm của Task 7.
