# 기획·결정 문서를 이 레포로 모은다

> 날짜: 2026-11-25 · 영향 레포: API, Front

## 계기

기획서가 API 레포 `docs/` 에, 결정 기록은 API 레포 로컬 `DECISIONS.md` 에, 프론트 관련 결정도 API 쪽에 섞여 있었다.
기능 하나가 두 레포에 걸치는 경우가 대부분이라 어느 레포에 써도 반쪽이었다.

## 결정

- 기획·결정·공통 규칙·아키텍처 소개는 mapshot-planning 에 둔다. 기획은 폴더 단위(`plans/YYYY-MM-주제/`), 결정은 파일 단위.
- 코드 레포에는 `CLAUDE.md` 작업 가이드만 두고, 이 레포를 먼저 보라고 안내한다.
- 옮긴 것: `Mapshot-API:docs/news-ai-digest-feature.md`, `docs/frontend-news-digest.md` → `plans/2026-06-news-ai-digest/`,
  `docs/parcel-*.md` → `plans/archive/2026-parcel-info/`, 로컬 `DECISIONS.md` → `decisions/`.
- `Mapshot-API:docs/api.adoc` 은 API 문서 빌드에 쓰여서 그대로 둔다.
  → 번복(2026-11-25, 비공개 저장소의 API 문서를 외부에 공개할 이유가 없어 docs.kmapshot.com 을 닫고 `docs/` 폴더째 삭제. Mapshot-API PR #138)

## 버린 선택지

- 각 코드 레포에 `docs/` 유지: 두 레포에 걸친 기능의 문서가 갈라진다.
- GitHub Wiki: PR 리뷰를 못 거치고, 화면 캡처·데이터 파일 같이 두기가 불편하다.
