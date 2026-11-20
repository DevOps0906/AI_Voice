# 코드 실행 검사 결과

- 실행: `python scripts/run_code.py day02 day03 day04 day05 --venv .venv-code` (API 키 뺌 → 키 없는 대체 경로)
- 일시: 2026-11-20 12:33 · Windows 11 (빌드 10.0.26300)
- Python: Python 3.11.9 (`.venv-code\Scripts\python.exe`) · Node: v26.13.1
- 방법: 스니펫 하나를 빈 임시 폴더에 파일 하나로 써서 실행, 제한 300초
- 판정: 종료코드 0이고 출력에 'Traceback' · '[다시]'(정답 확인 실패)가 없으면 통과
- 결과: 108개 중 통과 108 · 실패 0
- 이번 실행(2026-11-20 D2~D5 72개, `--venv .venv-code`)과 이전 실행(D1 · D10 36개, 05:15)의 행을 한 표로 합쳤다. D1 · D10은 코드가 바뀌지 않아 이전 결과를 그대로 둔다(그 venv에는 faster-whisper · jiwer 등이 더 설치돼 있음).
- 이 검사로 확인하지 않는 경로: API 키 경로(Claude · Whisper API, --with-keys로만), 데모 화면(--serve), 마이크 녹음(--record), GPU(CUDA) 추론, 사용자 WAV 인자 실행. 인터넷이 필요한 edge-tts는 실행 환경에 따라 실제 음성 또는 합성 신호 대체 경로를 탄다.

