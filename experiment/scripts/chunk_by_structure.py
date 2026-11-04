"""Split by document structure with an 800-token ceiling (cl100k_base).

Run from repository root: python experiment/scripts/chunk_by_structure.py
"""
from collections import Counter
import argparse
from functools import lru_cache
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import statistics

import tiktoken

ROOT = Path(__file__).resolve().parents[1]
# Accept the existing OCR spelling "Điêu" without changing source text.
ARTICLE = re.compile(r'^\s*(?:#{1,6}\s*)?(Đi[ềê]u\s*(\d+)[.:].*)$', re.I)
SECTION = re.compile(r'^\s*(?:#{1,6}\s*)?(Mục\s+(\d+)(?![\d.]).*)$', re.I)
# Require a Roman/Arabic chapter number. "chương trình ..." is prose.
CHAPTER = re.compile(r'^\s*(?:#{1,6}\s*)?(Chương\s+(?:[IVXLCDM]+|\d+)\b.*)$', re.I)
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


def build_sections(pages, sources):
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
        body = chunk['text'][chunk.get('body_char_start', 0):]
        assert ''.join(''.join(restored).split()) == ''.join(body.split())
    assert all(all(flags) for flags in covered.values()), 'Source characters lost'


class BoundedSplitter:
    def __init__(self, encoding, max_tokens=800):
        self.encoding = encoding
        self.max_tokens = max_tokens

    @lru_cache(maxsize=8192)
    def count(self, text):
        return len(self.encoding.encode(text, disallowed_special=()))

    def split_prose(self, text, begin, end, prefix, level=0):
        """Prefer whole clauses, then paragraphs/bullets, sentences and words."""
        if self.count(prefix + text[begin:end]) <= self.max_tokens:
            return [(begin, end)]
        patterns = [r'(?m)^[ \t]*[“"«]?\d{1,2}[.,][ \t]+',
                    r'\n[ \t]*\n+',
                    r'(?m)^[ \t]*(?:[a-zđ]\)|[-•])[ \t]+',
                    r'(?<=[.!?;:])[ \t\n]+', r'\s+']
        if level >= len(patterns):
            # Work on Unicode characters, not sliced token byte sequences.
            result, cursor = [], begin
            while cursor < end:
                lo, hi = cursor, end
                while lo < hi:
                    mid = (lo+hi+1)//2
                    if self.count(prefix + text[cursor:mid]) <= self.max_tokens:
                        lo = mid
                    else:
                        hi = mid-1
                if lo == cursor:
                    raise ValueError('Context leaves no room for source text')
                result.append((cursor, lo))
                cursor = lo
            return result
        cuts = [begin]
        for match in re.finditer(patterns[level], text[begin:end]):
            pos = begin + (match.start() if level in (0, 2) else match.end())
            if begin < pos < end and pos != cuts[-1]:
                cuts.append(pos)
        cuts.append(end)
        if len(cuts) == 2:
            return self.split_prose(text, begin, end, prefix, level+1)
        units = []
        for a, b in zip(cuts, cuts[1:]):
            units.extend(self.split_prose(text, a, b, prefix, level+1))
        packed = []
        for a, b in units:
            if packed and self.count(prefix + text[packed[-1][0]:b]) <= self.max_tokens:
                packed[-1] = packed[-1][0], b
            else:
                packed.append((a, b))
        return packed

    @staticmethod
    def regions(text):
        """Detect complete Markdown table runs; preserve individual row lines."""
        lines = list(re.finditer(r'[^\n]+\n?|\n', text))
        regions, cursor, i = [], 0, 0
        while i < len(lines):
            if not lines[i].group().lstrip().startswith('|'):
                i += 1
                continue
            j = i+1
            while j < len(lines) and lines[j].group().lstrip().startswith('|'):
                j += 1
            run = lines[i:j]
            if len(run) < 3 or not re.match(r'^\s*\|[\s:|\-]+\|\s*$', run[1].group()):
                i = j
                continue
            start, end = run[0].start(), run[-1].end()
            if start > cursor:
                if text[cursor:start].strip() or not regions:
                    regions.append(dict(begin=cursor, end=start, kind='prose'))
                else:
                    regions[-1]['end'] = start
            regions.append(dict(begin=start, end=end, kind='table',
                                header=(start, run[1].end()),
                                rows=[(line.start(), line.end()) for line in run[2:]]))
            cursor, i = end, j
        if cursor < len(text):
            if text[cursor:].strip() or not regions:
                regions.append(dict(begin=cursor, end=len(text), kind='prose'))
            else:
                regions[-1]['end'] = len(text)
        return regions

    def pieces(self, parent):
        text = parent['text']
        context = (f"Tài liệu: {parent['document_title']}\n"
                   f"Phần: {parent['instrument']} | {parent['section']}\n\n")
        if self.count(context + text) <= self.max_tokens:
            return [(0, len(text), context, 'section', [])]
        regions = self.regions(text)
        first_table = next((r for r in regions if r['kind'] == 'table'), None)
        tuition = parent['doc_id'] == 'D03' and parent['instrument'] == 'appendix' and parent['section_number'] == '1'
        legend = (0, first_table['begin']) if tuition and first_table else None
        result = []
        for region in regions:
            a, b = region['begin'], region['end']
            if region['kind'] == 'prose':
                result.extend((x, y, context, 'prose', [])
                              for x, y in self.split_prose(text, a, b, context))
                continue
            ha, hb = region['header']
            cursor = a
            for row_a, row_b in region['rows']:
                # Original header is present in the first body of each table.
                repeated = ([legend] if legend else []) + ([(ha, hb)] if cursor != a else [])
                prefix = context + ''.join(text[x:y]+'\n' for x, y in repeated)
                if self.count(prefix + text[cursor:row_b]) > self.max_tokens:
                    if cursor == row_a or row_a == hb and cursor == a:
                        raise ValueError(f"A table row exceeds the token ceiling: {parent['chunk_id']}")
                    result.append((cursor, row_a, prefix, 'table', repeated))
                    cursor = row_a
                    repeated = ([legend] if legend else []) + [(ha, hb)]
                    prefix = context + ''.join(text[x:y]+'\n' for x, y in repeated)
                    if self.count(prefix + text[cursor:row_b]) > self.max_tokens:
                        raise ValueError(f"A table row exceeds the token ceiling: {parent['chunk_id']}")
            repeated = ([legend] if legend else []) + ([(ha, hb)] if cursor != a else [])
            prefix = context + ''.join(text[x:y]+'\n' for x, y in repeated)
            if self.count(prefix + text[cursor:b]) > self.max_tokens:
                # Trailing whitespace can be measured differently by BPE.
                raise ValueError('Table trailing text exceeds the token ceiling')
            result.append((cursor, b, prefix, 'table', repeated))
        return result


