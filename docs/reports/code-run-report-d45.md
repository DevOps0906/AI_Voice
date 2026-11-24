# 코드 실행 검사 결과

- 실행: `python scripts/run_code.py day45 --venv .venv-code-w9` (API 키 뺌 → 키 없는 대체 경로)
- 일시: 2026-11-23 21:33 · Windows 11 (빌드 10.0.26300)
- Python: Python 3.11.9 (`.venv-code-w9\Scripts\python.exe`) · Node: v26.13.1
- 방법: 스니펫 하나를 빈 임시 폴더에 파일 하나로 써서 실행, 제한 300초
- 판정: 종료코드 0이고 출력에 'Traceback' · '[다시]'(정답 확인 실패)가 없으면 통과
- 결과: 18개 중 통과 18 · 실패 0
- 이 검사로 확인하지 않는 경로: API 키 경로(Claude · Whisper API, --with-keys로만), 데모 화면(--serve), 마이크 녹음(--record), GPU(CUDA) 추론, 사용자 WAV 인자 실행. 인터넷이 필요한 edge-tts는 실행 환경에 따라 실제 음성 또는 합성 신호 대체 경로를 탄다.

| 일차 | hash | 언어 | 종료코드 | 초 | 판정 | 마지막 출력 |
|---|---|---|---|---|---|---|
| D45 | flow | Python | 0 | 2.3 | 통과 | [정답] 정답입니다! |
| D45 | flow | TypeScript | 0 | 0.6 | 통과 | [정답] 정답입니다! |
| D45 | req | Python | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D45 | req | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D45 | menu | Python | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D45 | menu | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D45 | slots | Python | 0 | 0.5 | 통과 | [정답] 정답입니다! |
| D45 | slots | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D45 | talk | Python | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D45 | talk | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D45 | noise | Python | 0 | 2.8 | 통과 | [정답] 정답입니다! |
| D45 | noise | TypeScript | 0 | 0.5 | 통과 | [정답] 정답입니다! |
| D45 | edit | Python | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D45 | edit | TypeScript | 0 | 0.1 | 통과 | [정답] 정답입니다! |
| D45 | receipt | Python | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D45 | receipt | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D45 | recap | Python | 0 | 0.1 | 통과 | [정답] 정답입니다! |
| D45 | recap | TypeScript | 0 | 0.1 | 통과 | [정답] 정답입니다! |
