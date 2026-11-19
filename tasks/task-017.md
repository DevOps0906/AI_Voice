# task-017 D1·D10 코드 단독 실행 보장 + 사용 라이브러리 정리

- 위험도: 보통이나 난이도 높음(task-015에서 sonnet 미완) → builder(opus)
- 대상: `scripts/build_code.py`, `data/code/day01.json`, `data/code/day10.json`, `dashboard/index.html`(libs 표 부분만)

## 배경
task-015에서 화면은 완료. 코드 데이터는 노트북 셀을 그대로 이어 붙여 앞 셀 의존·`await`·`google.colab`이 남고, TS는 브라우저 전용이라 실행 검증을 못 했다(`scratchpad/t15/review.md`).

## 사용자 결정 (2026-11-20)
- 강사용 노트북 사용 금지. 빈칸 없는 **완성 코드**만.
- **반드시 실행되는 코드** + 작성하면서 코드 리뷰.
- 탭은 Python · TypeScript 두 개.
- 라이브러리를 쓰면 라이브러리 정리를 붙인다.

## Python (18개)
- 각 스니펫은 **새 파일 하나로 단독 실행**된다: 필요한 앞 셀 정의(함수·상수)를 스니펫 안에 포함, `await` → `asyncio.run(main())`, `google.colab`·`IPython.display`·`!pip`·`%` 제거 또는 표준 대체(파일 저장·print).
- 입력은 코드 안에서 생성(합성 오디오: numpy 사인파·잡음, 필요 시 gTTS 대신 합성). 네트워크·모델 다운로드는 가장 작은 모델만(faster-whisper `tiny`), API 키(ANTHROPIC_API_KEY 등) 없으면 규칙 기반 대체 경로로 끝까지 실행.
- 맨 위 `# pip install a==x b==y` 주석.
- 검증: `scratchpad/t17/venv`(uv venv, Python 3.11)에 필요한 패키지만 설치 → 18개 실제 실행, timeout 300s, 종료코드 0. 결과 표를 `scratchpad/t17/run-python.md`.

## TypeScript (18개)
- **Node 26에서 `node --experimental-strip-types x.ts`로 실행**되는 코드로 다시 쓴다(브라우저 API 금지). 같은 일을 하는 Node 코드: 오디오는 Float32Array 합성·WAV 바이트 직접 쓰기(fs), LLM은 `fetch`로 Anthropic Messages API(키 없으면 대체), STT는 키 없이 가능한 범위(예: 합성 신호로 파이프라인 구조만 실행하고 실제 인식은 키·모델이 있을 때만 — 그 분기를 명시).
- strip-types 금지 문법(enum·namespace·parameter property) 사용 금지, any 금지, 반환 타입 명시.
- 외부 npm이 꼭 필요하면 `scratchpad/t17/tsenv`에만 설치하고 실행 검증, 가능하면 Node 내장만.
- 검증: 18개 실행 종료코드 0, 결과 표 `scratchpad/t17/run-ts.md`.

## 라이브러리 정리
- 각 hash 항목에 `libs: {python:[...], typescript:[...]}`. 원소 `{name, version, purpose(한국어 한 줄), install, docs, license}`. version은 venv `pip show`/`npm ls` 실제 값, 내장은 "내장".
- 화면: task-015에서 넣은 libs 표 코드를 브라우저에서 실제로 확인·수정(코드 위 출처 줄 아래 "사용 라이브러리 (N)", 기본 펼침, 선택 언어 기준, 문서 링크 새 창).

## 코드 리뷰
- 스니펫마다 작성 직후 자체 리뷰(정의 누락·import·API 실존·오디오 dtype/샘플레이트·0 나누기·빈 입력·TS 문법·대체 경로) → `scratchpad/t17/review.md`에 "발견→수정" 한 줄씩.
- 완료 후 팀장이 독립 리뷰어로 재실행·검토한다.

## 완료 조건
- Python 18 · TS 18 실행 종료코드 0(표 첨부), `___` 0, 앞 셀 의존 0(스니펫 단독 파일 실행으로 증명).
- libs 버전 = 실제 설치 버전.
- `#d1-anim`·`#d10-anim` Python·TS 탭과 라이브러리 표 표시, 라이트·다크 × 1440·390 콘솔 오류 0, 가로 넘침 0.
- 금지: `day*/`·`data/day*.json`·`dashboard/d*/`·`dashboard/lab/` 수정, 프로젝트 의존성 추가, commit·push.
- (2026-11-20 사용자 명확화) 코드는 허브가 아니라 애니메이션 페이지 항목별로 표시(task-019). 이 작업은 data/code·build_code.py·scripts/run_code.py만, index.html 수정 중지.
