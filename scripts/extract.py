#!/usr/bin/env python3
"""원본 dayNN/ 에서 대시보드용 data/dayNN.json, data/course.json 을 만든다.

사용: python scripts/extract.py 1 10   (인자 = 변환할 일차. course.json의 ready 표시 대상)
표준 라이브러리만 사용. 원본은 읽기만 한다. 계약: docs/PLAN.md#7
"""
import glob
import json
import os
import re
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPO = "DevOps0906/AI_Voice"
KIND = {".pdf": "pdf", ".pptx": "pptx", ".ipynb": "ipynb", ".html": "html"}
IMG = re.compile(r"!\[[^\]]*\]\(data:[^)]*\)")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def plain(s):
    return s.replace("**", "").strip()


# ---------- JS 리터럴 -> Python ----------
def literal_end(s, i):
    """s[i]가 [ 또는 { 일 때 짝이 맞는 닫는 괄호 다음 위치(문자열 인식)."""
    depth, q, j = 0, None, i
    while j < len(s):
        c = s[j]
        if q:
            if c == "\\":
                j += 1
            elif c == q:
                q = None
        elif c in "'\"`":
            q = c
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ValueError("unbalanced literal")


def js_to_py(src):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in "'\"":
            j, buf = i + 1, []
            while src[j] != c:
                if src[j] == "\\":
                    buf.append(src[j:j + 2])
                    j += 2
                    continue
                buf.append(src[j])
                j += 1
            raw = "".join(buf)
            if c == "'":
                raw = raw.replace("\\'", "'").replace('"', '\\"')
            out.append('"' + raw + '"')
            i = j + 1
        elif c.isalpha() or c == "_":
            j = i
            while j < n and (src[j].isalnum() or src[j] == "_"):
                j += 1
            word = src[i:j]
            k = j
            while k < n and src[k] in " \t\r\n":
                k += 1
            if k < n and src[k] == ":":
                out.append('"%s"' % word)
            else:
                out.append(word)  # true/false/null
            i = j
        else:
            out.append(c)
            i += 1
    text = re.sub(r",(\s*[\]}])", r"\1", "".join(out))
    return json.loads(text)


def js_const(text, name):
    m = re.search(r"const\s+%s\s*=\s*" % re.escape(name), text)
    if not m:
        raise ValueError("const %s not found" % name)
    start = m.end()
    return text[start:literal_end(text, start)]


# ---------- 노트북 ----------
def notebook_md(day):
    path = glob.glob(os.path.join(ROOT, "day%02d" % day, "*_실습.ipynb"))[0]
    with open(path, encoding="utf-8") as f:
        nb = json.load(f)
    cells = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "markdown"]
    return IMG.sub("", "\n\n".join(cells))


def section(md, heading_re):
    """heading_re 에 맞는 제목 줄 다음부터 다음 ##/###/--- 직전까지."""
    m = re.search(r"^#{2,3} " + heading_re + r".*$", md, re.M)
    if not m:
        return ""
    rest = md[m.end():]
    e = re.search(r"^(#{2,3} |---\s*$)", rest, re.M)
    return rest[:e.start()] if e else rest


def numbered(block):
    return [plain(x) for x in re.findall(r"^\d+\.\s+(.*\S)\s*$", block, re.M)]


def table_rows(block):
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows[1:]  # 머리글 제외


