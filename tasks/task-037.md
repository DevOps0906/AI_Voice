# task-037 — 46일차 애니메이션 코드 상자(Python·TS)

- 위험도: 보통 · 담당: builder(sonnet) · 선행: task-036

## 목표
D46 애니메이션 9개(flow·engine·spec·slot·guard·mask·accept·report·recap) 각각에 단독 실행 Python·TS 코드를 붙여 코드 상자를 띄운다. D45(task-031)와 같은 방식.

## 근거
- 방식 정본: `scripts/build_code.py` 머리 docstring · 예시 `scripts/code_map/day45.json` · 스니펫 원본 `.nomad/code_src/w10/{py,ts}/d45_*.{py,ts}`
- 내용 근거: `Edu/day46/D46_*_실습.ipynb`(노트북 셀), `data/day46.json` anims(제목·설명)
- 교훈·함정: `tasks/README.md#교훈`, `tasks/NOW.md` 주의 목록

## 완료 조건
- `scripts/code_map/day46.json`, `.nomad/code_src/w10/{py,ts}/d46_<hash>.*` 18개 → `python scripts/build_code.py day46 --src .nomad/code_src/w10` → `data/code/day46.json`
- `python scripts/build_code_index.py` 로 `data/code/index.json`에 46 추가, `python scripts/reskin.py 46`
- `python scripts/run_code.py day46 --venv .venv-code-w9 --out docs/reports/code-run-report-d46.md` 18/18 통과
- 가짜 통과 금지: 상수끼리 비교·빈 목록 all()/every()·응답 확인 없는 성공 출력
- day01~45 data/code 무변경

## 하지 않을 것
- `Edu/` 원본 수정 · 다른 일차 코드 수정 · 새 의존성(D45가 쓴 범위 밖) 추가
