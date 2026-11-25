# 도시소식 지도 레이어 — 작동 플로우

코드 위치는 `레포:경로`. 클래스 이름은 2026-11-25 브랜치 기준.

## 전체

```
[국토부]                [Mapshot-API]                                   [Mapshot-Front]
RSS(최신 10건) ──①──▶ PressScheduler (매시 정각)
상세·PDF     ──②──▶   └ PressCollectService.collect()
                          ├ saveNew()      : 새 보도자료 + PDF 본문 저장(scope=UNKNOWN)
                          └ extractPending(): Gemini 1회로 지역 추출
                                              → RegionDictionary 로 코드 변환
                                              → scope=LOCAL/NATIONAL 로 갱신
                                   press_release (H2)
                                         │
                       GET /news/map?days=30 ◀──③── pressMap 스토어 load()
                       PressMapService.getMap()      │
                                         └──────────▶ markers / listItems 계산
                                                      ├ 지도: pressOverlays.render()
                                                      └ 패널: PressPanel / PressItem
```

## 수집 방식 요약

| 항목 | 지금 방식 |
|---|---|
| 트리거 | 스프링 `@Scheduled`, 매시 정각(`0 0 * * * *`, Asia/Seoul). 수동: `POST /admin/press/collect` |
| 목록 | 국토부 공식 RSS(XML) 1회 요청. 최신 10건 |
| 상세 | 처음 보는 건만 상세 HTML 을 1건씩 요청(요청 사이 400ms) |
| 본문 | 상세에서 찾은 PDF 첨부를 내려받아 PDFBox 로 앞쪽 10쪽 텍스트 추출(요청 사이 400ms) |
| HTTP | Jsoup, User-Agent `MapshotBot/1.0 (+https://kmapshot.com)`, 타임아웃 HTML 8초·PDF 20초, PDF 30MB 상한 |
| 중복 | `(source, external_id)` 로 거름. 국토부 게시글 id 가 바뀌지 않는 한 같은 건은 한 번만 저장 |
| LLM | 새 건이나 재시도할 건이 있을 때만 Gemini 1회(10건씩). 없으면 호출 안 함 |
| 비용(추정) | 새 건이 없는 시간: RSS 1요청. 새 건 n개: RSS 1 + 상세 n + PDF n(건당 약 2MB) + Gemini 1 |

1시간 간격으로 정한 이유: 보도자료가 하루 중 여러 번 올라오고(조간 배포 전날 오후, 당일 오전, 밤 해명자료), 새 건이 없을 때 비용이 RSS 한 번뿐이라 더 자주 돌려도 부담이 없다. 주기를 바꾸려면 `press.collect.cron` 만 고치면 된다.

## 문서를 어떻게 읽나

국토부 보도자료 한 건은 이렇게 생겼다.

- 상세 페이지 HTML: 제목, 부제(요약 불릿 1~3줄), 담당부서, 등록일, 첨부파일 링크
- 본문: 페이지 안의 iframe 문서뷰어(Synap Document Viewer). 자바스크립트로 그려서 HTML 을 받아도 본문 글자가 없다
- 첨부: 같은 내용의 **HWPX** 와 **PDF**

지금 읽는 것(2026-11-25 부터)

- 상세 HTML(Jsoup): 제목, 부제, 담당부서, PDF 첨부 링크
- **PDF 본문(Apache PDFBox 3.0.3, Apache 2.0)**: `Mapshot-API:infra/client/molit/PdfTextExtractor`
  - 내려받기: `MolitPressClient.fetchPdfText()`. 다운로드 응답 Content-Type 이 `application/x-msdownload` 라 타입 검사를 끄고(`ignoreContentType`), 대신 첫 바이트가 `%PDF-` 인지 확인해 오류 페이지를 거른다.
  - 추출: `PDFTextStripper`, 화면 위치 순서(`setSortByPosition`), 앞쪽 10쪽만. 공백을 하나로 줄이고 빈 줄·쪽 번호 줄(`- 1 -`)을 지운다.
  - 저장: `press_release.body_text`(최대 2만 자)
  - 지역 추출 프롬프트에 건당 본문 앞 3,000자를 넣는다. 그래서 한 번에 넘기는 건수를 20건 → 10건으로 줄였다.
  - 화면에는 여전히 부제만 보여준다(본문은 추출용).
