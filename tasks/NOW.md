# NOW — 재진입 스냅샷 (30줄 이내, 매 작업 끝에 덮어쓴다)

- 갱신: 2026-11-20
- 현재 작업: 없음 — task-001~030 모두 완료, main push (https://devops0906.github.io/AI_Voice/dashboard/)
- 마지막으로 한 일: task-030 모듈 이름·모바일 접기·메뉴 문구, task-020~029 코드 탭 792개
- 다음 한 걸음: 없음. 선택 사항 — API 키 경로(D14 --real·D22·D23) 실제 키로 검증
- 열린 결정(사용자 확인 필요): 없음 (M1·M2 모듈 이름은 머리말에 없어 일차 제목으로 붙인 이름 — 정식 이름 있으면 scripts/extract.py MODULE_NAMES 수정)
- 주의(이번 작업에서 알게 된 함정):
  - 애니메이션은 scripts/reskin.py로만 다시 만든다(원본 script 변경 금지, 일차별 CSS 보정은 DAY_FIX)
  - 원본 D1~34 script는 IIFE라 연결 코드는 닫는 줄 앞에 넣어야 한다
  - git status의 dashboard/d* 변경은 줄바꿈(CRLF) 차이일 수 있음 → `git diff --ignore-cr-at-eol --stat`로 확인
  - 코드 탭: 일차별 설정은 scripts/code_map/dayNN.json, 스니펫 원본은 .nomad/code_src/wN(커밋 안 함, 없으면 build_code.py --export로 꺼냄)
  - 코드 검사 venv는 주차별 .venv-code*(gitignore). run_code.py는 --out 없으면 docs/code-run-report.md를 통째로 덮어씀
- SDLC 단계: 08 배포 완료
- 담당 모델/역할: 팀장(Opus) · builder(sonnet)×주차별 · codex-reviewer
- 수정 파일: dashboard/index.html, scripts/build_code.py, scripts/code_map/day02~44.json, data/code/*.json, docs/code-run-report.md
- 테스트 상태: run_code 792/792 통과(주차별 venv .venv-code*), 로컬 브라우저 코드 상자 9일차 확인
- 남은 작업: 없음 (열린 결정만)
