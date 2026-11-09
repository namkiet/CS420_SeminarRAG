# G3 Task 6 — Q&A tham khảo

**Cập nhật: 09/11/2026.** Chuẩn bị cho khoảng 5 phút hỏi đáp; không cần trình bày hết 15 câu. Mỗi đáp án nên nói trong 20–40 giây, mở nguồn chi tiết khi cần. Phân công dưới đây là gợi ý theo [outline hiện tại](../slides/OUTLINE.md); mỗi thành viên cần trả lời ít nhất một câu.

| Người trả lời chính | Câu chuẩn bị | Trọng tâm |
|---|---|---|
| Kiệt | Q02–Q04, Q07 | Nền tảng, phương trình, các retriever |
| Huy | Q05–Q06, Q08–Q11, Q14 | Dữ liệu, chunking, thiết kế và đánh giá thí nghiệm |
| Lĩnh | Q01, Q12–Q13, Q15 | Kết luận, citation, failure cases và cải tiến |

## Q01. Cung cấp tài liệu bên ngoài có loại bỏ hallucination không?

**Chính: Lĩnh · Dự phòng: Huy.** Không. Trong lần chạy bốn nhánh, không RAG đúng nội dung chính 0/20 câu; TF-IDF và embedding cùng 10/20, BM25 9/20. RAG giúp cải thiện trên bộ câu hỏi này nhưng vẫn có đáp án sai hoặc ngoài nguồn; cả 60 đáp án RAG thiếu citation-ID hợp lệ. Kết quả không chứng minh mọi hệ thống RAG đều đạt mức cải thiện đó. **Nguồn:** [bảng điểm][scores], [đáp án thật][outputs].

## Q02. RAG khác fine-tuning và đưa toàn bộ tài liệu vào prompt thế nào?

**Chính: Kiệt · Dự phòng: Lĩnh.** Parametric memory là kiến thức trong trọng số model; bộ tài liệu và chỉ mục bên ngoài là non-parametric memory. Fine-tuning cập nhật trọng số. RAG truy xuất một phần tài liệu phù hợp rồi đưa vào prompt; đưa toàn bộ tài liệu vào prompt thì không có bước chọn evidence bằng retriever. Trong triển khai của nhóm, Qwen giữ nguyên trọng số, không được train hay fine-tune bằng corpus HCMUS. **Nguồn:** [report][report], [pipeline][pipeline], [cấu hình chạy][manifest].

## Q03. RAG-Sequence và RAG-Token khác nhau thế nào? Ví dụ số ra sao?

**Chính: Kiệt · Dự phòng: Huy.** Sequence lấy tổng theo tài liệu ở ngoài tích xác suất các token; Token lấy tổng theo tài liệu ở từng vị trí token:

$$
p_{\mathrm{seq}}(y\mid x)\approx\sum_{z\in\mathrm{top}\text{-}k}p_\eta(z\mid x)\prod_{i=1}^{T}p_\theta(y_i\mid x,z,y_{<i})
$$

$$
p_{\mathrm{tok}}(y\mid x)\approx\prod_{i=1}^{T}\sum_{z\in\mathrm{top}\text{-}k}p_\eta(z\mid x)p_\theta(y_i\mid x,z,y_{<i})
$$

Ở đây, $x$ là câu hỏi, $y$ là đáp án, $z$ là đoạn truy xuất, $\eta/\theta$ là tham số retriever/generator, $k$ là số đoạn và $T$ là số token đáp án. Các xác suất nằm trong [0, 1], không có đơn vị.

Ví dụ giả định hai đoạn có trọng số 0,7/0,3; xác suất token thứ nhất là 0,8/0,4 và token thứ hai có điều kiện là 0,9/0,2:

- Sequence: `0,7 × 0,8 × 0,9 + 0,3 × 0,4 × 0,2 = 0,5280`.
- Token: `(0,7 × 0,8 + 0,3 × 0,4) × (0,7 × 0,9 + 0,3 × 0,2) = 0,4692`.

