#!/usr/bin/env python3
"""data/code/dayNN.json 을 훑어 data/code/index.json 을 만든다: {"1":["flow","tech",...], ...}
애니메이션 페이지 코드 상자가 파일이 있는 일차만 fetch 하도록 쓴다(404 방지). 표준 라이브러리만 사용.
사용: python scripts/build_code_index.py
"""
import glob
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data", "code")


def main():
    idx = {}
    for p in sorted(glob.glob(os.path.join(D, "day*.json"))):
        m = re.fullmatch(r"day(\d+)\.json", os.path.basename(p))
        if not m:
            continue
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        idx[str(int(m.group(1)))] = [k for k, v in data.items() if isinstance(v, dict) and (v.get("python") or v.get("typescript"))]
    with open(os.path.join(D, "index.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(idx, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("index.json: %d일차 (%s)" % (len(idx), ", ".join("D" + k for k in idx)))


if __name__ == "__main__":
    main()
