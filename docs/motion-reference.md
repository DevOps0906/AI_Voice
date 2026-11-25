# 모션 레퍼런스

루트 `index.html`의 S8 탭(`#motion`)에 있는 효과 목록이에요. 화면의 코드와 이 문서의 코드는 같아요(실제로 동작하는 CSS).

- 원본 459개 모션을 기법 15가지로 정리한 **기법 카드**(맨 아래 `## 기법 카드` 절) + 공통 효과 CSS 25종 + scope 헬퍼(JS) 10종. 화면 맨 아래에는 원본 459개 전체 목록(일차·기법·구동 필터)이 있어요.
- 공통 효과 출처: 원본에서 온 것은 처음 나오는 일차를 적고(`dots` 원본 D1~34 · `shake` 원본 D35~51 대시보드판 · `scope`·`ease`·`grid`·`tour` 원본 D35~51(D42에서 가져옴) · `rr` D1 · `rng` D4 · `wave` D37 · `bars` D1 heroLoop · `hbar` D47 · `lanes` D21), 나머지는 대시보드 작성이에요.
- 동작 줄이기(`prefers-reduced-motion: reduce`)에서는 `animation`과 `transition`을 모두 끄고 정지 화면으로 보여요.
- 호버·누름 효과는 데모 상자에서 `.on` 클래스로도 재생해요.

## 등장

### 아래에서 떠오르기 (`.m-fadeup`)

투명에서 시작해 14px 위로 올라오며 나타나요.

```css
.m-fadeup{animation:mk-fadeup .7s ease both}
@keyframes mk-fadeup{from{opacity:0;transform:translateY(14px)}}
```

### 계단식 등장 (`.m-stagger`)

--i 값에 따라 시간차를 두고 하나씩 나타나요. 목표 목록에 써요.

```css
.m-stagger{animation:mk-stag .5s ease both;animation-delay:calc(var(--i)*.12s)}
@keyframes mk-stag{from{opacity:0;transform:translateX(-14px)}}
```

### 톡 튀어나오기 (`.m-pop`)

작게 시작해 살짝 커졌다가 제자리로 돌아와요.

```css
.m-pop{animation:mk-pop .5s ease both}
@keyframes mk-pop{0%{transform:scale(.6);opacity:0}70%{transform:scale(1.06)}100%{transform:scale(1)}}
```

### 옆에서 밀려오기 (`.m-slide`)

왼쪽 24px 밖에서 미끄러져 들어와요.

```css
.m-slide{animation:mk-slide .6s ease both}
@keyframes mk-slide{from{opacity:0;transform:translateX(-24px)}}
```

### 흐림 풀기 (`.m-blur`)

흐릿한 상태에서 또렷해지며 나타나요.

```css
.m-blur{animation:mk-blur .8s ease both}
@keyframes mk-blur{from{opacity:0;filter:blur(8px)}}
```

### 가림막 걷기 (`.m-reveal`)

clip-path로 왼쪽에서 오른쪽으로 드러나요.

```css
.m-reveal{animation:mk-reveal .9s ease both}
@keyframes mk-reveal{from{clip-path:inset(0 100% 0 0)}}
```

### 타자 효과 (`.m-type`)

steps()로 글자가 하나씩 찍혀요. 너비를 글자 수(em)에 맞추고 steps 수도 같게 해요.

```css
.m-type{display:inline-block;white-space:nowrap;overflow:hidden;vertical-align:bottom;width:5em;border-right:2px solid currentColor;animation:mk-type 1.6s steps(5) both}
@keyframes mk-type{from{width:0}}
```

## 상태·피드백

### 오답 흔들기 (`.m-shake`)

좌우로 5px 흔들어 틀렸다고 알려요. 퀴즈 오답에 써요.

```css
.m-shake{animation:mk-shake .3s;border-color:var(--bad)}
@keyframes mk-shake{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
```

### 퍼지는 고리 (`.m-ring`)

테두리에서 고리가 퍼져 나가요. 정답·주목에 써요.

```css
.m-ring{animation:mk-ring 1.4s ease-out infinite}
@keyframes mk-ring{from{box-shadow:0 0 0 0 var(--ok)}to{box-shadow:0 0 0 14px transparent}}
```

### 통통 튀기 (`.m-bounce`)

위로 12px 올라갔다 내려와요.

```css
.m-bounce{animation:mk-bounce .8s ease infinite}
@keyframes mk-bounce{40%{transform:translateY(-12px)}}
```

### 진행 막대 채우기 (`.m-fill`)

scaleX로 왼쪽에서 채워져요. 과제 진행 막대에 써요.

```css
.m-fill{width:80%;height:10px;background:var(--soft);border-radius:99px;overflow:hidden}
.m-fill i{display:block;height:100%;background:var(--a1);transform-origin:left;animation:mk-fill 1.2s ease both}
@keyframes mk-fill{from{transform:scaleX(0)}}
```

### 체크 그리기 (`.m-check`)

stroke-dashoffset으로 체크 표시를 그려요.

```css
.m-check{stroke-dasharray:24;animation:mk-check .6s ease both}
@keyframes mk-check{from{stroke-dashoffset:24}}
```

### 배경 반짝 (`.m-flash`)

주황 배경이 서서히 사라져요. 값이 바뀐 곳을 알려요.

```css
.m-flash{animation:mk-flash 1.2s ease both}
@keyframes mk-flash{from{background:color-mix(in srgb,var(--a2) 45%,transparent)}}
```

### 두근두근 (`.m-beat`)

1.12배까지 두 번 커졌다 돌아와요.

```css
.m-beat{animation:mk-beat 1.4s ease infinite}
@keyframes mk-beat{15%{transform:scale(1.12)}30%{transform:scale(1)}45%{transform:scale(1.08)}60%{transform:scale(1)}}
```

### 불러오는 중 반짝 (`.m-shimmer`)

스켈레톤 줄 위로 빛이 지나가요. 내용이 올 자리를 미리 보여줘요.

```css
.m-shimmer{width:80%;height:12px;margin-bottom:8px;border-radius:99px;background:linear-gradient(90deg,var(--soft) 30%,color-mix(in srgb,var(--a4) 25%,var(--soft)) 50%,var(--soft) 70%) 0 0/200% 100%;animation:mk-shimmer 1.4s linear infinite}
@keyframes mk-shimmer{from{background-position:100% 0}to{background-position:-100% 0}}
```

## 호버·누름

### 떠오르는 카드 (`.m-lift`)

마우스를 올리면 4px 떠오르며 그림자가 생겨요.

```css
.m-lift{transition:transform .2s,box-shadow .2s}
.m-lift:hover,.on .m-lift{transform:translateY(-4px);box-shadow:0 8px 24px rgb(140 149 159 / .2)}
```

### 눌림 (`.m-press`)

누르는 동안 94%로 작아져요.

```css
.m-press{transition:transform .1s}
.m-press:active,.on .m-press{transform:scale(.94)}
```

### 밑줄 늘어나기 (`.m-ul`)

마우스를 올리면 밑줄이 왼쪽에서 늘어나요.

```css
.m-ul{background:linear-gradient(currentColor,currentColor) 0 100%/0 2px no-repeat;transition:background-size .3s}
.m-ul:hover,.on .m-ul{background-size:100% 2px}
```

### 테두리 빛나기 (`.m-glow`)

테두리 색이 바뀌고 부드러운 고리가 생겨요.

```css
.m-glow{transition:box-shadow .25s,border-color .25s}
.m-glow:hover,.on .m-glow{border-color:var(--a4);box-shadow:0 0 0 3px color-mix(in srgb,var(--a4) 30%,transparent)}
```

### 살짝 기울이기 (`.m-tilt`)

-3도 기울며 조금 커져요.

```css
.m-tilt{transition:transform .2s}
.m-tilt:hover,.on .m-tilt{transform:rotate(-3deg) scale(1.04)}
```

## 지속(루프)

### 돌아가는 고리 (`.m-spin`)

불러오는 중임을 알려요.

