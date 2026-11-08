"""Build the standalone, four-condition Kaggle notebook from frozen rankings."""
import json
from pathlib import Path
import sys
import textwrap

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from task6_comparison import prepare_plan


def build(root=ROOT):
    plan = prepare_plan(root)
    cells = []

    def add(kind, source):
        cell = dict(cell_type=kind,id=f'task6_{len(cells):03d}',metadata={},source=textwrap.dedent(source).strip()+'\n')
        if kind=='code':
            cell.update(execution_count=None,outputs=[])
        cells.append(cell)

    add('markdown','''
        # G2 Task 6 — Qwen: không RAG / TF-IDF / BM25 / embedding
        **20 câu × 4 điều kiện = 80 câu trả lời**, một model/revision, cùng system prompt,
        greedy decoding, ngân sách output và lịch sử hội thoại mới cho mỗi lần gọi.

        Dùng thứ hạng top-5 đã lưu của Task 3–4. Không huấn luyện lại retriever, không tải
        BGE-M3, không dùng lại đáp án Qwen cũ, không dùng reference answer trong prompt.
        Notebook này là thí nghiệm mới, không ghi đè lần chạy embedding trước.

        **Cách chạy:** Import notebook vào Kaggle, gắn Dataset **S07 HCMUS RAG Corpus**
        của nhóm (snapshot 162 chunks), bật Internet và GPU T4/P100, rồi Run All.
        Không cần API key. Mặc định chạy đủ 20 câu; không coi smoke test 2 câu là kết quả toàn bộ.
    ''')
    add('code','%pip install -q transformers==4.57.1 accelerate==1.11.0 huggingface-hub==0.36.0')
    helper = (root/'task6_comparison.py').read_text(encoding='utf-8').split("\nif __name__=='__main__':")[0]
    add('code',helper)
    add('code','import json\nFROZEN_PLAN = json.loads('+repr(json.dumps(plan,ensure_ascii=False))+')')
    add('markdown','''
        ## 1. Khóa cấu hình và kiểm tra dữ liệu
        Chỉ khác nội dung evidence. Cùng một baseline được dùng đối chiếu cả ba cách retrieval.
        Mô hình Qwen và SHA giữ theo lần chạy của nhóm; output budget tăng đồng đều lên 768
        để giảm nguy cơ cắt câu ở 384 token. FP32 + SDPA theo cấu hình Kaggle đã chạy được.
        Mọi thay đổi cấu hình/câu hỏi yêu cầu thư mục output mới, tránh resume lẫn thí nghiệm.
    ''')
    add('code','''
        import importlib.metadata, platform, torch

        DATA_ROOT = None  # auto-detect; set explicitly if several datasets share this schema
        OUTPUT = Path('/kaggle/working/s07_task6_4way')
        EVAL_LIMIT = None  # None = 20 questions / 80 answers; 2 = smoke test / 8 answers
        CONFIG = dict(DEFAULT_CONFIG, evaluation_limit=EVAL_LIMIT)
        if DATA_ROOT is None:
            candidates = sorted({p.parent.parent for p in Path('/kaggle/input').rglob('chunks_by_structure.json')
                                 if p.parent.name=='chunks' and (p.parent.parent/'questions.json').is_file()})
            if len(candidates)!=1:
                raise ValueError(f'Attach the group corpus dataset or set DATA_ROOT; found {len(candidates)} datasets')
            DATA_ROOT = candidates[0]
        chunks, all_questions = load_inputs(DATA_ROOT,FROZEN_PLAN)
        if EVAL_LIMIT is not None and (not isinstance(EVAL_LIMIT,int) or not 1<=EVAL_LIMIT<=len(all_questions)):
            raise ValueError('EVAL_LIMIT must be None or a positive number <=20')
        questions = all_questions if EVAL_LIMIT is None else all_questions[:EVAL_LIMIT]
        OUTPUT.mkdir(parents=True,exist_ok=True)
        manifest = dict(config=CONFIG, data_sha256=FROZEN_PLAN['data_sha256'],
                        retrieval_plan_sha256=digest(FROZEN_PLAN), modes=list(MODES),
                        question_ids=[q['question_id'] for q in questions],
                        expected_answers=len(questions)*len(MODES),
                        generation_status='not_completed', human_review_status='pending',
                        python=platform.python_version(),
                        gpu=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
                        packages={name:importlib.metadata.version(name) for name in
                                  ['torch','transformers','accelerate','huggingface-hub']})
        print({'chunks':len(chunks),'questions':len(questions),'conditions':list(MODES),
               'expected_answers':manifest['expected_answers'],'cuda':torch.cuda.is_available()})
        print('Retrieval frozen from:',FROZEN_PLAN['provenance'])
        expected_fingerprint = digest(dict(plan=FROZEN_PLAN,config=CONFIG,
                                           question_ids=[q['question_id'] for q in questions]))
        if (OUTPUT/'answers_comparison.json').exists():
            if read_json(OUTPUT/'answers_comparison.json').get('run_fingerprint')!=expected_fingerprint:
                raise ValueError('Output belongs to another configuration; choose a new OUTPUT directory')
        save_json(OUTPUT/'run_manifest.json',manifest)
    ''')
    add('markdown','''
        ## 2. Sinh câu trả lời
        Checkpoint sau từng câu/điều kiện. Run All lại để tiếp tục nếu cùng cấu hình và còn output.
        Mỗi lần gọi tạo mới messages và không truyền lịch sử/past KV cache của câu trước.
        Không cắt ngầm chunk: nếu quá ngân sách input, bỏ nguyên chunk cuối và ghi lại ID bị bỏ.
        Lỗi NaN/Inf hoặc output không có chữ sẽ dừng; không tạo số liệu thay cho output lỗi.
    ''')
    add('code','''
        from IPython.display import display, Markdown, FileLink
        existing_path = OUTPUT/'answers_comparison.json'
        existing_run = read_json(existing_path) if existing_path.exists() else None
        already_complete = (existing_run is not None and len(existing_run['questions'])==len(questions)
                            and all(set(q['answers'])==set(MODES) for q in existing_run['questions']))
        if already_complete:
            run = existing_run
            validate_run(run)
            print('All answers already saved under the same fingerprint; no model calls needed.')
        else:
            tokenizer, generate = load_generator(CONFIG)
            run = execute(chunks,questions,FROZEN_PLAN,OUTPUT,CONFIG,tokenizer,generate)
            del generate
        manifest.update(generation_status='completed',
                        completed_answers=sum(len(q['answers']) for q in run['questions']))
        save_json(OUTPUT/'run_manifest.json',manifest)
        export_review(run,OUTPUT)
        import gc
        gc.collect()
        torch.cuda.empty_cache()
        print('Completed:',manifest['completed_answers'],'/',manifest['expected_answers'])
        print('Human correctness scores remain empty until review.')
    ''')
    add('markdown','''
        ## 3. Xem một câu và tải output
        `generation_summary.csv` chỉ có token/thời gian/cờ cắt/citation-ID, chưa phải accuracy.
        Chấm `manual_review.csv` theo rubric trong `experiment/TASK6.md`, đối chiếu nguồn gốc.
        Reference answer trong output chỉ phục vụ chấm, không nằm trong prompt đã gửi LLM.
        Citation-ID đúng không chứng minh kết luận đúng hoặc được nguồn hỗ trợ.
    ''')
    add('code','''
        example = run['questions'][0]
        display(Markdown('### '+example['question_id']+' — '+example['question']))
        for mode in MODES:
            display(Markdown('**'+mode+'**\\n\\n'+example['answers'][mode]['answer']))
        archive = package_results(OUTPUT)
        print('Download:',archive)
        display(FileLink(str(archive)))
    ''')
    notebook = dict(cells=cells,metadata=dict(kernelspec=dict(display_name='Python 3',language='python',name='python3'),
                                            language_info=dict(name='python'),
                                            kaggle=dict(isInternetEnabled=True,isGpuEnabled=True,accelerator='nvidiaTeslaT4')),
                    nbformat=4,nbformat_minor=5)
    target = root/'notebooks/S07_Task6_RAG_Comparison.ipynb'
    target.write_text(json.dumps(notebook,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(target)
    print(f"Plan verified: {len(plan['question_ids'])} questions, {plan['chunk_count']} chunks, 3 retrievers x top-5")
    return target


if __name__=='__main__':
    build()
