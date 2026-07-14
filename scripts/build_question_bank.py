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
        if re.fullmatch(r'\s*\d+\s*', line):
            # Standalone PDF page number; table rows contain more than one value.
            continue
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
        exhibits[exhibit.group(1).replace('–', '-').lower()] = normalize_block(exhibit.group(1) + exhibit.group(2))
    mc_without_exhibits = exhibit_pattern.sub('', mc_text)
    mc_marks = [(pos - sum(max(0, min(pos, m.end()) - m.start()) for m in exhibit_pattern.finditer(mc_text)), page)
                for pos, page in page_marks if pos < problem_match.start()]
    mc = split_numbered(mc_without_exhibits, 'mc', chapter, mc_marks or [(0, 1)])
    for record in mc:
        ref = re.search(r'Refer to\s+(Exhibit\s+\d+[-–]\d+)', record['text'], re.I)
        if ref:
            key = ref.group(1).replace('–', '-').lower()
            record['exhibit'] = exhibits.get(key, '')
        else:
            record['exhibit'] = ''

    problem_page_marks = [(max(0, pos - problem_match.end()), page) for pos, page in page_marks if pos >= problem_match.end()]
    problems = split_numbered(problem_text, 'problem', chapter, problem_page_marks or [(0, 1)])
    for record in problems:
        record['exhibit'] = ''
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
