# AI_Voice — 음성 AI 전문가 과정 학습 대시보드

음성 AI 전문가 과정(9주·44일) 수업 자료와, 일차별 흐름·목표·자료·과제·퀴즈를 한 화면에서 보는 학습 대시보드입니다.
[imguru-mooc/AI_Voice](https://github.com/imguru-mooc/AI_Voice)의 fork이며, 자료·Colab 링크는 이 레포로 연결됩니다.

## 진행 현황
- ✅ 44일 데이터 추출 (`data/day01~44.json`)
- ✅ 대시보드 허브 (과정 지도·오늘의 흐름·목표·애니메이션·자료·배운 것·과제·퀴즈·모션 레퍼런스)
- ✅ 44일 애니메이션 새 디자인 적용 (애니메이션 동작은 원본 그대로)
- ✅ 애니메이션 코드 상자: 44일 단독 실행 코드 Python·TS 792개 (실행 검사 `docs/code-run-report.md`)
- ✅ GitHub Pages 배포

## 콘텐츠 바로가기
| 콘텐츠 | 링크 |
|---|---|
| 📊 학습 대시보드 | https://devops0906.github.io/AI_Voice/ |
| 🗺️ 과정 지도 | https://devops0906.github.io/AI_Voice/#map |
| 🎬 애니메이션 (예: D1) | https://devops0906.github.io/AI_Voice/dashboard/d1/animation.html |
| 📁 일차별 수업 자료 | [`day01/`](day01/) ~ [`day44/`](day44/) |
| 📝 기획 문서 | [`docs/PLAN.md`](docs/PLAN.md) |
| 🎨 디자인 토큰 | [`design/tokens.css`](design/tokens.css) · [`design/DESIGN.md`](design/DESIGN.md) |

## 로컬에서 보기
```bash
python -m http.server 8000
# http://localhost:8000/
```

## 데이터·화면 다시 만들기
```bash
PYTHONIOENCODING=utf-8 python scripts/extract.py all   # 노트북 → data/*.json
python scripts/reskin.py all                           # 원본 애니메이션 → dashboard/dN/
```