```css
.m-spin{width:34px;height:34px;border:4px solid var(--soft);border-top-color:var(--a4);border-radius:50%;animation:mk-spin .9s linear infinite}
@keyframes mk-spin{to{transform:rotate(360deg)}}
```

### 깜빡이는 커서 (`.m-caret`)

글자 끝에서 커서가 깜빡여요.

```css
.m-caret::after{content:"";display:inline-block;width:2px;height:1.1em;background:currentColor;margin-left:3px;vertical-align:text-bottom;animation:mk-blink 1s steps(2,start) infinite}
@keyframes mk-blink{to{visibility:hidden}}
```

### 둥실 떠 있기 (`.m-float`)

위아래로 6px 천천히 오가요.

```css
.m-float{animation:mk-float 2s ease-in-out infinite alternate}
@keyframes mk-float{to{transform:translateY(-6px)}}
```

### 로딩 점 (`.m-dots`)

글자 뒤에 점이 하나씩 늘어나요. content를 steps(4)로 바꿔요.

```css
.m-dots::after{content:"";animation:mk-dots 1s steps(4) infinite}
@keyframes mk-dots{0%{content:""}25%{content:"."}50%{content:".."}75%{content:"..."}}
```

### 이퀄라이저 막대 (`.m-eq`)

막대가 시간차로 오르내려요. 듣는 중·말하는 중을 보여줘요.

```css
.m-eq{display:flex;align-items:flex-end;gap:4px;height:32px}
.m-eq i{width:6px;height:100%;border-radius:99px;background:var(--a4);transform-origin:bottom;animation:mk-eq .9s ease-in-out infinite alternate;animation-delay:calc(var(--i)*-.2s)}
@keyframes mk-eq{from{transform:scaleY(.2)}to{transform:scaleY(1)}}
```

## scope 헬퍼

원본 D35~51 페이지에 공통으로 있는 헬퍼예요(`day42/animation.html`에서 가져옴).

### scope 입자 흐름 (`scope`)

어두운 계측기 화면에 빛나는 점이 선을 따라 흘러요. dot()으로 그려요.

```js
const u=(t*0.5+k/5)%1;
dot(c,12+u*(w-24),h/2,3,K.sp[k%5],10);
function dot(c,x,y,r,col,glow=0){c.save();if(glow){c.shadowColor=col;c.shadowBlur=glow;}
  c.fillStyle=col;c.beginPath();c.arc(x,y,r,0,7);c.fill();c.restore();}
```

### ease 지수 보간 (`ease`)

목표 위치로 부드럽게 따라가요. 프레임 시간(dt)에 맞춰 같은 속도로 움직여요.

```js
const ease=(cur,tg,dt,k=9)=>cur+(tg-cur)*(1-Math.exp(-k*dt));
st.cur=ease(st.cur,st.tg,dt);
```

### fit + grid 눈금 배경 (`grid`)

fit()으로 캔버스를 화면 배율에 맞추고, grid()로 눈금을 깔아요.

```js
function fit(cv){const r=Math.min(2,devicePixelRatio||1),w=cv.clientWidth||cv.parentElement.clientWidth||640,h=+cv.dataset.h||300;
  if(cv.width!==Math.round(w*r)||cv.height!==Math.round(h*r)){cv.width=Math.round(w*r);cv.height=Math.round(h*r);cv.style.height=h+'px';}
  const c=cv.getContext('2d');c.setTransform(r,0,0,r,0,0);c.clearRect(0,0,w,h);return {c,w,h};}
function grid(c,w,h,step=40){c.strokeStyle=K.grid;c.lineWidth=1;c.beginPath();
  for(let x=step;x<w;x+=step){c.moveTo(x+.5,0);c.lineTo(x+.5,h);}
  for(let y=step;y<h;y+=step){c.moveTo(0,y+.5);c.lineTo(w,y+.5);}c.stroke();}
```

### 시연 자막 (tour) (`tour`)

단계마다 자막을 바꾸고 시간 막대를 채우는 시연 방식이에요. 시연 보기 버튼이 써요.

```js
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function runTour(){for(let i=0;i<steps.length;i++){if(tok.stop)return;
  cap.textContent=steps[i].say;await wait(1600);}}
```

아래 6종은 `dashboard/d10·d11·d21·d37·d47/animation.html`의 구현을 짧게 정리한 것이에요. 화면에서는 `K`(색 토큰)와 위의 `dot()`·`ease()`·`txt()`를 같이 써요.

### rr 둥근 사각형 (`rr`)

모서리가 둥근 상자를 테두리색·채움색으로 그려요. 단계 상자·막대에 써요.

```js
function rr(c,x,y,w,h,col,fill){c.strokeStyle=col;c.lineWidth=1.8;c.beginPath();c.roundRect(x,y,w,h,6);if(fill){c.fillStyle=fill;c.fill();}c.stroke();}
rr(c,x,y,60,34,K.sp[k],K.grid);
```

### mulberry + gauss 고정 난수 (`rng`)

같은 씨앗이면 매번 같은 점이 나와요. gauss()로 가운데에 몰린 잡음 점을 만들어요.

```js
function mulberry(a){return()=>{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
function gauss(r){let u=0;while(u===0)u=r();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*r());}
const r=mulberry(7);
for(let i=0;i<60;i++)dot(c,12+r()*(w-24),h/2+gauss(r)*h*0.15,2,K.sp[i%5]);
```

### wave 파형 선 (`wave`)

소리 파형처럼 출렁이는 선이에요. 사인 두 개를 곱해 크기가 오르내려요.

```js
c.strokeStyle=K.sp[4];c.lineWidth=2;c.beginPath();
for(let x=12;x<=w-12;x+=2){const y=h/2+Math.sin(x*0.06+t*3)*Math.sin(x*0.015-t)*h*0.34;x>12?c.lineTo(x,y):c.moveTo(x,y);}
c.stroke();
```

### bars 막대 채우기 (`bars`)

막대 줄이 왼쪽에서 오른쪽으로 하나씩 켜져요. 진행 상태 표시에 써요.

```js
const n=Math.floor((w-24)/8),head=Math.floor((t*14)%(n+20));
for(let i=0;i<n;i++){const bh=10+(Math.sin(i*0.5)+1)*14;
  c.fillStyle=i<=head?K.sp[0]:K.line;c.fillRect(12+i*8,h/2-bh/2,5,bh);}
```

### hbar 가로 게이지 (`hbar`)

목표 값을 ease로 따라가는 가로 게이지예요. 점수·진행률에 써요.

```js
if(st.tg===undefined){st.tg=.8;st.cur=.8;st.next=0;}
st.next-=dt;if(st.next<=0){st.next=1.6;st.tg=st.tg>.5?.25:.8;}
st.cur=ease(st.cur,st.tg,dt);
rr(c,14,h/2-6,w-28,12,K.line,K.grid);
rr(c,14,h/2-6,Math.max(12,(w-28)*st.cur),12,K.sp[1],K.sp[1]);
txt(c,Math.round(st.cur*100)+'%',14,h/2-14,K.tx,12,true);
```

### lanes 화자 타임라인 (`lanes`)

화자별 레인에 말한 구간을 깔고 재생 막대가 지나가요. 지나간 구간은 색이 채워져요.

```js
const S=[[0,0,.3],[1,.3,.55],[0,.55,.8],[1,.8,1]],p=(t*0.2)%1,W=w-28;
S.forEach(([k,a,b])=>rr(c,14+a*W,16+k*30,(b-a)*W-3,18,K.sp[k],p>b?K.sp[k]:K.grid));
c.fillStyle=K.tx;c.fillRect(14+p*W,8,2,h-16);
```

## 기법 카드 (원본 459개 분석)

원본 `Edu/dayNN/animation.html` 51개의 애니메이션 459개를 기법별로 나눈 결과예요(데이터 `data/motion/anims.json` · `data/motion/techs.json`). 정적 그림(static)을 뺀 15가지를 카드로 보여줘요. 원본 CSS 애니메이션은 `@keyframes dots`(D1~34)와 `shake`(D35~51) 둘뿐이고, 나머지는 모두 JS 캔버스·DOM 모션이에요.

