#!/usr/bin/env python3
"""애니메이션 카드용 코드 데이터(data/code/dayNN.json) 생성·관리.

코드 정본은 data/code/dayNN.json 이다. 각 hash 항목:
  part · nb · ord   근거가 된 실습 노트북 Part와 Colab 코드 셀 순번(아래 MAP)
  python            단독 실행 완성 코드 (Python 3.11, 맨 위 `# pip install a==x` 줄)
  typescript        단독 실행 완성 코드 (Node 26 `node --experimental-strip-types x.ts`, Node 내장만)
  libs              {python:[...], typescript:[...]} 사용 라이브러리 정리(이 파일이 코드에서 다시 계산)

사용:
  python scripts/build_code.py day01 day10                 메타(part·nb·ord)와 libs만 다시 계산
  python scripts/build_code.py day01 day10 --src DIR       DIR/py/dNN_<hash>.py · DIR/ts/dNN_<hash>.ts를 읽어 코드 교체
  python scripts/build_code.py day01 day10 --export DIR    JSON의 코드를 DIR/py · DIR/ts 파일로 꺼냄(고친 뒤 --src로 되돌림)
실행 검사는 scripts/run_code.py.

MAP · NOTEBOOK에 없는 일차(D2~)는 scripts/code_map/dayNN.json 에서 읽는다(일차마다 파일이 따로라 병렬 작업해도 안 겹친다):
  {"notebook": "day02/D2_*_실습.ipynb",
   "map": {hash: [Part 설명, [노트북 셀 번호...]]},
   "py_libs": {import 이름: [pip 이름, 용도, 문서, 라이선스]},     그 일차에서만 PY_LIBS보다 우선
   "ts_libs": [[코드에서 찾을 정규식, 이름, 용도, 문서]]}          그 일차에서만 적용: 이름이 TS_LIBS와 같으면 대신하고, 새 이름은 뒤에 더함
"""
import argparse
import glob
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# day -> 화면에 보여 줄 노트북 glob (빈칸 없는 실습 노트북, 강사용은 쓰지 않음)
NOTEBOOK = {1: "day01/D1_*_실습.ipynb", 10: "day10/D10_*_실습.ipynb"}

# day -> {hash: (Part 설명, [근거 노트북 셀 번호(0부터)...])}  ord(코드 셀 순번)를 계산하는 데만 쓴다
MAP = {
    1: {
        "flow":     ("Part 1~6 · 오늘의 흐름 전체", [3, 5, 7, 9, 11, 15, 16, 18, 20, 23, 26, 29, 31, 32, 33, 35, 38, 40, 43, 45, 46, 48, 49, 52]),
        "tech":     ("Part 2 · TTS + Part 5 · ASR", [15, 16, 18, 20, 31, 32, 33, 35, 38, 40, 43]),
        "stack":    ("Part 1 · 개발환경 확인 및 설치", [3, 5, 7, 9, 11]),
        "file":     ("Part 2 · TTS 맛보기: 글자 → 소리", [15, 16, 18, 20]),
        "sampling": ("Part 3 · 소리 눈으로 보기", [23, 26]),
        "mic":      ("Part 4 · 내 목소리 녹음하기", [29]),
        "asr":      ("Part 5 · ASR 받아쓰기와 RTF", [31, 32, 33, 35]),
        "cer":      ("Part 5 · CER 계산", [38, 40, 43]),
        "agent":    ("Part 6 · 미니 음성 비서", [45, 46, 48, 49, 52]),
    },
    10: {
        "flow":     ("Part 0~5 · 오늘의 흐름 전체", [2, 3, 5, 6, 9, 12, 16, 18, 22, 25, 28, 31, 32, 34, 37, 40, 42, 44, 47, 51, 54, 56]),
        "editdist": ("Part 1 · 편집 거리 표", [9]),
        "wercer":   ("Part 1 · WER · CER", [9, 12]),
        "norm":     ("Part 2 · jiwer와 한국어 정규화", [16, 18, 22, 25, 28]),
        "numbers":  ("Part 2 · 숫자 읽기", [22]),
        "pipeline": ("Part 3 · 회의록 파이프라인 조립", [31, 32, 34, 37]),
        "prompt":   ("Part 4 · LLM으로 요약 · 결정 사항 · 할 일", [40, 42, 44, 47]),
        "eval":     ("Part 5 · 평가표", [51]),
        "demo":     ("Part 5 · 하나로 묶기 + 데모 화면", [54, 56]),
    },
}

