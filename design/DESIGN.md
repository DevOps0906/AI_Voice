# DESIGN — 학습 대시보드 (정답: design/tokens.css, 표: design/DESIGN_TOKENS.md, 미리보기: design/preview.html)

## 1. 브리프
대상 수강생 본인 · 일: 오늘 일차 파악 후 원본 이동 · 분위기: 깔끔·모던·정밀(평평한 1px 테두리 표면, Primer 계열 스타일 참고, 로고·명칭 사용 안 함).
피할 것: 원본 복제·장식 그라데이션·가로 탭 혼용·실측처럼 보이는 예시 숫자("수업용 예시 값" 표기). 서체는 Pretendard(OFL) 한 종 — `<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">`, 실패 시 시스템 글꼴로 대체. 캔버스 FONT도 같은 스택.

## 2. 3구간 폰트 표
| 토큰 | 모바일 ~767 | 태블릿 768~1199 | 데스크톱 1200~ |
|---|---|---|---|
| `--text-display` | 28px | 36px | 48px |
| `--text-h1` | 22px | 24px | 26px |
| `--text-h2` | 23px | 28px | 33px |
| `--text-body` | 14.5px | 15px | 16px |
| `--text-caption` | 12px | 12.5px | 13px |
| `--rail` / `--roadcols` / `--tap` | 0 / 2 / 44px | 212px / 3 / 40px | 248px / 6 / 40px |

## 3. 적용 규칙 (컴포넌트 명세, 20줄 이내)
1. 색·반경·그림자는 토큰만. 기존 이름(--page --panel --ink --muted --line --soft --a1~a5 --ok --bad --scope)은 값만 바뀐다. hex·px 직접 쓰기 금지.
2. 표면: 바탕 `--page`, 카드·레일 `--panel` + 1px `--line`, 반경 `--radius`(6px), 그림자는 `--shadow`(거의 없음). 떠 있는 것(메뉴)만 `--shadow-pop`.
3. 레일: 항목 높이 `--tap`, 평소 투명. 선택 = 왼쪽 2px `--a5` 막대 + `--soft` 배경 + 글자 `--ink`. 번호 원은 22px·1px 테두리, 연결선은 1px `--line`.
4. 모바일 탭: 레일이 상단 가로 스크롤 탭으로 바뀐다(번호 원 22px, 연결선 숨김). 선택 = 아래 2px `--a5` 막대. 페이지 가로 스크롤 0.
5. 카드: `--panel` + 1px `--line`, 패딩 16px, 로드맵 카드 위쪽 3px `--c` 띠(`--a1~a5` 순환). 호버는 `--soft` 배경만(그림자 이동 없음).
6. 칩: 높이 28px, 알약(`--radius-pill`), 1px `--line`. 선택(`aria-pressed=true`) = `--c` 채움 + 흰 글자(다크는 `--scope` 글자).
7. 버튼: 높이 `--tap`, 반경 `--radius-control`. 기본 = `--panel`+`--line`, 주요 = `--color-primary` 채움+`--color-primary-fg`. 비활성 = `--soft`+`--muted`.
8. 포커스: 모든 대화형 요소 `box-shadow: var(--ring)`, 제거 금지. `prefers-reduced-motion`이면 전환·애니메이션 최소화.
9. scope: 라이트·다크 모두 `--scope`(#0d1117) 계측기 캔버스, 글자 `--color-scope-fg`, 1px `--line`, 입자·파형은 `--a1~a5`. "수업용 예시 값" 라벨 필수.
10. 퀴즈: 선택지 = 버튼 규칙 + 왼쪽 정렬. 정답 `--ok`, 오답 `--bad` 테두리 1px + 아이콘·문구 병기(색만으로 구분 금지), 해설은 `--soft` 박스.
11. 숫자·KPI는 `--font-mono`, 캡션은 `--text-caption` + `--muted`. 본문 줄 높이 1.6.
12. 다크는 `[data-theme="dark"]`(또는 `.dark`)로 같은 이름의 값만 교체, 아이콘·경계 3:1, 본문 4.5:1(design-preview --check ❌ 0).
