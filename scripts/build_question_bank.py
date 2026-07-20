#!/usr/bin/env python3
"""Build a browser-ready question catalog from the professor-provided PDFs.

The generator preserves the English source text and numbering. It deliberately
keeps answer verification separate: no unverified answer is inferred here.
"""
from __future__ import annotations

import bisect
import json
import re
from pathlib import Path

from pypdf import PdfReader

BASE = Path('/Users/ortonhshieh/Library/Mobile Documents/com~apple~CloudDocs/NCCU MBA/商業數量管理/Quan1150(Chap12~18)Q-set')
FILES = {
    12: BASE / 'Quan1150(Chap12)Q-set.pdf',
    13: BASE / 'Quan1150(Chap13)Q-set.pdf',
    14: BASE / 'Quan1150(Chap14)Q-set.pdf',
    15: BASE / 'Quan1150(Chap15)Q-set.pdf',
    16: BASE / 'Quan1150(Chap16)Q-set.pdf',
    17: BASE / 'Quan1150(Chap17)Q-set.pdf',
    18: BASE / 'Quan1150Chap18)Q-set.pdf',
}
SOURCE_NAMES = {chapter: path.name for chapter, path in FILES.items()}

# pypdf preserves the values in these unequal-length Chapter 13 tables but
# loses the column position of trailing observations at a page break. Replace
# only the table body with an unambiguous, language-neutral column transcript.
CH13_TABLE_REPAIRS = {
    3: (
        'Store 1 Store 2 Store 3\n80 85 79\n75 86 85\n76 81 88\n89 80\n80',
        'Store 1: 80, 75, 76, 89, 80\nStore 2: 85, 86, 81, 80\nStore 3: 79, 85, 88',
    ),
    6: (
        'Treatment 1 Treatment 2 Treatment 3\n37 43 28\n33 39 32\n36 35 33\n38 38\n 40',
        'Treatment 1: 37, 33, 36, 38\nTreatment 2: 43, 39, 35, 38, 40\nTreatment 3: 28, 32, 33',
    ),
    8: (
        'Treatment 1 Treatment 2 Treatment 3\n45 31 39\n41 34 35\n37 35 40\n40 40\n42',
        'Treatment 1: 45, 41, 37, 40, 42\nTreatment 2: 31, 34, 35, 40\nTreatment 3: 39, 35, 40',
    ),
    12: (
        'University A University B University C\n89 60 82\n95 95 70\n75 89 90\n92 80 79\n99 66\n90',
        'University A: 89, 95, 75, 92, 99, 90\nUniversity B: 60, 95, 89, 80\nUniversity C: 82, 70, 90, 79, 66',
    ),
    14: (
        'Store 1 Store 2 Store 3\n88 76 85\n84 78 67\n88 60 58\n82 62\n93',
        'Store 1: 88, 84, 88, 82, 93\nStore 2: 76, 78, 60, 62\nStore 3: 85, 67, 58',
    ),
    30: (
        'Northern Central Southern\nUniversity University University\n75 85 80\n80 89 81\n84 86 84\n85 88 79\n81  83\n  85',
        'Northern University: 75, 80, 84, 85, 81\nCentral University: 85, 89, 86, 88\nSouthern University: 80, 81, 84, 79, 83, 85',
    ),
    31: (
        'Manufacturer A Manufacturer B Manufacturer C\n180 177 175\n175 180 176\n179 167 177\n\n176 172\n190',
        'Manufacturer A: 180, 175, 179, 176, 190\nManufacturer B: 177, 180, 167, 172\nManufacturer C: 175, 176, 177',
    ),
    46: (
        'Tennessee Kentucky Texas\n12 15 16\n13 19 18\n\n17 20\n10\n18',
        'Tennessee: 12, 13, 17, 10, 18\nKentucky: 15, 19, 20\nTexas: 16, 18',
    ),
}

