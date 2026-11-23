# task-032 — 코드 상자 로드 실패 표시

- 위험도: 보통(1~45일 애니메이션 전체 재생성) · 담당: builder(sonnet) · 선행: 031

## 목표
애니메이션 페이지 코드 상자가 코드 JSON을 못 불러오면(404·네트워크·파싱 오류) 조용히 사라지지 않고 상자 안에 한국어 안내 문구를 보인다.

## 근거
- `scripts/reskin.py` CODEBOX_JS (`r.ok`→null, `.catch(()=>{})`), 생성물 `dashboard/dN/animation.html` 1~45
- `tasks/README.md` 발견한 문제 2026-11-23 줄 · `tasks/NOW.md` 주의(reskin으로만 재생성, CRLF 차이)

## 완료 조건
- reskin.py 수정 후 1~45일 재생성: 각 animation.html diff가 CODEBOX_JS 부분뿐(`git diff --ignore-cr-at-eol`)
- 헤드리스: 정상 일차(D1·D45) 코드 상자 그대로·콘솔 오류 0, JSON 경로를 깨뜨린 사본에서 안내 문구 표시
- 안내 문구 색·크기는 기존 토큰 사용

## 하지 않을 것
- 코드 상자 외 로직·디자인 변경 · 원본 dayNN/ 수정
