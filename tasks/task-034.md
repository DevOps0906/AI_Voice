# task-034 — 사이트 주소에서 /dashboard/ 빼기

- 위험도: 보통(경로·라우팅) · 담당: builder(sonnet) · 선행: 033

## 목표
https://devops0906.github.io/AI_Voice/ 로 바로 대시보드가 열린다. 옛 주소(/AI_Voice/dashboard/#…)도 해시를 유지한 채 새 주소로 넘어간다.

## 방법(팀장 결정)
- `git mv dashboard/index.html index.html`(저장소 루트, GitHub Pages 루트). 상대 경로 수정: `'../data/'`→`'data/'`, `'d'+N+'/animation.html'`→`'dashboard/d'+N+…`, PDF 등 `'../'+…`→`''+…`, `lab/…`→`dashboard/lab/…` 등 루트 기준으로 모두.
- `dashboard/index.html`은 리다이렉트 한 장: `location.replace('../'+location.search+location.hash)` + `<meta http-equiv="refresh">`·링크 대비책.
- `dashboard/lab/*.html`의 대시보드 링크는 `../../index.html…`로.
- 애니메이션(dashboard/dN)은 그대로(`../../data` 유지), reskin.py 출력 경로도 그대로.
- 문서: README.md 사이트 주소, AGENTS.md 스택 표 위치, tasks/NOW.md 주소. 지난 task-0NN.md는 기록이라 수정하지 않음.

## 완료 조건
- 루트에서 로컬 http.server로 `/`·`/#d45-goals`·`/#map-w10-d45`·`/#lib-concepts-w10-d45`·`/#d45-anim`·자료실 PDF·애니메이션 미리보기 열림, 네트워크 404 0(favicon 제외)·콘솔 오류 0
- `/dashboard/#d45-goals` → `/#d45-goals`로 이동
- `grep "'\.\./data/'"`(루트 index.html) 0건

## 하지 않을 것
- 화면·로직 변경, 애니메이션 재생성, 원본 dayNN/ 수정
