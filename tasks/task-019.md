# task-019 애니메이션 페이지 항목별 코드 상자 (Python · TypeScript)

- 위험도: 보통 → builder(sonnet)
- 대상: `scripts/reskin.py`, `dashboard/d1~d44/animation.html`(재생성)

## 사용자 요구 (2026-11-20, 명확화)
"D1 음성 AI 첫걸음의 오늘의 흐름부터 음성 비서까지 **항목을 선택할 때마다 그 항목의 코드**가 Python 탭·TypeScript 탭으로 보이게. 아래에 덩그러니 전체 코드만 있는 게 아니라. 전체(44일)에 적용." JavaScript 탭 금지.

## 구현
- `reskin.py`가 각 애니메이션 페이지에 **코드 상자**를 추가한다(원본 `<script>`는 지금처럼 그대로 — diff 검사 유지. 코드 상자는 **별도 `<script>` 블록**과 CSS로만).
- 위치: 현재 보이는 항목(탭 패널)의 애니메이션 **바로 아래**. 항목을 바꾸면 코드도 그 항목 것으로 바뀐다.
  - 활성 항목 감지: 원본의 탭 전환 방식이 일차마다 다르므로(D1~34 가로탭 `#p0..`·HASH 표, D35~44 레일) `hashchange` + 활성 패널(`.panel.active` 등) MutationObserver로 현재 hash를 구한다. 구현 후 44일 모두에서 항목 9개 전환 시 hash가 data/code 키와 맞는지 자동 검사.
  - 상자를 하나 만들어 활성 패널 끝으로 옮기는 방식(DOM 이동) 권장.
- 상자 내용: 제목 "코드로 보기", 탭 `[Python] [TypeScript]`(role=tablist, 화살표 키), [복사], 출처 한 줄(`part`·노트북·코드 셀 — data/code 필드), **사용 라이브러리 표**(libs: 이름·버전·용도·설치·문서), 코드 `<pre>`(줄 번호, 전체 펼침, 가로 스크롤만), 간단 강조(키워드·문자열·주석).
- 데이터: `../../data/code/dayNN.json`을 페이지 로드 때 1회 fetch. **파일이 없거나 그 hash가 없으면 상자를 만들지 않는다(404 콘솔 오류도 피하려면 `../../data/code/index.json`(있는 일차 목록)을 먼저 받는다 — reskin.py가 아닌 build 스크립트가 만드는 파일이라면 이 작업에서 `scripts/build_code_index.py`로 생성).**
- 선택 언어 `aiVoiceDash.codeLang`(python|typescript, 'javascript'면 typescript) 공유 — 허브와 같은 키.
- 스타일: 기존 페이지 토큰(새 셸)만, 다크 모드, 반응형 3구간, 모바일 가로 넘침 0.

## 완료 조건
- `python scripts/reskin.py all` → 생성 44, 원본 script diff 검사 실패 0.
- D1·D10: 항목 9개 전환마다 코드 상자가 그 항목 코드로 바뀜(Playwright), 탭·복사·라이브러리 표 동작. 다른 일차: 상자 없음, 콘솔 오류 0.
- 44일 × 9항목 활성 hash 감지 정확(키 목록과 일치) — 표로 보고.
- 라이트·다크 × 1440·390 콘솔 오류 0, 가로 넘침 0(D1·D10·D35).

## 금지
- 원본 `day*/`, `data/day*.json`, `data/code/day*.json`(task-017 작업 중), `dashboard/index.html`(다른 작업 중), `dashboard/lab/` 수정. 새 의존성·CDN. commit·push.
