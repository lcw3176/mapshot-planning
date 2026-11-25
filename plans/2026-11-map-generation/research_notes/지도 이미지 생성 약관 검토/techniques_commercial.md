# 원클릭 대형 지도 이미지 생성 — 기술 메커니즘 & 해외 상용 이미지 API 카탈로그

> 조사일 2026-11-25. 카카오/네이버/구글/국내 공공데이터 약관 상세는 다른 리서처 담당 — 여기서는 기술적 메커니즘과 비한국 상용 대안만 다룸.
> 표기: `[실측]` = 이번 조사에서 curl 로 직접 확인한 것, `확인 필요` = 출처로 확정하지 못한 것.

## Q1. 확장 프로그램 없이 브라우저에서 캡처 (html2canvas류 / getDisplayMedia / Element·Region Capture / CDP / print)

### Takeaway
DOM→canvas 재그리기(html2canvas, dom-to-image, modern-screenshot)는 **타일 서버가 CORS 헤더를 주지 않으면 canvas 가 오염(taint)되어 export 불가** — 실측상 카카오 타일은 CORS 헤더가 없어 사실상 불가. 확장 없이 유일하게 "픽셀을 화면에서 그대로 떠오는" 경로는 `getDisplayMedia`(현재 탭 캡처, 매번 사용자 허락 필요)이며, 해상도는 뷰포트 크기로 제한되므로 5000px 결과물을 얻으려면 **지도를 프로그램적으로 패닝하며 프레임을 여러 장 찍어 이어붙이는 방식**이 필요하다.