Đây là ví dụ giả định, không phải xác suất đo từ Qwen hay cosine score của BGE-M3. **Nguồn:** [Lewis, mục 2.1][lewis], [report trang 3][report].

## Q04. Nhóm có triển khai đúng mô hình huấn luyện trong paper Lewis không?

**Chính: Kiệt · Dự phòng: Lĩnh.** Nhóm minh họa retrieval-augmented prompting: nhập tài liệu → chia chunk → lập chỉ mục → lấy top-5 → ghép evidence vào prompt → Qwen sinh đáp án. Nhóm không huấn luyện end-to-end retriever/generator và không thực hiện phép marginalization của RAG-Sequence/Token trong chương trình sinh. Công thức paper và triển khai thực nghiệm được trình bày riêng. **Nguồn:** [pipeline][pipeline], [report][report], [manifest][manifest].

## Q05. Corpus gồm những gì? Vì sao 51 trang trong khi đề gợi ý 5–10?

**Chính: Huy · Dự phòng: Lĩnh.** Bốn tài liệu là đào tạo 21 trang, rèn luyện 16, học phí 5 và ngoại ngữ 9; tổng 51 trang. Nhóm mở rộng phạm vi để hỏi trên nhiều quy định và giữ đầy đủ tài liệu thay vì chỉ lấy vài trang. Đây là khác biệt so với phạm vi khoảng 5–10 trang trong đề, cần nêu rõ và đối chiếu yêu cầu giảng viên. Dữ liệu là các phiên bản đã lưu với nguồn/hash, không mặc nhiên đại diện mọi quy định mới nhất. **Nguồn:** [nguồn corpus][sources], [yêu cầu][tasks], [report][report].

## Q06. Vì sao chia theo cấu trúc, trần 800 token? Có tối ưu chưa?

**Chính: Huy · Dự phòng: Kiệt.** Mỗi điều/mục là một đơn vị cha; phần quá dài được tách theo khoản, đoạn hoặc câu để giữ ý tương đối trọn vẹn. Bảng giữ nhóm hàng và lặp ngữ cảnh cần thiết. Có 80 điều/mục tạo thành 162 chunks; trần 800 token gồm cả ngữ cảnh lặp, chunk dài nhất thực tế 788 token. Đây là lựa chọn thử nghiệm, chưa chứng minh tối ưu; token theo `cl100k_base` cũng không đồng nghĩa số từ hay token của mọi model. **Nguồn:** [chunks và cấu hình][chunks], [hướng dẫn thực nghiệm][experiment].

## Q07. TF-IDF, BM25 và embedding là ba cách riêng với RAG hay sao?

**Chính: Kiệt · Dự phòng: Huy.** Đây là ba lựa chọn cho bước retrieval trong RAG. TF-IDF biểu diễn từ/cụm từ theo tần suất và độ hiếm rồi so cosine; BM25 cũng dựa vào từ khóa nhưng điều chỉnh sự bão hòa tần suất và độ dài đoạn. BGE-M3 tạo vector embedding rồi so cosine để tìm đoạn gần nhau trong không gian vector. Nhóm chạy riêng ba retriever với cùng generator; chưa triển khai hybrid kết hợp chúng. **Nguồn:** [code TF-IDF][tfidf], [code BM25][bm25], [benchmark][retrieval-readme].

## Q08. Vì sao chọn top-5? Đã đáp ứng so sánh hai cấu hình chưa?

**Chính: Huy · Dự phòng: Kiệt.** Retrieval được đánh giá tại k=1, 3 và 5, đáp ứng yêu cầu so sánh ít nhất hai giá trị k. Khi sinh đáp án, cả ba nhánh RAG cùng dùng top-5 để cố định số đoạn giữa các phương pháp. Chưa có thí nghiệm chất lượng đáp án theo nhiều k nên không kết luận k=5 tối ưu; thêm đoạn có thể tăng coverage nhưng cũng thêm nhiễu. **Nguồn:** [bảng retrieval][retrieval], [manifest][manifest], [yêu cầu][tasks].

