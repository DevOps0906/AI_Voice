# NOW — 재진입 스냅샷 (30줄 이내, 매 작업 끝에 덮어쓴다)

- 갱신: 2026-11-20
- 현재 작업: 없음 — task-020~029 완료, main push
- 마지막으로 한 일: 정리 퀴즈 정답 보기(020), 코드 탭 D2~D44 단독 실행 코드 792개 통과(021~029, 리뷰 2회 반영)
- 다음 한 걸음: 사용자 확인(배포 화면 코드 상자). API 키 경로(D14 --real·D22·D23) 실제 키 검증은 미실행
- 열린 결정(사용자 확인 필요):
  - 과정 지도 주차별 버튼(전체·1~9주차) 도입 여부
  - 주차 줄에 모듈 이름 표시(수업 자료에서 추출 필요) 여부
  - 모바일 '주차 한눈에' 접기 여부, 메뉴 카드 설명 문구 9개 확정
- 주의(이번 작업에서 알게 된 함정):
  - 애니메이션은 scripts/reskin.py로만 다시 만든다(원본 script 변경 금지, 일차별 CSS 보정은 DAY_FIX)
  - 원본 D1~34 script는 IIFE라 연결 코드는 닫는 줄 앞에 넣어야 한다
  - git status의 dashboard/d* 변경은 줄바꿈(CRLF) 차이일 수 있음 → `git diff --ignore-cr-at-eol --stat`로 확인
- SDLC 단계: 08 배포 완료
- 담당 모델/역할: 팀장(Opus) · builder(sonnet)×주차별 · codex-reviewer
- 수정 파일: dashboard/index.html, scripts/build_code.py, scripts/code_map/day02~44.json, data/code/*.json, docs/code-run-report.md
- 테스트 상태: run_code 792/792 통과(주차별 venv .venv-code*), 로컬 브라우저 코드 상자 9일차 확인
- 남은 작업: 없음 (열린 결정만)
