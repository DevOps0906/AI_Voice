# 작업 표

| 번호 | 제목 | 웨이브 | 선행 | 위험도 | 담당 | 상태 |
|---|---|---|---|---|---|---|
| task-001 | extract.py → data/day01·day10.json·course.json | W1 | — | 보통 | builder(sonnet) | 완료 |
| task-002 | D1 애니메이션 레일 디자인 재입힘(로직 원본 동일) | W1 | — | 보통 | builder(sonnet) | 완료 |
| task-003 | D10 애니메이션 레일 디자인 재입힘(로직 원본 동일) | W1 | — | 보통 | builder(sonnet) | 완료 |
| task-004 | 대시보드 허브 dashboard/index.html (9탭·레일·라우팅·테마) | W2 | 001 | 보통 | builder(sonnet) | 완료 |
| task-006 | 모던 리디자인 토큰 design/tokens.css·DESIGN.md·preview | W4 | — | 보통 | designer(sonnet) | 완료 |
| task-007 | extract.py 44일 전체 JSON + 검증 리포트 | W4 | 001 | 보통 | builder(sonnet) | 완료 |
| task-008 | scripts/reskin.py: 44일 애니메이션 일괄 재입힘(로직 원본 동일) | W5 | 006 | 보통 | builder(sonnet) | 완료 |
| task-009 | 대시보드 허브 44일 전체·새 토큰 적용 | W5 | 006,007 | 보통 | builder(sonnet) | 완료 |
| task-005 | Playwright 1440·1024·390 스크린샷·콘솔 0건(44일) | W6 | 008,009 | 낮음 | tester(haiku) | 완료(task-008 헤드리스 검사로 대체) |
| task-010 | 홈 대시보드(메뉴 집합 화면) dashboard/index.html | W7 | 009 | 보통 | builder(sonnet) | 완료 |
| task-011 | 교육내용 선택하기 + 과정 지도 자료실(개념·문제·그래프·애니메이션) | W8 | 010 | 보통 | builder(sonnet) | 완료 |
| task-012 | 과정 지도 일차 번호 공 선택기(전체+1~N) | W9 | 011 | 보통 | builder(sonnet) | 완료 |

상태: 대기 / 진행 / 완료 / 보류 · 위험도 → 워커 model: 낮음 haiku · 보통 sonnet · 높음 opus

## 발견한 문제 (범위 밖 — 나중 작업 후보)
| 날짜 | 위치 | 내용 | 제안 |
|---|---|---|---|
| 2026-11-20 | dashboard/index.html renderQuiz | 정리 퀴즈 탭이 fill(40)·bucket(20)·lab(10) 문항을 처리하지 않아 본문이 비어 보임 (자료실 문제 풀이는 "정답 보기"로 처리됨) | 정리 퀴즈 탭도 buildQ의 정답 보기 방식 적용 |

## 교훈 (다음 작업에 그대로 적용할 것만, 20줄 이내 유지)
- 
