#!/usr/bin/env python3
"""dayNN/animation.html 을 새 대시보드 셸로 감싸 dashboard/dNN/animation.html 로 만든다.

사용: python scripts/reskin.py all        (1~44일 전부 생성 + <script> diff 검사 표)
      python scripts/reskin.py 1 10 35    (지정한 일차만)
원본 dayNN/ 은 읽기만 한다. <script> 는 FONT 1줄 교체 + (D1~34만) 셸 연결 줄 추가 외에 바꾸지 않는다.
D1~34 = 가로 탭형, D35~44 = 레일형(원본이 이미 레일 구조). 토큰: design/tokens.css 값을 :root 에 평문으로 인라인.
표준 라이브러리만 사용. 폴더명은 d1, d10, d2 … 숫자 그대로.
"""
import difflib
import json
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

# 원본에 있던 모바일 가로 넘침 보정 (CSS만, script 는 손대지 않음)
DAY_FIX = {
    2: ".pipewrap>*{min-width:0}\n",            # 1열 그리드에서 긴 pre.code 가 칸을 늘리던 문제
    9: ".steplist>*{min-width:0;overflow-wrap:anywhere}\n",  # WhisperX 단계 목록의 긴 code
    14: "pre.outbox{overflow-x:auto;max-width:100%}\n",  # 모델 카드 미리보기 긴 줄
    29: ".tokgrid>*{min-width:0}\n",              # JWT 2열→1열 그리드 칸 늘어남
}

TOPBAR = ('<div class="topbar"><button id="themeBtn" class="btn" type="button">화면 모드 바꾸기</button>'
          '<span>키보드 ← → 로 탭을 넘길 수 있습니다.</span></div>\n')


CODEBOX_CSS = r"""
/* ---- 코드 상자 (task-019) ---- */
.codebox{margin-top:22px;min-width:0;max-width:100%;border:1px solid var(--line);border-radius:var(--radius);background:var(--panel);box-shadow:var(--shadow);padding:14px 16px 16px;box-sizing:border-box}
.codebox[hidden]{display:none}
.codebox .cb-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin-bottom:8px}
.codebox h3{margin:0;font-size:var(--text-body);font-weight:700;flex:1 1 auto}
.codebox .cb-tabs{display:flex;gap:2px;border:1px solid var(--line);border-radius:var(--radius-control);padding:2px;background:var(--soft)}
.codebox .cb-tabs button{min-height:32px;border:0;border-radius:var(--radius-control);background:transparent;color:var(--muted);padding:2px 14px;font-size:var(--text-caption);font-weight:600;cursor:pointer}
.codebox .cb-tabs button[aria-selected="true"]{background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
.codebox .cb-copy{min-height:36px;padding:2px 12px;font-size:var(--text-caption)}
.codebox .cb-src{margin:0 0 8px;color:var(--muted);font-size:var(--text-caption);overflow-wrap:anywhere}
.codebox details.cb-libs{margin:0 0 10px;font-size:var(--text-caption)}
.codebox details.cb-libs summary{cursor:pointer;font-weight:600;color:var(--ink);min-height:28px}
.codebox .cb-tw{overflow-x:auto;max-width:100%;margin-top:6px}
.codebox table{border-collapse:collapse;width:100%;min-width:520px}
.codebox th,.codebox td{border-bottom:1px solid var(--line);padding:4px 8px;text-align:left;vertical-align:top}
.codebox th{color:var(--muted);font-weight:600}
.codebox td code{font-family:var(--font-mono);font-size:.92em;overflow-wrap:anywhere}
.codebox a{color:var(--a5)}
.codebox pre.cb-code{margin:0;overflow-x:auto;max-width:100%;background:var(--scope);color:var(--color-scope-fg);border:1px solid var(--line);border-radius:var(--radius-control);padding:10px 0;font-family:var(--font-mono);font-size:var(--text-caption);line-height:1.55;tab-size:4;counter-reset:cb}
.codebox pre.cb-code .l{display:block;white-space:pre;padding:0 12px 0 0;width:max-content;min-width:100%;box-sizing:border-box}
.codebox pre.cb-code .l::before{counter-increment:cb;content:counter(cb);display:inline-block;width:3.2ch;margin-right:1.2ch;text-align:right;color:#9198a1;user-select:none}
.codebox .k{color:#ff7b72}.codebox .s{color:#a5d6ff}.codebox .c{color:#9ea7b3;font-style:italic}
"""

