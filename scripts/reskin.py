#!/usr/bin/env python3
"""dayNN/animation.html 을 새 대시보드 셸로 감싸 dashboard/dNN/animation.html 로 만든다.

사용: python scripts/reskin.py all        (1~44일 전부 생성 + <script> diff 검사 표)
      python scripts/reskin.py 1 10 35    (지정한 일차만)
원본 dayNN/ 은 읽기만 한다. <script> 는 FONT 1줄 교체 + (D1~34만) 셸 연결 줄 추가 외에 바꾸지 않는다.
D1~34 = 가로 탭형, D35~44 = 레일형(원본이 이미 레일 구조). 토큰: design/tokens.css 값을 :root 에 평문으로 인라인.
표준 라이브러리만 사용. 폴더명은 d1, d10, d2 … 숫자 그대로.
"""
import difflib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dashboard")
RAIL_FROM = 35  # D35~44 레일형

FONT_STACK = '"Pretendard Variable", Pretendard, -apple-system, "Segoe UI", "Malgun Gothic", sans-serif'
FONT_LINE = "const FONT = '%s';" % FONT_STACK
PRETENDARD = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/'
              'dist/web/variable/pretendardvariable-dynamic-subset.min.css">')

CONN = r"""
/* 셸 연결(추가): seen 표시 · 테마 버튼 · 키보드 ← → */
const markSeen=()=>tabs.forEach(x=>{if(x.getAttribute('aria-selected')==='true')x.classList.add('seen');});
new MutationObserver(markSeen).observe(document.querySelector('nav.tabs'),{subtree:true,attributes:true,attributeFilter:['aria-selected']});markSeen();
$('themeBtn').onclick=()=>{const r=document.documentElement;const dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;r.dataset.theme=dark?'light':'dark';};
addEventListener('keydown',e=>{if(/INPUT|SELECT|TEXTAREA/.test(document.activeElement.tagName))return;
  const i=tabs.findIndex(b=>b.getAttribute('aria-selected')==='true');if(e.key==='ArrowRight'&&i<tabs.length-1)tabs[i+1].click();if(e.key==='ArrowLeft'&&i>0)tabs[i-1].click();});
"""

LIGHT = ("--page:#f6f8fa;--panel:#ffffff;--ink:#1f2328;--muted:#59636e;--line:#d0d7de;--soft:#eaeef2;"
         "--a1:#1b7c83;--a2:#9a6700;--a3:#bf3989;--a4:#8250df;--a5:#0969da;--ok:#1a7f37;--bad:#d1242f;"
         "--scope:#0d1117;--color-scope-fg:#f0f6fc;--color-primary:#0969da;--color-primary-fg:#ffffff;--on-accent:#ffffff;"
         "--input:#818b98;--ring:0 0 0 2px rgb(9 105 218 / 0.4);--shadow:0 1px 0 rgb(31 35 40 / 0.04);")
DARK = ("--page:#0d1117;--panel:#151b23;--ink:#f0f6fc;--muted:#9198a1;--line:#3d444d;--soft:#212830;"
        "--a1:#39c5cf;--a2:#d29922;--a3:#db61a2;--a4:#ab7df8;--a5:#4493f8;--ok:#3fb950;--bad:#f85149;"
        "--color-primary:#4493f8;--color-primary-fg:#0d1117;--on-accent:#0d1117;"
        "--input:#727b87;--ring:0 0 0 2px rgb(68 147 248 / 0.5);--shadow:0 0 0 1px rgb(61 68 77 / 0.5);")