- 국토부 PDF 는 글자가 들어 있는 PDF 다. 2026-11-25 보도자료 하나로 확인: 생성기 `Hancom PDF 1.3`, ToUnicode 폰트 있음, 4쪽, 약 2MB. 그래서 OCR 은 필요 없다.
- 실패해도 수집은 계속한다. PDF 가 없거나, 내려받기·파싱이 실패하거나, 글자가 안 나오면(스캔본) `body_text` 는 비우고 부제만으로 지역을 뽑는다.

검토했다 쓰지 않은 것

- HWPX: zip 안 XML 이라 표준 라이브러리로도 읽히지만, PDF 가 다른 부처·지자체에도 공통이라 PDF 로 맞췄다.
- iText: AGPL.
- Tesseract(Tess4J) OCR: 지금 자료엔 필요 없고, 서버 메모리(컨테이너 512MB) 부담이 크다. 스캔본 출처가 생기면 다시 본다.

남은 확인

- [ ] 실제 운영에서 본문 추출 성공률(`[PressCollect] PDF 본문 추출 실패`, `글자를 못 뽑음` 로그 빈도)
- [ ] 표 안 텍스트 순서가 섞이는지(`setSortByPosition` 효과)
- [ ] 본문을 넣었을 때 지역 추출이 부제만 쓸 때보다 나아졌는지 → `eval/`

## ① 수집: 새 보도자료 저장

`Mapshot-API:application/press/PressCollectService.saveNew()`

1. `MolitPressClient.fetchLatest()` 가 RSS 를 XML 로 읽는다.
   - 항목마다 `link` 의 `id` 파라미터를 외부 id 로 쓴다. 추적 파라미터(`src`, `kw`)는 버리고 상세 URL 을 `.../dtl.jsp?id=<id>` 로 정규화한다.
   - `pubDate`(RFC 1123, +0900)를 서울 시간 `LocalDateTime` 으로.
2. `(source='MOLIT', externalId)` 가 이미 있으면 건너뛴다(유니크 인덱스도 있음).
3. 처음 보는 건만 `fetchDetail(url)` 로 상세 페이지를 연다. 요청 사이 400ms 쉰다.
   - 부제: `ul.bd_view_ul_lst > li` 중 【로 시작하는 줄(국정과제 분류) 제외
   - 담당부서: `ul.bd_view_ul_info` 의 '담당부서'
   - PDF 링크: 첫 `.pdf` 링크(지금은 저장만)
   - 상세 조회가 실패해도 제목만으로 저장한다.
4. PDF 링크가 있으면 `fetchPdfText()` 로 본문을 뽑는다(위 '문서를 어떻게 읽나'). 실패하면 본문 없이 진행.
5. `press_release` 에 `scope=UNKNOWN` 으로 저장. 이 상태는 API 응답에 안 나간다.

RSS 자체가 실패하면 이번 회차는 저장 0건으로 끝나고, 다음 회차(1시간 뒤)에 다시 읽는다. RSS 가 최신 10건만 주므로 1시간 사이에 10건 넘게 올라오면 일부를 놓친다. 2026-11 기준 하루 최대 7건 정도라 현실적으로는 일어나지 않는다.

## ② 지역 추출

`PressCollectService.extractPending()` → `PressRegionExtractor`, `RegionDictionary`