CH14_FORMULA_REPAIRS = {
    20: ('\n = 75.061 - 6.254X', '\nŶ = 75.061 − 6.254X'),
    25: ('The least squares estimated line is  = 4.348 + 0.0826 X.',
         'The least squares estimated line is Ŷ = 4.348 + 0.0826X.'),
    32: ('\uf053X = 75 \uf053\uf020\uf028Y- )\uf028X- ) = -59\n'
         '\uf053Y = 135 \uf053\uf020\uf028X- )2 = 94\n'
         '\uf053\uf020\uf028Y- )2 = 100',
         'ΣX = 75    Σ(Y − ȳ)(X − x̄) = −59\n'
         'ΣY = 135   Σ(X − x̄)² = 94\n'
         'Σ(Y − ȳ)² = 100'),
    33: ('\uf053X = 42 \uf053 (Y - )(X - ) = 37\n'
         '\uf053Y = 63 \uf053\uf020(X - )2 = 84\n'
         'n = 7 \uf053 (Y - )2 = 28',
         'ΣX = 42    Σ(Y − ȳ)(X − x̄) = 37\n'
         'ΣY = 63    Σ(X − x̄)² = 84\n'
         'n = 7      Σ(Y − ȳ)² = 28'),
}

CH15_FORMULA_REPAIRS = {
    14: (
        'The estimated equation is\n. The standard errors',
        'The estimated equation is\nŶ = 23.5 − 14.28X₁ + 6.72X₂ + 15.68X₃. The standard errors',
    ),
    16: (
        'The following estimated\nequation was obtained.\n\nThe standard errors',
        'The following estimated\nequation was obtained.\n\nŶ = 23.72 + 12.61X + 0.798Z\n\nThe standard errors',
    ),
    20: (
        'equation was\nobtained.\n\nFor this model',
        'equation was\nobtained.\n\nŶ = 17 + 4X₁ − 3X₂ + 8X₃ + 5X₄ + 8X₅\n\nFor this model',
    ),
    25: (
        'The following regression model has been proposed to predict sales at a furniture store.\n\na.',
        "The following regression model has been proposed to predict sales at a furniture store.\n\n"
        "Ŷ = 10 − 4X₁ + 7X₂ + 18X₃\n"
        "where X₁ = competitor's previous day's sales (in $1,000s),\n"
        "X₂ = population within 1 mile (in 1,000s),\n"
        "X₃ = 1 if any form of advertising was used, 0 otherwise, and\n"
        "Ŷ = sales (in $1,000s).\n\na.",
    ),
    28: (
        'The following regression model has been proposed to predict sales at a fast food outlet.\n\na.',
        'The following regression model has been proposed to predict sales at a fast food outlet.\n\n'
        'Ŷ = 18 − 2X₁ + 7X₂ + 15X₃\n'
        'where X₁ = the number of competitors within 1 mile,\n'
        'X₂ = the population within 1 mile (in 1,000s),\n'
        'X₃ = 1 if drive-up windows are present, 0 otherwise, and\n'
        'Ŷ = sales (in $1,000s).\n\na.',
    ),
    29: (
        'The following regression model has been proposed to predict sales at a computer store.\n\nPredict sales',
        "The following regression model has been proposed to predict sales at a computer store.\n\n"
        "Ŷ = 50 − 3X₁ + 20X₂ + 10X₃\n"
        "where X₁ = competitor's previous day's sales (in $1,000s),\n"
        "X₂ = population within 1 mile (in 1,000s),\n"
        "X₃ = 1 if radio advertising was used, 0 otherwise, and\n"
        "Ŷ = sales (in $1,000s).\n\nPredict sales",
    ),
    30: (
        'The following regression model has been proposed to predict monthly sales at a shoe store.\n\na.',
        "The following regression model has been proposed to predict monthly sales at a shoe store.\n\n"
        "Ŷ = 40 − 3X₁ + 12X₂ + 10X₃\n"
        "where X₁ = competitor's previous month's sales (in $1,000s),\n"
        "X₂ = store's previous month's sales (in $1,000s),\n"
        "X₃ = 1 if radio advertising was used, 0 otherwise, and\n"
        "Ŷ = sales (in $1,000s).\n\na.",
    ),
}