TOKENS = """:root{
  %s
  --font-sans:%s;--font-mono:ui-monospace,"SF Mono",Consolas,monospace;
  --text-display:28px;--text-h1:22px;--text-h2:23px;--text-body:14.5px;--text-caption:12px;--fs-h2:1.45rem;
  --rail:0px;--roadcols:2;--tap:44px;
  --radius-control:6px;--radius-card:6px;--radius-pill:999px;--radius:6px;--shadow-pop:0 8px 24px rgb(140 149 159 / 0.2);
  --bg:var(--page);--asr:var(--a1);--llm:var(--a2);--tts:var(--a3);--s2s:var(--a4);--net:var(--muted);--warn:var(--a2);
  box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
}
@media (width >= 768px){:root{--text-display:36px;--text-h1:24px;--text-h2:28px;--text-body:15px;--text-caption:12.5px;--fs-h2:1.75rem;--rail:212px;--roadcols:3;--tap:40px}}
@media (width >= 1200px){:root{--text-display:48px;--text-h1:26px;--text-h2:33px;--text-body:16px;--text-caption:13px;--fs-h2:2.05rem;--rail:248px;--roadcols:6}}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  %s --shadow-pop:0 8px 24px rgb(1 4 9 / 0.6);}}
:root[data-theme="dark"]{
  %s --shadow-pop:0 8px 24px rgb(1 4 9 / 0.6);}
""" % (LIGHT, FONT_STACK, DARK, DARK)

COMMON = """/* ---- 새 셸 (design/tokens.css · DESIGN.md) ---- */
body{margin:0;background:var(--page);color:var(--ink);font-family:var(--font-sans);font-size:var(--text-body);line-height:1.6}
button,input,select{font-family:inherit}
h2{font-size:var(--text-h2);line-height:1.25;letter-spacing:-.01em}
.note,.lead+.note{font-size:var(--text-caption)}
.big,.kv b,label.sl output{font-family:var(--font-mono)}
button:focus-visible,input:focus-visible,select:focus-visible{outline:0;box-shadow:var(--ring)}
.btn{min-height:var(--tap);border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:var(--radius-control);padding:6px 14px;font-weight:500}
.btn:hover{background:var(--soft);border-color:var(--line)}
.btn.primary,.btn.go{background:var(--color-primary);color:var(--color-primary-fg);border-color:var(--color-primary);font-weight:700}
.btn:disabled{background:var(--soft);color:var(--muted);opacity:1}
.chip{min-height:28px;padding:2px 12px;border:1px solid var(--line);border-radius:var(--radius-pill);color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--c,var(--a4));border-color:var(--c,var(--a4));color:var(--on-accent)}
.stage,.ctl,.detail,.roaddetail,.scen,.kv div,.scope{border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow)}
.scope{background:var(--scope);color:var(--color-scope-fg);box-shadow:none}
.road{grid-template-columns:repeat(var(--roadcols),1fr)}
.road button{border:1px solid var(--line);border-top:3px solid var(--c);border-radius:var(--radius);background:var(--panel);color:var(--ink)}
.road button:hover{background:var(--soft)}
.road button[aria-pressed="true"]{background:var(--c);color:var(--on-accent)}
.road button[aria-pressed="true"] b{color:var(--on-accent)}
.scen .opts button.right{border-color:var(--ok)}
.scen .opts button.wrong{border-color:var(--bad)}
.scen .opts button.right::before{content:"\\2713  "}
.scen .opts button.wrong::before{content:"\\2717  "}
input[type=range]{accent-color:var(--a5)}
"""

TABS_CSS = """header h1{font-size:var(--text-h1);line-height:1.25;letter-spacing:-.01em}
.topbar{display:flex;justify-content:flex-end;align-items:center;gap:10px;margin-bottom:6px;color:var(--muted);font-size:var(--text-caption)}
nav.tabs{display:flex;gap:2px;overflow-x:auto;border-bottom:1px solid var(--line);margin-bottom:22px;scrollbar-width:thin}
nav.tabs button{flex:0 0 auto;min-height:var(--tap);border:0;border-bottom:2px solid transparent;border-radius:0;background:transparent;color:var(--muted);font-size:var(--text-body);padding:6px 12px;cursor:pointer;white-space:nowrap}
nav.tabs button:hover{background:var(--soft);color:var(--ink)}
nav.tabs button[aria-selected="true"]{color:var(--ink);font-weight:700;border-bottom-color:var(--a5)}
nav.tabs button.seen::after{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--a1);margin-left:6px;vertical-align:middle}
"""