- 데모 코드는 대표 원본을 근거로 짧게 다시 짠 것이고 화면(`index.html`의 `CVT`)과 `techs.json`의 `demo` 필드가 같아요. 공통 헬퍼 `fit`·`grid`·`dot`·`txt`·`rr`·`K`·`ease`·`mulberry`·`gauss`·`clamp`·`DARK`·`RM`을 써요.
- "원본 N개"는 그 기법이 들어간 애니메이션 수, "주 기법"은 첫 번째 기법으로 분류된 수예요.
- 나오는 곳 링크는 `dashboard/dN/animation.html#해시`(대시보드판 원본)예요.

### 단계 진행 (`stepper`) — JS

- 원본 145개 · 주 기법 90개 · 49일
- 대표 출처: [D14 · 오늘의 흐름](../dashboard/d14/animation.html#flow) — `showRoad` (raf). Part 버튼으로 단계 상세가 바뀌고, 상단 히어로의 색 막대 다섯 개는 사인 값에 맞춰 rAF마다 길이가 오르내린다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#flow) · [D2](../dashboard/d2/animation.html#flow) · [D3](../dashboard/d3/animation.html#flow) · [D4](../dashboard/d4/animation.html#flow) · [D5](../dashboard/d5/animation.html#flow) · [D6](../dashboard/d6/animation.html#flow) · [D7](../dashboard/d7/animation.html#flow) · [D8](../dashboard/d8/animation.html#flow) · [D9](../dashboard/d9/animation.html#flow) · [D10](../dashboard/d10/animation.html#flow) · [D11](../dashboard/d11/animation.html#flow) · [D12](../dashboard/d12/animation.html#flow) · [D13](../dashboard/d13/animation.html#flow) · [D14](../dashboard/d14/animation.html#flow) · [D15](../dashboard/d15/animation.html#flow) · [D16](../dashboard/d16/animation.html#flow) · [D17](../dashboard/d17/animation.html#flow) · [D18](../dashboard/d18/animation.html#flow) · [D19](../dashboard/d19/animation.html#flow) · [D20](../dashboard/d20/animation.html#flow) · [D21](../dashboard/d21/animation.html#flow) · [D22](../dashboard/d22/animation.html#flow) · [D23](../dashboard/d23/animation.html#loop) · [D24](../dashboard/d24/animation.html#rpc) · [D25](../dashboard/d25/animation.html#turn) · [D26](../dashboard/d26/animation.html#ws) · [D27](../dashboard/d27/animation.html#proc) · [D28](../dashboard/d28/animation.html#barge) · [D29](../dashboard/d29/animation.html#session) · [D30](../dashboard/d30/animation.html#tools) · [D31](../dashboard/d31/animation.html#flow) · [D32](../dashboard/d32/animation.html#flow) · [D33](../dashboard/d33/animation.html#flow) · [D34](../dashboard/d34/animation.html#flow) · [D36](../dashboard/d36/animation.html#rules) · [D37](../dashboard/d37/animation.html#compare) · [D38](../dashboard/d38/animation.html#paths) · [D39](../dashboard/d39/animation.html#deid) · [D40](../dashboard/d40/animation.html#text) · [D41](../dashboard/d41/animation.html#judge) · [D42](../dashboard/d42/animation.html#layers) · [D44](../dashboard/d44/animation.html#flow) · [D45](../dashboard/d45/animation.html#flow) · [D46](../dashboard/d46/animation.html#flow) · [D47](../dashboard/d47/animation.html#flow) · [D48](../dashboard/d48/animation.html#flow) · [D49](../dashboard/d49/animation.html#flow) · [D50](../dashboard/d50/animation.html#flow) · [D51](../dashboard/d51/animation.html#flow)

원본 코드:

```js
function showRoad(i){const r=ROAD[i];[...$('road').children].forEach((b,j)=>b.setAttribute('aria-pressed',j===i));
cols.forEach((col,k)=>{const v=0.3+0.6*Math.abs(Math.sin(heroT*1.3+k*1.1));const bw=(w-40)/cols.length;c.fillStyle=css(col);c.globalAlpha=0.8;c.fillRect(20+k*bw,h-4-v*(h-8),bw-8,v*(h-8));
```

데모 코드:

```js
function stepper(c,w,h,t){const n=5,g=8,bw=(w-28-g*(n-1))/n,i=Math.floor(t/1.2)%n;
  for(let k=0;k<n;k++){const x=14+k*(bw+g),on=k===i,v=0.3+0.6*Math.abs(Math.sin(t*1.3+k*1.1));
    rr(c,x,22,bw,40,on?K.sp[k]:K.line,on?K.sp[k]+'33':DARK);txt(c,String(k+1),x+bw/2,47,on?K.tx:K.mu,14,on,'center');
    c.fillStyle=K.sp[k];c.globalAlpha=0.8;c.fillRect(x+bw*0.2,h-10-v*30,bw*0.6,v*30);c.globalAlpha=1;}
  txt(c,(i+1)+'단계',14,14,K.mu,11);}
```

### 슬라이더 즉시 반응 (`slider`) — JS

- 원본 186개 · 주 기법 68개 · 49일
- 대표 출처: [D13 · 양자화](../dashboard/d13/animation.html#quant) — `drawQt` (click). 비트 수 칩에 따라 -1~+1 구간을 2^b칸 눈금으로 다시 그리고 세 값의 원래 점과 양자화 점의 어긋남을 보여 준다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#sampling) · [D2](../dashboard/d2/animation.html#sampling) · [D3](../dashboard/d3/animation.html#sum) · [D4](../dashboard/d4/animation.html#snr) · [D5](../dashboard/d5/animation.html#data) · [D6](../dashboard/d6/animation.html#align) · [D7](../dashboard/d7/animation.html#arch) · [D8](../dashboard/d8/animation.html#quant) · [D9](../dashboard/d9/animation.html#der) · [D10](../dashboard/d10/animation.html#numbers) · [D11](../dashboard/d11/animation.html#kspon) · [D12](../dashboard/d12/animation.html#finetune) · [D13](../dashboard/d13/animation.html#prompt) · [D14](../dashboard/d14/animation.html#leaderboard) · [D15](../dashboard/d15/animation.html#fix) · [D16](../dashboard/d16/animation.html#hangul) · [D17](../dashboard/d17/animation.html#phonemes) · [D18](../dashboard/d18/animation.html#arch) · [D19](../dashboard/d19/animation.html#consent) · [D20](../dashboard/d20/animation.html#goals) · [D21](../dashboard/d21/animation.html#budget) · [D22](../dashboard/d22/animation.html#cost) · [D23](../dashboard/d23/animation.html#chunk) · [D24](../dashboard/d24/animation.html#voice) · [D25](../dashboard/d25/animation.html#card) · [D26](../dashboard/d26/animation.html#frame) · [D27](../dashboard/d27/animation.html#loop) · [D28](../dashboard/d28/animation.html#volume) · [D29](../dashboard/d29/animation.html#pipeline) · [D30](../dashboard/d30/animation.html#s2s) · [D31](../dashboard/d31/animation.html#upload) · [D32](../dashboard/d32/animation.html#perm) · [D33](../dashboard/d33/animation.html#path) · [D34](../dashboard/d34/animation.html#itn) · [D35](../dashboard/d35/animation.html#cosine) · [D38](../dashboard/d38/animation.html#bleu) · [D39](../dashboard/d39/animation.html#vad) · [D40](../dashboard/d40/animation.html#dataq) · [D41](../dashboard/d41/animation.html#wer) · [D42](../dashboard/d42/animation.html#quant) · [D43](../dashboard/d43/animation.html#alert) · [D44](../dashboard/d44/animation.html#budget) · [D45](../dashboard/d45/animation.html#noise) · [D46](../dashboard/d46/animation.html#slot) · [D47](../dashboard/d47/animation.html#amdahl) · [D48](../dashboard/d48/animation.html#fuzzy) · [D49](../dashboard/d49/animation.html#speech) · [D50](../dashboard/d50/animation.html#endpoint) · [D51](../dashboard/d51/animation.html#scope)

원본 코드:

```js
const L=Math.min(2**b,64),x0=30,x1=w-30,y=110;c.strokeStyle=css('--line');c.beginPath();c.moveTo(x0,y);c.lineTo(x1,y);c.stroke();
  for(let i=0;i<=L;i++){const x=x0+(x1-x0)*i/L;c.strokeStyle=css('--asr');c.beginPath();c.moveTo(x,y-10);c.lineTo(x,y+10);c.stroke();}
```

데모 코드:

```js
function slider(c,w,h,t){const b=1+Math.floor(t/0.8)%6,L=2**b,x0=20,x1=w-20,y=54;
  c.strokeStyle=K.line;c.lineWidth=1.5;c.beginPath();c.moveTo(x0,y);c.lineTo(x1,y);c.stroke();
  c.strokeStyle=K.sp[0];c.beginPath();for(let i=0;i<=L;i++){const x=x0+(x1-x0)*i/L;c.moveTo(x,y-10);c.lineTo(x,y+10);}c.stroke();
  c.fillStyle=K.line;c.fillRect(x0,h-22,x1-x0,4);dot(c,x0+(x1-x0)*(b-1)/5,h-20,7,K.sp[1],8);
  txt(c,b+'비트 · '+L+'칸',x0,20,K.tx,12,true);}
```

### 막대 자라기·게이지 (`bargrow`) — JS

- 원본 105개 · 주 기법 51개 · 44일
- 대표 출처: [D47 · 카드로 목표 맞추기](../dashboard/d47/animation.html#report) — `STG.report.draw` (raf). 카드 선택에 따라 처리 시간·비용 막대가 새 값으로 부드럽게 변하고 목표 달성 체크가 바뀐다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#mic) · [D2](../dashboard/d2/animation.html#editor) · [D3](../dashboard/d3/animation.html#live) · [D4](../dashboard/d4/animation.html#norm) · [D5](../dashboard/d5/animation.html#data) · [D6](../dashboard/d6/animation.html#w2v) · [D7](../dashboard/d7/animation.html#arch) · [D8](../dashboard/d8/animation.html#bottleneck) · [D9](../dashboard/d9/animation.html#flow) · [D10](../dashboard/d10/animation.html#eval) · [D11](../dashboard/d11/animation.html#hfstream) · [D12](../dashboard/d12/animation.html#teacher) · [D13](../dashboard/d13/animation.html#targets) · [D14](../dashboard/d14/animation.html#latency) · [D15](../dashboard/d15/animation.html#ci) · [D16](../dashboard/d16/animation.html#duration) · [D17](../dashboard/d17/animation.html#duration) · [D18](../dashboard/d18/animation.html#cfg) · [D19](../dashboard/d19/animation.html#embed) · [D20](../dashboard/d20/animation.html#loud) · [D21](../dashboard/d21/animation.html#arch) · [D22](../dashboard/d22/animation.html#cost) · [D25](../dashboard/d25/animation.html#history) · [D26](../dashboard/d26/animation.html#stream) · [D28](../dashboard/d28/animation.html#volume) · [D32](../dashboard/d32/animation.html#graph) · [D33](../dashboard/d33/animation.html#nlms) · [D34](../dashboard/d34/animation.html#confirm) · [D36](../dashboard/d36/animation.html#events) · [D37](../dashboard/d37/animation.html#trap) · [D38](../dashboard/d38/animation.html#langid) · [D39](../dashboard/d39/animation.html#snr) · [D40](../dashboard/d40/animation.html#evalm) · [D41](../dashboard/d41/animation.html#stress) · [D42](../dashboard/d42/animation.html#layers) · [D43](../dashboard/d43/animation.html#trace) · [D44](../dashboard/d44/animation.html#budget) · [D45](../dashboard/d45/animation.html#menu) · [D46](../dashboard/d46/animation.html#report) · [D47](../dashboard/d47/animation.html#amdahl) · [D48](../dashboard/d48/animation.html#metric) · [D49](../dashboard/d49/animation.html#retest) · [D50](../dashboard/d50/animation.html#card) · [D51](../dashboard/d51/animation.html#scope)

원본 코드:

```js
RP.s=RM?m.sec:mix(RP.s,m.sec,dt*7);RP.cst=RM?m.cost:mix(RP.cst,m.cost,dt*7);
  const goals=[['① 처리 시간',m.sec<=RP0.sec/12,`${f1(m.sec)}초 (×${(RP0.sec/m.sec).toFixed(1)})`],['② 비용',m.cost<=RP0.cost/3,`${f1(m.cost)}원 (${(m.cost/RP0.cost*100).toFixed(0)}%)`],['③ 정확도',true,`CER ${m.cer}%`],['④ 서버 응답',m.gap<=0.1,`멈춤 ${m.gap}초`],['⑤ 내용',true,'결정 3 · 할 일 3']],n=goals.filter(g=>g[1]).length;
```

데모 코드:

```js
function bargrow(c,w,h,t,dt,st){const L=['처리 시간','비용','정확도'],k=Math.floor(t/1.6),
  tg=L.map((_,i)=>0.2+0.7*Math.abs(Math.sin(k*1.7+i*2.3)));
  st.v=(st.v||tg).map((v,i)=>RM?tg[i]:ease(v,tg[i],dt,7));
  L.forEach((nm,i)=>{const y=14+i*34,x=84,W=w-x-50;txt(c,nm,14,y+14,K.mu,12);
    rr(c,x,y,W,18,K.line,K.grid);rr(c,x,y,Math.max(12,W*st.v[i]),18,K.sp[i],K.sp[i]);
    txt(c,Math.round(st.v[i]*100)+'%',x+W+8,y+14,K.tx,12,true);});}
```

### 그래프 그려 나가기 (`plot`) — JS

- 원본 45개 · 주 기법 30개 · 27일
- 대표 출처: [D2 · 소리의 정체](../dashboard/d2/animation.html#sound) — `drawSine / drawDv / drawRd` (raf). 주파수·진폭 슬라이더로 사인파를 다시 그리고, 단계별 유도 캔버스에서 회전하는 원의 각도에 따라 사인 곡선이 이어 그려지며 라디안 유도도 같은 방식으로 재생된다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#sampling) · [D2](../dashboard/d2/animation.html#sound) · [D3](../dashboard/d3/animation.html#dft) · [D4](../dashboard/d4/animation.html#filter) · [D5](../dashboard/d5/animation.html#train) · [D8](../dashboard/d8/animation.html#quant) · [D12](../dashboard/d12/animation.html#lr) · [D13](../dashboard/d13/animation.html#lr) · [D15](../dashboard/d15/animation.html#curves) · [D16](../dashboard/d16/animation.html#vocoder) · [D18](../dashboard/d18/animation.html#prosody) · [D19](../dashboard/d19/animation.html#phone) · [D20](../dashboard/d20/animation.html#mos) · [D22](../dashboard/d22/animation.html#history) · [D30](../dashboard/d30/animation.html#phone) · [D32](../dashboard/d32/animation.html#compare) · [D33](../dashboard/d33/animation.html#path) · [D35](../dashboard/d35/animation.html#oppoint) · [D36](../dashboard/d36/animation.html#timeline) · [D38](../dashboard/d38/animation.html#simul) · [D39](../dashboard/d39/animation.html#vad) · [D40](../dashboard/d40/animation.html#steps) · [D41](../dashboard/d41/animation.html#stress) · [D42](../dashboard/d42/animation.html#load) · [D43](../dashboard/d43/animation.html#flow) · [D44](../dashboard/d44/animation.html#thresh) · [D48](../dashboard/d48/animation.html#pre)

원본 코드:

```js
(function dvLoop(){const now=performance.now(),dt=Math.min(0.05,(now-dvLast)/1000);dvLast=now;
if(active('sound')&&$('dvCv').clientWidth){if(dvRun)dvT+=dt;drawDv();}
const theta=dvCur<2?(dvT*Math.PI*0.6)%(2*Math.PI):2*Math.PI*f*(dvT%secs);
```

데모 코드:

```js
function plot(c,w,h,t){const r=Math.min(34,h/2-12),cx=14+r,cy=h/2,x0=cx+r+16,W=w-x0-14,th=(t*Math.PI*0.6)%(2*Math.PI),X=a=>x0+W*a/(2*Math.PI);
  c.strokeStyle=K.line;c.lineWidth=1.5;c.beginPath();c.arc(cx,cy,r,0,7);c.moveTo(x0,cy);c.lineTo(x0+W,cy);c.stroke();
  const px=cx+r*Math.cos(th),py=cy-r*Math.sin(th);
  c.strokeStyle=K.sp[4];c.lineWidth=2;c.beginPath();for(let a=0;a<=th;a+=0.05){const y=cy-r*Math.sin(a);a?c.lineTo(X(a),y):c.moveTo(X(a),y);}c.stroke();
  c.strokeStyle=K.mu;c.lineWidth=1;c.setLineDash([3,3]);c.beginPath();c.moveTo(px,py);c.lineTo(X(th),py);c.stroke();c.setLineDash([]);
  dot(c,px,py,4,K.sp[1],8);dot(c,X(th),py,4,K.sp[4],8);}
```

### 파형 (`wave`) — JS

- 원본 48개 · 주 기법 29개 · 31일
- 대표 출처: [D50 · 말하기 단계와 명료도](../dashboard/d50/animation.html#steps) — `STG.steps.draw` (raf). 목표 파형과 단계 수에 따라 거칠어진 파형이 시간에 따라 옆으로 흐르며 명료도(CER) 막대가 변한다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#mic) · [D2](../dashboard/d2/animation.html#channel) · [D3](../dashboard/d3/animation.html#sum) · [D4](../dashboard/d4/animation.html#snr) · [D5](../dashboard/d5/animation.html#feature) · [D11](../dashboard/d11/animation.html#pcm) · [D12](../dashboard/d12/animation.html#flow) · [D15](../dashboard/d15/animation.html#record) · [D16](../dashboard/d16/animation.html#vits) · [D18](../dashboard/d18/animation.html#flow) · [D19](../dashboard/d19/animation.html#snr) · [D20](../dashboard/d20/animation.html#flow) · [D21](../dashboard/d21/animation.html#flow) · [D22](../dashboard/d22/animation.html#flow) · [D23](../dashboard/d23/animation.html#flow) · [D24](../dashboard/d24/animation.html#flow) · [D25](../dashboard/d25/animation.html#flow) · [D26](../dashboard/d26/animation.html#flow) · [D28](../dashboard/d28/animation.html#flow) · [D29](../dashboard/d29/animation.html#flow) · [D30](../dashboard/d30/animation.html#flow) · [D31](../dashboard/d31/animation.html#endpoint) · [D32](../dashboard/d32/animation.html#resample) · [D36](../dashboard/d36/animation.html#prosody) · [D37](../dashboard/d37/animation.html#bottleneck) · [D39](../dashboard/d39/animation.html#snr) · [D40](../dashboard/d40/animation.html#flow) · [D43](../dashboard/d43/animation.html#mask) · [D44](../dashboard/d44/animation.html#stream) · [D45](../dashboard/d45/animation.html#noise) · [D50](../dashboard/d50/animation.html#endpoint)

원본 코드:

```js
const u=x/gw+now*0.05,v=stTarget(u)*(1-noise*0.55)+noise*0.75*(Math.sin(x*1.7+now*7)*0.5+Math.sin(x*0.63+now*3.1)*0.5);c.lineTo(x0+x,y-v*28);}c.stroke();};
  draw(84,0,K.sp[0],'만들려던 소리');draw(190,rough,cer<=20?K.ok:K.bad,`${st}단계로 만든 소리`);
```

데모 코드:

```js
function wave(c,w,h,t){const W=w-28,line=(y,noise,col)=>{c.strokeStyle=col;c.lineWidth=2;c.beginPath();
    for(let x=0;x<=W;x+=3){const u=x/W+t*0.2,v=Math.sin(u*Math.PI*6)*(1-noise*0.55)+noise*0.75*(Math.sin(x*1.7+t*7)*0.5+Math.sin(x*0.63+t*3.1)*0.5);
      x?c.lineTo(14+x,y-v*h*0.14):c.moveTo(14,y-v*h*0.14);}c.stroke();};
  line(h*0.3,0,K.sp[0]);line(h*0.74,0.5,K.sp[2]);
  txt(c,'만들려던 소리',14,12,K.mu,11);txt(c,'거칠어진 소리',14,h*0.52,K.mu,11);}
```

### 표·격자 채우기 (`tablefill`) — JS

- 원본 52개 · 주 기법 29개 · 29일
- 대표 출처: [D48 · 틀린 것을 읽는다](../dashboard/d48/animation.html#errors) — `STG.errors.draw` (raf). 정답과 들림 문장의 자모 칸이 0.12초마다 하나씩 나타나며 다른 칸이 빨갛게 표시된다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#cer) · [D2](../dashboard/d2/animation.html#channel) · [D5](../dashboard/d5/animation.html#conv) · [D6](../dashboard/d6/animation.html#ctcloss) · [D7](../dashboard/d7/animation.html#sizes) · [D9](../dashboard/d9/animation.html#trellis) · [D10](../dashboard/d10/animation.html#editdist) · [D11](../dashboard/d11/animation.html#manifest) · [D12](../dashboard/d12/animation.html#collator) · [D13](../dashboard/d13/animation.html#domain) · [D14](../dashboard/d14/animation.html#fair) · [D15](../dashboard/d15/animation.html#goals) · [D18](../dashboard/d18/animation.html#compare) · [D19](../dashboard/d19/animation.html#wm) · [D20](../dashboard/d20/animation.html#metrics) · [D23](../dashboard/d23/animation.html#chunk) · [D25](../dashboard/d25/animation.html#card) · [D26](../dashboard/d26/animation.html#tcpudp) · [D34](../dashboard/d34/animation.html#slots) · [D35](../dashboard/d35/animation.html#ident) · [D37](../dashboard/d37/animation.html#tokens) · [D38](../dashboard/d38/animation.html#bleu) · [D39](../dashboard/d39/animation.html#align) · [D40](../dashboard/d40/animation.html#mas) · [D41](../dashboard/d41/animation.html#regress) · [D42](../dashboard/d42/animation.html#cost) · [D45](../dashboard/d45/animation.html#receipt) · [D46](../dashboard/d46/animation.html#accept) · [D48](../dashboard/d48/animation.html#errors)

원본 코드:

```js
shown=RM?99:Math.floor(ER.t/0.12);
  const fs=wide?13:10.5,cw=Math.min(wide?34:22,(w-100)/Math.max(ja.length,jb.length)),x0=wide?92:66;
  txt(c,'정답',14,52,K.mu,fs);txt(c,a,14,74,K.ok,wide?18:14,true);txt(c,'들림',14,128,K.mu,fs);
```

데모 코드:

```js
function tablefill(c,w,h,t){const A=[...'오늘날씨어때요'],B=[...'오늘날시어대요'],n=A.length,cw=Math.min(30,(w-64)/n),shown=Math.floor((t%3)/0.15);
  txt(c,'정답',14,h/2-14,K.mu,11);txt(c,'들림',14,h/2+22,K.mu,11);
  for(let i=0;i<Math.min(n,shown);i++){const x=52+i*cw,bad=A[i]!==B[i];
    rr(c,x,h/2-32,cw-4,26,K.line,K.grid);txt(c,A[i],x+(cw-4)/2,h/2-14,K.ok,13,true,'center');
    rr(c,x,h/2+4,cw-4,26,bad?K.sp[2]:K.line,K.grid);txt(c,B[i],x+(cw-4)/2,h/2+22,bad?K.sp[2]:K.tx,13,true,'center');}}
```

### 재생 막대·타임라인 (`playhead`) — JS

- 원본 67개 · 주 기법 26개 · 36일
- 대표 출처: [D26 · batch vs streaming](../dashboard/d26/animation.html#stream) — `drawSt` (raf). 재생을 누르면 경과시간 따라 입력·batch·streaming 레인이 채워지고 20ms 프레임 조각이 하나씩 나타난다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#agent) · [D3](../dashboard/d3/animation.html#stft) · [D4](../dashboard/d4/animation.html#vad) · [D5](../dashboard/d5/animation.html#conv) · [D6](../dashboard/d6/animation.html#compare) · [D7](../dashboard/d7/animation.html#stamp) · [D8](../dashboard/d8/animation.html#engine) · [D9](../dashboard/d9/animation.html#stamps) · [D11](../dashboard/d11/animation.html#flow) · [D17](../dashboard/d17/animation.html#stream) · [D20](../dashboard/d20/animation.html#stream) · [D21](../dashboard/d21/animation.html#turn) · [D22](../dashboard/d22/animation.html#stream) · [D23](../dashboard/d23/animation.html#latency) · [D24](../dashboard/d24/animation.html#voice) · [D25](../dashboard/d25/animation.html#turn) · [D26](../dashboard/d26/animation.html#stream) · [D27](../dashboard/d27/animation.html#assemble) · [D28](../dashboard/d28/animation.html#turn) · [D29](../dashboard/d29/animation.html#pipeline) · [D30](../dashboard/d30/animation.html#dispatch) · [D31](../dashboard/d31/animation.html#loop) · [D32](../dashboard/d32/animation.html#rec) · [D34](../dashboard/d34/animation.html#silence) · [D36](../dashboard/d36/animation.html#flow) · [D37](../dashboard/d37/animation.html#duplex) · [D38](../dashboard/d38/animation.html#simul) · [D39](../dashboard/d39/animation.html#deid) · [D42](../dashboard/d42/animation.html#path) · [D43](../dashboard/d43/animation.html#flow) · [D44](../dashboard/d44/animation.html#stream) · [D46](../dashboard/d46/animation.html#slot) · [D47](../dashboard/d47/animation.html#profile) · [D49](../dashboard/d49/animation.html#speech) · [D50](../dashboard/d50/animation.html#latency) · [D51](../dashboard/d51/animation.html#demo)

원본 코드:

```js
c.fillStyle=css('--asr');c.fillRect(X(0),20,X(Math.min(now,L))-X(0),20);
for(let t=0;t<Math.min(now,L);t+=0.02){c.fillStyle=(Math.round(t/0.02)%2)?css('--s2s'):css('--net');c.fillRect(X(t),120,Math.max(1,X(0.016)-X(0)),20);}
(function loop(){stT=(performance.now()-t0)/1000*1.5;drawSt();if(stT<T)requestAnimationFrame(loop);
```

데모 코드:

```js
function playhead(c,w,h,t){const L=3,T=(t*1.2)%(L+1.5),now=Math.min(T,L),X=s=>52+(w-66)*s/L;
  txt(c,'입력',8,31,K.mu,11);txt(c,'batch',8,63,K.mu,11);txt(c,'stream',8,95,K.mu,11);
  c.fillStyle=K.sp[0];c.fillRect(X(0),20,X(now)-X(0),14);
  for(let s=0;s<now;s+=0.1){c.fillStyle=Math.round(s/0.1)%2?K.sp[3]:K.sp[4];c.fillRect(X(s),84,Math.max(1,X(0.08)-X(0)),14);}
  if(T>L){c.fillStyle=K.sp[1];c.fillRect(X(0),52,(X(L)-X(0))*Math.min(1,(T-L)/0.5),14);}
  c.fillStyle=K.tx;c.fillRect(X(now),12,2,h-20);}
```

### 도식 흐름 (`nodeflow`) — JS

- 원본 36개 · 주 기법 20개 · 25일
- 대표 출처: [D38 · 오늘의 흐름](../dashboard/d38/animation.html#flow) — `STG.flow.draw` (raf). 4초 주기로 환자 문장이 바뀌며 통역기 상자 안에서 언어 감지·받아쓰기·번역·합성 단계가 차례로 노란색으로 강조되고 말풍선이 환자와 직원 사이를 오간다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#tech) · [D5](../dashboard/d5/animation.html#net) · [D9](../dashboard/d9/animation.html#wxpipe) · [D10](../dashboard/d10/animation.html#pipeline) · [D13](../dashboard/d13/animation.html#adapters) · [D17](../dashboard/d17/animation.html#arch) · [D19](../dashboard/d19/animation.html#layers) · [D24](../dashboard/d24/animation.html#nxm) · [D26](../dashboard/d26/animation.html#rtc) · [D27](../dashboard/d27/animation.html#proc) · [D29](../dashboard/d29/animation.html#room) · [D30](../dashboard/d30/animation.html#handoff) · [D31](../dashboard/d31/animation.html#http) · [D34](../dashboard/d34/animation.html#states) · [D35](../dashboard/d35/animation.html#flow) · [D37](../dashboard/d37/animation.html#arch) · [D38](../dashboard/d38/animation.html#flow) · [D39](../dashboard/d39/animation.html#flow) · [D41](../dashboard/d41/animation.html#flow) · [D42](../dashboard/d42/animation.html#flow) · [D43](../dashboard/d43/animation.html#inject) · [D44](../dashboard/d44/animation.html#wake) · [D45](../dashboard/d45/animation.html#req) · [D48](../dashboard/d48/animation.html#decode) · [D49](../dashboard/d49/animation.html#layers)

원본 코드:

```js
STG.flow={draw(dt,now){const {c,w,h}=fit($('flCv'));grid(c,w,h);if(!RM)FL.t+=dt;const T=RM?1.6:FL.t,i=Math.floor(T/4)%FLS.length,ph=(T%4)/4,[lang,src,out]=FLS[i],wide=w>=640,en=lang==='en';
steps.forEach((s,k)=>txt(c,s,cx,py-8+k*17,ph>0.3&&ph<0.7&&k===st?K.th:K.mu,12,ph>0.3&&ph<0.7&&k===st,'center'));
```

데모 코드:

```js
function nodeflow(c,w,h,t){const ph=(t%4)/4,S=['언어 감지','받아쓰기','번역','합성'],k=Math.min(3,Math.floor(ph*4)),
  bw=Math.min(96,w*0.26),y=h/2-18,xs=[14,w/2-bw/2,w-14-bw],nm=['환자','','직원'];
  c.strokeStyle=K.line;c.lineWidth=1.5;c.beginPath();c.moveTo(xs[0]+bw,h/2);c.lineTo(xs[1],h/2);c.moveTo(xs[1]+bw,h/2);c.lineTo(xs[2],h/2);c.stroke();
  xs.forEach((x,i)=>{rr(c,x,y,bw,36,i===1?K.sp[1]:K.line,DARK);txt(c,i===1?S[k]:nm[i],x+bw/2,y+23,i===1?K.sp[1]:K.tx,12,i===1,'center');});
  txt(c,'통역기',w/2,y-8,K.mu,11,false,'center');
  const u=ph<0.5?ph*2:(ph-0.5)*2,a=ph<0.5?xs[0]+bw:xs[1]+bw,b=ph<0.5?xs[1]:xs[2];dot(c,a+(b-a)*u,h/2,4,K.sp[0],10);}
```

### 점 분포·군집 (`scatter`) — JS

- 원본 23개 · 주 기법 20개 · 16일
- 대표 출처: [D50 · 문지기와 문턱값](../dashboard/d50/animation.html#verify) — `STG.verify.draw` (raf). 등록 작업자와 외부인 점수 점이 위아래로 일렁이고 문턱 슬라이더에 따라 거절/수락 영역과 오류 수가 바뀐다.
- 나오는 곳: [D6](../dashboard/d6/animation.html#ssl) · [D9](../dashboard/d9/animation.html#embed) · [D11](../dashboard/d11/animation.html#landscape) · [D20](../dashboard/d20/animation.html#utmos) · [D21](../dashboard/d21/animation.html#pct) · [D23](../dashboard/d23/animation.html#search) · [D25](../dashboard/d25/animation.html#latency) · [D26](../dashboard/d26/animation.html#jitter) · [D35](../dashboard/d35/animation.html#space) · [D36](../dashboard/d36/animation.html#baseline) · [D39](../dashboard/d39/animation.html#pseudo) · [D43](../dashboard/d43/animation.html#sample) · [D44](../dashboard/d44/animation.html#quant) · [D48](../dashboard/d48/animation.html#shake) · [D50](../dashboard/d50/animation.html#verify) · [D51](../dashboard/d51/animation.html#interp)

원본 코드:

```js
dot(c,X(v),yW+Math.sin(now*1.7+i*1.3)*(RM?0:9)+(i%3-1)*7,bad?7:5.5,bad?K.bad:K.tgt,bad?14:6);});
  d.x.forEach((v,i)=>{const bad=v>=th;dot(c,X(v),yX+Math.sin(now*1.5+i*2.1)*(RM?0:9)+(i%3-1)*7,bad?7:5.5,bad?K.bad:K.non,bad?14:6);
```

데모 코드:

```js
function scatter(c,w,h,t){const r=mulberry(3),th=0.5+0.2*Math.sin(t*0.7),X=v=>14+v*(w-28);
  c.strokeStyle=K.tx;c.lineWidth=1;c.setLineDash([4,4]);c.beginPath();c.moveTo(X(th),8);c.lineTo(X(th),h-8);c.stroke();c.setLineDash([]);
  txt(c,'등록',14,14,K.mu,11);txt(c,'외부인',14,h-6,K.mu,11);
  for(let i=0;i<24;i++){const reg=i<12,v=clamp((reg?0.68:0.32)+gauss(r)*0.13,0,1),bad=reg?v<th:v>=th,
    y=(reg?h*0.34:h*0.68)+Math.sin(t*1.6+i*1.3)*6;dot(c,X(v),y,bad?6:4.5,bad?K.sp[2]:K.sp[reg?0:4],bad?12:4);}}
```

### 스펙트로그램·히트맵 (`heatmap`) — JS

- 원본 25개 · 주 기법 14개 · 14일
- 대표 출처: [D3 · 시간-주파수 트레이드오프](../dashboard/d3/animation.html#live) — `loopLive` (raf). 마이크/데모 소리의 주파수 분석 결과를 한 열(2px)씩 오른쪽으로 칠해 시간-주파수 트레이드오프를 실시간 스펙트로그램으로 보여준다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#mic) · [D3](../dashboard/d3/animation.html#stft) · [D4](../dashboard/d4/animation.html#snr) · [D5](../dashboard/d5/animation.html#feature) · [D6](../dashboard/d6/animation.html#ctcloss) · [D9](../dashboard/d9/animation.html#trellis) · [D11](../dashboard/d11/animation.html#features) · [D13](../dashboard/d13/animation.html#lora) · [D16](../dashboard/d16/animation.html#mel) · [D17](../dashboard/d17/animation.html#voicepack) · [D18](../dashboard/d18/animation.html#f5) · [D33](../dashboard/d33/animation.html#snr) · [D39](../dashboard/d39/animation.html#align) · [D40](../dashboard/d40/animation.html#loss)

원본 코드:

```js
for(let y=0;y<h;y++){const bin=Math.floor((1-y/h)*maxBin);const v=fd[bin]/255;c.fillStyle=`hsl(${260-v*220},85%,${5+v*58}%)`;c.fillRect(lx,y,2,1);}lx+=2;
```

데모 코드:

```js
function heatmap(c,w,h,t){const cw=4,n=Math.floor((w-28)/cw),bins=24,bh=(h-16)/bins;
  for(let j=0;j<n;j++){const tt=t*4-(n-j)*0.15,f=bins*(0.3+0.2*Math.sin(tt*0.5));
    for(let b=0;b<bins;b++){const v=clamp(Math.exp(-((b-f)**2)/6)+0.5*Math.exp(-((b-2*f)**2)/10)+0.1*(Math.sin(tt*3+b*1.7)+1)/2,0,1);
      c.fillStyle=`hsl(${260-v*220},85%,${5+v*58}%)`;c.fillRect(14+j*cw,h-8-(b+1)*bh,cw,bh+0.5);}}}
```

### 입자 흐름 (`particle`) — JS

- 원본 19개 · 주 기법 11개 · 10일
- 대표 출처: [D42 · 마이크로 배치](../dashboard/d42/animation.html#batch) — `STG.batch.draw` (raf). 요청이 도착률대로 큐에 쌓이다 배치 크기·대기 시간 조건이 되면 묶여서 GPU 상자에서 처리된다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#tech) · [D27](../dashboard/d27/animation.html#flow) · [D35](../dashboard/d35/animation.html#eer) · [D36](../dashboard/d36/animation.html#emotion) · [D37](../dashboard/d37/animation.html#flow) · [D39](../dashboard/d39/animation.html#flow) · [D41](../dashboard/d41/animation.html#flow) · [D42](../dashboard/d42/animation.html#quant) · [D43](../dashboard/d43/animation.html#inject) · [D49](../dashboard/d49/animation.html#layers)

원본 코드:

```js
if(!MB.busy&&MB.q.length&&(MB.q.length>=B||MB.q[0].t>=W||B===1)){const n=Math.min(B,MB.q.length);MB.q.splice(0,n);MB.busy={n,left:svc(n),tot:svc(n)};}}
  const gx=w-(wide?210:130),gy=h/2-60,gw=wide?190:116,gh=120,qx1=gx-24;
```

데모 코드:

```js
function particle(c,w,h,t){const B=4,gap=0.3,tr=0.6,gx=w-90,gy=h/2-24,qx=gx-20,k0=Math.floor(t/gap);
  rr(c,gx,gy,76,48,K.sp[3],DARK);txt(c,'GPU',gx+38,gy+29,K.sp[3],12,true,'center');txt(c,'배치 '+B+'개씩',14,14,K.mu,11);
  for(let k=Math.max(0,k0-12);k<=k0;k++){const a=k*gap,i=k%B,go=(Math.floor(k/B)*B+B-1)*gap+tr,y=h/2+(i-1.5)*9;let x;
    if(t<a+tr)x=14+(qx-i*10-14)*(t-a)/tr;else if(t<go)x=qx-i*10;else if(t<go+0.3)x=qx-i*10+(gx+38-qx+i*10)*(t-go)/0.3;else continue;
    dot(c,x,y,3.5,K.sp[Math.floor(k/B)%5],8);}}
```

### 퀴즈 선택 피드백 (`quiz`) — JS·DOM

- 원본 12개 · 주 기법 12개 · 11일
- 대표 출처: [D31 · 상태 코드](../dashboard/d31/animation.html#status) — `(stList onclick)` (click). 상태 코드 버튼을 누르면 정답이면 right, 오답이면 wrong 클래스로 표시되고 정답이 공개된다.
- 나오는 곳: [D2](../dashboard/d2/animation.html#libs) · [D31](../dashboard/d31/animation.html#status) · [D32](../dashboard/d32/animation.html#recap) · [D33](../dashboard/d33/animation.html#recap) · [D34](../dashboard/d34/animation.html#recap) · [D35](../dashboard/d35/animation.html#recap) · [D36](../dashboard/d36/animation.html#recap) · [D37](../dashboard/d37/animation.html#recap) · [D38](../dashboard/d38/animation.html#recap) · [D39](../dashboard/d39/animation.html#recap) · [D40](../dashboard/d40/animation.html#recap)

원본 코드:

```js
$('stList').querySelectorAll('.scen').forEach(s=>s.querySelectorAll('button').forEach(b=>b.onclick=()=>{const a=ST[+s.dataset.i][1];s.querySelectorAll('button').forEach(x=>x.className='');b.className=(+b.dataset.c===a)?'right':'wrong';
```

데모 코드:

```js
function quiz(box){box.innerHTML='<div class="scen"><div class="q">없는 주소를 요청하면?</div><div class="opts"><button type="button" data-c="0">200 OK</button><button type="button" data-c="1">404 Not Found</button><button type="button" data-c="2">500 Server Error</button></div></div>';
  const s=box.firstChild,ans=1;
  s.querySelectorAll('button').forEach(b=>b.onclick=()=>{s.querySelectorAll('button').forEach(x=>x.className='');
    b.className=+b.dataset.c===ans?'right':'wrong';
    if(b.className==='wrong'){s.classList.remove('shk');void s.offsetWidth;s.classList.add('shk');}});}
```

### 맥동·퍼지는 원 (`pulse`) — JS

- 원본 20개 · 주 기법 8개 · 12일
- 대표 출처: [D41 · 평가의 세 단계](../dashboard/d41/animation.html#pyramid) — `STG.pyramid.draw` (raf). 실패 유형을 고르면 3단 피라미드 중 잡아낸 단이 초록색으로 깜빡인다.
- 나오는 곳: [D13](../dashboard/d13/animation.html#flow) · [D27](../dashboard/d27/animation.html#loop) · [D29](../dashboard/d29/animation.html#session) · [D35](../dashboard/d35/animation.html#flow) · [D37](../dashboard/d37/animation.html#tokens) · [D41](../dashboard/d41/animation.html#pyramid) · [D42](../dashboard/d42/animation.html#cost) · [D43](../dashboard/d43/animation.html#pillars) · [D45](../dashboard/d45/animation.html#req) · [D47](../dashboard/d47/animation.html#loop) · [D50](../dashboard/d50/animation.html#fuzzy) · [D51](../dashboard/d51/animation.html#tutor)

원본 코드:

```js
pulse=hit&&!RM?0.5+0.5*Math.sin(now*4):1;rr(c,x,y,bw,80,hit?K.ok:K.line,hit?`rgba(87,224,138,${(0.08+0.1*pulse).toFixed(2)})`:DARK);
    txt(c,nm,x+14,y+26,hit?K.ok:K.tx,wide?16:13.5,true);if(wide||i>0)txt(c,qn,x+(wide?70:54),y+26,K.tx,wide?13:10.5);
```

데모 코드:

```js
function pulse(c,w,h,t){const L=['단위','통합','종단'],hit=Math.floor(t/2)%3,p=0.5+0.5*Math.sin(t*4);
  L.forEach((nm,i)=>{const bw=(w-28)*(0.4+0.3*i),x=w/2-bw/2,y=8+i*36,on=i===hit;rr(c,x,y,bw,30,on?K.ok:K.line,DARK);
    if(on){c.globalAlpha=0.12+0.3*p;c.fillStyle=K.ok;c.beginPath();c.roundRect(x,y,bw,30,6);c.fill();c.globalAlpha=1;}
    txt(c,nm,w/2,y+20,on?K.ok:K.tx,12,true,'center');});}
```

### 글자·토큰 스트리밍 (`typing`) — JS

- 원본 25개 · 주 기법 7개 · 19일
- 대표 출처: [D18 · AR vs NAR](../dashboard/d18/animation.html#arnar) — `drawAn` (raf). 재생하면 rAF로 시간이 흘러 위쪽 AR 줄은 토큰 칸이 하나씩 늘어나 STOP에서 멈추고, 아래쪽 NAR 격자는 한꺼번에 잡음에서 선명해진다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#tech) · [D6](../dashboard/d6/animation.html#compare) · [D7](../dashboard/d7/animation.html#tokens) · [D8](../dashboard/d8/animation.html#agree) · [D9](../dashboard/d9/animation.html#minutes) · [D10](../dashboard/d10/animation.html#prompt) · [D18](../dashboard/d18/animation.html#arnar) · [D22](../dashboard/d22/animation.html#stream) · [D23](../dashboard/d23/animation.html#loop) · [D24](../dashboard/d24/animation.html#rpc) · [D26](../dashboard/d26/animation.html#ws) · [D27](../dashboard/d27/animation.html#svc) · [D29](../dashboard/d29/animation.html#token) · [D30](../dashboard/d30/animation.html#tools) · [D41](../dashboard/d41/animation.html#sim) · [D45](../dashboard/d45/animation.html#flow) · [D46](../dashboard/d46/animation.html#engine) · [D48](../dashboard/d48/animation.html#errors) · [D49](../dashboard/d49/animation.html#speech)

원본 코드:

```js
function anLoop(){anT+=RM?100:0.25;drawAn();if(anT<34&&!RM)anRaf=requestAnimationFrame(anLoop);
const shown=Math.min(L+1,Math.floor(anT*1.0));
const step=Math.min(AN_NFE,Math.max(0,Math.floor((anT-2)*AN_NFE/30)));const a=1-step/AN_NFE;
```

데모 코드:

```js
function typing(c,w,h,t){const T=t%6,tk=[...'안녕하세요'],n=tk.length,shown=Math.min(n,Math.floor(T*1.5)),cw=Math.min(34,(w-70)/n),a=1-Math.min(1,T/4),r=mulberry(Math.floor(T*8));
  txt(c,'AR',14,36,K.mu,11,true);txt(c,'NAR',14,86,K.mu,11,true);
  for(let i=0;i<n;i++){const x=56+i*cw,m=(cw-4)/2;
    if(i<shown){rr(c,x,18,cw-4,26,K.sp[0],K.grid);txt(c,tk[i],x+m,36,K.tx,13,true,'center');}
    rr(c,x,68,cw-4,26,K.sp[3],K.grid);c.globalAlpha=1-a;txt(c,tk[i],x+m,86,K.tx,13,true,'center');
    c.globalAlpha=a;for(let j=0;j<6;j++)dot(c,x+r()*(cw-4),68+r()*26,1.5,K.mu);c.globalAlpha=1;}}
```

### 부드럽게 따라가기 (`easemove`) — JS

- 원본 39개 · 주 기법 6개 · 20일
- 대표 출처: [D46 · 본인 확인과 넘기기](../dashboard/d46/animation.html#guard) — `STG.guard.draw` (raf). 질문 상자에서 판정 상자로 선이 뻗고 결과 문장이 투명도 0→1로 서서히 나타난다.
- 나오는 곳: [D1](../dashboard/d1/animation.html#stack) · [D2](../dashboard/d2/animation.html#sound) · [D3](../dashboard/d3/animation.html#dft) · [D5](../dashboard/d5/animation.html#train) · [D11](../dashboard/d11/animation.html#hfstream) · [D27](../dashboard/d27/animation.html#dir) · [D35](../dashboard/d35/animation.html#cosine) · [D36](../dashboard/d36/animation.html#prosody) · [D37](../dashboard/d37/animation.html#tokens) · [D38](../dashboard/d38/animation.html#langid) · [D39](../dashboard/d39/animation.html#split) · [D40](../dashboard/d40/animation.html#evalm) · [D44](../dashboard/d44/animation.html#quant) · [D45](../dashboard/d45/animation.html#menu) · [D46](../dashboard/d46/animation.html#guard) · [D47](../dashboard/d47/animation.html#amdahl) · [D48](../dashboard/d48/animation.html#metric) · [D49](../dashboard/d49/animation.html#report) · [D50](../dashboard/d50/animation.html#quant) · [D51](../dashboard/d51/animation.html#peer)

원본 코드:

```js
GD.a=RM?1:mix(GD.a,1,dt*2.5);
  bubble(c,14,20,w-28,'👤 '+S[1],true,K.sp[1],wide?15:12);const gx=w/2-(wide?110:80),gw=wide?220:160;rr(c,gx,96,gw,70,good?K.ok:K.bad,good?'rgba(87,224,138,.12)':'rgba(255,107,107,.12)');
```

데모 코드:

```js
function easemove(c,w,h,t,dt,st){const cyc=Math.floor(t/3);if(st.c!==cyc){st.c=cyc;st.a=0;}st.a=RM?1:ease(st.a,1,dt,2.5);
  const bw=Math.min(110,w*0.3),x0=14+bw,x1=w-14-bw;
  rr(c,14,h/2-18,bw,36,K.sp[1],DARK);txt(c,'질문',14+bw/2,h/2+5,K.tx,12,true,'center');
  c.strokeStyle=K.line;c.lineWidth=2;c.beginPath();c.moveTo(x0,h/2);c.lineTo(x0+(x1-x0)*st.a,h/2);c.stroke();
  c.globalAlpha=st.a;rr(c,x1,h/2-18,bw,36,K.ok,DARK);txt(c,'통과',x1+bw/2,h/2+5,K.ok,12,true,'center');c.globalAlpha=1;}
```
