"""One structural section per RAG chunk. Uses only Python's standard library.

Run from repository root: python experiment/scripts/chunk_by_structure.py
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
# Accept the existing OCR spelling "Điêu" without changing source text.
ARTICLE = re.compile(r'^\s*(?:#{1,6}\s*)?(Đi[ềê]u\s*(\d+)[.:].*)$', re.I)
SECTION = re.compile(r'^\s*(?:#{1,6}\s*)?(Mục\s+(\d+)(?![\d.]).*)$', re.I)
CHAPTER = re.compile(r'^\s*(?:#{1,6}\s*)?(Chương\s+\S+.*)$', re.I)
APPENDIX = re.compile(r'^\s*#{1,6}\s+((\d+)\.\s+.*)$')
TUITION = re.compile(r'^\s*(([23])\.\s+.*)$')


def instrument(page):
    """Instrument boundaries in the four source PDFs, not page chunk sizes."""
    doc, n = page['doc_id'], page['pdf_page']
    if doc == 'D02' and n >= 14:
        return 'amendment_2023'
    if n == 1:
        return 'decision'
    if doc == 'D03' or (doc == 'D02' and n >= 9):
        return 'appendix'
    return 'regulation'


def split_sections(text, mode='regulation', tuition=False):
    """Keep clauses, bullets and tables inside their parent article/section.

    Introductory text joins the first section. Chapter headings join the next
    section and are also recorded as metadata. Page breaks are not boundaries.
    """
    starts = []
    chapter, pending_chapter = None, None
    for line in re.finditer(r'[^\n]*(?:\n|$)', text):
        value = line.group().rstrip('\r\n')
        match = CHAPTER.match(value)
        if match:
            chapter, pending_chapter = match[1].strip(), line.start()
            continue
        kind = 'article'
        if mode == 'appendix':
            match = (TUITION if tuition else APPENDIX).match(value)
            kind = 'section'
        else:
            match = ARTICLE.match(value)
            if match is None:
                match, kind = SECTION.match(value), 'section'
        if match:
            start = pending_chapter if pending_chapter is not None else line.start()
            starts.append((start, match[1].strip(), kind, match[2], chapter))
            pending_chapter = None
    if tuition:
        # Source appendix starts with the complete C1-C7 legend and table.
        # Its next top-level items are explicitly numbered 2 and 3.
        starts.insert(0, (0, 'Mục 1. Đơn giá tín chỉ học phí và bảng học phí',
                          'section', '1', None))
    if not starts:
        return [(0, len(text), 'Phần mở đầu', 'front_matter', None, chapter)]
    starts[0] = (0, *starts[0][1:])
    return [(start, starts[i+1][0] if i+1 < len(starts) else len(text),
             title, kind, number, parent)
            for i, (start, title, kind, number, parent) in enumerate(starts)]


def build(pages, sources):
    groups = {}
    for page in pages:
        key = (page['doc_id'], page.get('revision_role', 'source_document'), instrument(page))
        groups.setdefault(key, []).append(page)
    source_lookup = {s['doc_id']: s for s in sources}
    counts, chunks = Counter(), []
    for (doc_id, role, part), rows in groups.items():
        pieces, positions, cursor = [], [], 0
        for page in sorted(rows, key=lambda p: p['pdf_page']):
            if pieces:
                pieces.append('\n\n')
                cursor += 2
            body = page['text']
            positions.append((cursor, cursor+len(body), page))
            pieces.append(body)
            cursor += len(body)
        text = ''.join(pieces)
        for begin, end, title, kind, number, chapter in split_sections(
                text, part, tuition=doc_id == 'D03' and part == 'appendix'):
            spans, included = [], []
            for a, b, page in positions:
                if max(a, begin) < min(b, end):
                    spans.append(dict(pdf_page=page['pdf_page'],
                                      char_start=max(a, begin)-a, char_end=min(b, end)-a))
                    included.append(page)
            counts[doc_id] += 1
            source = source_lookup[doc_id]
            chunks.append(dict(
                chunk_id=f'structure_{doc_id}_{counts[doc_id]:03d}', doc_id=doc_id,
                instrument=part, revision_role=role, chapter=chapter, section=title,
                section_type=kind, section_number=number,
                pdf_pages=[p['pdf_page'] for p in included],
                text=text[begin:end], char_count=end-begin, source_spans=spans,
                document_title=source['title'], application_note=source.get('application_note'),
                source_url=source['source_url'], source_pdf_url=source['source_pdf_url'],
                review_status=sorted({p['review_status'] for p in included}),
                human_review_status='pending'))
    validate(pages, chunks)
    return chunks


def validate(pages, chunks):
    lookup = {(p['doc_id'], p['pdf_page']): p for p in pages}
    covered = {key: bytearray(len(p['text'])) for key, p in lookup.items()}
    ids = set()
    for chunk in chunks:
        assert chunk['chunk_id'] not in ids, 'Duplicate chunk ID'
        ids.add(chunk['chunk_id'])
        restored = []
        for span in chunk['source_spans']:
            key = chunk['doc_id'], span['pdf_page']
            page = lookup[key]
            assert instrument(page) == chunk['instrument']
            assert page.get('revision_role', 'source_document') == chunk['revision_role']
            a, b = span['char_start'], span['char_end']
            assert 0 <= a < b <= len(page['text'])
            assert not any(covered[key][a:b]), 'Overlapping source ranges'
            covered[key][a:b] = b'\1' * (b-a)
            restored.append(page['text'][a:b])
        assert ''.join(''.join(restored).split()) == ''.join(chunk['text'].split())
    assert all(all(flags) for flags in covered.values()), 'Source characters lost'


def main():
    corpus = ROOT / 'data/processed/corpus_pages.json'
    sources = ROOT / 'data/sources.json'
    pages = json.loads(corpus.read_text(encoding='utf-8'))
    chunks = build(pages, json.loads(sources.read_text(encoding='utf-8')))
    payload = dict(
        config=dict(strategy='one_structural_section_per_chunk', version='structure_v1',
                    unit='article_in_regulations; top_level_section_in_appendices',
                    max_tokens=None, overlap=0, preserve_lists_and_tables=True,
                    front_matter='attached_to_first_section_of_each_instrument',
                    corpus_sha256=hashlib.sha256(corpus.read_bytes()).hexdigest(),
                    sources_sha256=hashlib.sha256(sources.read_bytes()).hexdigest()),
        statistics=dict(source_pages=len(pages), chunks=len(chunks),
                        by_document=dict(Counter(c['doc_id'] for c in chunks)),
                        by_instrument=dict(Counter(f"{c['doc_id']}/{c['instrument']}" for c in chunks)),
                        cross_page_chunks=sum(len(c['pdf_pages']) > 1 for c in chunks),
                        max_char_count=max(c['char_count'] for c in chunks),
                        all_source_characters_covered=True), chunks=chunks)
    output = ROOT / 'data/chunks/chunks_by_structure.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(payload['statistics'], ensure_ascii=False, indent=2))
    print(f'Output: {output}')


if __name__ == '__main__':
    main()