CODEBOX_JS = r"""<script>
/* 코드 상자(task-019): 활성 항목의 코드를 Python·TypeScript 탭으로. 원본 script 와 별개 블록. */
(function(){
const DAY=__DAY__,PM=__PM__,LS='aiVoiceDash.codeLang';
const $=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e;};
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const getLang=()=>{try{let v=localStorage.getItem(LS);if(v==='javascript')v='typescript';return v==='typescript'?'typescript':'python';}catch(e){return 'python';}};
const setLang=l=>{try{localStorage.setItem(LS,l);}catch(e){}};
const KW={python:'and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield',
 typescript:'abstract|as|async|await|break|case|catch|class|const|continue|default|delete|else|enum|export|extends|false|finally|for|from|function|if|implements|import|in|instanceof|interface|let|new|null|of|private|public|readonly|return|static|super|switch|this|throw|true|try|type|typeof|undefined|var|void|while|yield'};
const RX={python:new RegExp(/(#[^\n]*)|("{3}[\s\S]*?"{3}|'{3}[\s\S]*?'{3}|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')/.source+'|\\b('+KW.python+')\\b','g'),
 typescript:new RegExp(/(\/\/[^\n]*|\/\*[\s\S]*?\*\/)|(`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*')/.source+'|\\b('+KW.typescript+')\\b','g')};
function hl(code,lang){
  const wrap=(cls,t)=>t.split('\n').map(l=>'<span class="'+cls+'">'+esc(l)+'</span>').join('\n');
  let out='',last=0,m;const re=RX[lang];re.lastIndex=0;
  while((m=re.exec(code))){out+=esc(code.slice(last,m.index));out+=wrap(m[1]!=null?'c':m[2]!=null?'s':'k',m[0]);last=m.index+m[0].length;}
  out+=esc(code.slice(last));
  return out.split('\n').map(l=>'<span class="l">'+l+'</span>').join('');
}
function copy(text){
  if(navigator.clipboard&&navigator.clipboard.writeText)return navigator.clipboard.writeText(text);
  return new Promise((ok,no)=>{const t=document.createElement('textarea');t.value=text;t.style.cssText='position:fixed;opacity:0';document.body.appendChild(t);t.select();try{document.execCommand('copy')?ok():no();}catch(e){no(e);}t.remove();});
}
const LANGS=[['python','Python'],['typescript','TypeScript']];
function init(data){
  const box=$('section','codebox');box.id='codebox';box.setAttribute('aria-label','코드로 보기');box.hidden=true;
  const head=$('div','cb-head'),h=$('h3',null,'코드로 보기');
  const tl=$('div','cb-tabs');tl.setAttribute('role','tablist');tl.setAttribute('aria-label','언어');
  const tb={};LANGS.forEach(([k,n])=>{const b=$('button',null,n);b.type='button';b.id='cb-t-'+k;b.setAttribute('role','tab');b.dataset.l=k;tl.appendChild(b);tb[k]=b;});
  const cp=$('button','btn cb-copy','복사');cp.type='button';
  head.append(h,tl,cp);
  const src=$('p','cb-src'),libs=$('details','cb-libs'),pre=$('pre','cb-code');pre.tabIndex=0;
  box.append(head,src,libs,pre);
  let key=null,lang=getLang(),cur=null;
  const avail=e=>LANGS.filter(([k])=>e&&e[k]).map(l=>l[0]);
  function libList(e){let L=e.libs;if(L&&!Array.isArray(L))L=L[lang];return Array.isArray(L)?L:[];}
  function render(){
    const e=cur;if(!e){box.hidden=true;return;}
    const av=avail(e);if(!av.length){box.hidden=true;return;}
    if(av.indexOf(lang)<0)lang=av[0];
    box.hidden=false;
    LANGS.forEach(([k])=>{const on=k===lang;tb[k].hidden=av.indexOf(k)<0;tb[k].setAttribute('aria-selected',on);tb[k].tabIndex=on?0:-1;});
    const od=Array.isArray(e.ord)?e.ord.map(r=>Array.isArray(r)?(r[0]===r[1]?r[0]:r[0]+'~'+r[1]):r).join(', '):'';
    src.textContent=lang==='typescript'?'TypeScript · Node 26에서 실행 (node --experimental-strip-types)':['📓 '+(e.nb||''),e.part,od?'코드 셀 '+od:''].filter(x=>x&&x!=='📓 ').join(' · ');
    src.hidden=!src.textContent;
    const L=libList(e);libs.textContent='';libs.hidden=!L.length;
    if(L.length){
      libs.open=true;libs.appendChild($('summary',null,'사용 라이브러리 ('+L.length+')'));
      const w=$('div','cb-tw'),t=$('table'),tr=$('tr');
      ['이름','버전','용도','설치','문서'].forEach(x=>tr.appendChild($('th',null,x)));
      const th=$('thead');th.appendChild(tr);t.appendChild(th);const bd=$('tbody');
      L.forEach(x=>{const r=$('tr');
        const c0=$('td');c0.appendChild($('code',null,x.name||''));
        const c3=$('td');c3.appendChild($('code',null,x.install||''));
        const c4=$('td');if(/^https?:\/\//.test(x.docs||'')){const a=$('a',null,'문서');a.href=x.docs;a.target='_blank';a.rel='noopener noreferrer';c4.appendChild(a);}
        r.append(c0,$('td',null,x.version||''),$('td',null,x.purpose||''),c3,c4);bd.appendChild(r);});
      t.appendChild(bd);w.appendChild(t);libs.appendChild(w);
    }
    pre.innerHTML=hl(e[lang],lang);
    pre.setAttribute('aria-label',(lang==='python'?'Python':'TypeScript')+' 코드');
  }
  function sync(){
    const p=document.querySelector('section.panel.active');if(!p)return;
    const k=PM[p.id]||p.id;
    if(box.parentNode!==p)p.appendChild(box);
    if(k===key&&cur)return;
    key=k;cur=data[k]||null;render();
  }
  tl.addEventListener('click',e=>{const b=e.target.closest('button[data-l]');if(!b)return;lang=b.dataset.l;setLang(lang);render();});
  tl.addEventListener('keydown',e=>{
    if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft'&&e.key!=='Home'&&e.key!=='End')return;
    const av=avail(cur);if(av.length<2)return;e.stopPropagation();e.preventDefault();
    let i=av.indexOf(lang);i=e.key==='Home'?0:e.key==='End'?av.length-1:(i+(e.key==='ArrowRight'?1:-1)+av.length)%av.length;
    lang=av[i];setLang(lang);render();tb[lang].focus();});
  cp.addEventListener('click',()=>{if(!cur)return;copy(cur[lang]).then(()=>{cp.textContent='복사됨';},()=>{cp.textContent='복사 실패';}).then(()=>setTimeout(()=>{cp.textContent='복사';},1500));});
  const mo=new MutationObserver(sync);
  document.querySelectorAll('section.panel').forEach(p=>mo.observe(p,{attributes:true,attributeFilter:['class']}));
  addEventListener('hashchange',()=>setTimeout(sync,0));
  sync();
}
function fail(){
  const box=$('section','codebox'),head=$('div','cb-head');box.id='codebox';box.setAttribute('aria-label','코드로 보기');box.setAttribute('role','status');
  head.appendChild($('h3',null,'코드로 보기'));
  box.append(head,$('p','cb-src','코드를 불러오지 못했습니다. 새로고침하거나 잠시 뒤 다시 열어 주세요.'));
  const put=()=>{const p=document.querySelector('section.panel.active');if(p&&box.parentNode!==p)p.appendChild(box);};
  const mo=new MutationObserver(put);
  document.querySelectorAll('section.panel').forEach(p=>mo.observe(p,{attributes:true,attributeFilter:['class']}));
  addEventListener('hashchange',()=>setTimeout(put,0));
  put();
}
const j=r=>{if(!r.ok)throw new Error(r.status);return r.json();};
fetch('../../data/code/index.json').then(j).then(ix=>{
  if(!ix||!ix[String(DAY)])return null;
  return fetch('../../data/code/day'+String(DAY).padStart(2,'0')+'.json').then(j);
}).then(d=>{if(d)init(d);}).catch(fail);
})();
</script>
"""


def panel_map(src):
    """탭형: 원본 HASH={key:'pN'} 에서 패널 id -> data/code 키. 레일형은 패널 id 가 곧 키(빈 맵)."""
    m = re.search(r"const HASH=\{([^}]*)\}", src)
    if not m:
        return {}
    return {v: k for k, v in re.findall(r"(\w+):'(\w+)'", m.group(1))}


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
    s = s[:m.start()] + PRETENDARD + "\n<style>" + restyle(m.group(1), rail) + DAY_FIX.get(n, "") + CODEBOX_CSS + "</style>" + s[m.end():]
    m = re.search(r"<script>(.*?)</script>", s, re.S)
    assert s.count("<script>") == 1
    s = s[:m.start(1)] + transform_script(m.group(1), rail) + s[m.end(1):]
    box = CODEBOX_JS.replace("__DAY__", str(n)).replace("__PM__", json.dumps(panel_map(src)))
    i = s.rindex("</body>")
    s = s[:i] + box + s[i:]
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
