#!/usr/bin/env python3
"""data/code/dayNN.json 코드가 단독으로 실행되는지 검사하고 결과 표를 docs/reports/code-run-report.md에 쓴다.

사용: python scripts/run_code.py day01 day10 [--venv 경로] [--only python|typescript] [--with-keys]
- 각 hash의 python · typescript 코드를 '빈 임시 폴더 하나에 파일 하나'로 써서 실행한다(앞 셀 의존이 있으면 실패).
  Python: <venv>/Scripts/python.exe(Windows) 또는 <venv>/bin/python, --venv가 없으면 지금 실행 중인 python
  TypeScript: node --experimental-strip-types <파일>.ts
- 제한 시간 300초. 종료코드 0이어도 출력에 'Traceback' · '[다시]'가 있으면 실패. 기본은 ANTHROPIC_API_KEY · OPENAI_API_KEY를 빼고 실행한다(키 없는 대체 경로 검사). --with-keys면 그대로.
- 전체 출력은 스니펫마다 임시 폴더의 out.log에 남는다.
"""
import argparse
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIMEOUT = 300
KEYS = ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")


def python_exe(venv):
    if not venv:
        return sys.executable
    v = Path(venv)
    exe = v / "Scripts" / "python.exe" if os.name == "nt" else v / "bin" / "python"
    if not exe.exists():
        sys.exit(f"{exe} 이 없어요")
    return str(exe)


def version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return "없음"


def run_one(code, name, cmd, env):
    d = Path(tempfile.mkdtemp(prefix=f"code_{name}_"))
    f = d / name
    f.write_text(code, encoding="utf-8", newline="\n")
    t0 = time.time()
    try:
        p = subprocess.run(cmd + [f.name], cwd=d, env=env, capture_output=True, timeout=TIMEOUT)
        rc, raw = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        rc, raw = "timeout", (e.stdout or b"") + (e.stderr or b"")
    sec = time.time() - t0
    try:
        out = raw.decode("utf-8")
    except UnicodeDecodeError:
        out = raw.decode("cp949", errors="replace")       # Windows 콘솔 기본 인코딩으로 나온 출력
    (d / "out.log").write_text(out, encoding="utf-8")
    lines = [l for l in out.splitlines() if l.strip() and not re.search(r"Warning|--trace-warnings|Reparsing|eliminate this warning", l)]
    why = []                                              # 종료코드 0이어도 실패로 볼 출력
    if "Traceback" in out:
        why.append("Traceback")
    if "[다시]" in out:
        why.append("정답 확인 실패([다시])")
    ok = rc == 0 and not why
    return ok, rc, sec, (lines[-1] if lines else ""), ("통과" if ok else "실패: " + (", ".join(why) or f"종료코드 {rc}"))


def os_name():
    """Windows 11은 release가 '10'으로 나오므로 빌드 번호(22000 이상 = 11)로 구분한다."""
    if platform.system() == "Windows":
        build = int(platform.version().split(".")[-1] or 0)
        return f"Windows {'11' if build >= 22000 else '10'} (빌드 {platform.version()})"
    return f"{platform.system()} {platform.release()} ({platform.version()})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("days", nargs="*", default=["day01", "day10"])
    ap.add_argument("--venv", help="Python 가상환경 폴더 (기본: 지금 실행 중인 python)")
    ap.add_argument("--only", choices=["python", "typescript"])
    ap.add_argument("--with-keys", action="store_true", help="API 키 환경 변수를 빼지 않고 실행")
    ap.add_argument("--out", default=str(ROOT / "docs" / "reports" / "code-run-report.md"))
    a = ap.parse_args()

    py = python_exe(a.venv)
    env = dict(os.environ) if a.with_keys else {k: v for k, v in os.environ.items() if k not in KEYS}
    langs = [a.only] if a.only else ["python", "typescript"]
    cmds = {"python": ([py], "py"), "typescript": (["node", "--experimental-strip-types"], "ts")}
    rows, fails = [], 0
    for day in a.days:
        n = int(re.sub(r"\D", "", day))
        data = json.load(open(ROOT / "data" / "code" / f"day{n:02d}.json", encoding="utf-8"))
        for h, e in data.items():
            for lang in langs:
                cmd, ext = cmds[lang]
                ok, rc, sec, last, verdict = run_one(e.get(lang, ""), f"d{n:02d}_{h}.{ext}", cmd, env)
                fails += not ok
                rows.append((f"D{n}", h, lang, rc, sec, verdict, last))
                print(f"D{n} {h:9s} {lang:10s} rc={rc} {sec:6.1f}s {verdict}  {last[:60]}", flush=True)

    md = [
        "# 코드 실행 검사 결과",
        "",
        f"- 실행: `python scripts/run_code.py {' '.join(a.days)}" + (f" --venv {a.venv}" if a.venv else "") + (f" --only {a.only}" if a.only else "") + ("` (API 키 포함)" if a.with_keys else "` (API 키 뺌 → 키 없는 대체 경로)"),
        f"- 일시: {datetime.now():%Y-%m-%d %H:%M} · {os_name()}",
        f"- Python: {version([py, '--version'])} (`{py}`) · Node: {version(['node', '--version'])}",
        f"- 방법: 스니펫 하나를 빈 임시 폴더에 파일 하나로 써서 실행, 제한 {TIMEOUT}초",
        "- 판정: 종료코드 0이고 출력에 'Traceback' · '[다시]'(정답 확인 실패)가 없으면 통과",
        f"- 결과: {len(rows)}개 중 통과 {len(rows) - fails} · 실패 {fails}",
        "- 이 검사로 확인하지 않는 경로: API 키 경로(Claude · Whisper API, --with-keys로만), 데모 화면(--serve), 마이크 녹음(--record),"
        " GPU(CUDA) 추론, 사용자 WAV 인자 실행. 인터넷이 필요한 edge-tts는 실행 환경에 따라 실제 음성 또는 합성 신호 대체 경로를 탄다.",
        "",
        "| 일차 | hash | 언어 | 종료코드 | 초 | 판정 | 마지막 출력 |",
        "|---|---|---|---|---|---|---|",
    ]
    for d, h, lang, rc, sec, verdict, last in rows:
        cell = last.replace("|", "\\|")[:80]
        md.append(f"| {d} | {h} | {'Python' if lang == 'python' else 'TypeScript'} | {rc} | {sec:.1f} | {verdict} | {cell} |")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
    print(f"표 → {a.out} · 실패 {fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
