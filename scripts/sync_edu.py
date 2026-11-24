#!/usr/bin/env python3
"""강사 저장소(upstream)의 새 수업 자료를 받아 Edu/ 아래로 정리한다.

upstream은 자료를 저장소 루트의 dayNN/ 에 올린다. 이 스크립트는
  1) upstream/main 을 받아 병합하고 (upstream 리모트가 없으면 origin pull)
  2) 루트에 생긴 dayNN/ 을 Edu/dayNN/ 으로 git mv 한 뒤
  3) 이동만 담은 커밋을 만든다. push 는 하지 않는다.

사용: python scripts/sync_edu.py           # 받기 + 이동 + 커밋
      python scripts/sync_edu.py --no-pull # 이미 받은 상태에서 이동만
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDU = ROOT / "Edu"
DAY = re.compile(r"^day\d{2}$")


def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        sys.exit("git %s 실패:\n%s%s" % (" ".join(args), r.stdout, r.stderr))
    return r.stdout.strip()


def pull():
    if git("status", "--porcelain"):
        sys.exit("커밋하지 않은 변경이 있어요. 먼저 커밋하거나 정리한 뒤 다시 실행하세요.")
    if "upstream" in git("remote").split():
        git("fetch", "upstream")
        print(git("merge", "--no-edit", "upstream/main") or "upstream: 새 내용 없음")
    else:
        print(git("pull", "--ff-only") or "origin: 새 내용 없음")


def move_days():
    moved = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and DAY.match(p.name)):
        dest = EDU / d.name
        if not dest.exists():
            EDU.mkdir(exist_ok=True)
            git("mv", d.name, "Edu/" + d.name)
        else:  # 이미 있는 일차에 파일이 추가·교체된 경우: 파일 단위로 옮김(같은 이름은 upstream 판으로 덮음)
            for f in sorted(x for x in d.rglob("*") if x.is_file()):
                rel = f.relative_to(ROOT).as_posix()
                (EDU / f.relative_to(ROOT)).parent.mkdir(parents=True, exist_ok=True)
                git("mv", "-f", rel, "Edu/" + rel)
            for sub in sorted((p for p in d.rglob("*") if p.is_dir()), reverse=True):
                sub.rmdir()
            d.rmdir()
        moved.append(d.name)
    return moved


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 콘솔(cp949)에서도 한글 출력
    if "--no-pull" not in argv:
        pull()
    moved = move_days()
    if not moved:
        print("루트에 새 dayNN/ 없음 (정리할 것 없음)")
        return 0
    git("commit", "-m", "[edu] 새 수업 자료를 Edu/로 이동: %s" % ", ".join(moved),
        "-m", "scripts/sync_edu.py 자동 정리(upstream은 루트 dayNN/에 올림).")
    print("Edu/로 이동·커밋: %s" % ", ".join(moved))
    print("대시보드 반영: python scripts/extract.py all && python scripts/reskin.py all")
    print("확인 후 push: git push")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