# 라이브러리 정보. version은 코드 맨 위 `# pip install 이름==버전` 줄에서 읽는다(검사용 venv의 실제 설치 버전).
# import 이름 -> (pip 이름, 용도, 문서, 라이선스)
PY_LIBS = {
    "faster_whisper": ("faster-whisper", "음성 → 글자 받아쓰기(Whisper, tiny 모델)", "https://github.com/SYSTRAN/faster-whisper", "MIT"),
    "ctranslate2":    ("ctranslate2", "faster-whisper 추론 엔진 · GPU(CUDA) 수 확인", "https://opennmt.net/CTranslate2/", "MIT"),
    "edge_tts":       ("edge-tts", "글자 → 음성 합성(인터넷 필요, 안 되면 합성 신호)", "https://github.com/rany2/edge-tts", "LGPL-3.0"),
    "librosa":        ("librosa", "오디오 읽기 · 16kHz 변환 · 멜 스펙트로그램 · MFCC", "https://librosa.org/doc/latest/", "ISC"),
    "soundfile":      ("soundfile", "WAV 파일 쓰기 · 정보 읽기", "https://python-soundfile.readthedocs.io/", "BSD-3-Clause"),
    "numpy":          ("numpy", "오디오 배열 계산", "https://numpy.org/doc/stable/", "BSD-3-Clause"),
    "matplotlib":     ("matplotlib", "파형 · 스펙트로그램 · 막대 그림을 PNG로 저장", "https://matplotlib.org/stable/", "PSF 기반(matplotlib)"),
    "jiwer":          ("jiwer", "WER · CER 채점", "https://jitsi.github.io/jiwer/", "Apache-2.0"),
    "anthropic":      ("anthropic", "Claude API 호출(ANTHROPIC_API_KEY 있을 때만)", "https://docs.anthropic.com/en/api/client-sdks", "Apache-2.0"),
    "pandas":         ("pandas", "표 출력", "https://pandas.pydata.org/docs/", "BSD-3-Clause"),
    "sklearn":        ("scikit-learn", "화자 특징 군집(AgglomerativeClustering)", "https://scikit-learn.org/stable/", "BSD-3-Clause"),
    "scipy":          ("scipy", "화자 번호 ↔ 이름 1:1 짝짓기(linear_sum_assignment)", "https://docs.scipy.org/doc/scipy/", "BSD-3-Clause"),
    "gradio":         ("gradio", "데모 웹 화면(--serve)", "https://www.gradio.app/docs", "Apache-2.0"),
    "sounddevice":    ("sounddevice", "마이크 녹음(--record 일 때만)", "https://python-sounddevice.readthedocs.io/", "MIT"),
}

# TypeScript: Node 내장 모듈·전역 API. 키는 코드에서 찾을 정규식
NODE_DOC = "https://nodejs.org/api/"
TS_LIBS = [
    (r'from "node:fs"', "node:fs", "WAV · 그림 · 회의록 파일 읽고 쓰기", NODE_DOC + "fs.html"),
    (r'from "node:child_process"', "node:child_process", "ffmpeg 설치 여부 확인", NODE_DOC + "child_process.html"),
    (r'from "node:http"', "node:http", "데모 웹 화면(--serve)", NODE_DOC + "http.html"),
    (r'from "node:crypto"', "node:crypto", "요청마다 다른 임시 파일 이름(randomUUID)", NODE_DOC + "crypto.html"),
    (r"\bfetch\(", "fetch", "Claude · Whisper API 호출(키가 있을 때만)", NODE_DOC + "globals.html#fetch"),
    (r"\bnew FormData\(", "FormData · Blob", "받아쓰기 API에 WAV 파일 올리기", NODE_DOC + "globals.html#formdata"),
    (r"\bBuffer\.alloc\(", "Buffer", "WAV · BMP 바이트 직접 쓰기", NODE_DOC + "buffer.html"),
]


def merge_ts(base, extra):
    """이름이 같은 항목은 extra가 대신하고(자리 유지), 새 이름은 뒤에 붙인다."""
    new = {e[1]: e for e in extra}
    return [new.pop(b[1], b) for b in base] + list(new.values())


def day_cfg(day):
    """(노트북 glob, {hash: (Part, [셀])}, PY_LIBS, TS_LIBS) — D1·D10은 위 상수, 그 밖은 scripts/code_map/dayNN.json."""
    if day in MAP:
        return NOTEBOOK[day], MAP[day], PY_LIBS, TS_LIBS
    f = ROOT / "scripts" / "code_map" / f"day{day:02d}.json"
    if not f.exists():
        sys.exit(f"day{day}: MAP에도 {f.relative_to(ROOT)}에도 없어요")
    c = json.load(open(f, encoding="utf-8"))
    return (c["notebook"], {h: (v[0], v[1]) for h, v in c["map"].items()},
            {**PY_LIBS, **{k: tuple(v) for k, v in c.get("py_libs", {}).items()}},
            merge_ts(TS_LIBS, [tuple(v) for v in c.get("ts_libs", [])]))