def parse_notebook(day):
    md = notebook_md(day)
    lines = md.splitlines()
    h1 = re.match(r"# D\d+\.\s*(.+)", lines[0])
    title = h1.group(1).strip()
    metaline = next(l for l in lines[1:8] if "주차" in l)
    wm = re.search(r"(\d+)주차\s+(M\d+)", metaline)
    hm = re.search(r"(\d+)시간", metaline)
    tm = re.search(r"시간\s*[|·]\s*(.+?)\**\s*$", metaline)
    meta = {
        "week": int(wm.group(1)),
        "module": wm.group(2),
        "hours": int(hm.group(1)),
        "tag": tm.group(1).strip() if tm else "",
    }
    periods = []
    for r in table_rows(section(md, r"오늘의 실습 흐름")):
        n = re.match(r"(\d+)교시", r[0])
        if n and len(r) >= 3:
            periods.append({"n": int(n.group(1)), "topic": plain(r[1]), "parts": plain(r[2])})
    parts = [{"n": int(n), "title": t.strip()}
             for n, t in re.findall(r"^## Part (\d+)\.\s*(.+)$", md, re.M)]
    blanks = 0
    for head in re.findall(r"^### 🧩 빈칸 실습 ([^:\n]+)", md, re.M):
        blanks += len(re.findall(r"\d+", head))
    learned = []
    for r in table_rows(section(md, r"오늘 배운 것")):
        learned.append({
            "concept": plain(r[0]),
            "summary": plain(r[1]),
            "code": r[2].replace("`", "").strip() if len(r) > 2 else "",
        })
    if not learned:  # D15형: '오늘 한 것' 표(단계·한 일·배운 날·코드)
        for r in table_rows(section(md, r"오늘 한 것")):
            if len(r) >= 4:
                learned.append({"concept": plain(r[0]), "summary": plain(r[1]),
                                "code": r[3].replace("`", "").strip()})
    if not learned:  # D25형: 'N주차 돌아보기' 표(날·배운 것·쓴 곳)
        for r in table_rows(section(md, r"\d+주차 돌아보기")):
            if len(r) >= 3:
                learned.append({"concept": plain(r[0]), "summary": plain(r[1]),
                                "code": r[2].replace("`", "").strip()})
    return {
        "title": title,
        "meta": meta,
        "goals": numbered(section(md, r"(?:학습|프로젝트) 목표")),
        "periods": periods,
        "parts": parts,
        "blanks": blanks,
        "learned": learned,
        "homework": numbered(section(md, r"📝 과제")),
        "checks": [plain(x) for x in re.findall(
            r"^[-*]\s+\[[ xX]\]\s+(.*\S)\s*$", section(md, r"✅ 오늘의 확인"), re.M)],
    }


# ---------- animation.html ----------
def parse_anims(day, html):
    tabs = re.findall(r'<button[^>]*data-t="(\w+)"[^>]*>(.*?)</button>', html, re.S)
    hm = re.search(r"const\s+HASH\s*=\s*(\{.*?\});", html, re.S)
    hash_map = js_to_py(hm.group(1)) if hm else None  # {hash: tabId}
    inv = {v: k for k, v in hash_map.items()} if hash_map else {}
    anims = []
    for tid, label in tabs:
        title = re.sub(r"<span[^>]*>.*?</span>", "", label, flags=re.S)
        title = re.sub(r"<[^>]+>", "", title).strip()
        anims.append({"hash": inv.get(tid, tid), "title": title, "desc": ""})
    return anims, inv


def parse_road(html, inv):
    road = []
    for r in js_to_py(js_const(html, "ROAD")):
        item = {"p": r["p"], "t": r["t"], "c": r["c"], "go": inv.get(r["go"], r["go"]),
                "items": r["items"], "q": r["q"]}
        more = []
        for k in ("more", "more2"):  # 값은 [[hash,label],...] 또는 D7형 단일 [hash,label]
            v = r.get(k)
            if v:
                more += [v] if isinstance(v[0], str) else v
        if more:
            item["more"] = [{"hash": m[0], "label": m[1]} for m in more]
        road.append(item)
    return road


# ---------- worksheet.html ----------
def norm_q(q):
    """D1 원본 키를 D10 형식(ty·p·o·a·w, match left/right, order steps)으로."""
    if "ty" in q:  # D35~44: 이미 D10 형식
        return q
    n = {"ty": q["t"], "p": q["q"]}
    for k, v in q.items():
        if k in ("t", "q", "p"):
            continue
        n[{"e": "w", "l": "left", "r": "right", "items": "steps", "calc": "hint"}.get(k, k)] = v
    if q["t"] == "match":
        n["a"] = list(range(len(q["l"])))  # 원본은 l[i]-r[i] 정렬
    elif q["t"] == "order":
        n["a"] = list(range(len(q["items"])))  # 원본 items는 정답 순서
    return n


