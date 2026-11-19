# 모션 레퍼런스

`dashboard/index.html`의 S8 탭(`#motion`)에 있는 효과 목록이에요. 화면의 코드와 이 문서의 코드는 같아요(실제로 동작하는 CSS).

- CSS 효과 21종 + scope 헬퍼 4종.
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

## scope 헬퍼

원본 `day42/animation.html`의 헬퍼를 그대로 쓴 것이에요.

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