RAIL_CSS = """.shell{display:grid;grid-template-columns:minmax(0,1fr);min-height:100vh}
@media (min-width:768px){.shell{grid-template-columns:var(--rail) minmax(0,1fr)}.rail{position:sticky;top:0;align-self:start;height:100vh;overflow-y:auto}}
.rail{background:var(--panel);border-right:1px solid var(--line);padding:20px 12px 16px;display:flex;flex-direction:column;gap:16px}
.rail h1{font-size:var(--text-h1);font-weight:700;line-height:1.25;letter-spacing:-.01em;margin:0}
.rail h1 small{display:block;font-size:var(--text-caption);font-weight:400;color:var(--muted);letter-spacing:0;margin-bottom:4px}
nav.tabs{display:flex;flex-direction:column;gap:2px;position:relative}
nav.tabs::before{content:"";position:absolute;left:20px;top:16px;bottom:16px;width:1px;background:var(--line)}
nav.tabs button{position:relative;display:grid;grid-template-columns:22px 1fr;align-items:center;gap:10px;min-height:var(--tap);padding:4px 8px;border:0;border-left:2px solid transparent;border-radius:var(--radius-control);background:transparent;color:var(--muted);text-align:left;cursor:pointer;font-size:var(--text-body)}
nav.tabs button .tc{width:22px;height:22px;border-radius:50%;display:grid;place-items:center;background:var(--panel);border:1px solid var(--line);font-family:var(--font-mono);font-weight:700;font-size:.72rem}
nav.tabs button:hover{background:var(--soft);color:var(--ink)}
nav.tabs button[aria-selected="true"]{color:var(--ink);font-weight:700;background:var(--soft);border-left-color:var(--a5)}
nav.tabs button[aria-selected="true"] .tc{background:var(--a5);border-color:var(--a5);color:var(--on-accent)}
nav.tabs button.seen .tc{border-color:var(--a1)}
.railfoot{margin-top:auto;display:flex;flex-direction:column;gap:8px;font-size:var(--text-caption);color:var(--muted)}
.railfoot button{min-height:var(--tap);border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:var(--radius-control);padding:6px 10px;cursor:pointer;font-size:var(--text-caption);text-align:left}
.railfoot button:hover{background:var(--soft)}
main{padding:30px clamp(16px,3vw,40px) 60px;max-width:1120px;width:100%;min-width:0}
@media (max-width:767px){
  .rail{border-right:0;border-bottom:1px solid var(--line);padding:12px 12px 8px;gap:8px}
  nav.tabs{flex-direction:row;overflow-x:auto;gap:4px}
  nav.tabs::before{display:none}
  nav.tabs button{flex:0 0 auto;grid-template-columns:22px auto;gap:6px;border-left:0;border-bottom:2px solid transparent;border-radius:0;white-space:nowrap}
  nav.tabs button[aria-selected="true"]{background:transparent;border-bottom-color:var(--a5)}
  .railfoot{flex-direction:row;margin-top:0;align-items:center}
  .railfoot span{display:none}
  main{padding-top:18px}
  label.sl{grid-template-columns:96px 1fr 66px;font-size:.88rem}
}
"""

TOPBAR = ('<div class="topbar"><button id="themeBtn" class="btn" type="button">화면 모드 바꾸기</button>'
          '<span>키보드 ← → 로 탭을 넘길 수 있습니다.</span></div>\n')


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def radius_tok(m):
    nums = [float(x) for x in re.findall(r"[\d.]+", m.group(1))]
    return "border-radius:var(--radius)" if m.group(1).count("px") == len(nums) and all(7 <= v < 50 for v in nums) else m.group(0)


