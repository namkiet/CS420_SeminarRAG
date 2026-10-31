"""Build the four-document corpus and 20-question evaluation set.

Input Markdown contains visually checked, explicitly selected source excerpts.
Original complete PDFs are retained separately; no network or model calls here.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = DATA / 'processed'
ARCHIVE = DATA / 'archive/single_document_v1'

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

sources = read_json(ARCHIVE/'sources.json')
sources[0].update(processed_paths=['data/processed/D01_corpus.md','data/processed/D01_tot_nghiep.md'],
    scope='Học phần, tín chỉ, tổ chức học tập; bổ sung Điều 19 về điều kiện tốt nghiệp; giữ Điều 27 về chuyển tiếp.',
    application_note='Câu hỏi theo Quy chế 2026. Phải đọc Điều 27 khi áp dụng cho khóa 2025 trở về trước; không mặc định mọi quy định mới áp dụng nguyên trạng cho khóa cũ.',
    corpus_version='multi_document_v2', updated_date='2026-11-01',
    extraction_method='Bản trích chọn đã đối chiếu ảnh PDF; D01_corpus.md giữ 6 trang cũ, D01_tot_nghiep.md bổ sung các khoản của Điều 19.')

def source(doc, title, number, date, raw, md, url, file_url, note):
    return dict(doc_id=doc, title=title, publisher='Trường Đại học Khoa học tự nhiên, ĐHQG-HCM',
        decision_number=number, version_or_issue_date=date, accessed_date='2026-11-01',
        source_url=url, source_pdf_url=file_url, raw_path='data/raw/'+raw,
        processed_path='data/processed/'+md, processed_paths=['data/processed/'+md],
        usage_basis='Văn bản quyết định/quy chế do Trường công bố; lưu nguồn cho nghiên cứu seminar. Không gán giấy phép mở cho toàn website.',
        application_note=note, extraction_method='Chép sạch các phần trích chọn từ ảnh PDF; giữ bảng, số liệu và nguồn theo trang.',
        verified=True, human_review_status='pending', corpus_version='multi_document_v2')

sources += [source('D02','Quy chế đánh giá kết quả rèn luyện 2020 và sửa đổi 2023',
    '1028/QĐ-KHTN; sửa đổi 2739/QĐ-KHTN','2023-12-12',
    'D02_quy_che_diem_ren_luyen_2020_sua_2023.pdf','D02_corpus.md',
    'https://hcmus.edu.vn/quy-che-danh-gia-ket-qua-ren-luyen-sinh-vien-he-chinh-quy/',
    'https://hcmus.edu.vn/wp-content/uploads/2024/03/QD-1028-QC-DRL-2020_20231.pdf',
    'Snapshot PDF 2020 + sửa đổi 2023, không mặc định là quy định mới nhất năm 2026. Phần sửa đổi được ưu tiên trong phạm vi snapshot. Nguồn sửa đổi ghi 1208 cho số quyết định gốc, khác 1028 trên trang đầu; không tự sửa.'),
source('D03','Định mức học phí 2026–2027, chính quy đại trà khóa 2022–2026',
    '3317/QĐ-KHTN','2026-10-14', 'D03_hoc_phi_2026_2027_K2022_ve_sau.pdf','D03_corpus.md',
    'https://hcmus.edu.vn/thong-bao-nop-hoc-phi-hoc-ky-1-2026-2027-chuong-trinh-dai-tra/',
    'https://drive.google.com/file/d/1G4lC45rem_Sxd3FXL22IvUBb5fX34Cbr/view?usp=drivesdk',
    'Năm học 2026–2027; hệ chính quy đại trà, kể cả cử nhân tài năng; khóa 2022, 2023, 2024, 2025, 2026. Không áp dụng bảng này cho khóa trước 2022 hoặc chương trình đề án. Tín chỉ học phí được tính từ số tiết thực học.'),
source('D04','Chuẩn ngoại ngữ trong quá trình học và khi tốt nghiệp — đại trà/tài năng',
    '2464/QĐ-KHTN','2026-08-11', 'D04_chuan_ngoai_ngu_tot_nghiep_2026.pdf','D04_corpus.md',
    'https://hcmus.edu.vn/quy-dinh-ve-viec-hoc-ngoai-ngu-va-chuan-trinh-do-ngoai-ngu-khi-tot-nghiep-dai-hoc/',
    'https://hcmus.edu.vn/wp-content/uploads/2026/08/QD-2464_QD-chuan-NN-2026_DT_TN-1.pdf',
    'Phần quyết định ghi đại trà/tài năng từ khóa 2022 trở về sau. Chuẩn đầu ra tài năng phân biệt khóa 2022 và khóa 2023 trở về sau. Không dùng QĐ2464 cho chương trình tăng cường tiếng Anh/tiên tiến có quyết định khác.')]
by_source = {s['doc_id']:s for s in sources}

pages=[]
for s in sources:
    for relative in s['processed_paths']:
        content=(ROOT/relative).read_text(encoding='utf-8')
        parts=re.split(r'^## \[PDF (\d+) \| Trang in (.*?) \| (.*?)\]\n',content,flags=re.M)
        assert len(parts)>1, relative
        for i in range(1,len(parts),4):
            n,printed,section,body=parts[i:i+4]
            pages.append(dict(doc_id=s['doc_id'],pdf_page=int(n),
                printed_page=int(printed) if printed.isdigit() else None,
                section=section,text=body.strip(),source_url=s['source_url'],
                source_pdf_url=s['source_pdf_url'],corpus_version='multi_document_v2'))
    ps=sorted(p['pdf_page'] for p in pages if p['doc_id']==s['doc_id'])
    assert len(ps)==len(set(ps))
    s['selected_pdf_pages']=ps
    s['selected_printed_pages']=[p['printed_page'] for p in sorted(pages,key=lambda x:x['pdf_page']) if p['doc_id']==s['doc_id']]
    raw=ROOT/s['raw_path']
    with pymupdf.open(raw) as pdf:
        s['source_total_pages']=len(pdf)
    s['sha256']=hashlib.sha256(raw.read_bytes()).hexdigest()
    s['page_data_path']=f'data/processed/{s["doc_id"]}_pages.json'
    s['processed_coverage']='selected_excerpts_not_full_pdf'
    dump(OUT/f'{s["doc_id"]}_pages.json',[p for p in pages if p['doc_id']==s['doc_id']])
lookup={(p['doc_id'],p['pdf_page']):p for p in pages}

def ev(doc,page,section,quote):
    assert quote in lookup[doc,page]['text'],(doc,page,quote)
    s=by_source[doc]
    return dict(doc_id=doc,pdf_page=page,printed_page=lookup[doc,page]['printed_page'],
        section=section,quote=quote,source_url=s['source_url'],source_pdf_url=s['source_pdf_url'],
        local_pdf=s['raw_path']+f'#page={page}')

old=read_json(ARCHIVE/'questions.json')
questions=[]
def add(kind,question,answer,evidence,points,note=''):
    questions.append(dict(question_id=f'Q{len(questions)+1:02}',question=question,
        reference_answer=answer,question_type=kind,expected_key_points=points,evidence=evidence,
        relevant_chunk_ids=[],verified=True,human_review_status='pending',
        verification_method='Trợ lý đọc ảnh PDF và đối chiếu đoạn trích; script kiểm tra quote có trong đúng trang bản sạch.',
        corpus_version='multi_document_v2',notes=note))

for index in [0,2,16,19]:
    q=old[index]
    add(q['question_type'],q['question'],q['reference_answer'],q['evidence'],q['expected_key_points'],q['notes'])
add('direct_lookup','Theo Điều 19 Quy chế đào tạo 2026, chỉ tích lũy đủ tín chỉ đã đủ điều kiện xét tốt nghiệp chưa?',
    'Chưa. Còn phải không đang bị đình chỉ học tập do kỷ luật tại thời điểm xét, đạt học lực từ trung bình trở lên, hoàn tất GDQP có chứng chỉ và GDTC, đạt chuẩn ngoại ngữ, chuẩn tin học của chương trình và thỏa các quy định của quy chế.',
    [ev('D01',17,'Điều 19 khoản 1',lookup['D01',17]['text'].split('1. ',1)[1].split('\n\n2.',1)[0])],
    ['Không chỉ đủ tín chỉ','Không đang bị đình chỉ học tập','Học lực từ trung bình','GDQP và GDTC','Ngoại ngữ và tin học','Các quy định của quy chế'])

add('paraphrase','Theo bản quy chế điểm rèn luyện 2020 kèm sửa đổi 2023 trong D02, tổng các nội dung được 112 điểm thì ghi điểm rèn luyện bao nhiêu?',
    'Quy về 100 điểm vì tổng điểm nội dung đánh giá vượt 100.',
    [ev('D02',3,'Điều 4 khoản 4','Trong trường hợp tổng điểm các nội dung đánh giá lớn hơn 100 điểm thì Điểm rèn luyện quy về điểm 100.')],['100 điểm'])
add('direct_lookup','Theo D02 (quy chế 2020 kèm sửa đổi 2023), sinh viên được 68 điểm rèn luyện xếp loại gì?',
    'Loại Khá theo ngưỡng từ 65 đến 79 điểm của Điều 7 trong bản PDF này.',
    [ev('D02',5,'Điều 7 khoản 2(c)','Từ 65 đến 79 điểm: loại Khá.')],['Loại Khá','Đúng bản D02 2020 + sửa đổi 2023'],
    'Không dùng ngưỡng của bài trích lược theo Thông tư 40/2026 ở ngoài corpus để thay đáp án của câu hỏi phiên bản này.')
add('paraphrase','Theo sửa đổi 2739 năm 2023 trong D02, sinh viên nghỉ học tạm thời hoặc còn thời gian đào tạo nhưng không đăng ký học phần được đánh giá rèn luyện ra sao?',
    'Được xếp loại Trung bình, 50 điểm trong học kỳ đó.',
    [ev('D02',15,'QĐ2739 Điều 1 mục 3, sửa Điều 8 khoản 5','Sinh viên nghỉ học tạm thời hoặc sinh viên còn đang trong thời gian đào tạo nhưng không đăng ký học phần thì kết quả rèn luyện trong học kỳ đó được xếp loại Trung bình (50 điểm).')],
    ['Trung bình','50 điểm','Theo sửa đổi 2023'])
add('worked_calculation','Theo công thức sửa đổi năm 2023 của D02, ba học kỳ chính có đánh giá lần lượt là 70, 80 và 90 điểm thì điểm rèn luyện toàn khóa trước các khoản cộng đặc biệt là bao nhiêu?',
    'R = (70 + 80 + 90) / 3 = 80 điểm, lấy trung bình các học kỳ chính có đánh giá.',
    [ev('D02',15,'QĐ2739 Điều 1 mục 2, sửa Điều 6 khoản 3','Điểm rèn luyện toàn khóa học là trung bình cộng của điểm rèn luyện các học kỳ chính có đánh giá kết quả rèn luyện của khóa học và được tính theo công thức: R = (r_1 + ... + r_N) / N.')],
    ['Trung bình học kỳ chính có đánh giá','80 điểm'], 'Số liệu giả định và phép tính do nhóm tạo, không phải kết quả của sinh viên thật.')
add('direct_lookup','Theo Điều 9 của bản D02, thời hạn tiếp nhận phản hồi và đề nghị điều chỉnh kết quả rèn luyện dự kiến là bao lâu kể từ công bố?',
    'Trong vòng 15 ngày kể từ thời điểm công bố kết quả dự kiến.',
    [ev('D02',6,'Điều 9 khoản 4','Phòng Công tác Sinh viên công bố kết quả rèn luyện dự kiến học kỳ đánh giá qua hộp thư điện tử của sinh viên và tiếp nhận phản hồi, cập nhật minh chứng, đề nghị điều chỉnh trong vòng 15 ngày kể từ thời điểm công bố, đồng thời gửi kết quả của sinh viên trước và sau điều chỉnh đến Hội đồng đánh giá kết quả rèn luyện cấp Khoa.')],
    ['15 ngày','Từ công bố dự kiến','Theo phiên bản D02'])

add('direct_lookup','Theo QĐ3317, học phí được thu theo học kỳ dựa trên gì và một tín chỉ học phí tương ứng bao nhiêu tiết thực học?',
    'Căn cứ tổng số tiết thực học của các học phần đã đăng ký trong học kỳ và mức thu một tín chỉ học phí theo năm học; 15 tiết thực học bằng một tín chỉ học phí.',
    [ev('D03',1,'Điều 1','Học phí đối với sinh viên trình độ đại học hệ chính quy chương trình đại trà (kể cả sinh viên cử nhân tài năng) được thu theo học kỳ căn cứ vào tổng số tiết thực học của các học phần mà sinh viên đăng ký học trong học kỳ và mức thu của một tín chỉ học phí được quy định theo năm học, trong đó 15 tiết thực học được tính là một tín chỉ học phí.')],
    ['Theo tiết thực học và đơn giá năm học','15 tiết = 1 tín chỉ học phí'])
header=ev('D03',2,'Phụ lục I, chú giải cột C5','C5: đơn giá 01 tín chỉ học phí các học phần khối kiến thức giáo dục chuyên nghiệp gồm cơ sở ngành, chuyên ngành, tốt nghiệp...')
ai=ev('D03',4,'Phụ lục I dòng 16','| 16 | 7480107 | Trí tuệ nhân tạo | không có | 488.000 | 488.000 | 734.000 | 1.014.000 | 40.500.000 | 162.000.000 |')
it=ev('D03',4,'Phụ lục I dòng 17','| 17 | 7480201 | Nhóm ngành Công nghệ thông tin | 488.000 | 488.000 | 488.000 | 734.000 | 974.000 | 40.500.000 | 162.000.000 |')
add('multi_evidence','Trong bảng QĐ3317 năm học 2026–2027 cho khóa 2022–2026, đơn giá một tín chỉ học phí khối giáo dục chuyên nghiệp ngành Trí tuệ nhân tạo là bao nhiêu?',
    '1.014.000 đồng cho một tín chỉ học phí khối giáo dục chuyên nghiệp; không phải đơn giá chung cho mọi học phần của ngành.',
    [header,ai],['1.014.000 đồng','Khối giáo dục chuyên nghiệp','Một tín chỉ học phí'])
add('worked_calculation','Theo QĐ3317, đơn giá tín chỉ học phí khối giáo dục chuyên nghiệp ngành Trí tuệ nhân tạo cao hơn nhóm ngành Công nghệ thông tin bao nhiêu trong năm học 2026–2027?',
    'Trí tuệ nhân tạo: 1.014.000 đồng; nhóm ngành CNTT: 974.000 đồng. Chênh lệch 40.000 đồng cho một tín chỉ học phí của khối này.',
    [header,ai,it],['1.014.000','974.000','Chênh 40.000 đồng'], 'Phép trừ do nhóm thực hiện từ bảng nguồn; không suy ra chênh lệch học phí cả năm.')
add('paraphrase','Có thể dùng bảng học phí QĐ3317 năm học 2026–2027 trong D03 để tính học phí cho sinh viên khóa 2020 không?',
    'Không. Bảng này quy định cho hệ chính quy đại trà khóa tuyển 2022, 2023, 2024, 2025 và 2026; khóa 2020 ngoài phạm vi, cần văn bản áp dụng riêng.',
    [ev('D03',1,'Điều 2','Mức thu của một tín chỉ học phí trong năm học 2026-2027 đối với sinh viên trình độ đại học hệ chính quy chương trình đại trà khóa tuyển 2022, 2023, 2024, 2025 và 2026 theo loại học phần được quy định tại phụ lục I đính kèm quyết định này.')],
    ['Không','Chỉ khóa 2022–2026','Cần nguồn khác cho khóa 2020'])
add('cross_document','Sinh viên đại trà khóa 2024 đã nộp IELTS 4.5 hợp lệ do British Council hoặc IDP cấp có cơ sở được xét miễn học Anh văn không; nếu phải học thì đơn giá tín chỉ học phí Anh văn năm 2026–2027 là bao nhiêu?',
    'Có cơ sở được xét miễn: QĐ2464 công nhận IELTS 4.5 do British Council hoặc IDP Australia cấp trong danh sách chuẩn đầu ra đại trà, còn QĐ3317 nêu được xét miễn học Anh văn khi nộp chứng chỉ đạt chuẩn theo quy định. Nếu phải học, đơn giá một tín chỉ học phí Anh văn là 488.000 đồng. Việc xét cần đáp ứng thủ tục và hiệu lực chứng chỉ, không tự động chỉ từ điểm IELTS.',
    [ev('D04',6,'Điều 7 khoản 2(a)','Chứng chỉ IELTS 4.5 do British Council hoặc IDP Australia cấp.'),
     ev('D03',5,'Phụ lục I mục 3','Các học phần Anh văn là học phần điều kiện và thuộc khối kiến thức bổ trợ, sinh viên được xét miễn học nếu nộp chứng chỉ ngoại ngữ đạt chuẩn đầu ra theo quy định hiện hành.'),
     ev('D03',5,'Phụ lục I mục 3','Đối với sinh viên trình độ đại học chương trình đại trà khóa tuyển 2022, 2023, 2024, 2025 và 2026, đơn giá 01 tín chỉ học phí các học phần Anh văn là 488.000 đồng.')],
    ['Được xét miễn khi nộp chứng chỉ hợp lệ','IELTS 4.5 đúng đơn vị cấp','488.000 đồng/tín chỉ học phí','Không tự động miễn chỉ vì có điểm IELTS'])

add('multi_evidence','Theo QĐ2464, mức IELTS tối thiểu trong danh sách chuẩn đầu ra khác nhau thế nào giữa đại trà khóa 2024 và cử nhân tài năng khóa 2024?',
    'Đại trà khóa 2024: IELTS 4.5 (chuẩn bậc 3/6). Cử nhân tài năng khóa 2024 thuộc nhóm khóa 2023 trở về sau: IELTS 5.0 (chuẩn bậc 4/6). Chứng chỉ do British Council hoặc IDP Australia cấp và phải đáp ứng điều kiện hiệu lực, hồ sơ.',
    [ev('D04',6,'Điều 7 khoản 2(a)','Chứng chỉ IELTS 4.5 do British Council hoặc IDP Australia cấp.'),
     ev('D04',6,'Điều 8 khoản 2','Sinh viên từ khóa tuyển 2023 trở về sau: Chuẩn ngoại ngữ đầu ra của sinh viên tốt nghiệp trình độ đại học hệ chính quy chương trình cử nhân tài năng là ngoại ngữ tiếng Anh và phải đạt tối thiểu bậc 4/6 theo khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam.'),
     ev('D04',7,'Điều 8 khoản 3(a)','Chứng chỉ IELTS 5.0 do British Council hoặc IDP Australia cấp.')],
    ['Đại trà 4.5','Tài năng khóa 2024: 5.0','Đúng tổ chức cấp và hồ sơ hợp lệ'])
add('multi_evidence','Theo QĐ2464, hoàn thành Anh văn 1–4 có đồng nghĩa tự động đạt chuẩn ngoại ngữ đầu ra đại trà không?',
    'Không. Hoàn thành Anh văn 1–4 là một cách đạt chuẩn trong quá trình học để xét học chuyên ngành. Chuẩn đầu ra đại trà được quy định riêng tại Điều 7; sinh viên phải nộp chứng chỉ/văn bằng theo khoản 2 hoặc 3 trước khi nộp hồ sơ xét tốt nghiệp.',
    [ev('D04',5,'Điều 6 khoản 2','Để được xét đăng ký và học các học phần chuyên ngành, SV phải thỏa một trong ba điều kiện như sau:\n\na) SV hoàn tất bốn học phần Anh văn trong chương trình đào tạo gồm: Anh văn 1, Anh văn 2, Anh văn 3 và Anh văn 4.'),
     ev('D04',6,'Điều 7 khoản 4','SV phải nộp chứng chỉ đạt chuẩn trình độ ngoại ngữ đầu ra theo khoản 2 hoặc khoản 3 Điều này trước khi nộp hồ sơ xét tốt nghiệp trình độ đại học chương trình đại trà.')],
    ['Không tự động','Phân biệt chuẩn quá trình học với chuẩn đầu ra','Nộp chứng chỉ/văn bằng theo Điều 7'])
add('paraphrase','Theo QĐ2464, hạn chậm nhất đạt chuẩn tiếng Anh trong quá trình học là khi nào và chưa đạt sẽ bị hạn chế gì?',
    'Chậm nhất cuối học kỳ thứ 6. Không đạt chuẩn theo khoản 2 và 3 Điều 6 thì không được tiếp tục đăng ký và học các học phần chuyên ngành.',
    [ev('D04',5,'Điều 6 khoản 3–4','3. Chậm nhất là cuối học kỳ thứ 6, SV phải đạt chuẩn tiếng Anh trong quá trình học theo khoản 2 Điều này.\n\n4. Đối với SV không đạt chuẩn tiếng Anh theo quy định tại khoản 2 và khoản 3 Điều này, SV không được tiếp tục đăng ký và học các học phần chuyên ngành.')],
    ['Cuối học kỳ 6','Không tiếp tục đăng ký và học chuyên ngành'])
add('direct_lookup','Theo QĐ2464, chứng chỉ ngoại ngữ không ghi thời hạn hiệu lực được tính hiệu lực thế nào khi xét chuẩn đầu ra?',
    'Hiệu lực 2 năm tính từ ngày cấp (được tính ngay sau khi công bố kết quả thi chứng chỉ) đến ngày đăng ký xét đạt chuẩn ngoại ngữ đầu ra cho Trường.',
    [ev('D04',8,'Điều 11 khoản 2','Đối với chứng chỉ không ghi hiệu lực thời gian: Hiệu lực của chứng chỉ ngoại ngữ là 02 (hai) năm tính từ ngày cấp (được tính ngay sau khi công bố kết quả thi chứng chỉ của sinh viên) đến ngày đăng ký xét đạt chuẩn ngoại ngữ đầu ra cho Trường.')],
    ['2 năm','Đúng mốc cấp/công bố và đăng ký xét chuẩn'])
add('direct_lookup','Hồ sơ xét chuẩn ngoại ngữ đầu ra theo Điều 12 QĐ2464 gồm gì?',
    'Đơn đăng ký xét chuẩn đầu ra ngoại ngữ; bản photo công chứng chứng chỉ hoặc bản photo kèm bản chính đối chiếu; mang Căn cước công dân để đối chiếu.',
    [ev('D04',8,'Điều 12','1. Đơn đăng ký xét đạt chuẩn đầu ra ngoại ngữ.\n\n2. Bản photo có công chứng các chứng chỉ (hoặc bản photo chứng chỉ kèm bản chính đối chiếu).\n\n3. Mang theo Căn cước công dân để đối chiếu.')],
    ['Đơn đăng ký','Bản sao chứng chỉ đúng hình thức','CCCD đối chiếu'])

assert len(questions)==20
for q in questions:
    for e in q['evidence']:
        assert e['quote'] in lookup[e['doc_id'],e['pdf_page']]['text']
dump(DATA/'sources.json',sources)
dump(DATA/'questions.json',questions)
dump(OUT/'corpus_pages.json',pages)
manifest=dict(corpus_version='multi_document_v2',updated_date='2026-11-01',
    source_document_count=len(sources),raw_pdf_pages=sum(s['source_total_pages'] for s in sources),
    selected_source_page_count=len(pages),processed_coverage='selected_excerpts_not_full_51_pages',
    retrieval_input='data/processed/corpus_pages.json',question_count=len(questions),
    evidence_spans=sum(len(q['evidence']) for q in questions),
    doc_evidence_counts=dict(Counter(e['doc_id'] for q in questions for e in q['evidence'])),
    human_review_status='pending')
dump(DATA/'corpus_manifest.json',manifest)

corpus=[]
for s in sources:
    corpus += [f"# {s['doc_id']} — {s['title']}",'', 'Phạm vi/phiên bản: '+s['application_note'],'']
    for p in pages:
        if p['doc_id']==s['doc_id']:
            corpus += [f"## [{p['doc_id']} PDF {p['pdf_page']}] {p['section']}",'',p['text'],'']
(OUT/'corpus_all.md').write_text('\n'.join(corpus)+'\n',encoding='utf-8')

lines=['# Bộ 20 câu hỏi — corpus 4 tài liệu HCMUS','',
    'Phiên bản: multi_document_v2. Bộ câu hỏi cũ một nguồn được giữ tại `archive/single_document_v1/`. Không so sánh trực tiếp điểm số của hai bộ như cùng một benchmark.','',
    'Tất cả câu hỏi có bằng chứng trong corpus trích chọn. Đã được trợ lý đọc ảnh và kiểm tra tính nhất quán; nhóm chưa được ghi nhận đã tự kiểm chứng.','',
    'D02 là phiên bản PDF 2020 + sửa đổi 2023; câu hỏi về D02 có ghi rõ phiên bản, không mặc định là quy định mới nhất năm 2026.','']
for q in questions:
    lines += [f"## {q['question_id']}. {q['question']}",'',f"**Loại:** {q['question_type']}",'',
        '**Đáp án chuẩn:** '+q['reference_answer'],'','**Ý cần có:** '+'; '.join(q['expected_key_points'])+'.','', '**Bằng chứng:**','']
    for e in q['evidence']:
        raw=Path(by_source[e['doc_id']]['raw_path']).name
        lines += [f"- [{e['doc_id']}, PDF {e['pdf_page']}, {e['section']}](raw/{raw}#page={e['pdf_page']}):",'',
            '> '+e['quote'].replace('\n\n','\n> \n> '),'']
    if q['notes']:
        lines += ['**Lưu ý:** '+q['notes'],'']
(DATA/'questions.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
