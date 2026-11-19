# NOW — 재진입 스냅샷 (30줄 이내, 매 작업 끝에 덮어쓴다)

- 갱신: 2026-11-20
- 현재 작업: 없음 — task-001~011 모두 완료, main 배포됨 (https://devops0906.github.io/AI_Voice/dashboard/)
- 마지막으로 한 일: task-011 홈 "교육내용 선택하기" 문구, 과정 지도 자료실 4페이지(#lib-concepts|quiz|graphs|anims) 구현·배포
- 다음 한 걸음: 사용자 지시 대기 (사용자가 작업 중단을 요청함)
- 열린 결정(사용자 확인 필요):
  - 정리 퀴즈 탭 fill·bucket·lab 문항 빈 화면 수정 여부 (tasks/README.md 발견한 문제)
  - 과정 지도 주차별 버튼(전체·1~9주차) 도입 여부
  - 주차 줄에 모듈 이름 표시(수업 자료에서 추출 필요) 여부
  - 모바일 '주차 한눈에' 접기 여부, 메뉴 카드 설명 문구 9개 확정
- 주의(이번 작업에서 알게 된 함정):
  - 애니메이션은 scripts/reskin.py로만 다시 만든다(원본 script 변경 금지, 일차별 CSS 보정은 DAY_FIX)
  - 원본 D1~34 script는 IIFE라 연결 코드는 닫는 줄 앞에 넣어야 한다
  - git status의 dashboard/d* 변경은 줄바꿈(CRLF) 차이일 수 있음 → `git diff --ignore-cr-at-eol --stat`로 확인
- SDLC 단계: 08 배포 완료
- 담당 모델/역할: 팀장(Opus) · builder(sonnet)
- 수정 파일: dashboard/index.html, dashboard/d*/animation.html, scripts/reskin.py, scripts/extract.py, scripts/build_library.py, data/library.json, data/*.json, README.md
- 테스트 상태: 통과 (Playwright 1440·1024·390 콘솔 오류 0, 390px 가로 넘침 0, reskin 검사 실패 0)
- 남은 작업: 없음
