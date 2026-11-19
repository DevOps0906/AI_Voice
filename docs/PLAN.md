# AI_Voice 학습 대시보드 — 기획 + 디자인 시안 계획

## Context
사용자가 수강 중인 "음성 AI 전문가 과정(160h)" 레포(D:\WorkSpace\DEV\AI_Voice, upstream imguru-mooc/AI_Voice의 fork)를
일차별 학습 대시보드로 묶으려 한다. 이번 범위는 **기획 문서 + 디자인 시안까지**이고, 구현(extract.py·dashboard)은
사용자가 시안을 확정한 뒤 시작한다. 레포는 이미 로컬에 있으므로 별도 clone(`ref/`)은 하지 않는다.

## 1. 분석 결과 (검증 완료, 붙여 넣은 내용과 다른 점 표시)
- 44일 = M1~M9(M9만 4일). 모든 일차: animation.html · worksheet.html · slides.pdf · _실습.ipynb.
  없는 파일: 강사용 노트북 D1~3·D7, pptx D7.
- 디자인 두 세대: D1~34 가로 탭(IBM Plex Sans KR, `--bg` 팔레트) / D35~44 레일형(Gothic A1, `--page` 팔레트).
- **D1** "음성 AI 첫걸음: 기술 지형도 & 개발환경 구축" · 1주차 M1 · 목표 4 · Part 0~7 · 빈칸 6 · 오늘 배운 것 6행 · 과제 3 · 워크시트 15문항(Part별, mc4·match3·order3·ox2·num2·multi1).
  애니메이션 해시 flow·tech·stack·file·sampling·mic·asr·cer·agent — ✅ 맞음(내부 탭 id는 p0~p8이고 HASH 표로 변환). ROAD 6개.
- **D10** "ASR 평가 + 미니 프로젝트: WER·CER·한국어 정규화·자동 회의록 생성기" · 2주차 M2 · 금요일 미니PJ · 목표 5 · Part 0~6 · 빈칸 9칸(10개) · 오늘 배운 것 9행(개념|한 줄 정리|코드) · 과제 3 · 워크시트 4교시×10(JSON, 정답·해설 포함). ROAD 5개(+more 링크).
- 교시표에는 시각이 없고 "N교시 → Part 범위"만 있다 → 타임라인 막대는 4등분 + Part 매핑으로 그린다.
- day42 원본: 레일 236px, 분기점 900/820/760px (지시서 248/212·1200/768은 **우리 3구간 규칙으로 의도적 변경**).
  day42 `<title>`이 D41 제목으로 잘못 들어가 있음(원본 버그, 우리는 노트북 제목 사용).
- 워크시트 형식이 두 가지(D1 JS 리터럴·Part별 / D10 strict JSON·교시별) → extract.py에 파서 2종 + 정규화 필요.

## 2. 기획 내용 (planner가 docs/PLAN.md로 작성)
- 목적: 수강생이 그날의 흐름·목표·자료·과제·복습 퀴즈를 한 화면에서 보고, 원본(github.io 애니메이션·Colab)으로 1클릭 이동.
- 사용자: 본인(복습·진도). 원본 콘텐츠는 복제하지 않고 링크로 연결.
- 데이터 흐름: `dayNN/*_실습.ipynb + animation.html + worksheet.html` → `scripts/extract.py` → `data/dayNN.json`, `data/course.json` → `dashboard/index.html`(정적 단일 HTML, fetch).
- dayNN.json 필드: title, meta{week,module,hours,tag}, goals[], periods[{n,topic,parts}], parts[{n,title}], blanks, anims[{hash,title,desc}], road[], learned[{concept,summary,code}], homework[], worksheet{format,groups[{title,qs[]}]}, files[{name,size,url,colab}].
- 화면 표(03_SCREENS_UX 형식, 9탭 + 공통 레일):

