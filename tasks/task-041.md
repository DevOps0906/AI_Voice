# task-041 — 모션 레퍼런스 확장 (CSS 4종 + 캔버스 헬퍼 6종)

- 위험도: 보통 · 담당: builder(sonnet) · 선행: task-039

## 배경 (팀장 분석)
- 모션 레퍼런스(S8 `#motion`)의 정본은 `index.html` 안의 세 곳: `<style id="motionCss">`(CSS), `<script id="motionData">`(JSON `fx`·`js`), JS의 `CVD`(캔버스 데모 함수). 문서 `docs/motion-reference.md`는 같은 코드를 사람이 읽게 옮긴 것.
- 현재 CSS 효과 21종(등장 6 · 상태·피드백 7 · 호버·누름 5 · 지속 3) + 캔버스 헬퍼 4종(scope·ease·grid·tour).
- `dashboard/d*/animation.html` 51개를 훑은 결과, 자주 쓰는데 레퍼런스에 없는 것: 로딩 점 `@keyframes dots`(34쪽), `rr` 둥근 사각형(28), `mulberry`+`gauss` 고정 난수·잡음(18·27), `heroLoop` 막대 진행(34), `wave` 파형(15), `lanes` 타임라인(7), `hbar` 가로 게이지(5).

## 추가할 것
- CSS `fx` 4종(그룹은 기존 이름 재사용):
  - `dots` 로딩 점(지속) — 원본 페이지의 `content` 단계 애니메이션
  - `eq` 이퀄라이저 막대(지속) — 막대 3~5개가 시간차로 오르내림(듣는 중·말하는 중 표시)
  - `type` 타자 효과(등장) — `steps()`로 글자가 하나씩, 커서는 기존 `mk-blink` 재사용 가능
  - `shimmer` 불러오는 중 반짝(상태·피드백) — 스켈레톤 줄 위로 빛이 지나감
- 캔버스 `js` 6종(헬퍼 그룹): `rr`(둥근 사각형) · `rng`(mulberry 고정 난수 + gauss 잡음 점) · `wave`(파형 선) · `bars`(heroLoop식 막대가 왼→오른쪽으로 채워짐) · `hbar`(값이 ease로 따라가는 가로 게이지) · `lanes`(화자 레인 타임라인에 재생 막대가 지나감). 코드는 원본 페이지 구현을 근거로 짧게 정리.

## 완료 조건
- `index.html`: motionCss·motionData·CVD에 위 10종 추가 → 화면 제목이 "효과 25종과 scope 헬퍼 10종"이 됨(문구는 길이로 자동)
- `docs/motion-reference.md`: 같은 코드·설명 추가, 머리 문장 숫자(21종 + 4종) 갱신. `docs/PLAN.md` S8 행 숫자 갱신
- 화면 코드 = 문서 코드(복사해 붙이면 그대로 동작). 키프레임 이름은 `mk-` 접두사, 클래스는 `.m-`
- 색·크기는 토큰(CSS 변수 · 캔버스는 기존 `K`)만, 새 hex·px 직접 금지(기존 효과가 쓰는 px 이동량 수준은 허용)
- 동작 줄이기에서 정지 화면(기존 전역 규칙으로 꺼지는지, 캔버스는 `RM?1:now`로 그려지는지) 확인
- 로컬 `python -m http.server`로 `#motion`을 열어 콘솔 오류 0, 카드 35개 표시 · 필터 칩 동작 확인

## 하지 않을 것
- 기존 21+4종 코드·문구 변경 · `dashboard/d*/animation.html`·`scripts/reskin.py` 수정 · 외부 라이브러리 추가