def parse_worksheet(day, html):
    src = "day%02d/worksheet.html" % day
    raw = js_to_py(js_const(html, "Q"))
    if raw and "qs" in raw[0]:  # D10 형식: 교시별 그룹
        groups = [{"title": g["t"], "anim": g.get("anim", ""), "qs": g["qs"]} for g in raw]
    elif raw and "ty" in raw[0]:  # D35~44: 교시 구분 없는 평면 목록 -> 한 그룹
        groups = [{"title": "전체", "qs": raw}]
    else:  # D1 형식: Part별
        groups, idx = [], {}
        for q in raw:
            if q["p"] not in idx:
                idx[q["p"]] = len(groups)
                groups.append({"title": q["p"], "qs": []})
            groups[idx[q["p"]]]["qs"].append(norm_q(q))
    return {"source": src, "groups": groups}


# ---------- 파일 ----------
def pdf_pages(path):
    try:
        with open(path, "rb") as f:
            n = len(re.findall(rb"/Type\s*/Page(?![s\w])", f.read()))
        return n or None
    except OSError:
        return None


def parse_files(day):
    d = "day%02d" % day
    files = []
    for name in sorted(os.listdir(os.path.join(ROOT, d))):
        path = os.path.join(ROOT, d, name)
        kind = KIND.get(os.path.splitext(name)[1].lower())
        if not kind or not os.path.isfile(path):
            continue
        rel = "%s/%s" % (d, quote(name))
        files.append({
            "name": name,
            "kind": kind,
            "size": os.path.getsize(path),
            "url": "https://github.com/%s/blob/main/%s" % (REPO, rel),
            "colab": ("https://colab.research.google.com/github/%s/blob/main/%s" % (REPO, rel))
            if kind == "ipynb" else None,
            "pages": pdf_pages(path) if kind == "pdf" else None,
        })
    return files


# ---------- 조립 ----------
def build_day(day):
    nb = parse_notebook(day)
    d = os.path.join(ROOT, "day%02d" % day)
    anim_html = read(os.path.join(d, "animation.html"))
    anims, inv = parse_anims(day, anim_html)
    ws = parse_worksheet(day, read(os.path.join(d, "worksheet.html")))
    learned = nb["learned"]
    homework, extra = nb["homework"], {}
    if not learned and day >= 36:  # D36~44: 배운 것 절 없음 -> 마지막 Part '정리' 표
        md = notebook_md(day)
        m = list(re.finditer(r"^## Part \d+\. 정리", md, re.M))
        for r in table_rows(section(md[m[-1].start():], r"Part \d+\. 정리") if m else ""):
            if 2 <= len(r) <= 3:
                learned.append({"concept": plain(r[0]), "summary": plain(r[1]),
                                "code": r[2].replace("`", "").strip() if len(r) > 2 else ""})
        if learned:
            extra["learnedSource"] = "정리 표"
    if not homework and nb["checks"]:  # D29~44: 과제 절 없음 -> 오늘의 확인 체크리스트
        homework = nb["checks"]
        extra["homeworkSource"] = "오늘의 확인"
    return dict({
        "day": day,
        "title": nb["title"],
        "meta": nb["meta"],
        "goals": nb["goals"],
        "periods": nb["periods"],
        "parts": nb["parts"],
        "blanks": nb["blanks"],
        "anims": anims,
        "road": parse_road(anim_html, inv),
        "learned": learned,
        "homework": homework,
        "worksheet": ws,
        "files": parse_files(day),
    }, **extra)


def course_entry(day, ready):
    md = notebook_md(day)
    first = md.splitlines()[0]
    title = re.match(r"# D\d+\.\s*(.+)", first).group(1)
    title = re.split(r":| — ", title, maxsplit=1)[0].strip()
    meta = parse_notebook_meta(md)
    return {"day": day, "week": meta[0], "module": meta[1], "title": title, "ready": ready}


def parse_notebook_meta(md):
    line = next(l for l in md.splitlines()[1:8] if "주차" in l)
    m = re.search(r"(\d+)주차\s+(M\d+)", line)
    return int(m.group(1)), m.group(2)


