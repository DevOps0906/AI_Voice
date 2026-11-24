#!/usr/bin/env python3
"""개념 정리 데이터(data/concepts/dayNN.json) 생성 + 리포트(docs/reports/concepts-report.md).

사용: python scripts/build_concepts.py all   (또는 1 10 …)
- 입력: dayNN/*_실습.ipynb(강사용 제외), dayNN/*_slides.pdf(PyMuPDF), data/dayNN.json(parts·learned)
- 출력: {day, title, parts:[{n, title, notes:[{t:md|code, s}], slides:[{page, title, points}]}], glossary}
"""
import glob
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "concepts"
IMG_NOTE = "(그림: 노트북 참고)"
MAX_CODE_LINES = 15
MAX_POINTS = 8
MAX_POINT_LEN = 200

PART_RE = re.compile(r"^##\s+Part\s+(\d+)", re.M)


def clean_md(s):
    """마크다운 셀 정리. 비면 ''."""
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    # 이미지(data:, attachment:, 외부 링크 모두) -> 자리표시
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", IMG_NOTE, s)
    s = re.sub(r"<img\b[^>]*>", IMG_NOTE, s, flags=re.I)
    # <details> 래퍼 벗기기, summary는 굵은 줄로
    s = re.sub(r"<summary>\s*(.*?)\s*</summary>", r"**\1**\n", s, flags=re.S | re.I)
    s = re.sub(r"</?details[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    # 남은 HTML 장식 태그 제거(코드·수식의 부등호는 건드리지 않도록 태그 이름을 한정)
    s = re.sub(r"</?(div|span|p|center|font|b|i|u|table|tr|td|th|thead|tbody|style|svg|a)\b[^>]*>", "", s, flags=re.I)
    s = re.sub(rf"({re.escape(IMG_NOTE)}\s*)+", IMG_NOTE + "\n\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s).strip()
    s = re.sub(r"^(---\s*\n)+", "", s).strip()
    return s


def drop_md(raw):
    """통째로 버릴 markdown 셀(빈칸 안내, 정답, 힌트, 과제 체크)."""
    head = raw.strip()[:200]
    if re.match(r"#{1,4}\s*🧩", head):
        return True
    if "<details" in raw and re.search(r"정답|힌트", raw.split("</summary>")[0]):
        return True
    if re.match(r"#{1,4}\s*.*(과제 체크|제출 체크|체크리스트)", head):
        return True
    return False


def drop_code(src):
    """노트북 도우미·빈칸 코드 셀은 예시로 쓰지 않는다."""
    if not src.strip():
        return True
    if "____" in src or "🧩" in src or "✍️" in src or "채점 도우미" in src:
        return True
    if "data:image" in src or "base64," in src:
        return True
    if re.match(r"\s*(!pip|%pip)", src):
        return True
    return False


def build_notes(cells):
    """Part n -> notes 블록 리스트."""
    notes = {}
    cur = None
    skip_code = False
    for c in cells:
        src = "".join(c["source"])
        if c["cell_type"] == "markdown":
            m = PART_RE.search(src)
            if m:
                cur = int(m.group(1))
                notes.setdefault(cur, [])
                # Part 제목 줄과 그 앞의 --- 만 제거
                src = src[m.start():]
                src = src.split("\n", 1)[1] if "\n" in src else ""
            if cur is None:
                skip_code = True
                continue
            if drop_md(src):
                skip_code = True
                continue
            txt = clean_md(src)
            if not txt:
                skip_code = True
                continue
            notes[cur].append({"t": "md", "s": txt})
            skip_code = False
        elif c["cell_type"] == "code" and cur is not None:
            # 설명 바로 뒤 코드 셀만(markdown 뒤 첫 코드 셀)
            if skip_code or not notes[cur] or notes[cur][-1]["t"] != "md":
                continue
            if drop_code(src):
                continue
            lines = src.rstrip().split("\n")[:MAX_CODE_LINES]
            notes[cur].append({"t": "code", "s": "\n".join(lines)})
            skip_code = True
    return notes


NOISE = re.compile(r"^(음성 AI 전문가 과정 · Day \d+.*|\d{1,3}|▶ 애니메이션.*|)$")


D1_SECTION = {1: 0, 2: 0, 3: 1, 4: 2, 5: 5, 6: 6}


def build_slides(pdf_path, part_nums, day=0):
    """part n -> slides 리스트. 못 배정하면 첫 Part."""
    out = {}
    doc = pymupdf.open(pdf_path)
    first, last = part_nums[0], part_nums[-1]
    for i, page in enumerate(doc):
        pno = i + 1
        if pno == 1:
            continue  # 표지
        lines = [ln.strip() for ln in page.get_text().split("\n")]
        lines = [ln for ln in lines if not NOISE.match(ln)]
        if not lines:
            continue
        title, rest = lines[0], lines[1:]
        m = re.match(r"^(\d+)(?:\.\d+)?\s*·\s*(.*)$", title)
        if m:
            n = int(m.group(1))
            if not m.group(2).strip() and rest:  # 제목이 줄바꿈으로 갈린 경우
                title = f"{title.split('·')[0].strip()} · {rest[0]}"
                rest = rest[1:]
            if day <= 3 and n == day:  # D1~D3 슬라이드는 "일차.절" 번호를 쓴다
                sec = int(re.match(r"^\d+\.(\d+)", title).group(1)) if re.match(r"^\d+\.\d+", title) else 0
                if day == 1:
                    sec = D1_SECTION.get(sec, 0)
                    if sec == 2 and re.search(r"소리 눈으로|샘플 수", title):
                        sec = 3
                n = sec
            part = n if n in part_nums else first
        elif title.startswith("정리") or title.startswith("다음 시간"):
            part = last
        else:
            part = first
        pts, seen = [], set()
        for ln in rest:
            ln = ln[:MAX_POINT_LEN]
            if ln in seen:
                continue
            seen.add(ln)
            pts.append(ln)
            if len(pts) >= MAX_POINTS:
                break
        out.setdefault(part, []).append({"page": pno, "title": title, "points": pts})
    return out


def find_one(pattern):
    hits = [p for p in glob.glob(pattern) if "강사용" not in p]
    return hits[0] if hits else None


def build_day(d):
    day = f"day{d:02d}"
    dj = json.load(open(ROOT / "data" / f"{day}.json", encoding="utf-8"))
    nb_path = find_one(str(ROOT / "Edu" / day / "*_실습.ipynb"))
    pdf_path = find_one(str(ROOT / "Edu" / day / "*_slides.pdf"))
    nb = json.load(open(nb_path, encoding="utf-8"))
    notes = build_notes(nb["cells"])
    nums = [p["n"] for p in dj["parts"]]
    slides = build_slides(pdf_path, nums, d)
    parts = []
    for p in dj["parts"]:
        parts.append({
            "n": p["n"],
            "title": p["title"],
            "notes": notes.get(p["n"], []),
            "slides": slides.get(p["n"], []),
        })
    data = {"day": d, "title": dj["title"], "parts": parts, "glossary": dj.get("learned", [])}
    OUT.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (OUT / f"{day}.json").write_text(text, encoding="utf-8")
    pages = len(pymupdf.open(pdf_path))
    nblocks = sum(len(p["notes"]) for p in parts)
    nslides = sum(len(p["slides"]) for p in parts)
    chars = sum(len(b["s"]) for p in parts for b in p["notes"]) + sum(
        len(s["title"]) + sum(len(x) for x in s["points"]) for p in parts for s in p["slides"])
    empty = [p["n"] for p in parts if not p["notes"]]
    return {
        "day": d, "parts": len(parts), "blocks": nblocks, "slides": nslides, "pages": pages,
        "chars": chars, "kb": len(text.encode("utf-8")) / 1024,
        "b64": len(re.findall(r"data:image|attachment:|[A-Za-z0-9+/=]{200,}", text)),
        "empty": empty,
    }


def write_report(rows):
    L = ["# 개념 정리 추출 리포트", "",
         "`python scripts/build_concepts.py all`이 만든다. 이미지는 `(그림: 노트북 참고)`로 대체했고, 일차 JSON 크기 목표는 150KB 이하다.", "",
         "| 일차 | Part | notes 블록 | slides 쪽(PDF 쪽수) | 글자 수 | 크기(KB) | base64 | notes 없는 Part |",
         "|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in rows:
        L.append(f"| {r['day']} | {r['parts']} | {r['blocks']} | {r['slides']} ({r['pages']}) | {r['chars']} | "
                 f"{r['kb']:.1f} | {r['b64']} | {','.join(map(str, r['empty'])) or '-'} |")
    over = [r["day"] for r in rows if r["kb"] > 150]
    L += ["", f"- 일차 수: {len(rows)}",
          f"- base64 덩어리(data:image·attachment:·영숫자 200자 이상) 잔존 합계: {sum(r['b64'] for r in rows)}",
          f"- 150KB 초과 일차: {', '.join(map(str, over)) or '없음'}",
          f"- 최대 크기: {max(r['kb'] for r in rows):.1f}KB"]
    (ROOT / "docs" / "reports").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs" / "reports" / "concepts-report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    days = list(range(1, 45)) if argv[0] == "all" else [int(re.sub(r"\D", "", a)) for a in argv]
    rows = [build_day(d) for d in days]
    if argv[0] == "all":
        write_report(rows)
    for r in rows:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
