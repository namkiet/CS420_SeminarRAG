"""Rebuild the FULL 51-page dataset from its stored text and reference inputs.

No network or OCR model is needed for the normal rebuild. OCR drafts
are produced separately by extract_full_pdf_ocr.py and require visual review.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import unicodedata
import pymupdf

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
OUT=DATA/'processed'
VERSION='full_document_v3'
EXPECTED={'D01':21,'D02':16,'D03':5,'D04':9}
PATTERN=r'^## \[PDF (\d+) \| Trang in (.*?) \| (.*?)\]\n'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    sources=read(DATA/'source_catalog.json')
    questions=read(DATA/'questions.reference.json')
    review={(p['doc_id'],p['pdf_page']):p for p in read(DATA/'page_review.json')}
    assert {s['doc_id'] for s in sources}==set(EXPECTED),'Source IDs differ from expected corpus'
    pages=[]
    for s in sources:
        doc=s['doc_id']
        raw_path=ROOT/s['raw_path']
        with pymupdf.open(raw_path) as pdf:
            count=len(pdf)
        assert count==EXPECTED[doc],f'{doc}: expected {EXPECTED[doc]} PDF pages, found {count}'
        sha=hashlib.sha256(raw_path.read_bytes()).hexdigest()
        assert sha==s['sha256'],f'{doc}: source PDF changed; review metadata and transcription'
        relative=f'data/processed/{doc}_corpus.md'
        parts=re.split(PATTERN,(ROOT/relative).read_text(encoding='utf-8'),flags=re.M)
        document_pages=[]
        for i in range(1,len(parts),4):
            n,printed,section,body=parts[i:i+4]
            number=int(n)
            info=review[doc,number]
            body=unicodedata.normalize('NFC',body.strip())
            assert body,f'{doc} page {number}: empty transcription'
            p=dict(doc_id=doc,pdf_page=number,printed_page=int(printed) if printed.isdigit() else None,
                section=section,text=body,source_url=s['source_url'],source_pdf_url=s['source_pdf_url'],
                corpus_version=VERSION,extraction_method=info['extraction_method'],
                review_status=info['review_status'],revision_role=info['revision_role'],
                human_review_status='pending')
            document_pages.append(p)
        numbers=[p['pdf_page'] for p in document_pages]
        assert numbers==list(range(1,count+1)),f'{doc}: missing, duplicate, or unordered pages: {numbers}'
        extracted=read(DATA/f'extracted/{doc}_ocr_pages.json')
        assert [p['pdf_page'] for p in extracted]==numbers,f'{doc}: incomplete raw OCR record'
        assert all(p['text'].strip() and p['source_sha256']==sha for p in extracted)
        # Coverage is measured separately from transcription accuracy.
        s.update(source_total_pages=count,included_pdf_pages=numbers,
            scope=f'Toàn bộ nội dung {count} trang PDF, gồm điều khoản, phụ lục, bảng và văn bản sửa đổi có trong file gốc.',
            included_printed_pages=[p['printed_page'] for p in document_pages],
            processed_path=relative,processed_paths=[relative],
            page_data_path=f'data/processed/{doc}_pages.json',
            raw_ocr_path=f'data/extracted/{doc}_ocr_pages.json',
            corpus_version=VERSION,processed_coverage='all_pdf_pages',
            full_pdf_page_coverage=True,text_accuracy_fully_reviewed=False,
            source_verified=True,human_review_status='pending',updated_date='2026-11-01',
            extraction_method='Full-page OCR with visually checked page/table transcriptions and reference corrections; per-page quality is recorded.')
        for key in ['selected_pdf_pages','selected_printed_pages','verified']:
            s.pop(key,None)
        dump(OUT/f'{doc}_pages.json',document_pages)
        (OUT/f'{doc}_corpus.txt').write_text('\n\n'.join(f'[{doc} PDF {p["pdf_page"]}]\n{p["text"]}' for p in document_pages)+'\n',encoding='utf-8')
        pages.extend(document_pages)

    assert len(pages)==51 and len(review)==51
    lookup={(p['doc_id'],p['pdf_page']):p for p in pages}
    assert len(questions)==20 and len({q['question_id'] for q in questions})==20
    by_source={s['doc_id']:s for s in sources}
    for q in questions:
        q['corpus_version']=VERSION
        q['relevant_chunk_ids']=[]
        q['human_review_status']='pending'
        q['verification_method']='Reference evidence previously checked against PDF images; literal match checked in full corpus. Independent team review pending.'
        for e in q['evidence']:
            assert e['quote'] in lookup[e['doc_id'],e['pdf_page']]['text'],f"{q['question_id']}: evidence missing from full corpus"

    dump(DATA/'sources.json',sources)
    dump(DATA/'questions.json',questions)
    dump(OUT/'corpus_pages.json',pages)
    statuses=Counter(p['review_status'] for p in pages)
    manifest=dict(corpus_version=VERSION,updated_date='2026-11-01',source_document_count=4,
        raw_pdf_pages=51,included_source_page_count=51,processed_coverage='all_pdf_pages',
        full_pdf_page_coverage=True,text_accuracy_fully_reviewed=False,
        page_review_counts=dict(statuses),retrieval_input='data/processed/corpus_pages.json',
        question_count=len(questions),evidence_spans=sum(len(q['evidence']) for q in questions),
        human_review_status='pending',
        benchmark_note='The existing 20 reference questions remain valid; they are not exhaustive coverage of all 51 pages.')
    dump(DATA/'corpus_manifest.json',manifest)
    dump(DATA/'coverage_report.json',dict(corpus_version=VERSION,documents=[dict(
        doc_id=s['doc_id'],expected_pages=EXPECTED[s['doc_id']],included_pages=s['included_pdf_pages'],
        missing_pages=[],duplicate_pages=[],raw_pdf_sha256=s['sha256'],
        review_counts=dict(Counter(p['review_status'] for p in pages if p['doc_id']==s['doc_id']))) for s in sources],
        total_expected_pages=51,total_included_pages=51,all_evidence_quotes_found=True,
        accuracy_note='Full page coverage does not certify every OCR character or table cell. See page review statuses.'))

    combined=['# Corpus HCMUS — đủ 51/51 trang','',
        'Toàn bộ trang của bốn PDF gốc; không chọn bỏ điều hoặc phụ lục. Bản OCR gốc được giữ trong data/extracted/. Văn bản có các mức chất lượng khác nhau; xem page_review.json và coverage_report.json. Giữ cả bản gốc và sửa đổi, không phải văn bản hợp nhất chính thức.','']
    for s in sources:
        combined += [f'# {s["doc_id"]} — {s["title"]}','',s['application_note'],'']
        for p in pages:
            if p['doc_id']==s['doc_id']:
                combined += [f'## [{p["doc_id"]} PDF {p["pdf_page"]}] {p["section"]}','',p['text'],'']
    (OUT/'corpus_all.md').write_text('\n'.join(combined)+'\n',encoding='utf-8')
    (OUT/'corpus_all.txt').write_text('\n\n'.join(f'[{p["doc_id"]} PDF {p["pdf_page"]}]\n{p["text"]}' for p in pages)+'\n',encoding='utf-8')

    lines=['# Bộ 20 câu hỏi tham chiếu — corpus đầy đủ 51 trang','',
        f'Phiên bản corpus: `{VERSION}`. Đây là 20 câu hỏi đã có, được kiểm tra lại bằng chứng với corpus toàn bộ; không phải bộ câu hỏi bao phủ hết mọi điều khoản của 51 trang.','',
        'Câu hỏi D02 cố định ở bản PDF 2020 kèm sửa đổi 2023. Giữ phân biệt phiên bản, khóa, chương trình và năm học.','']
    for q in questions:
        lines += [f'## {q["question_id"]}. {q["question"]}','',f'**Loại:** {q["question_type"]}','',
            '**Đáp án chuẩn:** '+q['reference_answer'],'','**Ý cần có:** '+'; '.join(q['expected_key_points'])+'.','', '**Bằng chứng:**','']
        for e in q['evidence']:
            raw=Path(by_source[e['doc_id']]['raw_path']).name
            lines += [f'- [{e["doc_id"]}, PDF {e["pdf_page"]}, {e["section"]}](raw/{raw}#page={e["pdf_page"]}):','',
                '> '+e['quote'].replace('\n\n','\n> \n> '),'']
        if q['notes']:lines += ['**Lưu ý:** '+q['notes'],'']
    (DATA/'questions.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
