# task-018 과정 지도 하위 메뉴 + 개념 정리 보강(슬라이드 PDF·실습 노트북)

- 위험도: 보통 → builder(sonnet)
- 단계 A(바로): `scripts/build_concepts.py`, `data/concepts/day01~44.json`
- 단계 B(task-017 끝난 뒤 팀장 신호): `dashboard/index.html` 레일 하위 메뉴 + 개념 정리 페이지

## 사용자 요청 (2026-11-20)
- 과정 지도 하위 메뉴로 개념 정리 · 문제 풀이 · 그래프 정리 · 애니메이션 정리.
- 개념 정리 내용이 부족하다 → 일차별 **학습 PDF**와 **실습 .ipynb**에서 수업에서 정리한 내용을 넣어, 자료를 보면서 이해할 수 있게.

## 단계 A — 추출 (`scripts/build_concepts.py all | 1 10 …`)
- 입력: `dayNN/*_slides.pdf`(pypdf 또는 PyMuPDF — 이미 설치된 것만), `dayNN/*_실습.ipynb`(강사용 사용 금지), `data/dayNN.json`(parts·learned).
- 출력 `data/concepts/dayNN.json`:
  `{day, title, parts:[{n, title, notes:[블록], slides:[{page, title, points:[...]}]}], glossary:[learned 그대로]}`
  - **notes(노트북 설명)**: 그 Part(`## Part N`부터 다음 Part 전까지)의 markdown 셀을 순서대로. 블록 = `{t:"md", s:마크다운}` 또는 `{t:"code", s:짧은 예시 코드(≤15줄, 설명 바로 뒤 코드 셀 첫 부분만)}`.
    - 제거: 이미지(`![..](data:...)`, `attachment:`, base64), HTML 장식, 🧩 빈칸 안내·정답 확인 셀, 과제 체크 셀, 빈 셀. 이미지 자리는 `(그림: 노트북 참고)` 한 줄.
    - 유지: 제목·문단·목록·표·수식(`$...$`, `$$...$$` 원문 그대로)·인라인 코드.
  - **slides(PDF 요점)**: 페이지별 텍스트를 줄 단위로 정리 — 첫 줄=제목, 나머지=요점(중복·쪽번호·머리글 제거, 페이지당 ≤8개). 슬라이드 제목/본문의 "Part N" 또는 내용 키워드로 Part에 배정, 못 하면 `parts[0]`(개요)에.
- 검사·리포트 `docs/concepts-report.md`: 일차별 Part 수·notes 블록 수·slides 쪽수·글자 수, 이미지 base64 잔존 0, 일차 JSON 크기(≤150KB 목표, 넘으면 notes 정리 규칙 보강).
- 44일 전체 실행.

## 단계 B — 화면 (`dashboard/index.html`)
1. **레일 하위 메뉴**: "과정 지도" 아래에 들여쓴 4항목(개념 정리 · 문제 풀이 · 그래프 정리 · 애니메이션 정리 → `#lib-concepts` 등). 작은 글씨·왼쪽 들여쓰기·연결선, 선택 시 기존 레일 강조 규칙. 모바일 가로 탭에서는 과정 지도 뒤에 이어서 표시. 번호는 하위 항목에 붙이지 않음. ← → 키 이동에 포함.
2. **개념 정리 페이지(`#lib-concepts`)를 일차 학습 노트로 개편**: 자료실 보조 메뉴에서 일차 선택 → 그 일차 화면:
   - 위: `D{n} · 제목`, [슬라이드 PDF ↗][실습 노트북 Colab ↗], "오늘 배운 것" 요약 표(기존 glossary).
   - 본문: Part별 접이식 섹션(첫 Part 펼침) — **노트북 설명**(마크다운 렌더: 제목·문단·목록·표·굵게·인라인/블록 코드, 수식은 원문 `<code>` 표시 또는 기존 페이지에 KaTeX가 없으면 원문 유지) + **슬라이드 요점** 카드(쪽별 제목·요점, `PDF p.N ↗` = GitHub PDF URL `#page=N`).
   - Part 목차(위쪽 칩, sticky)로 바로 이동. 검색은 현재 일차 안 텍스트 필터.
   - 일차 JSON은 선택 시 1개만 fetch.
- 마크다운 렌더는 직접 작성한 작은 함수(새 라이브러리·CDN 금지), 모든 텍스트 esc 처리 후 변환(XSS 방지).

## 완료 조건
- A: 44일 JSON 생성, base64 0, 리포트 작성. D1·D10 notes에 노트북 설명 문단이 Part별로 들어감(눈으로 확인).
- B: 레일 하위 메뉴 4개 이동, `#lib-concepts-w1-d1`에 Part별 노트·슬라이드 요점·PDF 쪽 링크, 라이트·다크 × 1440·1024·390 콘솔 오류 0·가로 넘침 0.
- 금지: `day*/`·`data/day*.json`·`dashboard/d*/`·`dashboard/lab/`·`data/code/`·`scripts/build_code.py` 수정, 새 의존성, commit·push.

## 팀장 결정 (단계 A 결과 반영)
- notes가 빈 Part(예: D20 Part 1)는 숨기지 않고 "이 Part는 그림 위주예요 — 슬라이드 PDF·노트북에서 보세요" 안내 + 링크.
- slides가 0쪽인 Part는 슬라이드 카드 생략. glossary가 빈 일차(D29~35)는 요약 표 대신 안내 한 줄.
