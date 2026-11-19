"""data/day01~44.json + course.json -> data/library.json (자료실용 요약본)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
QKEYS = ("ty", "p", "o", "a", "w", "left", "right", "steps", "unit", "hint", "items", "cats", "c")


def main():
    course = json.loads((DATA / "course.json").read_text(encoding="utf-8"))
    days = []
    nc = nq = na = 0
    for c in course:
        f = DATA / f"day{c['day']:02d}.json"
        e = {"day": c["day"], "week": c["week"], "module": c["module"], "title": c["title"],
             "concepts": [], "questions": [], "anims": [], "road": []}
        if c.get("ready") and f.exists():
            d = json.loads(f.read_text(encoding="utf-8"))
            e["concepts"] = [{"concept": x.get("concept", ""), "summary": x.get("summary", ""), "code": x.get("code", "")}
                             for x in d.get("learned") or []]
            for g in (d.get("worksheet") or {}).get("groups", []):
                for q in g.get("qs", []):
                    o = {"g": g.get("title", "")}
                    o.update({k: q[k] for k in QKEYS if k in q})
                    e["questions"].append(o)
            e["anims"] = [{"hash": a["hash"], "title": a.get("title", ""), "desc": a.get("desc", "")} for a in d.get("anims") or []]
            e["road"] = [{"p": r.get("p", ""), "t": r.get("t", "")} for r in d.get("road") or []]
        nc += len(e["concepts"]); nq += len(e["questions"]); na += len(e["anims"])
        days.append(e)
    out = DATA / "library.json"
    out.write_text(json.dumps({"days": days}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"개념 {nc} · 문항 {nq} · 애니메이션 {na} · {out.stat().st_size // 1024}KB")


if __name__ == "__main__":
    main()