| ID | 탭 | 핵심 내용 | 상태 |
|---|---|---|---|
| S0 | 과정 지도 `#map` | 9주×일차 노선도, 준비됨/준비 중, 클릭→일차 이동 | 정상·준비 중 일차 |
| S1 | 오늘의 흐름 `#dN-flow` | scope 캔버스(D1 마이크→STT→LLM→TTS→스피커, D10 녹음→받아쓰기·정렬→화자분리→LLM요약→회의록), KPI 카드, ROAD 로드맵, ▶ 시연 | 재생/정지/동작 줄이기 |
| S2 | 목표·교시 `#dN-goals` | 목표 계단식 등장, 1~4교시 막대 + Part 매핑 | — |
| S3 | 애니메이션 9종 `#dN-anim` | github.io animation.html#해시 카드 | — |
| S4 | 수업 자료 `#dN-files` | pdf·pptx·ipynb(GitHub+Colab)·html, 없는 파일은 "없음" | 파일 누락 |
| S5 | 오늘 배운 것 `#dN-learned` | 개념 표(코드 열은 있으면 표시) | — |
| S6 | 과제·진도 `#dN-tasks` | 체크리스트+진행 막대, localStorage(try/catch) | 저장 불가 시 안내 |
| S7 | 정리 퀴즈 `#dN-quiz` | 원본 워크시트 문항, 오답 shake+해설 | 미응답·정답·오답 |
| S8 | 모션 레퍼런스 `#motion` | 효과 21+4종 라이브 데모·명칭·코드 복사 | 동작 줄이기 |

## 3. 디자인 시안 (/design 절차)
브리프: 대상 수강생 본인 / 주된 일 오늘 일차 파악 후 원본 이동 / 분위기 계측기·차분한·정밀한 /
기준 day42 레일·scope·Gothic A1·토큰 그대로(새 색 금지) / 피할 것 원본 복제·장식 그라데이션·가로 탭 혼용·실측처럼 보이는 예시 숫자("수업용 예시 값" 표기).

- 토큰: `design/tokens.css` = day42 라이트·다크 13색 + `--scope #0A1024` + 3구간 타입 토큰
  (데스크톱 1200+: 레일 248·본문 16·h2 2.05rem·로드맵 6열 / 태블릿 768~1199: 212·15·1.75rem·3열 / 모바일 ~767: 상단 가로 탭·14.5·1.45rem·2열·터치 44px).
- 데스크톱 와이어(S1):
```
┌ rail 248 ────────┬ main (max 1120) ─────────────────────────┐
│ 음성 AI 전문가 과정│ D1 · 1주차 M1 · 4시간                       │
│ [D1 ▾] D10 …준비중│ h2 음성 AI 첫걸음                            │
│ ① 과정 지도      │ ┌ scope (dark) ─────────────────────────┐ │
│ │                │ │ 🎤 → STT → LLM → TTS → 🔊  (입자 흐름)   │ │
│ ② 오늘의 흐름 ●  │ └ 수업용 예시 값 ──────────── ▶ 시연 보기 ┘ │
│ │ … ⑨ 모션       │ [KPI 300ms][700ms][400ms][합계]            │
│ ─────────────    │ 로드맵: Part1 … Part6 (6열 카드, 위쪽 4px 띠)│
│ ☀/☾  ← → 탭 이동 │                                            │
└──────────────────┴────────────────────────────────────────────┘
```
- 모바일: 레일 → 상단 가로 스크롤 탭(번호 원 26px, 연결선 숨김), 로드맵 2열, 360px 가로 스크롤 0.
- 산출: `design/tokens.css`, `design/preview.html`(design-preview 자동), `design/wireframes/index.html`(plan2spec), 375·768·1280·1440 스크린샷.

