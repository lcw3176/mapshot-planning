# 점검 배너는 프론트 빌드 환경변수로 켠다

> 날짜: 2026-11-25 · 영향 레포: Front · 코드: `Mapshot-Front:src/components/MaintenanceBanner.vue`
> (Mapshot-API 로컬 `DECISIONS.md` 에 있던 기록을 옮김)

## 계기

네이버 API 교체로 API 전체 순단이 예상됐다.

## 결정

배너는 API 가 아니라 Cloudflare Pages 빌드 환경변수만으로 켠다.

- `VUE_APP_MAINTENANCE_MESSAGE`: 문구. 비우면 배너 없음.
- `VUE_APP_MAINTENANCE_END`(선택): ISO 시각(예 `2026-11-27T02:00:00+09:00`). 지나면 재배포 없이 자동으로 숨는다.
  점검 후 환경변수 지우는 걸 잊어도 배너가 남지 않게 하려는 것. 형식이 틀리면 숨기지 않고 계속 보여준다.
- 빌드 타임 변수라 값을 바꾸면 Pages 재배포가 필요하다. 순단 전에 미리 넣고 배포해둔다.
- 닫기(X)는 같은 문구 기준으로 탭 세션 동안만 기억(sessionStorage). 문구가 바뀌면 다시 뜬다.

## 버린 선택지

- 공지 API 로 배너 내려받기: 알려야 하는 순간이 곧 API 가 죽은 시간이라, 정작 필요할 때 안 뜬다.
- `public/` 정적 JSON: 어차피 Pages 재배포가 필요해 이점이 없다.
