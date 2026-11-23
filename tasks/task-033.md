# task-033 — 글꼴 Pretendard 통일 · 결과값 글자 크기 고정

- 위험도: 낮음(스타일만, 45개 재생성이라 sonnet) · 담당: builder(sonnet) · 선행: 032

## 결정(사용자 확인 2026-11-23)
- 본문·결과값·숫자·슬라이더 값·큰 숫자(.big)·캔버스 글자 모두 Pretendard. **코드 상자(pre·code)만 고정폭 유지.**
- 결과값(.kv b, .kv b.s, label.sl output, .big 등 결과를 보여 주는 값)은 "손님의 말"(.ctl h3, 0.9rem) 크기로 고정. 굵기 600~700, tabular-nums 유지, 줄간격 1.45 내외로 읽기 좋게.
- 적용: 1~45일 애니메이션 전체(reskin.py 일괄 재생성) + dashboard/index.html의 코드 아닌 모노 글꼴.

## 근거
- d45 예: `.kv b{font-size:1.22rem;font-weight:900}` · `.big,.kv b,label.sl output{font-family:var(--font-mono)}` (reskin 덮어쓰기 CSS) · `.ctl h3{font-size:.9rem}`
- `scripts/reskin.py` 덮어쓰기 CSS · `design/tokens.css`(--font-sans·--text-*) · `tasks/NOW.md` 주의(reskin all은 1~44 → 1~45 직접 지정)

## 완료 조건
- reskin.py 1..45 재생성, 각 파일 diff가 CSS 덮어쓰기 구간뿐
- 헤드리스 D1·D10·D45에서 계산 스타일 확인: .kv b font-size = .ctl h3 font-size, font-family Pretendard, pre.cb-code는 고정폭
- 390·1024·1440 가로 넘침 없음

## 하지 않을 것
- 원본 dayNN/ 수정 · 로직·문구 변경 · 코드 상자 글꼴 변경