| 일차 | hash | 언어 | 종료코드 | 초 | 판정 | 마지막 출력 |
|---|---|---|---|---|---|---|
| D1 | flow | Python | 0 | 14.0 | 통과 | [정답] 정답입니다! |
| D1 | flow | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D1 | tech | Python | 0 | 10.5 | 통과 | [정답] 정답입니다! |
| D1 | tech | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D1 | stack | Python | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D1 | stack | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D1 | file | Python | 0 | 8.4 | 통과 | [정답] 정답입니다! |
| D1 | file | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D1 | sampling | Python | 0 | 5.6 | 통과 | [정답] 정답입니다! |
| D1 | sampling | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D1 | mic | Python | 0 | 5.1 | 통과 | 묵음 구간  : 1.81~2.98초 |
| D1 | mic | TypeScript | 0 | 0.4 | 통과 | 묵음 구간  : 1.81~2.98초 |
| D1 | asr | Python | 0 | 11.6 | 통과 | [정답] 정답입니다! |
| D1 | asr | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D1 | cer | Python | 0 | 12.5 | 통과 |         CER: 35.14% |
| D1 | cer | TypeScript | 0 | 0.2 | 통과 |         CER: 100.00% |
| D1 | agent | Python | 0 | 11.9 | 통과 | [정답] 정답입니다! |
| D1 | agent | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D2 | flow | Python | 0 | 7.2 | 통과 | [정답] 정답입니다! |
| D2 | flow | TypeScript | 0 | 0.6 | 통과 | [정답] 정답입니다! |
| D2 | sound | Python | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D2 | sound | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D2 | sampling | Python | 0 | 5.3 | 통과 | [정답] 정답입니다! |
| D2 | sampling | TypeScript | 0 | 1.0 | 통과 | [정답] 정답입니다! |
| D2 | quant | Python | 0 | 0.9 | 통과 | [정답] 정답입니다! |
| D2 | quant | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D2 | channel | Python | 0 | 9.8 | 통과 | [정답] 정답입니다! |
| D2 | channel | TypeScript | 0 | 0.5 | 통과 | [정답] 정답입니다! |
| D2 | format | Python | 0 | 1.0 | 통과 | [정답] 정답입니다! |
| D2 | format | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D2 | libs | Python | 0 | 7.2 | 통과 | [정답] 정답입니다! |
| D2 | libs | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D2 | editor | Python | 0 | 0.9 | 통과 | [정답] 정답입니다! |
| D2 | editor | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D2 | pipeline | Python | 0 | 12.0 | 통과 | [정답] 정답입니다! |
| D2 | pipeline | TypeScript | 0 | 1.6 | 통과 | [정답] 정답입니다! |
| D3 | flow | Python | 0 | 8.3 | 통과 | [정답] 정답입니다! |
| D3 | flow | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | sum | Python | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D3 | sum | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | dft | Python | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | dft | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D3 | res | Python | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | res | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D3 | window | Python | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | window | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D3 | stft | Python | 0 | 6.0 | 통과 | [정답] 정답입니다! |
| D3 | stft | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | live | Python | 0 | 5.2 | 통과 | [정답] 정답입니다! |
| D3 | live | TypeScript | 0 | 0.6 | 통과 | [정답] 정답입니다! |
| D3 | mel | Python | 0 | 5.5 | 통과 | [정답] 정답입니다! |
| D3 | mel | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D3 | mfcc | Python | 0 | 4.0 | 통과 | [정답] 정답입니다! |
| D3 | mfcc | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D4 | flow | Python | 0 | 4.3 | 통과 | [정답] 정답입니다! |
| D4 | flow | TypeScript | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D4 | snr | Python | 0 | 3.1 | 통과 | [정답] 정답입니다! |
| D4 | snr | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D4 | norm | Python | 0 | 0.5 | 통과 | [정답] 정답입니다! |
| D4 | norm | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D4 | filter | Python | 0 | 4.6 | 통과 | [정답] 정답입니다! |
| D4 | filter | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D4 | specsub | Python | 0 | 7.7 | 통과 | [정답] 정답입니다! |
| D4 | specsub | TypeScript | 0 | 0.9 | 통과 | [정답] 정답입니다! |
| D4 | gate | Python | 0 | 8.9 | 통과 | [정답] 정답입니다! |
| D4 | gate | TypeScript | 0 | 0.6 | 통과 | [정답] 정답입니다! |
| D4 | vad | Python | 0 | 5.9 | 통과 | [정답] 정답입니다! |
| D4 | vad | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D4 | silero | Python | 0 | 5.1 | 통과 |   warnings.warn( |
| D4 | silero | TypeScript | 0 | 1.2 | 통과 | [정답] 정답입니다! |
| D4 | pipe | Python | 0 | 10.3 | 통과 |   warnings.warn( |
| D4 | pipe | TypeScript | 0 | 0.4 | 통과 | [정답] 정답입니다! |
| D5 | flow | Python | 0 | 26.4 | 통과 | [정답] 정답입니다! |
| D5 | flow | TypeScript | 0 | 23.5 | 통과 | [정답] 정답입니다! |
| D5 | data | Python | 0 | 0.9 | 통과 | [정답] 정답입니다! |
| D5 | data | TypeScript | 0 | 1.5 | 통과 | [정답] 정답입니다! |
| D5 | feature | Python | 0 | 6.1 | 통과 | [정답] 정답입니다! |
| D5 | feature | TypeScript | 0 | 7.9 | 통과 | [정답] 정답입니다! |
| D5 | conv | Python | 0 | 6.1 | 통과 | [정답] 정답입니다! |
| D5 | conv | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D5 | net | Python | 0 | 5.0 | 통과 | [정답] 정답입니다! |
| D5 | net | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D5 | softmax | Python | 0 | 4.6 | 통과 | [정답] 정답입니다! |
| D5 | softmax | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D5 | train | Python | 0 | 20.6 | 통과 | [정답] 정답입니다! |
| D5 | train | TypeScript | 0 | 33.5 | 통과 | [정답] 정답입니다! |
| D5 | confusion | Python | 0 | 49.2 | 통과 | [정답] 정답입니다! |
| D5 | confusion | TypeScript | 0 | 20.6 | 통과 | [정답] 정답입니다! |
| D5 | specaug | Python | 0 | 17.4 | 통과 | [정답] 정답입니다! |
| D5 | specaug | TypeScript | 0 | 32.6 | 통과 | [정답] 정답입니다! |
| D10 | flow | Python | 0 | 25.1 | 통과 | 요약 점수 40% |
| D10 | flow | TypeScript | 0 | 2.5 | 통과 | 요약 점수 0% |
| D10 | editdist | Python | 0 | 1.0 | 통과 | [정답] 정답입니다! |
| D10 | editdist | TypeScript | 0 | 0.1 | 통과 | [정답] 정답입니다! |
| D10 | wercer | Python | 0 | 0.3 | 통과 | [정답] 정답입니다! |
| D10 | wercer | TypeScript | 0 | 0.1 | 통과 | [정답] 정답입니다! |
| D10 | norm | Python | 0 | 15.5 | 통과 | 그림 저장: cer_compare.png |
| D10 | norm | TypeScript | 0 | 0.2 | 통과 | 그림 저장: cer_compare.svg |
| D10 | numbers | Python | 0 | 0.1 | 통과 | [정답] 정답입니다! |
| D10 | numbers | TypeScript | 0 | 0.1 | 통과 | [정답] 정답입니다! |
| D10 | pipeline | Python | 0 | 17.5 | 통과 | [00:31] 김팀장: 그럼, 금요일, 오후의 결과를 같이 검토합시다. |
| D10 | pipeline | TypeScript | 0 | 2.4 | 통과 | [00:28] 김팀장: (받아쓰기 생략) |
| D10 | prompt | Python | 0 | 0.1 | 통과 | - **[00:28] 김팀장**: 그럼 금요일 오후에 결과를 같이 검토합시다. |
| D10 | prompt | TypeScript | 0 | 0.1 | 통과 | - **[00:28] 김팀장**: 그럼 금요일 오후에 결과를 같이 검토합시다. |
| D10 | eval | Python | 0 | 0.5 | 통과 | [정답] 정답입니다! |
| D10 | eval | TypeScript | 0 | 0.2 | 통과 | [정답] 정답입니다! |
| D10 | demo | Python | 0 | 24.5 | 통과 | 저장: meeting.wav, meeting_minutes.md (화면은 --serve) |
| D10 | demo | TypeScript | 0 | 2.9 | 통과 | 저장: meeting_minutes.md (화면은 --serve) |
