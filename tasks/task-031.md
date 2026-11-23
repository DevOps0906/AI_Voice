# task-031 — 45일차(키오스크) 대시보드 연결

- 위험도: 보통 · 담당: builder(sonnet) · 선행: 없음

## 목표
pull로 들어온 `day45/`(슬라이드·노트북 2개·animation·worksheet)를 1~44일과 같은 파이프라인으로 대시보드에 붙이고, D45의 새 절(요구사항·체크포인트)도 보여 준다.

## 결정(사용자 확인 2026-11-23)
- D45 노트북에는 `N주차 MN` 머리말이 없다(`Day 45 / 51`, 45~51일 = 프로젝트 7일). D45~51은 **10주차 · M10 "프로젝트"** 로 둔다(일차 번호로 정하는 규칙, 이후 D46~51도 같은 규칙).
- 과정 지도·번호 공에는 **자료가 있는 일차만** 보인다(D46~51 자리 표시 없음).
- 실습 노트북의 **"요구사항 (고객의 말로)" R1~R6** 와 **"체크포인트와 점수"** 를 JSON에 새 필드로 담고 `목표·교시` 탭에 표로 보인다(필드가 없는 1~44일은 그 절을 숨김).

## 근거
- 파이프라인: `scripts/extract.py`(range 1~44 하드코딩·`parse_notebook_meta`·`MODULE_NAMES`) → `scripts/reskin.py`(RAIL_FROM=35) → `build_concepts.py` · `build_library.py` → 코드 탭 `scripts/code_map/dayNN.json` + `build_code.py` · `build_code_index.py` · `run_code.py`
- 화면: `dashboard/index.html` 목표·교시 탭 렌더 함수, MDESC.map "9주 44일"
- 함정: `tasks/NOW.md` 주의 목록, `tasks/README.md` 교훈

## 완료 조건
- `data/day45.json` 생성(요구사항·체크포인트 필드 포함), `course.json`에 D45(week 10, M10, 프로젝트), day01~44 JSON 무변경(`git diff --ignore-cr-at-eol --stat`)
- `dashboard/d45/` 애니메이션 재입힘, 콘솔 오류 0
- 코드 탭 D45 Python·TS 스니펫 `run_code.py --out`(D45 전용 리포트)로 전부 통과, 가짜 통과 금지 패턴(교훈) 준수
- 목표·교시 탭 D45에 요구사항·체크포인트 표, 다른 일차는 변화 없음 · 3구간(390·1024·1440) 확인
- MDESC 문구가 일차 수를 반영(데이터에서 계산)

## 하지 않을 것
- 원본 `day45/` 파일 수정 · 1~44일 데이터 재해석 · D46~51 자리 표시
