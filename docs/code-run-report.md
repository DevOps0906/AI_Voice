# 코드 실행 검사 결과

- 실행: `python scripts/run_code.py day01 day10 --venv <검사용 venv>` (API 키 뺌 → 키 없는 대체 경로)
- 일시: 2026-11-20 05:15 · Windows 11 (빌드 10.0.26300)
- Python: Python 3.11.9 (`<검사용 venv>`) · Node: v26.13.1
- 방법: 스니펫 하나를 빈 임시 폴더에 파일 하나로 써서 실행, 제한 300초
- 판정: 종료코드 0이고 출력에 'Traceback' · '[다시]'(정답 확인 실패)가 없으면 통과
- 결과: 36개 중 통과 36 · 실패 0
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
