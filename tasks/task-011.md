# task-011 교육내용 선택하기 + 과정 지도 자료실(개념·문제·그래프·애니메이션)

- 위험도: 보통 (데이터가 붙는 화면) → builder(sonnet)
- 대상: `dashboard/index.html`, 새 `scripts/build_library.py`, 새 `data/library.json`

## 1. 홈 문구
- 홈(`#home`)의 "주차 한눈에" 제목 → **"교육내용 선택하기"**. 동작은 그대로.

## 2. 데이터: `scripts/build_library.py` → `data/library.json`
- `data/day01~44.json`과 `course.json`을 읽어 아래만 모은다(중복·불필요 필드 제거, ensure_ascii=False, 들여쓰기 없음).
- `days[]`: `{day, week, module, title, concepts:[{concept,summary,code}], questions:[{g, ty,p,o,a,w}], anims:[{hash,title,desc}], road:[{p,t}]}` (`g`=워크시트 그룹 제목). 준비 안 된 일차는 빈 배열.
- 실행: `PYTHONIOENCODING=utf-8 python scripts/build_library.py` → 총계(개념·문항·애니메이션 수) 출력.

## 3. 과정 지도(`#map`) 위쪽에 카드 4개
- 제목 "자료실" 아래 4카드(데스크톱 4열 · 태블릿 2열 · 모바일 1열), 카드 = 이름 + 한 줄 설명 + 총계:
  개념 정리(개념 N개) · 문제 풀이(N문항) · 그래프 정리(흐름 그래프 44개) · 애니메이션 정리(N종).
- 카드 클릭 → `#lib-concepts` · `#lib-quiz` · `#lib-graphs` · `#lib-anims`. 이 화면들은 레일에서 "과정 지도"가 선택된 상태로 보이고, 맨 위에 "← 과정 지도" 링크.
- 기존 과정 지도(주차별 일차 목록)는 카드 아래에 그대로 둔다.

## 4. 자료실 페이지 공통 구조
- 머리: eyebrow "자료실", h2(페이지 이름), lead(총계).
- **주차 선택 버튼 줄**: [전체][1주차]…[9주차] (aria-pressed, 모바일은 가로 스크롤). 선택 주차는 해시에 유지: `#lib-concepts-w3`(전체는 `-w0` 또는 생략).
- 그 아래 **일차 선택 칩**(선택 주차의 일차, 전체면 생략) + 검색 입력(개념·문제만, 글자 포함 필터).
- 본문은 일차별 묶음(소제목 `D{n} · 제목`, 오른쪽에 "이 일차 열기 →" `#dN-flow`).

### 개념 정리 `#lib-concepts`
- 일차별 표/카드: 개념(굵게) · 한 줄 정리 · 코드(있으면 `<code>`). 기존 오늘 배운 것 탭 스타일 재사용.

### 문제 풀이 `#lib-quiz`
- 일차별 문항 목록. 문항 = 번호 + 문제 + 보기 버튼. 기존 정리 퀴즈 탭의 채점·해설 동작 재사용(정답 ✓/오답 shake+해설). mc 외 형식(match·order·ox·num·multi)은 기존 renderQuiz와 같은 방식으로 처리하거나, 처리 못 하면 "정답 보기" 토글로 답·해설만 보여 준다.
- 위쪽에 "맞힌 수 / 푼 수" 요약(이 페이지 안에서만, 저장 불필요). 한 번에 너무 길지 않게 일차별 접기(details, 첫 일차만 펼침).

### 그래프 정리 `#lib-graphs`
- 일차마다 작은 카드 1장: 그날 흐름 그래프(기존 `flowOf` 단계들을 정적 노드-화살표로; SVG 또는 정적 canvas 1회 그리기, 애니메이션 없음) + 제목 + "오늘의 흐름에서 보기 →".
- 그리드: 데스크톱 3열 · 태블릿 2열 · 모바일 1열. flowOf가 일차 JSON 전체를 요구하면 library.json의 road로 같은 단계 목록을 만든다.

### 애니메이션 정리 `#lib-anims`
- 일차별 애니메이션 목록(번호 D{n}-{i}, 제목, 설명). 클릭 → `d{n}/animation.html#해시`를 새 탭이 아니라 페이지 안 미리보기(iframe, lazy, 16:10, 하나만 열림)로 보여 주고 "새 창으로 열기 ↗" 링크도 둔다.

## 규칙
- library.json은 자료실 첫 진입 때 1번만 fetch(캐시). 일차 JSON 44개를 받지 않는다.
- 기존 토큰·Pretendard·반경 6px, 새 색 금지. 반응형 3구간, 모바일 가로 넘침 0, 터치 44px, 다크 모드.
- 기존 탭 동작·`dashboard/d*/`·`data/day*.json`·`scripts/extract.py`·`scripts/reskin.py`는 건드리지 않는다.

## 완료 조건
- build_library.py 실행 성공, 총계 = 개념 325 · 문항 1585 · 애니메이션 396.
- 4개 페이지 × (전체·3주차) × 라이트/다크 × 1440·1024·390 콘솔 오류 0, 가로 넘침 0.
- 주차 버튼·해시 유지·검색·문제 채점·애니메이션 미리보기·"이 일차 열기" 동작 확인.