def build(pages, sources, encoding=None, max_tokens=800):
    if encoding is None:
        encoding = tiktoken.get_encoding('cl100k_base')
    splitter = BoundedSplitter(encoding, max_tokens)
    page_lookup = {(p['doc_id'], p['pdf_page']): p for p in pages}
    chunks, parent_count = [], Counter()
    for parent in build_sections(pages, sources):
        parent_count[parent['doc_id']] += 1
        section_id = (f"{parent['doc_id']}_{parent['instrument']}_"
                      f"{parent['section_type']}_{parent['section_number'] or parent_count[parent['doc_id']]}")
        positions, cursor = [], 0
        for span in parent['source_spans']:
            source = page_lookup[parent['doc_id'], span['pdf_page']]['text']
            fragment = source[span['char_start']:span['char_end']]
            start = parent['text'].index(fragment, cursor)
            positions.append((start, start+len(fragment), span))
            cursor = start+len(fragment)

        def spans_for(begin, end):
            return [dict(pdf_page=s['pdf_page'],
                         char_start=s['char_start']+max(begin, a)-a,
                         char_end=s['char_start']+min(end, b)-a)
                    for a, b, s in positions if max(begin, a) < min(end, b)]

        pieces = splitter.pieces(parent)
        for index, (begin, end, prefix, kind, repeats) in enumerate(pieces, 1):
            body = parent['text'][begin:end]
            source_spans = spans_for(begin, end)
            chunk = dict(parent)
            chunk.update(chunk_id=f'{section_id}_{index:02d}', section_id=section_id,
                         chunk_index=index, chunks_in_section=len(pieces),
                         content_type=kind, text=prefix+body,
                         body_char_start=len(prefix), char_count=len(prefix+body),
                         word_count=len((prefix+body).split()),
                         token_count=splitter.count(prefix+body),
                         source_spans=source_spans,
                         pdf_pages=list(dict.fromkeys(s['pdf_page'] for s in source_spans)),
                         context_source_spans=[s for a, b in repeats for s in spans_for(a, b)],
                         context_is_derived=True)
            assert 0 < chunk['token_count'] <= max_tokens
            assert source_spans, 'Chunk has no source body'
            chunks.append(chunk)
    validate(pages, chunks)
    return chunks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-tokens', type=int, default=800)
    args = parser.parse_args()
    if args.max_tokens < 200:
        parser.error('--max-tokens must be at least 200 to allow source context')
    os.environ.setdefault('TIKTOKEN_CACHE_DIR', str(ROOT / 'tmp/tiktoken_cache'))
    encoding = tiktoken.get_encoding('cl100k_base')
    corpus = ROOT / 'data/processed/corpus_pages.json'
    sources = ROOT / 'data/sources.json'
    pages = json.loads(corpus.read_text(encoding='utf-8'))
    chunks = build(pages, json.loads(sources.read_text(encoding='utf-8')), encoding, args.max_tokens)
    tokens = [c['token_count'] for c in chunks]
    payload = dict(
        config=dict(strategy='structure_then_bounded_clauses_and_table_rows', version='structure_bounded_v2',
                    unit='article_in_regulations; top_level_section_in_appendices',
                    max_tokens=args.max_tokens, tokenizer='cl100k_base',
                    tiktoken_version=importlib.metadata.version('tiktoken'),
                    limit_includes_context=True, overlap=0,
                    table_policy='whole_rows_with_repeated_headers_and_tuition_legend',
                    prose_policy='clauses_then_paragraphs_bullets_sentences_words',
                    front_matter='attached_to_first_section_of_each_instrument',
                    corpus_sha256=hashlib.sha256(corpus.read_bytes()).hexdigest(),
                    sources_sha256=hashlib.sha256(sources.read_bytes()).hexdigest()),
        statistics=dict(source_pages=len(pages), chunks=len(chunks),
                        by_document=dict(Counter(c['doc_id'] for c in chunks)),
                        by_instrument=dict(Counter(f"{c['doc_id']}/{c['instrument']}" for c in chunks)),
                        cross_page_chunks=sum(len(c['pdf_pages']) > 1 for c in chunks),
                        sections=len({c['section_id'] for c in chunks}),
                        split_sections=sum(c['chunk_index'] == 1 and c['chunks_in_section'] > 1 for c in chunks),
                        total_tokens=sum(tokens), mean_tokens=round(statistics.mean(tokens), 1),
                        median_tokens=statistics.median(tokens), min_tokens=min(tokens), max_tokens=max(tokens),
                        token_bands={'1-500': sum(t <= 500 for t in tokens),
                                     '501-800': sum(500 < t <= 800 for t in tokens),
                                     '>800': sum(t > 800 for t in tokens)},
                        max_char_count=max(c['char_count'] for c in chunks),
                        all_source_characters_covered=True), chunks=chunks)
    output = ROOT / 'data/chunks/chunks_by_structure.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(payload['statistics'], ensure_ascii=False, indent=2))
    print(f'Output: {output}')


if __name__ == '__main__':
    main()