1. 최근 14일 안에 수집됐고 아직 `UNKNOWN` 인 건을 모은다(이번 회차 새 건 + 지난번 실패 건). 10건씩 끊는다.
2. Gemini 1회 호출.
   - 시스템 프롬프트: `PressRegionExtractor.SYSTEM_PROMPT`. LOCAL/NATIONAL 기준, 실제로 나온 지명만, 권역 표현(수도권 등)은 NATIONAL, 지역 최대 10곳.
     본문에 사업 위치가 표·목록으로 나오면 쓰고, 본문의 과거·비교·해외 사례와 문의처 지역은 뺀다.
   - 입력: 번호. 제목 / 부제 / 담당부서 / 본문(앞 3,000자, 줄바꿈은 공백으로)
   - 출력(JSON): `{"items":[{"no":1,"scope":"LOCAL","regions":[{"sido":"경남","sigungu":"창원시"}]}, ...]}`
   - Gemini 설정은 기존 `GeminiClient` 그대로(JSON 강제, 추론 끔, 모델 페일오버).
3. 응답 파싱(`PressRegionExtractor.parse`): 범위 밖 번호, 모르는 scope 는 무시. 깨진 JSON 이면 전부 `UNKNOWN` 유지 → 다음 회차 재시도.
4. 지명 → 행정구역(`RegionDictionary.resolve(sido, sigungu)`)
   - 시도 표기 정규화: '경남', '경상남도', '부산시' 등 → 정식 명칭
   - 시군구는 '창원시', '창원', '의창구', '창원시 의창구' 모두 받는다
   - 시군구가 비면 시도 대표점
   - 시도 없이 여러 곳과 겹치는 이름('중구', '고성군')은 버린다
   - 시도='광주', 시군구='광주시' 는 광주광역시, 시도='경기', 시군구='광주시' 는 경기 광주시
5. 저장: `regionCodes`(콤마 구분 코드), `scope`, `extractionRaw`(그 건에 해당하는 LLM 출력 JSON, 평가용).
   - LOCAL 인데 코드가 하나도 안 나오면 NATIONAL 로 바꿔 저장(전국 목록에라도 보이게).

LLM 키가 없거나 모든 모델이 실패하면 `UNKNOWN` 으로 남고 화면에 안 보인다. 14일 안에 성공하면 그때 나타난다.

## ③ 조회 API

`GET /news/map?days=30` → `PressMapController` → `PressMapService.getMap(days)`

- `days`: 1~180. 오늘 포함 며칠 전 0시부터.
- `published_at` 기준으로 기간 안의 건을 최신순으로 전부 읽고(하루 몇 건 수준이라 메모리에서 묶는다), `UNKNOWN` 은 뺀다.
- 응답

```json
{
  "days": 30,
  "from": "2026-10-27T00:00:00",
  "items": [
    { "id": 12, "source": "MOLIT", "sourceName": "국토교통부",
      "title": "새로운 도심융합특구 선도모델… 전주·창원 도심에 혁신거점 조성 추진",
      "subtitles": ["전주는 'AI 신뢰성 검·인증', 창원은 '방위·원자력' 특화 혁신거점으로", "..."],
      "department": "성장거점정책과",
      "url": "https://www.molit.go.kr/USR/NEWS/m_71/dtl.jsp?id=95092638",
      "publishedAt": "2026-11-24T17:00:00", "scope": "LOCAL",
      "regions": [{ "code": "52110", "label": "전주시", "sido": "전북" }, { "code": "48120", "label": "창원시", "sido": "경남" }] }
  ],
  "regions": [
    { "code": "52110", "level": "SIGUNGU", "label": "전주시", "sido": "전북", "lat": 35.82472, "lng": 127.11642, "itemIds": [12] }
  ],
  "nationalIds": [13, 14]
}
```

- 보도자료 본문은 `items` 에 한 번만 담고, 마커(`regions`)와 전국 목록(`nationalIds`)은 id 로만 가리킨다. 여러 지역에 걸친 건은 여러 마커가 같은 id 를 가진다.
- `Cache-Control: public, max-age=600`.
- 경로가 `NewsController` 의 `/news/{id}` 와 겹치지만 스프링은 리터럴 경로를 먼저 매칭한다.

## ④ 화면

`Mapshot-Front:src/store/pressMap.js`, `src/components/map/PressPanel.vue`, `PressItem.vue`, `pressOverlays.js`, `src/views/MapView.vue`