CH16_FORMULA_REPAIRS = {
    1: [
        ('\n = 0.80\nS = 5.0', '\nR² = 0.80\nS = 5.0'),
        ('Hint:   =\n , but also  = 1-\n .', 'Hint: R² = SSR/SST, but also R² = 1 − SSE/SST.'),
    ],
    2: [
        ('of the form\n was developed, using Excel.', 'of the form\nŶ = b₀ + b₁x was developed, using Excel.'),
        ('part a) of the form\n was developed.', 'part a) of the form\nŶ = b₀ + b₁x + b₂x² was developed.'),
    ],
    3: [
        ('of the form\n  was developed for the above', 'of the form\nŶ = b₀ + b₁x was developed for the above'),
        ('equation of the form\n was developed for the above data', 'equation of the form\nŶ = b₀ + b₁x + b₂x² was developed for the above data'),
    ],
    4: [
        ('independent variable.\n\nThe sample size', 'independent variable.\n\nŶ = 60 + 200x − 6x²\n\nThe sample size'),
    ],
    5: [
        ('function is provided.\n = 0.408 + 1.338x 1', 'function is provided.\nŶ = 0.408 + 1.338x₁'),
        ('following function.\n = 0.805 + 0.498x 1 - 0.477x2', 'following function.\nŶ = 0.805 + 0.498x₁ − 0.477x₂'),
    ],
    6: [
        ('Assume that a model in the form of\n\nbest describes', 'Assume that a model in the form of\n\nY = β₀ + β₁X² + ε\n\nbest describes'),
    ],
    7: [
        ('can best be given by\n\nEstimate', 'can best be given by\n\nY = β₀ + β₁X² + ε\n\nEstimate'),
    ],
    10: [
        ('following model from a sample of 28 observations.\n\nSSE', 'following model from a sample of 28 observations.\n\nŶ = 23.62 + 18.86X₁ + 24.72X₂\nSSE'),
        ('additional variable X3. The results are\n\nSSE', 'additional variable X₃. The results are\n\nŶ = 25.32 + 15.29X₁ + 7.63X₂ + 12.72X₃\nSSE'),
    ],
    11: [
        ('based on a sample of 25 observations.\n\nSSE', 'based on a sample of 25 observations.\n\nŶ = 62.42 − 1.836X₁ + 25.62X₂\nSSE'),
        ('including the 3 variables. The results are\n\nSSE', 'including the 3 variables. The results are\n\nŶ = 59.23 − 1.762X₁ + 25.638X₂ + 16.237X₃ + 15.297X₄ − 18.723X₅\nSSE'),
    ],
    17: [
        ('resulted in the following model.\n\nand the following', 'resulted in the following model.\n\nŶ = 120 − 0.03X₁ + 0.7X₂\n\nand the following'),
    ],
    18: [
        ('resulted in the following information.\n\nn = 20', 'resulted in the following information.\n\nŶ = 5,000 + 1.2X₁ + 0.9X₂\n\nn = 20'),
    ],
    23: [
        ('resulted in the following information.\n\nThe SSE', 'resulted in the following information.\n\nŶ = 0.408 + 1.3387X₁ + 2X₂\n\nThe SSE'),
        ('following information was\nprovided.\n\nThis latter', 'following information was\nprovided.\n\nŶ = 1.2 + 3.0X₁ + 12X₂ + 4.0X₃ + 8X₄\n\nThis latter'),
    ],
}

# The source uses a Symbol-font alpha that pypdf drops entirely. Restore the
# visible Greek character without changing any wording or numeric content.
CH17_FORMULA_REPAIRS = {
    5: [('with  = 0.2', 'with α = 0.2')],
    6: [('with  = 0.3', 'with α = 0.3')],
    7: [('Use  = 0.3', 'Use α = 0.3'), ('Use  = 0.1', 'Use α = 0.1'), ('which  provides', 'which α provides')],
}