## Q09. Hit Rate, Evidence Recall, All Evidence Hit và MRR khác nhau gì?

**Chính: Huy · Dự phòng: Kiệt.** Hit Rate hỏi có tìm được ít nhất một nhóm evidence liên quan không; Evidence Recall tính tỷ lệ nhóm evidence đã tìm được; All Evidence Hit yêu cầu đủ tất cả nhóm của câu hỏi. MRR@k dùng nghịch đảo hạng của kết quả liên quan đầu tiên, hoặc 0 nếu không có trong top-k. Các số được lấy trung bình trên 20 câu. Một câu cần hai nhóm mà chỉ tìm được một thì Hit=1, Recall=1/2 và All Evidence=0. Đây là chỉ số retrieval theo gold alignment, không phải độ đúng của câu trả lời. **Nguồn:** [định nghĩa benchmark][retrieval-readme], [CSV retrieval][retrieval].

## Q10. Vậy phương pháp nào tốt nhất?

**Chính: Huy · Dự phòng: Lĩnh.** Tùy tiêu chí. BM25 có Hit@1 cao nhất, 85%; embedding có Evidence Recall@5 cao nhất, 89,17%, và Hit@5=95%. Về đúng nội dung chính ở Task 6, embedding và TF-IDF đồng hạng 50%, BM25 45%. Embedding có ít câu chứa khẳng định sai/ngoài nguồn hơn trong bảng chấm này, nhưng chưa đủ để tuyên bố vượt mọi phương pháp. Với 20 câu, một câu đã tương ứng 5 điểm phần trăm. **Nguồn:** [retrieval][retrieval], [bảng điểm Task 6][scores].

## Q11. So sánh có/không RAG có công bằng không? Vì sao dùng Qwen?

**Chính: Huy · Dự phòng: Kiệt.** Lần chạy Task 6 có 20 câu × 4 nhánh = 80 đáp án, cùng Qwen2.5-1.5B-Instruct/revision, system prompt và cấu hình sinh greedy, seed 42, tối đa 768 token output. Baseline nhận câu hỏi và NGUỒN rỗng; RAG nhận thêm top-5, không có đáp án chuẩn trong prompt và không dùng lịch sử giữa các câu. Qwen là generator cố định cho phép so sánh này, không phải model được chứng minh tốt nhất; dùng Qwen cũng không tự loại bỏ bias chấm điểm. **Nguồn:** [manifest][manifest], [prompt/output][outputs], [hướng dẫn Task 6][task6].

## Q12. Câu trả lời đúng có nghĩa là citation đúng không?

**Chính: Lĩnh · Dự phòng: Huy.** Không. Cần tách đúng nội dung, ID có thật và nguồn có hỗ trợ phát biểu không. Cả 60 đáp án RAG lần mới thiếu citation-ID hợp lệ dù một số đúng nội dung. Q01 embedding phân biệt đúng tiên quyết/học trước nhưng không có citation; nếu nhóm thêm ID khi trình bày, phải ghi “nhóm bổ sung sau đối chiếu”, không gọi đó là citation model tự sinh. **Nguồn:** [output Q01][outputs], [bảng chấm][review], [note kiểm tra][audit].

## Q13. Nêu ba lỗi thực tế và nguyên nhân có bằng chứng?

**Chính: Lĩnh · Dự phòng: Huy.** Dùng các ca của lần Task 6 bốn nhánh:

- **Q07:** Top-5 thiếu ngưỡng 65–79 là Khá; model trả sai khi xếp 68 điểm. Đây là ca thiếu evidence cần thiết khi retrieval.
- **Q05:** Embedding đã nhận Điều 19 nhưng vẫn nói đủ tín chỉ là đủ tốt nghiệp, bỏ các điều kiện khác. Có evidence không bảo đảm generator sử dụng đầy đủ.
- **Q13:** BM25/embedding lấy C1=488.000 cho cả hai ngành rồi kết luận chênh 0; đúng là cột C5, AI 1.014.000 và CNTT 974.000, chênh 40.000. Đây là lỗi đọc/gắn cột bảng.