def restyle(css, rail):
    i = css.index("*,*::before")
    head = css[:i]
    assert head.count(":root") == 3, "토큰 영역 구조가 다르다"
    css = css[i:]
    css = re.sub(r"^.*\{color:#0A1024\}\}?\s*$\n?", "", css, flags=re.M | re.I)
    if rail:
        for pat in (r"^\.shell\{[^}]*\}\s*$", r"^\.rail[^{]*\{[^}]*\}\s*$", r"^nav\.tabs[^{]*\{[^}]*\}\s*$",
                    r"^\.railfoot[^{]*\{[^}]*\}\s*$", r"^main\{[^}]*\}\s*$"):
            css = re.sub(pat + r"\n?", "", css, flags=re.M)
        css, n = re.subn(r"@media \(max-width:820px\)\{\n  \.shell.*?\n\}\n", "", css, flags=re.S)
        assert n == 1, "820px 레일 접힘 블록 없음"
    css = re.sub(r"border-radius:([\d.]+px(?: [\d.]+px)*)", radius_tok, css)
    css = re.sub(r"color:#fff(?:fff)?\b", "color:var(--on-accent)", css, flags=re.I)
    return "\n" + TOKENS + css.rstrip("\n") + "\n" + COMMON + (RAIL_CSS if rail else TABS_CSS)


def transform_script(sc, rail):
    lines = sc.split("\n")
    idx = [k for k, l in enumerate(lines) if re.match(r"\s*const FONT\s*=", l)]
    assert len(idx) == 1, "FONT 줄이 1개가 아니다"
    lines[idx[0]] = FONT_LINE
    sc = "\n".join(lines)
    if not rail:
        # 원본 script 는 (function(){ ... })(); 로 감싸여 tabs·$ 가 지역 스코프 → 닫는 줄 앞에 넣는다
        k = sc.rstrip().rfind("\n})();")
        assert k >= 0 and sc[k + 6:].strip() == "", "IIFE 닫는 줄을 찾지 못함"
        sc = sc[:k] + "\n" + CONN.rstrip("\n") + sc[k:]
    return sc


def build(n):
    src = read(os.path.join(ROOT, "day%02d" % n, "animation.html"))
    rail = n >= RAIL_FROM
    s = re.sub(r"<link[^>]*fonts\.g[^>]*>\n?", "", src)
    m = re.search(r"<style>\n?(.*?)</style>", s, re.S)
    s = s[:m.start()] + PRETENDARD + "\n<style>" + restyle(m.group(1), rail) + "</style>" + s[m.end():]
    m = re.search(r"<script>(.*?)</script>", s, re.S)
    assert s.count("<script>") == 1
    s = s[:m.start(1)] + transform_script(m.group(1), rail) + s[m.end(1):]
    if not rail:
        assert s.count('<div class="wrap">\n') == 1
        s = s.replace('<div class="wrap">\n', '<div class="wrap">\n' + TOPBAR, 1)
    d = os.path.join(OUT, "d%d" % n)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "animation.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    return src


def script_of(s):
    return re.search(r"<script>(.*?)</script>", s, re.S).group(1)


def check(n, src):
    """원본 대 신규 <script> diff: FONT 교체 1줄 + 셸 연결 줄 추가만 허용."""
    new = script_of(read(os.path.join(OUT, "d%d" % n, "animation.html")))
    a, b = script_of(src).split("\n"), new.split("\n")
    conn = [l for l in CONN.split("\n") if l.strip()]
    font = ins = other = 0
    added = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace" and i2 - i1 == 1 and j2 - j1 == 1 and b[j1] == FONT_LINE and a[i1].lstrip().startswith("const FONT"):
            font += 1
        elif tag == "insert" or (tag == "replace" and i2 - i1 == 0):
            added += [l for l in b[j1:j2] if l.strip()]
        else:
            other += 1
    if added:
        ins = len(added)
        if added != conn:
            other += 1
    expect_ins = 0 if n >= RAIL_FROM else len(conn)
    ok = font == 1 and other == 0 and ins == expect_ins
    return font, ins, other, ok


def main(argv):
    days = list(range(1, 45)) if argv == ["all"] else [int(x) for x in argv]
    if not days:
        print(__doc__)
        return 2
    rows, fail = [], 0
    for n in days:
        src = build(n)
        font, ins, other, ok = check(n, src)
        fail += not ok
        rows.append((n, "레일" if n >= RAIL_FROM else "탭", font, ins, other, "OK" if ok else "FAIL"))
    print("일차  형  FONT  연결줄  기타diff  결과")
    for r in rows:
        print("D%-3d %-3s %4d %6d %8d  %s" % r)
    print("생성 %d개, 검사 실패 %d" % (len(rows), fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))