# Symbol-font characters in some multiple-choice options are visible in the
# PDF but are dropped or mis-decoded by pypdf. Keep these source-faithful
# repairs keyed by chapter and question so regenerated data stays correct.
MC_TEXT_REPAIRS = {
    (13, 18): [
        ('a.\nb. between-samples estimate of \nc. within-samples estimate of ',
         'a. x̄\nb. between-samples estimate of σ²\nc. within-samples estimate of σ²'),
    ],
}


def clean_page(text: str) -> str:
    lines = []
    skip_continuation = False
    for raw in text.replace('\u00a0', ' ').splitlines():
        line = raw.rstrip()
        if line.startswith('© '):
            skip_continuation = True
            continue
        if skip_continuation and ('publicly accessible website' in line or 'password-protected website' in line):
            skip_continuation = False
            continue
        skip_continuation = False
        # Do not discard standalone numbers. In unequal-size data tables the
        # PDF extractor often emits a final observation (for example "80") on
        # its own line. These are source data, not page numbers; deleting them
        # silently changes the problem and therefore its computed answer.
        lines.append(line)
    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def normalize_block(text: str) -> str:
    text = re.sub(r'\[\[PAGE:\d+\]\]', '', text)
    text = text.replace('NARRBEGIN:', '').replace('NARREND', '')
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_numbered(text: str, mode: str, chapter: int, page_marks: list[tuple[int, int]]) -> list[dict]:
    pattern = re.compile(r'(?m)^\s*(\d+)\.\s+')
    # Real question numbers are strictly sequential. This excludes decimal
    # values such as a line beginning "375." inside a data table.
    starts = []
    expected = 1
    for candidate in pattern.finditer(text):
        if int(candidate.group(1)) == expected:
            starts.append(candidate)
            expected += 1
    records = []
    for idx, match in enumerate(starts):
        number = int(match.group(1))
        end = starts[idx + 1].start() if idx + 1 < len(starts) else len(text)
        raw = normalize_block(text[match.end():end])
        if not raw:
            continue
        page_index = bisect.bisect_right([p[0] for p in page_marks], match.start()) - 1
        page = page_marks[max(0, page_index)][1]
        qid = f'ch{chapter}-{mode}-{number:03d}'
        records.append({
            'id': qid,
            'chapter': chapter,
            'section': 'Multiple Choice' if mode == 'mc' else 'Problem',
            'number': number,
            'page': page,
            'source': SOURCE_NAMES[chapter],
            'text': raw,
            'answerStatus': 'pending-verification',
            'answer': '',
            'explanation': '',
            'confidence': 'unverified',
        })
    return records


