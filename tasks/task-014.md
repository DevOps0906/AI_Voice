# task-014 애니메이션 카드 → 코드 탭(Python · JavaScript · TypeScript) — D1·D10 먼저

- 위험도: 보통 → builder(sonnet)
- 사용자 결정(2026-11-20): 범위 D1·D10(애니메이션 18개 × 3언어 = 54개). Python은 수업 노트북에서 추출, JS·TS는 그 코드를 옮긴 참고용 예시로 새로 작성.

## 데이터
- 새 파일 `data/code/day01.json`, `data/code/day10.json`:
  `{ "<anim hash>": { "part": "Part N · 제목" | null, "cells": [노트북 셀 번호...], "python": "...", "javascript": "...", "typescript": "..." } }` — 그날 `anims`의 hash 9개 모두.
- **Python 추출 규칙** (`scripts/build_code.py dayN...` — python 필드와 part/cells만 다시 쓰고, 이미 있는 javascript·typescript는 보존):
  1. 노트북 `day01/D1_*_실습.ipynb`, `day10/D10_*_실습.ipynb`의 markdown에 있는 🎬 `D{n}-{i}` 표시(i = anims 순번 1~9)를 찾으면 그 위치 이후 다음 Part/🎬 전까지 코드 셀.
  2. 없으면 `data/dayNN.json` road의 `go`/`more` hash → 그 Part(`## Part N`)의 코드 셀.
  3. 둘 다 없으면(예: flow·tech·cer) 제목·키워드로 가장 관련 있는 셀을 고르고 `part`에 근거를 적는다(flow는 Part 0 환경·import + 전체 파이프라인 셀).
  - 맨 앞에 그 코드가 쓰는 **import 줄을 노트북 앞쪽 셀에서 모아** 붙인다(중복 제거). 실습 빈칸(`___` 등)은 그대로 두고 상단 주석 `# 빈칸(___)은 실습 노트북에서 채워요` 추가. `!pip`·`%` 매직 줄은 주석 처리. 너무 길면 60줄 안쪽으로 핵심 셀만.
- **JavaScript / TypeScript** (사람이 쓰는 부분, 이 작업에서 builder가 작성):
  - 같은 일을 하는 브라우저/Node 코드. 맨 위 주석 `// 참고용 변환 예시 — 원본은 Python 노트북 Part N`. 필요한 라이브러리 import 포함(예: Web Audio API, `@huggingface/transformers`, `openai`/`@anthropic-ai/sdk`, `wavefile`, 편집 거리는 직접 구현 등 — 실제 존재하는 패키지·API만, 없으면 직접 구현).
  - TS는 JS와 같은 흐름에 타입(interface·반환 타입)을 붙인다. 각 60줄 이내, 한국어 주석.
  - 검사: JS는 `node --check`(ESM은 .mjs로), TS는 전역 `tsc`가 있으면 `tsc --noEmit --skipLibCheck`(외부 모듈 import 오류는 무시 가능, 문법·타입 오류는 0). 새 의존성 설치 금지.

## 화면 (`dashboard/index.html` renderAnim)
- 카드를 누르면 지금처럼 애니메이션 iframe이 열리고, 그 **아래에 코드 상자**: 탭 3개 [Python][JavaScript][TypeScript](role=tablist, 화살표 키 이동), 오른쪽 [복사] 버튼(복사됨 표시), 위에 출처 한 줄(`노트북 Part N · 셀 3~5` 또는 `참고용 변환 예시`).
- 코드는 `<pre><code>` 고정폭, 줄 번호, 가로 스크롤(페이지 넘침 0), 최대 높이 480px 세로 스크롤. 색은 기존 토큰(`--scope` 배경 등), 구문 강조 라이브러리 추가 금지(키워드·문자열·주석 3색 정도 간단한 정규식 강조는 허용).
- 선택 언어는 `aiVoiceDash.codeLang`에 저장(try/catch), 카드를 바꿔도 유지.
- `data/code/dayNN.json`이 없는 일차는 코드 상자 대신 "이 일차 코드는 준비 중이에요" 안내(오류 없이).
- 다른 탭·자료실·`dashboard/d*/` 동작 변경 금지.

## 완료 조건
- D1·D10 각 9개 hash × 3언어 비어 있지 않음, python에 import 줄 포함.
- JS `node --check` 통과, TS 검사(가능하면) 문법 오류 0.
- `#d1-anim`, `#d10-anim`에서 카드 클릭 → 코드 상자 갱신, 탭 전환·복사·언어 유지 동작. `#d2-anim`은 준비 중 안내.
- 라이트·다크 × 1440·1024·390 콘솔 오류 0, 가로 넘침 0.