Các quan sát này không chứng minh nguyên nhân bên trong mạng neural. Không dùng lỗi Q12 hay cắt output 384 token ở lần cũ để mô tả lần mới 768 token. **Nguồn:** [output và context][outputs], [lý do chấm từng câu][review], [report trang 7][report].

## Q14. Nhóm chấm điểm thế nào? Hạn chế đánh giá là gì?

**Chính: Huy · Dự phòng: Lĩnh.** Điểm nội dung là 2: đúng trọng yếu và điều kiện được hỏi; 1: đúng một phần; 0: sai trọng yếu hoặc không trả lời. Độ đầy đủ, khẳng định ngoài nguồn và citation được ghi riêng. Bảng điểm ban đầu do GPT hỗ trợ và có lý do từng câu để đối chiếu; người phụ trách đã xác nhận kiểm tra trong đợt chuẩn bị. Không gọi đó là chấm mù độc lập: chỉ có 20 câu do nhóm soạn, chưa có tập kiểm thử độc lập, và gold alignment có thể bỏ sót evidence diễn đạt khác. **Nguồn:** [rubric và kết quả][task6], [80 dòng chấm][review], [note kiểm tra][audit].

## Q15. Nếu làm tiếp, nhóm cải tiến và cập nhật tài liệu thế nào?

**Chính: Lĩnh · Dự phòng: Kiệt.** Ưu tiên kiểm tra từng kết luận với evidence, kiểm tra điều kiện/khóa/năm áp dụng và từ chối phần chưa đủ nguồn. Với bảng học phí, giữ rõ nhãn cột và đơn vị. Có thể thử hybrid/reranker rồi đánh giá lại cùng benchmark. Khi thay quy chế, lưu phiên bản/ngày hiệu lực/hash, thay chunks bị ảnh hưởng, cập nhật chỉ mục hoặc embedding và chạy lại đánh giá. Đây là hướng đề xuất, chưa có kết quả chứng minh cải thiện hoặc bảo đảm hết hallucination. **Nguồn:** [report trang 7–8][report], [pipeline][pipeline], [nguồn phiên bản][sources].

## Luyện tập và mở nguồn

- Kiệt tập Q03; Huy tập Q09 hoặc Q10; Lĩnh tập Q13. Sau đó đổi câu cho người dự phòng.
- Khi được hỏi số liệu, nói rõ **retrieval benchmark** hay **Task 6 bốn nhánh**, k và mẫu số; không trộn với lần chạy 05/11.
- Giữ sẵn report, CSV retrieval và JSON đáp án trên máy. Nếu chưa có bằng chứng, trả lời rõ giới hạn thay vì đoán.

[tasks]: TASKS.md
[lewis]: RAG.pdf
[report]: ../report/S07_Bao_Cao_RAG_HCMUS.pdf
[audit]: ../report/G3_TASK3_REVIEW.md
[pipeline]: ../research/G1_Task4_RAG_Pipeline.md
[sources]: ../experiment/data/sources.json
[chunks]: ../experiment/data/chunks/chunks_by_structure.json
[experiment]: ../experiment/README.md
[tfidf]: ../experiment/tfidf_retrieval.py
[bm25]: ../experiment/bm25_retrieval.py
[retrieval-readme]: ../experiment/results/rag_methods_2026-11-08/README.md
[retrieval]: ../experiment/results/rag_methods_2026-11-08/retrieval_summary.csv
[task6]: ../experiment/results/task6_4way/README.md
[manifest]: ../experiment/results/task6_4way/run_manifest.json
[outputs]: ../experiment/results/task6_4way/answers_comparison.json
[review]: ../experiment/results/task6_4way/manual_review.csv
[scores]: ../experiment/results/task6_4way/answer_quality_summary.csv
