# task-042 — 모션 레퍼런스를 원본 459개 분석으로 다시 짜기 (기법 카드 + 전체 목록 · 출처 표기)

- 위험도: 보통 · 담당: builder(sonnet) · 선행: task-041

## 배경 (팀장 분석)
- 원본 `Edu/dayNN/animation.html` 51개의 애니메이션 459개는 거의 전부 **JS 캔버스/DOM** 모션이다. 원본 CSS 애니메이션은 `@keyframes dots`(D1~34)와 `shake`(D35~51) 두 개뿐.
- 459개를 기법별로 분류한 결과가 `data/motion/anims.json`(팀장이 분석 결과를 합쳐 넣음): `{day,hash,title,tech[],fn,drive,excerpt,note}`. 주 기법(tech[0]) 개수: stepper 90 · slider 68 · bargrow 50 · static 38 · plot 30 · wave 29 · tablefill 29 · playhead 26 · nodeflow 20 · scatter 20 · heatmap 14 · particle 11 · quiz 12 · pulse 8 · typing 7 · easemove 6. 기법 이름은 같은 폴더 `techs.json`.
- 기존 S8 카드 35개(CSS 25 · JS 10)는 대부분 대시보드용으로 새로 작성한 것이라 출처가 원본이 아니다.

## 만들 것 (`index.html` S8 `#motion`)
1. **기법 카드**(맨 위): `techs.json`의 기법마다 카드 1장(static 제외, quiz 포함 → 15장). 카드 구성:
   - `JS` 배지(quiz는 `JS·DOM`) · 기법 이름 · "원본 N개" 수
   - 살아 있는 데모: 그 기법의 **대표 원본**(techs.json `rep`) excerpt를 근거로 짧게 재구성한 캔버스 데모(기존 `CVD`·`fit`·`grid`·`dot`·`txt`·`rr`·`K` 재사용, RM이면 정지)
   - 코드 보기/복사 = 데모 코드, 그 아래 "원본 코드 (D12 · 학습률 실험실)" excerpt 원문
   - "나오는 곳" 칩 목록: `D12 · 학습률 실험실` 형식, 누르면 `dashboard/d12/animation.html#lr` 새 탭
2. **기존 카드 35개에 배지·출처**: CSS/JS 배지 + 출처 한 줄. 원본에서 온 것만 원본 일차를 적는다(dots → 원본 D1~34, shake → 원본 D35~51(대시보드판), scope·ease·grid·tour → 원본 D42, rr·wave·rng·bars·hbar·lanes → `data/motion/anims.json`·원본 페이지에서 처음 나오는 일차를 grep으로 확인해 적기). 나머지는 "대시보드 작성".
3. **전체 모션 목록 459개**(맨 아래 표): 일차 선택 · 기법 칩 · 구동(raf·click·input·interval) 필터, 줄마다 `D·제목 · 기법 · 구동 · 함수 · 원본 링크`, 펼치면 note + excerpt. 데이터는 `data/motion/anims.json`을 fetch(첫 표시 때 1회). 모바일은 카드형으로 접힘.
- 상단 리드 문구: "원본 459개 모션을 기법 15가지로 정리했어요 · 공통 효과 CSS 25 · JS 10" 식으로 숫자는 데이터 길이에서.

## 완료 조건
- 로컬 `python -m http.server`로 `#motion` 열어: 기법 카드 15 · 공통 카드 35 · 표 459줄, 필터 동작, 원본 링크가 실제 파일(200), 콘솔 오류 0
- 3구간(~767 / 768~1199 / 1200~) 깨짐 없음, 색·크기 토큰만, 동작 줄이기에서 정지
- `docs/motion-reference.md`에 기법 15개 절(대표 출처·원본 코드·나오는 곳 일차 목록) 추가, `docs/PLAN.md` S8 행 갱신

## 하지 않을 것
- `Edu/`·`dashboard/d*/`·`scripts/reskin.py` 수정, 외부 라이브러리, 원본 애니메이션 전체 복제(데모는 기법 핵심만)
