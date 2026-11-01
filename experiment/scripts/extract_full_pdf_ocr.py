"""OCR every page of the four original PDFs locally, without page selection.

Example from repository root:
  python experiment/scripts/extract_full_pdf_ocr.py --tessdata /path/to/tessdata

Requires vie.traineddata and eng.traineddata. Output is an OCR draft/cache in
experiment/tmp/full_ocr/, not an automatic overwrite of the reviewed corpus.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import os
import pymupdf

ROOT = Path(__file__).resolve().parents[1]

def extract(job):
    pdf_path, doc_id, number, tessdata, output, dpi = job
    os.environ['OMP_THREAD_LIMIT'] = '1'
    with pymupdf.open(pdf_path) as pdf:
        page = pdf[number-1]
        tp = page.get_textpage_ocr(language='vie+eng', dpi=dpi, full=True, tessdata=tessdata)
        data = dict(doc_id=doc_id, pdf_page=number, text=page.get_text(textpage=tp),
                    words=page.get_text('words', textpage=tp), dpi=dpi,
                    extraction_method='Tesseract vie+eng full-page OCR via PyMuPDF',
                    source_sha256=hashlib.sha256(Path(pdf_path).read_bytes()).hexdigest())
    if not data['text'].strip():
        raise ValueError(f'{doc_id} page {number}: empty OCR output')
    Path(output).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return doc_id,number,len(data['text'])

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tessdata',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--dpi',type=int,default=300)
    args=parser.parse_args()
    tessdata=args.tessdata.resolve()
    for lang in ['vie','eng']:
        if not (tessdata/f'{lang}.traineddata').is_file():
            parser.error(f'Missing {lang}.traineddata in {tessdata}')
    output=ROOT/'tmp/full_ocr'
    output.mkdir(parents=True,exist_ok=True)
    jobs=[]
    for pdf_path in sorted((ROOT/'data/raw').glob('D0*.pdf')):
        with pymupdf.open(pdf_path) as pdf:
            count=len(pdf)
        for number in range(1,count+1):
            target=output/f'{pdf_path.name[:3]}_p{number:02}.json'
            digest=hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            if target.exists():
                cached=json.loads(target.read_text(encoding='utf-8'))
                if cached.get('source_sha256')==digest and cached.get('dpi')==args.dpi and cached.get('text','').strip():
                    continue
            jobs.append((str(pdf_path),pdf_path.name[:3],number,str(tessdata),str(target),args.dpi))
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(extract,job) for job in jobs]
        for future in as_completed(futures):
            doc,number,chars=future.result()
            print(f'{doc} page {number}: {chars} characters',flush=True)
    print(f'Full-page OCR cache: {output}',flush=True)

if __name__=='__main__':
    main()