### Cited Findings
**html2canvas / CORS / canvas tainting**
- 교차 출처 이미지를 CORS 승인 없이 canvas 에 그리면 canvas 가 오염되고, 이후 `toDataURL`/`toBlob`/`getImageData` 가 보안 오류로 막힌다 — [MDN: Use cross-origin images in a canvas](https://developer.mozilla.org/en-US/docs/CORS_Enabled_Image)
- html2canvas 의 `useCORS: true` 는 CORS 요청을 *시도*할 뿐이며, 타일 서버가 `Access-Control-Allow-Origin` 을 돌려주지 않으면 소용없다. `allowTaint: true` 는 오염된 canvas 를 내보낼 수 있게 해주지 않는다 — [html2canvas issue #722](https://www.github.com/niklasvh/html2canvas/issues/722), [html2canvas issue #1614](https://www.github.com/niklasvh/html2canvas/issues/1614), [html2canvas-pro configuration docs](https://raw.githubusercontent.com/yorickshan/html2canvas-pro/HEAD//docs/configuration.md)
- 구글 지도 위 폴리곤 등이 html2canvas 캡처 시 canvas 를 오염시키는 사례 보고 — [StackOverflow 아카이브 #41404690](https://kiwix.lema.org/stackoverflow.com_en_all_2023-11/questions/41404690/polygon-on-google-maps-taints-canvas-when-using-html2canvas)
- 우회책으로 흔히 제시되는 것은 "동일 출처 프록시로 타일을 재서빙" 또는 "타일 레이어를 캡처에서 제외" — [html2canvas issue #485](https://www.github.com/niklasvh/html2canvas/issues/485). (※ 프록시 재서빙은 지도사 약관상 타일 캐싱/재배포에 해당할 위험 — 약관 리서처 확인 대상)
- WebGL 기반 지도(Mapbox GL 등)는 `preserveDrawingBuffer` 가 꺼져 있으면 html2canvas 결과가 검게 나오는 문제가 알려져 있음 — [positioniseverything: black mapbox screenshots](https://www.positioniseverything.net/how-to-fix-black-mapbox-screenshots-with-html2canvas/) (저품질 블로그, 참고용)

**타일 서버 CORS 헤더 실측** `[실측]` (2026-11-25, `Origin: https://kmapshot.com` 으로 curl)
- 카카오 위성 타일 `map0.daumcdn.net/map_skyview/...jpg` → 200, `Access-Control-Allow-Origin` **없음**
- 카카오 일반 타일 `mts.daumcdn.net/api/v1/tile/PNG/...` → 200, ACAO **없음**
- 구글 래스터 타일 `mt0.googleapis.com/vt?...` → 200, `access-control-allow-origin: *` (단 Maps JS API 가 실제로 쓰는 타일 엔드포인트/벡터 렌더링 방식과 같은지는 확인 필요)
- 구글 위성 `khms0.googleapis.com/kh` → 404 이었으나 응답에 Origin 을 그대로 반사하는 ACAO 존재(실제 성공 응답 동작은 확인 필요)
- VWorld `xdworld.vworld.kr/2d/Satellite/...jpeg`, `api.vworld.kr/req/wmts/...` → `access-control-allow-origin: *`
- 네이버 지도 v3 타일 — 추정 URL 들이 400/403 으로 실패해 **확인 필요** (실제 SDK 요청 URL 을 DevTools Network 탭에서 확인해야 함)

**getDisplayMedia (Screen Capture API)**
- 일시적 사용자 활성화(클릭) 필요, HTTPS 필요, 허가는 영속화 불가 — "The user must be prompted for permission every time." — [MDN getDisplayMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia)
- `preferCurrentTab: true` 는 "This Tab" 을 가장 눈에 띄는 선택지로 제시할 뿐, 최종 선택은 사용자 몫 — [MDN getDisplayMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia)
- 제약조건에 `min`/`exact` 사용 불가(TypeError) — [MDN getDisplayMedia](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia)
- 캡처되는 것은 화면에 렌더된 탭 표면이므로, 스크롤 밖/뷰포트 밖 5000px 콘텐츠를 한 번에 잡는다는 공식 기술은 찾지 못함 → 화면에 보이는 것만 캡처된다고 보는 것이 안전(확인 필요: 공식 문서에 명시 문구 없음)

**Element Capture / Region Capture**
- Element Capture 는 Chrome 132 부터 데스크톱 전용, 현재는 자기 탭 캡처(self-capture)에만 허용, 시작은 여전히 `getDisplayMedia()` 사용자 동의 — "Element Capture is available from Chrome 132 on desktop only." — [Chrome Developers: Element Capture](https://developer.chrome.com/docs/web-platform/element-capture)
- Region Capture 는 탭 캡처를 특정 요소 영역으로 *잘라내는(crop)* 기능이며 가리는 요소는 제거하지 못함 — [Chrome Developers: Element Capture](https://developer.chrome.com/docs/web-platform/element-capture)
- 두 API 모두 해상도 한계·화면 밖 콘텐츠 캡처에 대한 언급 없음 — 같은 출처

**CDP `Page.captureScreenshot` / `chrome.tabs.captureVisibleTab`**
- CDP 는 일반 웹페이지에서 접근 불가하고 확장(`chrome.debugger`) 또는 헤드리스/원격 디버깅 브라우저에서만 사용 가능. `captureBeyondViewport` 파라미터로 뷰포트 밖까지 캡처하는 것이 DevTools "Capture full size screenshot" 의 원리 — 공식 문서 페이지 fetch 실패로 **확인 필요** ([CDP Page domain](https://chromedevtools.github.io/devtools-protocol/tot/Page/))
- `chrome.tabs.captureVisibleTab` 은 확장 API 이며 이름 그대로 *보이는 영역*만 캡처(GoFullPage 등은 스크롤하며 여러 장 이어붙임) — 확인 필요(공식 문서 미인용)

**window.print()**
- 지도 SDK 페이지 print 는 브라우저 인쇄 파이프라인을 타며, 타일은 결국 래스터 이미지라 "벡터 export" 효과는 없음. 대형 페이지 크기(@page size)로 PDF 저장 가능하나 WebGL canvas 인쇄 품질·페이지 분할 문제는 미검증 — **확인 필요**

### Inferences
- **html2canvas 계열은 카카오 지도에서는 원천 불가**(CORS 없음 → taint). 구글/VWorld 는 헤더상 가능해 보이나, 지도 SDK DOM(벡터/WebGL/CSS transform 다층 구조)을 html2canvas 가 정확히 재현하는지는 별개 문제이고 실패 사례가 많다. 프록시로 CORS 를 우회하는 것은 기술적으로 되지만 "타일을 서버가 받아 재배포"하는 구조라 약관 위험이 가장 크다.
- **가장 현실적인 '확장 없는 원클릭' 후보: getDisplayMedia + 프로그램적 패닝 + 프레임 스티칭.**
  1) 사용자가 "이미지 만들기" 클릭 → 2) 브라우저 공유 대화상자에서 "이 탭" 선택(1회 클릭) → 3) 페이지가 지도를 격자 단위로 `panTo`/`setCenter` 하고 타일 로딩 완료(idle 이벤트) 후 `ImageCapture.grabFrame()` 또는 `<video>`→canvas 로 프레임 획득 → 4) 오프스크린 canvas 에 이어붙여 PNG 다운로드.
  - 화면 픽셀을 받으므로 canvas taint 문제 없음(MediaStream 프레임은 오염되지 않음 — 확인 필요하나 일반적으로 그렇게 동작).
  - 결과물은 사용자가 자기 화면을 캡처한 것과 동일한 성격이라 현재 "사용자가 GoFullPage 로 스크린샷" 방식과 약관상 위치가 가장 비슷함(서버가 타일을 저장/재배포하지 않음).
  - 단점: 매번 공유 허락 대화상자, 캡처 중 탭 상단 "공유 중" 바, 해상도 = CSS 뷰포트 × devicePixelRatio, 패닝 경계의 라벨 중복/잘림(지도 라벨이 타일 경계를 넘어 재배치됨) → 겹침 여유를 두고 크롭해야 함. 모바일·Safari·Firefox 의 탭 캡처 지원은 제한적(확인 필요).
- Element/Region Capture 는 광고·UI 를 빼고 지도 div 만 깔끔히 잘라내는 데 유용(Chrome 데스크톱 한정). 핵심 문제(뷰포트 크기 제한)는 해결하지 않음.

### Gaps
- getDisplayMedia 프레임 해상도의 상한(고 DPI 디스플레이에서 실제 픽셀 수)과 브라우저별 `preferCurrentTab`/`selfBrowserSurface` 지원 현황 — 공식 표 미확인.
- Chrome canvas 최대 크기(5000×5000=2,500만 px 는 통상 안전하다고 알려졌으나 공식 수치 미확인).
- 네이버 지도 v3 실제 타일 호스트와 CORS 헤더 — 실측 실패.
- CDP 공식 문서 fetch 실패 → captureBeyondViewport 세부 동작 미인용.

## Q2. 서버 측 헤드리스 브라우저(Puppeteer/Playwright) 렌더링

### Takeaway
기술적으로는 가능(공식 SDK 페이지를 큰 뷰포트로 열고 타일 로딩 완료 후 PNG 반환)하지만, **512MB 서버로는 빠듯하고 Chromium 은 보통 1~2GiB 를 권장**받는다. Cloud Run 무료 한도 안에서 저빈도 운영은 숫자상 가능하나, 핵심 걸림돌은 비용보다 **지도사 약관(자동화 접근·서버 측 이미지 생성·캐싱)** 이다.

### Cited Findings
- Cloud Run 무료 한도: 가격 페이지 스냅샷마다 수치가 다름 — 요청 기반 과금 서비스 기준 월 180,000 vCPU-초 / 360,000 GiB-초 로 표시된 판과 240,000 vCPU-초 / 450,000 GiB-초 로 표시된 판이 공존. 라이브 페이지 재확인 필요 — [Cloud Run pricing](https://cloud.google.com/run/pricing)
- 1 GiB-초 = 1GiB 인스턴스 1초 = 256MiB 인스턴스 4초 — [Cloud Run pricing](https://cloud.google.com/run/pricing)
- Puppeteer/Chromium 은 요청당 여러 프로세스를 띄우고 임시 파일이 인메모리 파일시스템을 차지해 메모리를 추가로 소모; 1~2GiB·1vCPU 를 출발점으로 제안(비공식 3자 글) — [OneUptime: Puppeteer on Cloud Run](https://oneuptime.com/blog/post/2026-09-13-puppeteer-browser-lifecycle-cloud-run/view)
- 동일 목적의 오픈소스 선례: `mapbox-map-image-export` 는 헤드리스 브라우저로 Mapbox GL 지도를 고해상도 PNG 로 렌더링(Static API 가 1280px·JPEG 압축 한계라서) — [npm: mapbox-map-image-export](https://npmjs.com/package/mapbox-map-image-export)
- Esri 는 세션 토큰의 프로그램적 사용(예: 베이스맵 타일 대량 export)을 금지 — [Esri product-specific terms e300.pdf](https://www.esri.com/content/dam/esrisites/en-us/media/legal/product-specific-terms-of-use/e300.pdf) (검색 요약 기준, 원문 fetch 확인 필요)

### Inferences
- 대략 산정: 2GiB·1vCPU 인스턴스로 건당 20초 렌더 → 건당 40 GiB-초·20 vCPU-초. 무료 180k vCPU-초 기준 월 ~9,000건, 360k GiB-초 기준 월 ~9,000건 → 저트래픽이면 무료 범위. 단 5000×5000 + WebGL(SwiftShader 소프트웨어 렌더) 은 시간이 더 걸릴 수 있어 실측 필요. 콜드 스타트 수 초 추가.
- 기존 512MB 서버(Cloud Run 별도 서비스가 아닌 경우)에 Chromium 을 같이 올리는 것은 OOM 위험이 커서 비추천.
- **약관 측면의 구조적 문제**: 서버가 지도사 SDK 를 대신 돌려 이미지를 만들고 사용자에게 파일로 넘기면 (a) 자동화/헤드리스 접근, (b) 서버 측 콘텐츠 저장·재배포, (c) API 키의 서버 사용(도메인 제한 키를 서버에서 쓰기 위한 우회) 문제가 겹친다. 일반적으로 주요 지도사는 정적 이미지가 필요하면 자사 Static API 를 쓰라고 하고, JS SDK 화면을 서버에서 캡처해 배포하는 것은 허용 범위 밖으로 보는 경향 — 각 사 약관 리서처 결과로 확정할 것(여기서는 확인 필요).
- 반면 **약관이 명시적으로 허용하는 이미지원(예: 국내 공공 타일, 정적 이미지 API 의 결과물)** 을 서버에서 스티칭하는 용도로는 헤드리스가 필요 없음 — 단순 HTTP 타일 요청 + 이미지 합성(Pillow/sharp)이 훨씬 싸다.

### Gaps
- 5000×5000 WebGL 지도 렌더 시간/메모리 실측값 없음.
- Cloud Run 무료 한도 정확한 현재 수치(페이지 간 상충).

## Q3. 서비스 전용 소형 크롬 확장 vs 서드파티 확장

### Takeaway
자체 확장은 기술적으로 가장 깔끔한 원클릭(CDP `captureBeyondViewport` 또는 captureVisibleTab 스티칭)을 주지만, **"확장 설치"라는 장벽 자체는 그대로**이고 Web Store 심사·단일 목적·데이터 공개 정책 유지보수 부담이 생긴다. 지금의 "서드파티 확장 설치" 대비 이점은 UX 통합(맵샷 페이지 버튼 → 확장이 자동 캡처·저장)과 신뢰도.

### Cited Findings
- 단일 목적(single purpose) 요구: 좁은 주제 영역 또는 좁은 브라우저 기능이어야 하며, 목적과 무관한 권한 요청은 위반 소지 — [Extensions quality guidelines FAQ](https://developer.chrome.com/extensions/single_purpose)
- MV3 는 원격 호스팅 코드 금지: 확장 밖 스크립트 태그, 원격 문자열 eval 은 거절 사유; 전체 기능이 제출 코드로 파악 가능해야 함 — [CWS troubleshooting](https://developer.chrome.com/docs/webstore/troubleshooting.md.txt)
- 2026-07-01 정책 업데이트(8-01 시행): Limited Use 가 단일 목적에 엄격히 필요한 데이터 수집으로 제한, 모든 데이터 수집 공시 의무, 설치 후 데이터 관행 변경 시 고지 — [CWS policy updates 2026](https://developer.chrome.com/blog/cws-policy-updates-2026?hl=en)
- 정책 원문 — [Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies/policies)

### Inferences
- 맵샷 전용 확장 설계 시: `host_permissions` 를 kmapshot.com 으로만 한정, `activeTab` + `debugger`(CDP 전체 캡처용) 또는 `tabs.captureVisibleTab` 스티칭. `debugger` 권한은 설치 시 강한 경고 문구가 떠서 전환율에 불리할 수 있음(확인 필요). 데이터 수집 없음으로 공시하면 심사 부담 작음.
- 기술적 품질 순위: CDP captureBeyondViewport(한 장, 이음매 없음) > captureVisibleTab 스티칭 ≈ getDisplayMedia 스티칭.
- 자체 확장을 만들어도 결과물은 "사용자의 브라우저가 사용자 화면을 캡처"한 것이라 약관상 위치는 현재 방식과 동일 — 약관 리스크를 줄이지도 늘리지도 않음.
- 확장 없는 getDisplayMedia 방식(Q1)이 먼저 시도할 가치가 있고, 그 UX(공유 허락 대화상자)가 불만족스러우면 자체 확장을 2단계로 고려하는 순서가 합리적.

### Gaps
- `debugger` 권한 확장의 CWS 심사 통과 난이도와 설치 경고 문구의 전환율 영향 — 공식 자료 없음.

## Q4. "정적 이미지/인쇄/export 허용"을 명시한 해외 상용 이미지 API

### Takeaway
명시적으로 **인쇄·캐싱을 허용하는 정적 이미지 상품은 있으나 전부 유료이거나 1장 크기가 1280~2048px 로 작다**. 5000px 은 여러 장 스티칭이 필요하고, 스티칭/대량 다운로드는 많은 약관이 금지·제한한다. 무료 티어 + 상업적(애드센스) 사용 + 인쇄 허용을 동시에 만족하는 해외 위성 소스는 찾지 못했다.

### Cited Findings
**Mapbox**
- Static Images API: 가로·세로 각 1~1280px, `@2x` 로 고밀도 렌더, 기본 워터마크형 attribution, `attribution=false` 시 페이지/문서 다른 곳에 표기 의무 — [Mapbox Static Images API](https://docs.mapbox.com/api/maps/static-images/)
- "you cannot export at a higher resolution using the Static Images API" 및 SVG/PDF 등 벡터 미지원 — [Mapbox help: static maps](https://docs.mapbox.com/help/dive-deeper/static-maps/) (검색 요약 기준)
- Studio 인쇄 패널: 최대 8,000×8,000px, 계정당 100장; **"To print images generated from the Mapbox Studio print export option for any use" 는 영업팀 문의 필요**, 인쇄물에 Mapbox attribution 필수 — [Mapbox help: static maps](https://docs.mapbox.com/help/dive-deeper/static-maps/)
- 일반 ToS: 해지 시 서비스에서 다운로드한 콘텐츠 파기 의무, 독점권 표시 제거 금지 — [Mapbox ToS](https://www.mapbox.com/legal/tos). 정적 이미지 인쇄/캐싱 세부 조항은 Product Terms PDF 에 있으며 fetch 실패 → **확인 필요** ([Mapbox Product Terms](https://www.mapbox.com/legal/product-terms))
- 무료 월 요청 수(관행상 Static Images 50,000건/월로 알려짐)는 이번에 공식 확인 못함 → **확인 필요** ([Mapbox pricing](https://www.mapbox.com/pricing))

**MapTiler**
- Static Maps API: 각 변 1~2048px, `@2x`, PNG/JPG/WebP, attribution 끄면 앱에 직접 표기 의무, **무료 플랜에서는 Static Maps 동작 안 함(유료 전용)** — [MapTiler Static Maps API](https://docs.maptiler.com/cloud/api/static-maps/)
- 약관: 인쇄물/이미지/영상에도 웹지도와 유사한 attribution 필요(6.6), 픽셀 포함 지도 콘텐츠 조작·변형 금지(4.4), 상업적 2차 저작물 제작 금지(4.3), 재판매·재배포 금지(4.1), 무료 계정은 MapTiler 로고 표시(6.1) — [MapTiler Terms](https://www.maptiler.com/terms/)
- → "도면 배경으로 쓰려고 가공"하는 맵샷 사용 패턴은 4.4(조작 금지)·4.3 과 충돌 소지(해석 확인 필요).

**Stadia Maps**
- 무료 플랜: 월 200,000 크레딧, **상업적 사용 불가, 위성 없음**. Starter $20(상업 OK, 위성 없음), Standard $80(위성 O), Professional $250 — [Stadia pricing](https://stadiamaps.com/pricing/)
- Static map 20 크레딧/건, **Cacheable static map 2,000 크레딧/건**: 유료 구독 유지 동안 디지털 캐싱 가능 + "print up to 5,000 copies per image" — [Stadia pricing](https://stadiamaps.com/pricing/), [Stadia: cacheable static map images](https://stadiamaps.com/blog/announcing-cacheable-static-map-images/)
- Alidade Satellite 가 static/cacheable static 엔드포인트에서 사용 가능(2026 업데이트), 위성 사용 시 이미지 출처 별도 표기 — [Stadia docs: Alidade Satellite](https://docs.stadiamaps.com/map-styles/alidade-satellite)
- 크레딧 단가 표기 상충(20 vs 10 크레딧) — [Stadia pricing](https://stadiamaps.com/pricing/) vs [tiles.stadiamaps.com/pricing](https://tiles.stadiamaps.com/pricing)

**Esri / ArcGIS World Imagery**
- 표준 World Imagery 레이어는 오프라인 타일 export 용이 아니며, export 는 "World Imagery (for Export)" 레이어로, 그것도 **소량** 오프라인용 — [Esri Community](https://community.esri.com/t5/arcgis-image-server-questions/arcgis-online-basemap-imagery-licensing/m-p/257788), [Esri Support 000014855](https://support.esri.com/en/technical-article/000014855)
- Esri 약관 요약: 콘텐츠 패키지 외 방법으로 베이스맵 타일을 체계적으로 수확(harvest) 금지, 타일 재배포 금지, attribution 필수 — [Esri TOU summary](https://www.esri.com/content/dam/arcgisonline/docs/tou_summary.pdf) (검색 요약 기준, 현재 해당 URL 은 doc.arcgis.com 으로 리다이렉트되어 원문 재확인 필요)
- 실사례: Gaia GPS 는 2025-01-01 부로 Esri 오프라인 타일 다운로드 기능을 중단한다고 공지 — [Gaia GPS blog](https://blog.gaiagps.com/esriupdate)
- ArcGIS Location Platform 무료 티어 수치·상업적 사용 조건 — fetch 실패, **확인 필요** ([ArcGIS deployment terms of use](https://developers.arcgis.com/documentation/mapping-apis-and-services/deployment/terms-of-use/))

**Microsoft Azure Maps / Bing Maps**
- Azure Maps Render Static Image: width 80~2000, height 80~1500, `tilesetId` 에 `microsoft.imagery`(위성) 지원, 위성은 zoom 0~19. 공식 설명에 "report generation, or desktop applications" 용도 언급 — [Azure Maps Get Map Static Image](https://learn.microsoft.com/en-us/rest/api/maps/render/get-map-static-image)
- Render v1 Get Map Image 는 2026-09-17 퇴역 예정(v2 이전 필요) — [Microsoft Q&A / Render v1](https://learn.microsoft.com/en-us/rest/api/maps/render/get-map-image?view=rest-maps-1.0)
- Azure Maps 의 인쇄·캐싱 약관(Product Terms), 무료 월 거래 수 — 검색으로 확인 못함, **확인 필요** ([Azure Maps pricing](https://azure.microsoft.com/pricing/details/azure-maps/))
- Bing Maps for Enterprise: 무료/Basic 계정은 2025-06-30 종료, Enterprise 는 2028-06-30 종료, Azure Maps 로 이전 — [Microsoft Maps FAQ](https://www.microsoft.com/maps/faq.aspx), [Bing Maps blog 2025-01](https://blogs.bing.com/maps/2025-01/What-are-my-options-regarding-Bing-Maps-for-Enterprise-Retirement) → **신규 선택지에서 제외**.

**Thunderforest** — 이번 조사에서 확인 못함(위성 미제공으로 알려져 있으나 **확인 필요**).

### Inferences
- **명시적 인쇄 허용 + 위성**을 만족하는 건 사실상 Stadia(Standard $80/월 + cacheable 2,000크레딧/건 → 7.5M 크레딧이면 월 ~3,750장)와 Mapbox(Studio 인쇄는 영업 문의) 정도. 둘 다 1장 크기가 작아 5000px 은 다중 요청 스티칭이 필요하며, 스티칭을 명시 허용한 문구는 찾지 못함 → 원클릭 무료 서비스엔 비용·약관 모두 부적합.
- MapTiler 정적 지도는 무료 플랜 불가 + 지도 콘텐츠 변형 금지 조항 → 도면 배경 가공 용도와 맞지 않음.
- Esri 는 대량 수확·재배포를 명시적으로 금지하고 실제 집행(Gaia GPS) 사례도 있음 → 서버 측 스티칭 후보에서 제외.
- **한국 도시 위성 화질**: 해외 상용 위성(Mapbox Satellite/Maxar 계열, Esri World Imagery, Azure imagery)은 한국에서 국가 보안 시설 가림·해상도 정책 영향이 있고, 국내 업무용으로는 카카오/네이버/VWorld 항공사진보다 최신성·해상도가 떨어진다는 것이 업계 통념이나 이번에 객관 비교 자료는 찾지 못함 — **확인 필요**. 도시계획 실무자는 국내 항공영상(VWorld) 기대가 높을 것.
- 결론적으로 해외 상용 API 는 "약관이 깔끔한 유료 백업안"이지 무료·원클릭·5000px 요구를 동시에 충족하는 해법은 아님.

### Gaps
- Mapbox Product Terms(정적 이미지 인쇄/캐싱 조항) 원문, Mapbox Static Images 무료 월 한도.
- Azure Maps 정적 이미지 인쇄·캐싱 약관, 무료 거래 한도.
- ArcGIS Location Platform 무료 티어 수치·상업 조건.
- 한국 지역 해외 위성 영상 해상도·촬영 시점 비교.

## Q5. 국내 도시계획 실무자가 쓰는 기존 도구 (UX 벤치마크)

### Takeaway
실무자들은 QGIS + 브이월드 공식 플러그인(V_QGIS) 또는 XYZ 타일 직접 연결로 배경지도를 띄워 쓰는 경우가 많고, 이는 맵샷 경쟁/대체재이자 UX 벤치마크다. 브이월드 타일은 실측상 CORS 를 열어둬(`*`) 브라우저 캔버스 합성에도 기술적으로 가장 우호적이다.

### Cited Findings
- QGIS 공식 플러그인 저장소에 Vworld 가 등록한 "V_QGIS" 플러그인(최소 QGIS 3.0) — [QGIS plugins: V_QGIS](https://plugins.qgis.org/plugins/V_QGIS/latest/)
- 플러그인 메뉴 "공간정보 오픈플랫폼(브이월드)"에서 배경지도 선택 사용 안내 — [WikiDocs 233031](https://wikidocs.net/233031)
- 브이월드 위성지도를 XYZ 타일 URL 로 QGIS 에 직접 추가하는 방법(주소 끝 공백 주의) — [WikiDocs 279354](https://wikidocs.net/279354)
- TMS for Korea 플러그인 로드 오류 시 브이월드 QGIS 플러그인으로 대체하라는 답변 — [인프런 Q&A 1766708](https://www.inflearn.com/community/questions/1766708/tms-for-korea-설치되나-다음과-같은-에러가-뜨고-웹에-표시가-되지-않아요)
- 브이월드 타일 서버 `xdworld.vworld.kr`, `api.vworld.kr` 는 `Access-Control-Allow-Origin: *` `[실측]`

### Inferences
- QGIS 경로는 강력하지만 설치·학습 비용이 큼 → 맵샷의 가치 제안은 "QGIS 없이 브라우저에서 원클릭". 
- 브이월드는 CORS 가 열려 있어 **브라우저에서 타일을 직접 받아 canvas 로 합성 → PNG 다운로드**가 기술적으로 바로 가능(서버 비용 0, 헤드리스 불필요, 사용자 브라우저가 직접 요청). 공공데이터 이용조건(출처표시, 상업 이용 허용 여부 등)만 약관 리서처 결과로 확인되면 "원클릭 대형 이미지"의 1순위 후보. 카카오/네이버는 같은 방식이 CORS 로 막히므로 Q1 의 getDisplayMedia 스티칭이 대안.
- 다음/네이버 지도 웹의 자체 "인쇄" 기능, "Map Downloader" 류 도구의 라이선스 처리 방식은 이번에 조사하지 못함.

### Gaps
- 다음·네이버 지도 웹 인쇄 기능의 최대 출력 크기 및 인쇄물 이용 조건.
- "지도 다운로더"류 국내 도구(타일 수집형)의 실태 — 대부분 약관 위반 소지가 있는 타일 수확 방식일 것으로 추정되나 출처 없음.
- 브이월드 QGIS 플러그인 경유 이미지의 출력·상업 이용 조건(약관 리서처 담당 영역과 겹침).
