# 필지정보(PNU) 조회 — 1차 구현 메모

## 무엇을 만들었나

지도에서 필지를 클릭하면 지목·면적·개별공시지가·용도지역을 팝업으로 보여준다.
지시서의 **옵션 A(인터랙티브 팝업)** 만 구현했고, 옵션 B(정적 이미지 라벨링)는 스코프에서 제외했다.

## 호출 흐름

```
Vue (필지 조회 모드 ON) → 지도 클릭
  → GET {API}/parcel?lat=&lng=
     → VWorldClient.findParcelByPoint()   : 연속지적도 GetFeature 로 좌표 → PNU
     → ParcelCache 조회 (PNU 기준)
        ├─ 적중 & 미만료 → 즉시 응답 (브이월드 호출 0회)
        └─ 미스/만료    → 브이월드 4회 호출 후 캐시 저장
```

필지 1건을 새로 조회하면 브이월드 호출은 **최대 5회**(지적도 1 + 속성 4)다.
캐시가 살아 있으면 **좌표→PNU 1회만** 나간다. 캐시 적중률이 트래픽을 좌우한다.

## 브이월드 API

| 용도 | 엔드포인트 |
| --- | --- |
| 좌표 → PNU | `api.vworld.kr/req/data` (`data=LP_PA_CBND_BUBUN`, `geomFilter=POINT(lng lat)`) |
| 토지임야정보 (지목·면적) | `api.vworld.kr/ned/data/ladfrlList` |
| 개별공시지가 | `api.vworld.kr/ned/data/getIndvdLandPriceAttr` |
| 토지이용계획 | `api.vworld.kr/ned/data/getLandUseAttr` |
| 토지특성정보 | `api.vworld.kr/ned/data/getLandCharacteristics` |

응답 envelope 이 서비스마다 다르다(`fields/ladfrlVOList` vs `response/fields/field`).
경로를 하드코딩하지 않고 `VWorldClient` 가 JSON 트리를 재귀 탐색해 필드를 찾는다.

## 트래픽 안전장치 (지시서 3항 대응)

| 항목 | 구현 위치 |
| --- | --- |
| 서버 프록시 (키 미노출) | `ParcelController` / `VWorldClient` — 프론트는 브이월드 URL을 모른다 |
| PNU 기준 캐싱 (TTL 60일) | `ParcelCache` + `ParcelService`. `client.vworld.cache-ttl-days` 로 조정 |
| hover 금지 / 명시적 클릭만 | `parcel.js` 의 `enabled` 플래그. 기본값 OFF |
| 요청 중 중복 클릭 방지 | `parcel.js` 의 `isLoading` 가드 + 스위치 `disabled` |
| 동일 좌표 재클릭 차단 | `parcel.js` 의 `lastQueriedKey` |
| 일일 호출 카운터 | `VWorldCallGuard`. 상한 도달 시 호출 없이 429 |
| 지수 백오프 | `VWorldClient.call()` — 429/5xx 에 300ms → 600ms → 1200ms |
| 요청 rate limit | 기존 `RateLimitInterceptor` 에 `/parcel` 경로 추가 |
| 좌표 범위 검증 | `ParcelService.validateInKorea()` — 잘못된 파라미터로 쿼터 소모 방지 |

## 환경변수

```
vworldApiKey        # 필수. 브이월드 인증키
vworldDomain        # 기본값 https://kmapshot.com
vworldDailyLimit    # 기본값 30000 (아래 오픈 이슈 참고)
vworldCacheTtlDays  # 기본값 60
```

## 남은 일

- **`vworldDailyLimit` 실측치 확인이 먼저다.** 지금 값(30000)은 근거 없는 임시값이다.
  브이월드 개발자센터 로그인 → "제한사용초과요청" 에서 이 키의 실제 일일/초당 한도를 보고 맞춰야 한다.
  초당 한도가 걸리면 백오프만으로는 부족해서 요청 큐잉을 추가해야 할 수도 있다.
- 실제 키로 응답 스키마 검증. `VWorldClientJsonTest` 는 문서에서 추정한 응답 모양으로 짠 테스트라,
  실제 응답이 다르면 필드 탐색은 통과해도 값이 비어 나올 수 있다.
- 만료 캐시 정리(`ParcelService.evictExpired()`) 를 부르는 스케줄러가 아직 없다. 뉴스 수집 배치 옆에 붙이면 된다.
- 사용량이 쌓이면 옵션 B(정적 라벨링) 재검토. 상한(20~30필지) + 베타/유료 전제.
