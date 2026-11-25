# 필지 정보 조회 기능을 제거한다

> 날짜: 2026-11-25 · 영향 레포: API, Front · 기획 기록: `plans/archive/2026-parcel-info/`

## 결정

지도에서 필지를 눌러 지목·공시지가·용도지역을 보고 질문하던 '필지 선택하기' 기능을 프론트와 API 에서 모두 뺀다.
비는 자리(지도 왼쪽 패널의 모드 버튼, 작업 패널, 모바일 하단 시트)는 도시소식 지도 레이어가 쓴다.

## 제거한 것

- Front: `ParcelInfoCard.vue`, `store/parcel.js`, `MapView`·`map.js` 의 필지 분기, 개발 프록시의 `/parcel`
- API: `application/parcel`, `presentation/parcel`, `domain/parcel`, 브이월드·공공데이터 클라이언트, `GeminiParcelClient`,
  관련 테스트, `schema.sql` 의 `parcel_cache` 생성문, `application.yml` 의 `vworld`·`public-land` 설정, `/parcel` 레이트리밋·로깅·예외 분기

## 운영에서 같이 할 일

- 운영 DB 의 `parcel_cache` 테이블은 남아 있다. 필요 없으면 직접 `DROP TABLE parcel_cache`.
- 서버 환경변수 `vworldKey`, `vworldDomain`, `vworldDailyLimit`, `vworldCacheTtlDays`, `PUBLIC_DATA_SERVICE_KEY` 는 더 안 쓴다.

## 다시 볼 조건

필지 단위 정보가 다시 필요해지면 archive 의 기획 기록(호출량 통제, 캐시 설계)을 출발점으로 쓴다.