def py_libs(code, libs=PY_LIBS):
    pins = dict(re.findall(r"([\w-]+)==([\w.]+)", code.split("\n", 3)[1]))  # 두 번째 줄 = pip install 줄
    out, seen = [], set()
    for m in re.finditer(r"^\s*(?:import ([\w.]+)|from ([\w.]+) import)", code, re.M):
        top = (m.group(1) or m.group(2)).split(".")[0]
        if top not in libs or top in seen:
            continue
        seen.add(top)
        pkg, purpose, docs, lic = libs[top]
        if pkg not in pins:
            sys.exit(f"pip install 줄에 {pkg} 버전이 없어요")
        out.append(dict(name=pkg, version=pins[pkg], purpose=purpose, install=f"pip install {pkg}=={pins[pkg]}", docs=docs, license=lic))
    return out


def ts_libs(code, libs=TS_LIBS):
    return [dict(name=name, version="내장", purpose=purpose, install="설치 불필요 (Node 26 내장)", docs=docs, license="MIT (Node.js)")
            for pat, name, purpose, docs in libs if re.search(pat, code)]


def check_code(day, h, lang, code):
    if not code.strip():
        sys.exit(f"day{day} {h}: {lang} 코드가 비었어요")
    if "___" in code:
        sys.exit(f"day{day} {h}: {lang} 빈칸(___)이 남았어요")
    if lang == "python" and not code.split("\n")[1].startswith("# pip install"):
        sys.exit(f"day{day} {h}: python 두 번째 줄은 '# pip install ...' 이어야 해요")


def ordinals(day):
    f = next(iter(glob.glob(str(ROOT / day_cfg(day)[0]))))
    nb = json.load(open(f, encoding="utf-8"))
    codes = [i for i, c in enumerate(nb["cells"]) if c["cell_type"] == "code"]
    return Path(f).name, {i: k + 1 for k, i in enumerate(codes)}  # 노트북 셀 번호 → Colab 코드 셀 순번


def ranges(nums):
    out = []
    for n in nums:
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return out


def build(day, src=None, export=None):
    out_path = ROOT / "data" / "code" / f"day{day:02d}.json"
    old = json.load(open(out_path, encoding="utf-8")) if out_path.exists() else {}
    if export:
        for h, e in old.items():
            for lang, sub, ext in [("python", "py", "py"), ("typescript", "ts", "ts")]:
                p = Path(export) / sub / f"d{day:02d}_{h}.{ext}"
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(e[lang], encoding="utf-8", newline="\n")
        print(f"day{day:02d}: {len(old)}개 → {export}")
        return
    nb_name, ordinal = ordinals(day)
    _, day_map, pylibs, tslibs = day_cfg(day)
    anims = [a["hash"] for a in json.load(open(ROOT / "data" / f"day{day:02d}.json", encoding="utf-8"))["anims"]]
    res = {}
    for h in anims:
        part, idx = day_map[h]
        missing = [i for i in idx if i not in ordinal]
        if missing:
            sys.exit(f"day{day} {h}: 셀 {missing}은 코드 셀이 아니에요")
        code = {}
        for lang, sub, ext in [("python", "py", "py"), ("typescript", "ts", "ts")]:
            if src:
                code[lang] = (Path(src) / sub / f"d{day:02d}_{h}.{ext}").read_text(encoding="utf-8").replace("\r\n", "\n")
            else:
                code[lang] = old.get(h, {}).get(lang, "")
            check_code(day, h, lang, code[lang])
        res[h] = {
            "part": part,
            "nb": nb_name,
            "ord": ranges([ordinal[i] for i in idx]),
            "python": code["python"],
            "typescript": code["typescript"],
            "libs": {"python": py_libs(code["python"], pylibs), "typescript": ts_libs(code["typescript"], tslibs)},
        }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(out_path, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
    print(f"day{day:02d}: {len(res)}개 → {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("days", nargs="*", default=["day01", "day10"])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--src", help="스니펫 파일 폴더(py/ · ts/)에서 코드를 읽어 JSON에 넣기")
    g.add_argument("--export", help="JSON의 코드를 폴더(py/ · ts/)로 꺼내기")
    a = ap.parse_args()
    for d in a.days:
        build(int(re.sub(r"\D", "", d)), a.src, a.export)