def dump(path, obj):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def warnings(obj):
    w = [k for k in ("goals", "parts", "learned", "homework") if not obj[k]]
    if not obj["blanks"]:
        w.append("blanks")
    return w


def report(rows):
    out = ["# 추출 보고 (scripts/extract.py all)", "",
           "| 일차 | goals | parts | blanks | learned | homework | 퀴즈 | anims | road | 경고 |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for day, c, w in rows:
        if c is None:
            out.append("| D%d | 실패 | | | | | | | | %s |" % (day, w))
            continue
        extra = ["빈 필드: " + ", ".join(w)] if w else []
        if c[6] != 9:
            extra.append("anims %d (9 아님)" % c[6])
        if c[5] == 0:
            extra.append("퀴즈 0")
        out.append("| D%d | %s | %s |" % (day, " | ".join(str(x) for x in c), "; ".join(extra) or "-"))
    out += ["", "## 원인·분기 메모",
            "- D1~34 anims 9개·퀴즈 있음. D35~44는 worksheet `Q`가 이미 D10 형식(`ty`)의 평면 목록(25문항, `an` 필드 포함)이라 교시 구분 없이 그룹 하나(title `전체`)로 담는다.",
            "- D29~44: 노트북에 `빈칸 실습`·`오늘 배운 것`·`과제` 절이 없어 blanks는 0이다(원본 구조 차이). D36~44는 마지막 Part `정리` 표를 learned로 읽고 `learnedSource`(값 정리 표)를 적는다(2~3열은 concept·summary·code 순). D29~35 learned는 0 유지. homework는 `오늘의 확인` 체크리스트가 있는 D29~35만 채우고 JSON에 `homeworkSource`를 적는다. D36~44는 그 절이 없고 Part 5 정리 표만 있어 homework가 비어 있다.",
            "- D15: 학습 목표 대신 `프로젝트 목표` 절, 배운 것 대신 `오늘 한 것` 표를 learned로 사용. D25: `5주차 돌아보기` 표를 learned로 사용.",
            "- D7: ROAD의 `more`가 단일 쌍·`more2` 추가 쌍이라 `more` 배열로 합쳤다.",
            "- 빈칸 실습 제목은 콜론이 없는 경우(D24 등)도 센다."]
    path = os.path.join(ROOT, "docs", "extract-report.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")


def main(argv):
    days = list(range(1, 45)) if argv == ["all"] else [int(a) for a in argv] or [1, 10]
    os.makedirs(DATA, exist_ok=True)
    rows, ok = [], []
    for day in days:
        try:
            obj = build_day(day)
        except Exception as e:  # 한 일차 실패가 전체를 막지 않게
            print("day%02d: FAIL %s: %s" % (day, type(e).__name__, e))
            rows.append((day, None, "%s: %s" % (type(e).__name__, e)))
            continue
        dump(os.path.join(DATA, "day%02d.json" % day), obj)
        ok.append(day)
        qn = sum(len(g["qs"]) for g in obj["worksheet"]["groups"])
        print("day%02d: goals %d parts %d blanks %d learned %d homework %d quiz %d "
              "periods %d anims %d road %d files %d" % (
                  day, len(obj["goals"]), len(obj["parts"]), obj["blanks"], len(obj["learned"]),
                  len(obj["homework"]), qn, len(obj["periods"]), len(obj["anims"]),
                  len(obj["road"]), len(obj["files"])))
        rows.append((day, (len(obj["goals"]), len(obj["parts"]), obj["blanks"], len(obj["learned"]),
                           len(obj["homework"]), qn, len(obj["anims"]), len(obj["road"])),
                     warnings(obj)))
    course = [course_entry(d, d in ok) for d in range(1, 45)]
    dump(os.path.join(DATA, "course.json"), course)
    print("course.json: %d days, ready=%s" % (len(course), [c["day"] for c in course if c["ready"]]))
    if argv == ["all"]:
        report(rows)
        return 0 if len(ok) == len(days) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
