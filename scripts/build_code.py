#!/usr/bin/env python3
"""애니메이션 카드용 코드 탭 데이터(data/code/dayNN.json) 생성.

사용: python scripts/build_code.py day01 day10   (또는 1 10)
- 노트북 실습 셀에서 Python 코드를 추출해 python/part/cells 필드만 다시 쓴다.
- 이미 있는 javascript·typescript 필드는 보존한다(사람이 쓴 참고용 변환 예시).
- 노트북에는 🎬 링크가 hash 기준으로 걸려 있어, hash → 셀 번호 연결표(MAP)를 아래에 둔다.
  근거: 노트북 markdown의 🎬 링크 위치, 없으면 data/dayNN.json road의 go/more Part, 그래도 없으면 제목 키워드.
"""
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE = "# 빈칸(___)은 실습 노트북에서 채워요"
MAX_LINES = 60

# day -> (노트북 glob, {hash: (part 설명, [셀 번호...])})  셀 번호는 노트북 전체 셀 기준(0부터)
MAP = {
    1: ("day01/D1_*_실습.ipynb", {
        "flow":     ("Part 1 환경 확인 + Part 6 비서 · 근거: 제목 키워드", [5, 48]),
        "tech":     ("Part 2 TTS + Part 5 ASR · 근거: 제목 키워드", [16, 33]),
        "stack":    ("Part 1 · 개발환경 확인", [3, 5, 7]),
        "file":     ("Part 2 · TTS와 16kHz WAV 변환", [15, 16]),
        "sampling": ("Part 3 · 소리 눈으로 보기", [23, 26]),
        "mic":      ("Part 4 · 내 목소리 녹음", [29]),
        "asr":      ("Part 5 · ASR 받아쓰기와 RTF", [33]),
        "cer":      ("Part 5 · CER 계산", [38, 40]),
        "agent":    ("Part 6 · 음성 비서", [46, 52]),
    }),
    10: ("day10/D10_*_실습.ipynb", {
        "flow":     ("Part 0 준비 + Part 5 묶기 · 근거: 제목 키워드", [3, 54]),
        "editdist": ("Part 1 · 편집 거리 표", [9]),
        "wercer":   ("Part 1 · WER · CER 직접 계산", [9, 12]),
        "norm":     ("Part 2 · 정규화", [22, 25]),
        "numbers":  ("Part 2 · 숫자 읽기", [22]),
        "pipeline": ("Part 3 · 회의록 파이프라인", [32, 34]),
        "prompt":   ("Part 4 · LLM 프롬프트와 JSON", [40, 44]),
        "eval":     ("Part 5 · 평가표", [51]),
        "demo":     ("Part 5 · Gradio 데모", [56]),
    }),
}


def names_of(item):
    """import 항목 하나에서 코드가 쓰는 이름을 돌려준다."""
    item = item.strip()
    if " as " in item:
        return item.split(" as ")[1].strip()
    return item


def used(name, body):
    return re.search(r"(?<![\w.])" + re.escape(name) + r"(?![\w])", body) is not None


def collect_imports(cells, first, body):
    """first 셀보다 앞쪽 코드 셀의 import 중 body가 쓰는 항목만 모은다(중복 제거)."""
    found, seen = [], set()
    have = set()  # 선택 셀 안에서 이미 import한 이름은 다시 붙이지 않는다
    for line in body.split("\n"):
        m = re.match(r"^(?:import (.+)|from \S+ import (.+))$", line)
        if m:
            have |= {names_of(it) for it in (m.group(1) or m.group(2)).split(",")}
    for src in cells[:first]:
        for line in src.split("\n"):
            m = re.match(r"^import (.+)$", line)
            f = re.match(r"^from (\S+) import (.+)$", line)
            if m:
                for it in m.group(1).split(","):
                    n = names_of(it)
                    key = "import " + it.strip()
                    if (used(n, body) or ("." in n and n in body)) and key not in seen and n not in have:
                        seen.add(key)
                        found.append(key)
            elif f:
                for it in f.group(2).split(","):
                    n = names_of(it)
                    key = f"from {f.group(1)} import {it.strip()}"
                    if used(n, body) and key not in seen and n not in have:
                        seen.add(key)
                        found.append(key)
    # 같은 모듈의 from-import는 한 줄로 합친다
    merged, order = {}, []
    for k in found:
        if k.startswith("from "):
            _, mod, _, name = k.split(" ", 3)
            if mod not in merged:
                merged[mod] = []
                order.append(("from", mod))
            merged[mod].append(name)
        else:
            order.append(("imp", k))
    out = []
    for kind, v in order:
        out.append(f"from {v} import {', '.join(merged[v])}" if kind == "from" else v)
    # import a, import b → import a, b
    plain = [x[7:] for x in out if x.startswith("import ")]
    rest = [x for x in out if not x.startswith("import ")]
    return (["import " + ", ".join(plain)] if plain else []) + rest


def comment_magics(code):
    return "\n".join(("# " + l) if re.match(r"^\s*[!%]", l) else l for l in code.split("\n"))


def build(day):
    pat, table = MAP[day]
    nb = json.load(open(next(iter(glob.glob(str(ROOT / pat)))), encoding="utf-8"))
    cells = [("".join(c["source"]) if c["cell_type"] == "code" else "") for c in nb["cells"]]
    out_path = ROOT / "data" / "code" / f"day{day:02d}.json"
    old = json.load(open(out_path, encoding="utf-8")) if out_path.exists() else {}
    anims = [a["hash"] for a in json.load(open(ROOT / "data" / f"day{day:02d}.json", encoding="utf-8"))["anims"]]
    res = {}
    for h in anims:
        part, idx = table[h]
        for i in idx:
            if not cells[i].strip():
                sys.exit(f"day{day} {h}: 셀 {i}은 코드 셀이 아니에요")
        body = "\n\n".join(comment_magics(cells[i]).strip("\n") for i in idx)
        imps = collect_imports(cells, idx[0], body)
        imps = [l for l in imps if l not in body.split("\n")]
        head = [NOTE] if "___" in body else []
        code = "\n".join(head + imps + ([""] if imps else []) + [body])
        n = code.count("\n") + 1
        if n > MAX_LINES:
            print(f"경고 day{day} {h}: {n}줄 (>{MAX_LINES})")
        prev = old.get(h, {})
        res[h] = {
            "part": part,
            "cells": idx,
            "python": code,
            "javascript": prev.get("javascript", ""),
            "typescript": prev.get("typescript", ""),
        }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(out_path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(f"day{day:02d}: {len(res)}개 → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    args = sys.argv[1:] or ["day01", "day10"]
    for a in args:
        build(int(re.sub(r"\D", "", a)))