### 켜기·끄기

1. 데스크톱: 왼쪽 패널의 '지도에서 도시소식 보기'. 모바일: 지도 왼쪽 위 '도시소식'.
2. `press.toggle()` → 처음이거나 기간이 바뀌었으면 `load()` 로 `/news/map?days=` 호출.
3. 켜진 동안 데스크톱 왼쪽 패널은 검색 폼·검색 결과·광고를 `v-show` 로 숨기고 `PressPanel` 을 보여준다(패널 폭 320 → 360px). 모바일은 지도 아래쪽을 덮는 시트(높이 `min(440px, 62%)`).
4. 끄면 마커를 지우고 선택·펼침 상태를 초기화한다. 받아둔 데이터는 유지해서 다시 켤 때 바로 뜬다.

지도 클릭(캡처 범위 지정)은 도시소식과 상관없이 그대로 동작한다. 마커 클릭은 이벤트 전파를 막아 범위 지정으로 번지지 않는다.

### 마커

- `MapView` 가 카카오맵 `idle` 이벤트(이동·확대가 끝날 때)마다 `syncPressView()`: 현재 줌 레벨을 `press.mapLevel` 에, 지도 범위 안 마커 key 를 `press.visibleKeys` 에 넣는다.
- `press.markers`(getter)
  - 레벨 12 미만: 응답의 `regions` 그대로(시군구·구·시도 각각 하나의 마커)
  - 레벨 12 이상: 시도별로 묶는다. 같은 보도자료가 한 시도 안 여러 시군구에 걸려도 한 번만 센다. 위치는 그 시도의 SIDO 대표점이 응답에 있으면 그것, 없으면 시군구 대표점 평균.
- `pressOverlays.render()` 가 카카오 `CustomOverlay` 로 `지역명 + 건수` 버튼을 그린다. 선택된 마커는 반전 색. `markers` 나 `selected` 가 바뀔 때마다 다시 그린다.
- `#map` 에 `isolation: isolate` 를 줘서 마커가 왼쪽 패널 위로 올라오지 않게 했다.

### 목록

- `press.listItems`
  - 마커를 골랐으면: 그 마커의 보도자료
  - 아니면: 지도 범위 안 마커들의 보도자료 합집합(중복 제거)
  - 최신순
- 날짜별로 묶어 보여준다(오늘/어제는 따로 표시). 사흘 안 소식은 노란 점.
- 항목을 누르면 펼쳐서 부제 전체, '국토교통부 원문 보기'(새 탭), '지도에서 보기'.
- '지도에서 보기': 그 보도자료의 첫 지역으로 지도를 옮기고(레벨 10 이상이면 9로 확대) 해당 마커를 고른다.
- '전국 단위 소식 N건'은 접혀 있고, 누르면 펼친다.
- 비었을 때: 기간 안에 소식이 아예 없으면 그렇게, 범위 안에만 없으면 '지도를 넓히거나 기간을 늘려 보세요' + '최근 90일로 늘리기'.

## 운영

- 수동 수집: `POST /admin/press/collect`(어드민 토큰). 새로 저장한 건수를 돌려준다.
- 설정(`application.yml`)

```yaml
press:
  collect:
    enabled: ${pressCollectEnabled:true}
    cron: "0 0 * * * *"   # 매시 정각
    zone: Asia/Seoul
  molit:
    rss-url: https://www.molit.go.kr/dev/board/board_rss.jsp?rss_id=NEWS
```

- 테이블: `press_release`(`schema.sql`). 유니크 `(source, external_id)`, 인덱스 `published_at`. `body_text` 는 나중에 추가돼 `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` 도 같이 있다.
- 로그 키워드: `[PressCollect]`(저장·추출 건수, 지명 해석 실패, PDF 본문 추출 실패), `[PressScheduler]`.
- 지명 해석 실패 로그(`지명 해석 실패 sido=.. sigungu=..`)가 자주 보이면 `RegionDictionary` 별칭이나 프롬프트를 손본다.