## 4. 실행 순서 (승인 후)
0. `nomad-doctor . --fix` (승인됨) → tasks/·AGENTS.md·CLAUDE.md·.gitignore 생성/병합.
1. planner(sonnet): `docs/PLAN.md`(1·2장 내용) + 화면 표 작성.
2. `plan2spec` → wireframes 초안. 🔴 있으면 기획 수정.
3. designer + codex-designer 공동 → tokens.css, 교차 검토 1회.
4. `design-preview design/tokens.css --check` → `plan2spec` → `shot design/wireframes`.
5. **사용자 확정 대기** (여기서 이번 범위 종료).
6. 확정 후 tasks/README.md 작업·위험도:
   T1 extract.py+JSON(보통/sonnet) · T2 레일·라우팅·테마 셸(보통) · T3 scope 캔버스·시연(보통) · T4 S2~S7 탭(보통) · T5 모션 레퍼런스+docs/motion-reference.md(낮음/haiku) · T6 Playwright 3폭·콘솔 0건(낮음, tester).
   높음 없음(외부 API·인증·결제 없음, 정적 페이지).

## 5. 검증
- design-preview --check 대비·토큰 우회 ❌ 0, shot 4폭 스크린샷 육안 확인, 360px 가로 스크롤 없음.
- 기획 문서의 D1/D10 수치(목표 4/5, Part 0~7/0~6, 빈칸 6/9, 문항 15/40)가 노트북과 일치.

## 6. 사용자 결정 (2026-11-19)
- 이번 범위: **D1·D10만 구현**. 디자인 확정 대기 단계는 사용자 지시로 생략하고 바로 구현.
- **애니메이션은 원본과 동일해야 한다.** 방식:
  - `dashboard/d1/animation.html`, `dashboard/d10/animation.html` = 원본 `day01|day10/animation.html`을 day42 레일 디자인으로 다시 입힌 것.
    `<script>` 안 애니메이션 로직(캔버스 그리기·상태·ROAD·해시 표·탭 id)은 **원본 그대로 복사**하고, 바뀌는 것은 껍데기(HTML 구조·CSS·폰트·테마 토글)뿐.
    원본 CSS 변수(`--bg` 등)를 JS가 읽으면 같은 이름 별칭을 day42 토큰에 연결해 둔다.
  - 해시(D1: flow·tech·stack·file·sampling·mic·asr·cer·agent / D10: flow·editdist·wercer·norm·numbers·pipeline·prompt·eval·demo)는 원본과 같다.
  - 대시보드 S3 "애니메이션 9종" 탭은 이 페이지를 iframe/링크로 연다.
- 서빙: 레포 루트에서 `python -m http.server` → `/dashboard/index.html` (data/*.json fetch).

## 7. 데이터 계약 (data/dayNN.json)
```json
{"day":1,"title":"…","meta":{"week":1,"module":"M1","hours":4,"tag":""},
 "goals":["…"],"periods":[{"n":1,"topic":"…","parts":"Part 0"}],
 "parts":[{"n":0,"title":"…"}],"blanks":6,
 "anims":[{"hash":"flow","title":"오늘의 흐름","desc":""}],
 "road":[{"p":"Part 1","t":"…","c":"…","go":"stack","items":["…"],"q":"…"}],
 "learned":[{"concept":"…","summary":"…","code":""}],"homework":["…"],
 "worksheet":{"source":"day01/worksheet.html","groups":[{"title":"Part 0","qs":[{"ty":"mc","p":"…","o":["…"],"a":0,"w":"해설"}]}]},
 "files":[{"name":"…","kind":"pdf","size":123,"url":"https://github.com/imguru-mooc/AI_Voice/blob/main/day01/…","colab":null,"pages":null}]}
```
course.json: `[{"day":1,"week":1,"module":"M1","title":"음성AI 첫걸음","ready":true}, …44개]` (ready = D1·D10만 true).
퀴즈 정규화: 원본 타입(mc·ox·match·order·multi·num)을 `ty`로 유지, 정답 `a`, 해설 `w`(D1의 `e`→`w`).