def parse_chapter(chapter: int, path: Path) -> list[dict]:
    pages = PdfReader(path).pages
    chunks = []
    page_marks = []
    offset = 0
    for index, page in enumerate(pages, 1):
        token = f'\n[[PAGE:{index}]]\n'
        chunk = token + clean_page(page.extract_text() or '')
        page_marks.append((offset, index))
        chunks.append(chunk)
        offset += len(chunk) + 1
    full = '\n'.join(chunks)
    problem_match = re.search(r'(?m)^\s*PROBLEM\s*$', full)
    if not problem_match:
        raise RuntimeError(f'No PROBLEM marker found in chapter {chapter}')
    mc_text = full[:problem_match.start()]
    problem_text = full[problem_match.end():]

    # Remove exhibit blocks before finding MC question starts, then attach the
    # exact matching exhibit to every "Refer to Exhibit" question.
    exhibits: dict[str, str] = {}
    exhibit_pattern = re.compile(r'NARRBEGIN:\s*(Exhibit\s+\d+[-–]\d+)(.*?)NARREND', re.S | re.I)
    for exhibit in exhibit_pattern.finditer(mc_text):
        block = normalize_block(exhibit.group(1) + exhibit.group(2))
        # Some source PDFs have a stale internal NARRBEGIN label (for example,
        # "Exhibit 12-01") followed by the correct visible label
        # ("Exhibit 14-1"). Index every label found in the block so the visible
        # question reference always resolves to its required table/equation.
        labels = re.findall(r'Exhibit\s+\d+[-–]\d+', block, re.I)
        for label in labels:
            normalized = re.sub(r'-(?:0+)(\d+)$', r'-\1', label.replace('–', '-').lower())
            exhibits[normalized] = block
    mc_without_exhibits = exhibit_pattern.sub('', mc_text)
    mc_marks = [(pos - sum(max(0, min(pos, m.end()) - m.start()) for m in exhibit_pattern.finditer(mc_text)), page)
                for pos, page in page_marks if pos < problem_match.start()]
    mc = split_numbered(mc_without_exhibits, 'mc', chapter, mc_marks or [(0, 1)])
    for record in mc:
        for old, new in MC_TEXT_REPAIRS.get((chapter, record['number']), []):
            if old not in record['text']:
                raise RuntimeError(
                    f"Chapter {chapter} MC {record['number']} text repair no longer matches source extraction"
                )
            record['text'] = record['text'].replace(old, new, 1)
        ref = re.search(r'Refer to\s+(Exhibit\s+\d+[-–]\d+)', record['text'], re.I)
        if ref:
            key = re.sub(r'-(?:0+)(\d+)$', r'-\1', ref.group(1).replace('–', '-').lower())
            record['exhibit'] = exhibits.get(key, '')
        else:
            record['exhibit'] = ''

    problem_page_marks = [(max(0, pos - problem_match.end()), page) for pos, page in page_marks if pos >= problem_match.end()]
    problems = split_numbered(problem_text, 'problem', chapter, problem_page_marks or [(0, 1)])
    for record in problems:
        record['exhibit'] = ''
        if chapter == 13 and record['number'] in CH13_TABLE_REPAIRS:
            old, new = CH13_TABLE_REPAIRS[record['number']]
            if old not in record['text']:
                raise RuntimeError(f"Chapter 13 problem {record['number']} table repair no longer matches source extraction")
            record['text'] = record['text'].replace(old, new, 1)
        if chapter == 14 and record['number'] in CH14_FORMULA_REPAIRS:
            old, new = CH14_FORMULA_REPAIRS[record['number']]
            if old not in record['text']:
                raise RuntimeError(f"Chapter 14 problem {record['number']} formula repair no longer matches source extraction")
            record['text'] = record['text'].replace(old, new, 1)
        if chapter == 15 and record['number'] in CH15_FORMULA_REPAIRS:
            old, new = CH15_FORMULA_REPAIRS[record['number']]
            if old not in record['text']:
                raise RuntimeError(f"Chapter 15 problem {record['number']} formula repair no longer matches source extraction")
            record['text'] = record['text'].replace(old, new, 1)
        if chapter == 16 and record['number'] in CH16_FORMULA_REPAIRS:
            for old, new in CH16_FORMULA_REPAIRS[record['number']]:
                if old not in record['text']:
                    raise RuntimeError(f"Chapter 16 problem {record['number']} formula repair no longer matches source extraction")
                record['text'] = record['text'].replace(old, new, 1)
        if chapter == 17 and record['number'] in CH17_FORMULA_REPAIRS:
            for old, new in CH17_FORMULA_REPAIRS[record['number']]:
                if old not in record['text']:
                    raise RuntimeError(f"Chapter 17 problem {record['number']} formula repair no longer matches source extraction")
                record['text'] = record['text'].replace(old, new, 1)
    return mc + problems


def main() -> None:
    records = []
    for chapter, path in FILES.items():
        records.extend(parse_chapter(chapter, path))
    out = Path(__file__).resolve().parents[1] / 'question-bank.js'
    payload = json.dumps(records, ensure_ascii=False, separators=(',', ':'))
    out.write_text('const FULL_QUESTIONS=' + payload + ';\n', encoding='utf-8')
    counts = {}
    for record in records:
        key = (record['chapter'], record['section'])
        counts[key] = counts.get(key, 0) + 1
    print(json.dumps({'total': len(records), 'counts': {f'{k[0]} {k[1]}': v for k, v in counts.items()}}, indent=2))


if __name__ == '__main__':
    main()
