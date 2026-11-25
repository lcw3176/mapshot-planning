# Google Maps Platform 약관·제품: 대형 지도/위성 이미지 생성·다운로드 관점 검토 (2026-11-25 기준)

> 조사 범위: Google Maps Platform(GMP) 약관(ToS)·Service Specific Terms(SST)·제품별 Policies 문서, Google 지오 가이드라인(인쇄/스크린샷), 2025-03 가격 개편 후 무료 한도, Map Tiles API·Static API·Google Earth·Earth Engine.
> 1차 출처 원문은 2026-11-25 직접 받아 확인함. ToS는 "Last modified August 26, 2026", SST는 "Last modified November 24, 2026" 판본이며, Map Tiles 문서는 "Last updated 2026-11-09".
> 맵샷 맥락: 무료 서비스에 AdSense를 붙였으므로 **상업적 이용**이고, 산출물은 사용자가 내려받아 CAD/계획도면 배경으로 씀. 즉 **GMP 서비스 바깥에서 쓰이는 이미지 파일**이 남음.

## 1. GMP 약관 핵심 조항: 캐싱·저장, 대량 다운로드, Google 콘텐츠로 콘텐츠 만들기, 인쇄·스크린샷, 상업적 이용, 출처 표시

### Takeaway
현행 ToS §3.2.3(a)는 Google Maps Content를 "서비스 밖에서 쓰려고" export·extract·scrape하는 것을 금지하고, 그 예로 pre-fetch·store·rehost와 **타일 대량 다운로드**를 명시함. §3.2.3(b)는 SST가 명시적으로 허용하지 않는 캐싱을 금지함(지도 이미지·타일에 대한 캐싱 허용 조항은 SST에 없음). 그래서 "고해상도 지도 이미지를 만들어 파일로 내려주는" 형태는 어느 API를 쓰든 ToS 문언과 정면으로 부딪힘. 예외 경로는 Google 지오 가이드라인이 허용하는 **스크린샷·인쇄를 사업 문서(보고서·제안서·발표)에 쓰는 것**인데, 이는 최종 사용자 개인의 이용에 대한 허용이지, GMP 고객(맵샷)이 이미지 생성·배포 서비스를 운영해도 된다는 허용은 아님.

### Cited Findings
- **§3.2.3(a) No Scraping**(원문 발췌): "Customer will not export, extract, or otherwise scrape Google Maps Content for use outside the Services." 예시로 "(i) pre-fetch, index, store, reshare, or rehost Google Maps Content outside the services; (ii) bulk download Google Maps tiles…"를 듦. — [GMP Terms of Service](https://cloud.google.com/maps-platform/terms)
- **§3.2.3(b) No Caching**: "Customer will not cache Google Maps Content except as expressly permitted under the Maps Service Specific Terms." — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **§3.2.3(c) No Creating Content From Google Maps Content**: "Customer will not create content based on Google Maps Content." 예시로 "(i) trace or digitize roadways, building outlines… from the Maps JavaScript API Satellite base map type"와 "(vii) … train, test, validate or fine-tune" AI 모델을 듦. → 도시계획 도면의 배경으로 깔고 그 위에서 도로·건물을 **트레이싱**하면 바로 이 예시에 해당함. — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **§3.2.3(d) No Re-Creating Google Products**: 예시 "(i) re-distribute the Google Maps Core Services or pass them off as if they were Customer's services". 고객 제품은 "substantial, independent value"를 가져야 함. — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **§3.2.3(e) No Use With Non-Google Maps**: Google Maps Core Services를 non-Google 지도와 함께 쓰거나 그 근처에 두면 안 됨. (예: 브이월드·카카오 지도와 같은 화면에 섞는 경우) — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **§3.2.1(a)**: "copy, modify, create a derivative work of …" 금지. 이 조항은 문맥상 소스코드 추출 항목과 묶여 있음. **(b)** "sell, resell, sublicense, transfer, or distribute the Services" 금지. — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **§3.2.2(a) 이용약관 고지 의무**: 고객 앱의 이용약관에서 Google Maps 기능·콘텐츠가 포함돼 있음을 알리고, Google Maps/Google Earth Additional Terms(https://maps.google.com/help/terms_maps/)와 Google 개인정보처리방침을 따른다고 명시해야 함. — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **§3.2.2(b) Attribution**: Google이 서비스로 제공하는 로고·저작권 표기를 모두 표시해야 하며 "Customer will not modify, obscure, or delete such attribution." — [GMP ToS](https://cloud.google.com/maps-platform/terms)
- **SST 일반 §3 Google ID Caching**: 캐싱이 허용되는 것은 place_id, pano_ID, Aerial View video_ID 같은 **ID 값**뿐임. SST 목차(Address Validation, Directions, Geocoding, Google Earth, Maps SDK for Android, Places, Routes, Solar, Weather 등)에는 **Maps Static API, Map Tiles API, Maps JavaScript API에 대한 별도 캐싱 허용 조항이 없음.** — [GMP Service Specific Terms](https://cloud.google.com/maps-platform/terms/maps-service-terms)
- **과거 ToS(2018-02 판) §10.5(b) No derivative works**: 금지 예시로 "(i) creating server-side modification of map tiles; (ii) stitching multiple static map images together to display a map that is larger than permitted in the Maps APIs Documentation"를 들었음. 같은 판에 "No printing 5,000+ copies for direct marketing"과 "No use as a core part of printed matter" 조항도 있었음. — [Google Maps APIs Terms of Service (2018-02-07, 구판)](https://developers.google.com/maps/terms-20180207)
- **지오 가이드라인: 일반 원칙**: "You generally don't need to submit a request…" 다만 "For commercial uses where our mapping products are used for revenue-generating purposes, such as integrating Google Maps … into a mobile or web app, use Google Maps Platform instead." 또 스크린샷에 주석(점·선·라벨)을 다는 것은 허용하지만 "must not significantly alter how Google Maps… would look online", 색 변경이나 출처 표시 삭제는 불가. — [Google Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- **지오 가이드라인: Google Maps 인쇄**: "You may print Google Maps content for non-commercial or personal use". "GO FOR IT" 목록에 "Business documents such as company reports, proposals, presentations, etc."와 책(5천 부 이하)이 있음. "don't do this" 목록에는 5천 부 초과 서적, 인쇄 내비게이션물의 핵심 요소, 굿즈·포스터, 광고의 주된 소재가 있음. — [Google Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- **지오 가이드라인: 위성 이미지**: 온라인 동영상 항목에서 "Satellite View imagery falls under the same commercial restrictions as Google Earth"라고 명시함. — [Google Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- **지오 가이드라인: Street View**: 인쇄 용도 전면 금지. — [Google Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/); 같은 내용이 [Map Tiles API Policies](https://developers.google.com/maps/documentation/tile/policies)의 "Print" 절에도 있음.

### Inferences
- 현행 ToS에는 구판의 "stitching 금지" 문구가 직접 남아 있지 않음. 하지만 §3.2.3(a)(store/rehost/bulk download)과 (b)(캐싱 금지)가 더 넓게 같은 행위를 막음. 구판 문구는 **Google의 해석 방향**(모자이크로 문서상 크기 한도를 넘기는 것은 위반)을 보여주는 근거로 쓸 수 있음.
- 핵심 쟁점은 "for use outside the Services"임. 맵샷의 결과물은 CAD/도면에 붙는 파일이므로 정의상 서비스 밖에서 쓰임. 서버에서 합성하든 브라우저에서 합성하든 **Customer(맵샷)가 export를 가능하게 만드는 구조**이면 §3.2.3(a)와 "will not permit a third party to"(§3.2 서문)에 걸릴 위험이 큼.
- 현재 방식(JS API로 큰 지도를 띄우고 **사용자가 직접 브라우저로 캡처**)은, 캡처 행위가 최종 사용자의 지오 가이드라인상 허용 범위(사업 문서용 스크린샷·인쇄, 출처 표시 유지)에 기댈 여지가 있음. 그래서 서버 측 합성보다 방어 논리가 낫다고 판단함. 다만 5000×5000 지도를 띄우는 목적 자체가 "캡처용"이라는 점은 §3.2.3(a)의 정신과 긴장 관계에 있음 (**회색지대, 확인 필요**).
- **트레이싱 리스크**: 계획도면 배경으로 쓰는 사용자가 위성사진 위에서 도로·건물 윤곽을 따라 그리면 §3.2.3(c)(i)의 예시와 사실상 같음. 맵샷이 이를 "용도"로 홍보하면 위험이 커지므로 마케팅 문구에서 "트레이싱"·"디지타이징" 표현은 피하는 것이 안전함.

### Gaps
- "Google Maps Content" 정의 조항(ToS 정의 절)의 원문 문구는 이번에 발췌하지 못함 (확인 필요).
- 지오 가이드라인의 "Business documents"(사업 문서) 허용이 상업 엔지니어링 회사의 납품 도면·용역 보고서까지 포함하는지는 명시되지 않음. 문서 첫머리는 "non-commercial or personal use"라고 하고, 목록은 company reports/proposals를 허용해 서로 긴장함 (확인 필요, Google이 개별 문의에 예외를 주지 않는다고 명시).
- ToS 판 사이에 §3.2.3 문구가 바뀐 이력(2025-06, 2025-07, 2026-06, 2026-08 판)을 비교하지 못함.

## 2. Maps Static API: 최대 크기, 모자이크(스티칭), 다운로드, 무료 한도·가격

### Takeaway
Static API는 최대 640×640(scale=2이면 1280×1280 px)이고, 지원팀에 문의하면 2048×2048까지 "potential options"가 있음. 5000px급은 여러 장을 이어 붙여야 하는데, 이는 구판 ToS가 명시적으로 금지했던 행위이고 현행 ToS의 캐싱·스크래핑 금지에도 해당함. 2025-03-01부터 $200 월 크레딧이 없어지고 SKU별 무료 한도로 바뀜. Static Maps는 월 10,000건 무료, 이후 1,000건당 $2.00.

### Cited Findings
- 크기 한도: "scale=1 640x640 / scale=2 640x640 (returns 1280x1280 pixels)". scale은 1과 2만 허용. — [Maps Static API Get Started](https://developers.google.com/maps/documentation/maps-static/start)
- 확장: "For larger image sizes beyond the standard limits, contact Google Maps Platform support for potential options up to 2048x2048 pixels." — [Maps Static API Get Started](https://developers.google.com/maps/documentation/maps-static/start)
- 스티칭 금지(구판): "stitching multiple static map images together to display a map that is larger than permitted in the Maps APIs Documentation". — [Maps APIs ToS 2018-02-07](https://developers.google.com/maps/terms-20180207). 2차 인용으로 [Cesium 포럼](https://community.cesium.com/t/cesium-dev-static-maps-api-imagery-provider-functionality/5628)도 있음.
- 가격(2026-11 확인): Essentials SKU "Static Maps", 무료 한도 10,000건/월, 이후 1,000건당 $2.00 → $1.60 → $1.20 → $0.60 → $0.15(구간 할인). — [GMP Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- 2025-03-01 개편: "we are modifying the USD $200 monthly recurring credit by offering a free monthly usage threshold for each Core Services SKU". 무료 한도는 Essentials 10,000, Pro 5,000, Enterprise 1,000이고, 2D Map Tiles와 Street View Tiles만 100,000. — [GMP Billing FAQ](https://developers.google.com/maps/billing-and-pricing/faq)
- Static API 캐싱 허용 조항은 SST에 없음(1번 항목 참조). — [GMP SST](https://cloud.google.com/maps-platform/terms/maps-service-terms)

### Inferences
- 5000×5000 px를 Static(scale 2, 1280px)으로 덮으려면 최소 4×4=16장(겹침을 두면 그 이상)이 필요함. 무료 10,000건/월이면 대략 600건 내외/월만 처리 가능해 비용 면에서도 맞지 않고, 이어 붙이는 것 자체가 위반 소지임 → **Static API 모자이크 방식은 배제 권고.**
- 1280×1280 단일 이미지를 사용자가 저장하는 것(사업 문서용)은 지오 가이드라인에 기대 볼 수 있지만, 도면 배경으로는 해상도가 부족함.
- Static 이미지 `<img>`를 사용자가 "다른 이름으로 저장"하는 것을 Static API 문서가 명시적으로 허용하거나 금지하는 문구는 찾지 못함.

### Gaps
- Maps Static API 전용 Policies 페이지(이전 URL `/maps-static/policies`)는 2026-11 현재 404임. 현행 Static 정책 문서에 스티칭·저장 관련 문구가 있는지 확인하지 못함 (확인 필요).
- 2048×2048 확장이 유료 계약(구 Premium Plan) 전제인지는 문서에 없음 (확인 필요).

## 3. Map Tiles API (2D 위성 타일): 세션 토큰, 캐싱, 클라이언트 합성·내보내기, 무료 한도

### Takeaway
Map Tiles API는 위성 타일을 직접 받을 수 있어 기술적으로는 대형 이미지를 합성하기 가장 쉬운 경로임. 그러나 Policies가 "map visualizations" 용도로만 쓰라고 하고 **"Offline uses"를 금지 용도로 명시**하며, 캐싱은 HTTP Cache-Control 헤더를 따르는 범위로 제한함. 브라우저 canvas에서 합성한 뒤 PNG로 내보내 오프라인 도면에 쓰는 것은 이 정책과 ToS §3.2.3(a)에 걸릴 가능성이 높음. 무료 한도는 월 100,000 타일로 넉넉하지만, **기본 일일 쿼터가 15,000 타일/프로젝트**임.

### Cited Findings
- 용도 제한: "applications should use Map Tiles API for map visualizations. You may not use Map Tiles API for any non-visualization use cases, such as: Image analysis / Machine interpretation / Object detection or identification / Geodata extraction or resale / Offline uses, including for any of the above". — [Map Tiles API Policies](https://developers.google.com/maps/documentation/tile/policies)
- 캐싱: "you must not pre-fetch, index, store, or cache any Content except under the limited conditions stated in the terms." 응답의 Cache-Control(max-age, stale-while-revalidate, must-revalidate, private)과 ETag를 HTTP 규격대로 지켜야 함. — [Map Tiles API Policies](https://developers.google.com/maps/documentation/tile/policies)
- 인쇄: Policies의 "Print" 절은 "Street View imagery may not be used for print purposes"만 언급하고, 2D 타일의 인쇄에 대해서는 별도 문구가 없음. — [Map Tiles API Policies](https://developers.google.com/maps/documentation/tile/policies)
- Policies 요약문: "Content restrictions prohibit unauthorized caching, data extraction, and offline use". 동영상 제작과 3D 타일에는 별도 지침이 있음. — [Map Tiles API Policies](https://developers.google.com/maps/documentation/tile/policies)
- 세션 토큰: 2D·Street View 타일 요청에는 session 파라미터가 필수. mapType은 roadmap/satellite/terrain/streetview이고, 토큰 유효기간은 "currently valid for two weeks", 같은 토큰을 여러 클라이언트에서 쓸 수 있음. highDpi와 scaleFactor2x/4x 옵션이 있음. — [Session tokens](https://developers.google.com/maps/documentation/tile/session_tokens)
- 위성 타일 요청 형식: `https://tile.googleapis.com/v1/2dtiles/z/x/y?session=…&key=…`. 문서 예제는 curl로 타일을 로컬 파일에 저장함. 줌 0~22, viewport 요청 응답에 표시해야 할 attribution과 최대 줌이 포함됨. — [Satellite tiles](https://developers.google.com/maps/documentation/tile/satellite), [2D Tiles overview](https://developers.google.com/maps/documentation/tile/2d-tiles-overview)
- 가격: Essentials "Map Tiles API: 2D Map Tiles", 무료 100,000건/월, 이후 1,000건당 $0.60(100만 건까지) → $0.48 → $0.36 → $0.18 → $0.045. Photorealistic 3D Tiles는 Enterprise로 무료 1,000건, 1,000건당 $6.00. — [GMP Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- 쿼터: "Maximum 15,000 2D Tile, Street View Tile, Thumbnail, or Street View PanoID queries per project per day", 분당 6,000건. 상향은 지원팀 요청. — [Map Tiles API Usage and Billing](https://developers.google.com/maps/documentation/tile/usage-and-billing)
- 같은 페이지에 "$200 monthly credit is available until February 28, 2025"라는 문구가 남아 있음. 현행 정책은 SKU별 무료 한도임. — [Map Tiles Usage and Billing](https://developers.google.com/maps/documentation/tile/usage-and-billing); [Billing FAQ](https://developers.google.com/maps/billing-and-pricing/faq)

### Inferences
- 5000×5000 px는 256px 타일 기준 약 20×20 = **400타일/건**임(정렬 여유를 두면 441). 무료 100,000건/월이면 약 **230~250건/월**만 무료이고, 일일 기본 쿼터 15,000이면 하루 약 35건에서 막힘. 비용과 쿼터 모두 맵샷 규모에 맞지 않음(추정 계산).
- 클라이언트 canvas 합성 후 PNG 내보내기는 "Offline uses" 금지와 ToS §3.2.3(a)의 "export … for use outside the Services"에 해당한다고 보는 것이 합리적임. 2024-09에 서버 타일 스티칭을 접은 판단과 **같은 이유로 클라이언트 합성도 위험**함. 처리 위치(서버/클라이언트)는 약관상 핵심 변수가 아님.
- 2D 타일 인쇄 금지 문구가 Policies에 없다는 점은 "인쇄 자체는 Street View만 막혀 있다"는 근거가 될 수 있음. 그러나 오프라인 사용 금지가 우선 적용된다고 봐야 함.

### Gaps
- tile.googleapis.com 응답에 CORS 헤더(Access-Control-Allow-Origin)가 붙는지, 즉 canvas taint 없이 toDataURL이 되는지는 실측하지 못함 (확인 필요). 기술적으로 가능해도 약관상 문제는 그대로임.
- 2D 타일 Cache-Control max-age의 실제 값을 확인하지 못함 (확인 필요).

## 4. Google Earth / Earth Pro "이미지 저장"·인쇄, Google Earth(GMP 편입), Earth Engine, Aerial View

### Takeaway
지오 가이드라인상 Google Earth 콘텐츠는 "may not be used for any commercial or promotional purposes"가 원칙임. 인쇄는 사업 문서(보고서·제안서·발표)에 한해 허용되고, 웹·앱에서 상업적으로 쓰는 것(예: 건설 현장 위치 표시)은 금지됨. Earth Pro의 "Save Image"는 사용자 개인이 사업 문서용으로 쓰는 경로로는 가능하지만, 맵샷이 이를 서비스로 대행할 근거는 없음. Earth Engine에는 Google 위성 베이스맵이 들어 있지 않고, Aerial View는 동영상 제품이라 대형 정사 이미지 생성에는 맞지 않음.

### Cited Findings
- Earth 일반: "Google Earth content may not be used for any commercial or promotional purposes." 연구·교육·영화·비영리 용도는 허가 없이 가능하고, 출처 표시는 필수. — [Google Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- Earth 인쇄 "Go for it": 책(5천 부 이하), 정기간행물, "Business documents such as company reports, proposals, presentations, etc." — [Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- Earth 웹·앱 "don't do this": 상업·홍보 목적의 웹 사용 금지. 예시에 "Real estate listings or company profiles", "**Construction site locations**", 디지털 광고가 있음. 비상업 용도로 "a handful of static images" 내보내기는 허용. — [Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- Earth 산출물 재가공: "You may not use output, or use third party tools to capture output, from Google Earth, Google Earth Pro, or Earth Studio to reconstruct 3D models or create similar content, or to create other content, products, or services that may violate our Terms of Service." — [Geo Guidelines](https://about.google/brand-resource-center/products-and-services/geo-guidelines/)
- Earth Pro 이미지 저장 해상도: 4800×3200 px라는 출처가 다수([Neowin](https://www.neowin.net/software/google-earth-pro-73610201/), [Atlas](https://atlas.co/blog/top-5-features-in-google-earth-pro/))이고, 4800×4800([TechSpot](https://www.techspot.com/downloads/1018-google-earth.html)), 4800×3008([RedShark](https://www.redsharknews.com/vr-ar/item/5883-whats-the-best-photo-realistic-3d-animation-software-money-cant-buy)) 등 출처마다 다름. 공식 도움말은 [Save your favorite map image](https://support.google.com/earth/answer/148146?hl=en) (최대값 **확인 필요**).
- Google Earth(웹)의 GMP 편입: SST §8 "Google Earth" 신설. §8.3.1: 사용자가 Earth 디자인 기능으로 만든 디자인은 "can be downloaded (e.g. as a KMZ or PNG file) if they are Customer Data". §8.1.4: Customer Data는 Google Maps Content가 식별·역추적·대체될 수 없을 만큼 "substantially transformed"된 데이터로 정의됨. §8.2: 데이터 레이어 다운로드·export 금지. §8.3.2: "should not be used for construction or structural engineering designs". — [GMP SST](https://cloud.google.com/maps-platform/terms/maps-service-terms)
- Google Earth Professional/Professional Advanced는 2025-10-01부터 GMP Core Services로 편입돼 GMP 약관 적용, Standard는 무료. 가격은 $75/사용자/월이 어느 등급인지 페이지마다 달라 **확인 필요**. — [Google Earth plans](https://developers.google.com/maps/documentation/earth/earth-plans)
- Earth Engine: 비상업 쿼터 등급(Community 150 EECU-시간/월 등)은 2026-04-27부터 시행. 상업 이용은 유료(EECU-시간당 $0.40부터 등)이고, 비상업에서 상업으로 바꾸면 되돌릴 수 없음. — [Earth Engine noncommercial tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers), [Earth Engine pricing](https://cloud.google.com/earth-engine/pricing)
- Aerial View: Pro SKU, 무료 5,000건/월, 1,000건당 $16.00. SST에서는 video_ID 캐싱만 허용. — [GMP Pricing](https://developers.google.com/maps/billing-and-pricing/pricing), [GMP SST](https://cloud.google.com/maps-platform/terms/maps-service-terms)

### Inferences
- §8.3.1의 PNG 다운로드는 **사용자가 만든 디자인(Customer Data)**에 한정됨. Google 위성 이미지가 그대로 보이는 PNG는 "substantially transformed" 요건을 충족하지 못하므로 위성 배경 내보내기 근거가 될 수 없음. 게다가 §8.3.2가 건설·구조설계 용도를 배제함.
- Earth Engine은 Sentinel·Landsat 등 공개 데이터의 분석 플랫폼이고 Google 지도 위성 베이스맵을 제공하지 않음(카탈로그 근거는 **확인 필요**). 또 맵샷은 광고 수익이 있어 비상업 등급 대상이 아니라고 봄 → 무료 경로가 아님.
- 사용자에게 "Google Earth Pro로 직접 저장하라"고 안내하는 것은 맵샷의 약관 위반이 아님. 다만 그 사용의 적법성(사업 문서 범위 여부)은 사용자 책임이고, 맵샷의 상품 가치와도 무관함.

### Gaps
- Earth Pro 저장 이미지 최대 해상도 공식값 (확인 필요).
- Google Earth Professional의 이미지 내보내기 기능·한도·가격 (확인 필요).
- Earth Engine 카탈로그에 Google 고해상도 베이스맵이 없다는 것을 공식 문서로 확인하지 못함 (확인 필요).

## 5. Maps JavaScript API 타일의 canvas 내보내기(CORS)와 ToS, 한국 지도 데이터 현황

### Takeaway
JS API Policies는 ToS §3.2.3을 그대로 다시 적어 "Don't export, extract, or scrape Google Maps Content for use outside the Services"라고 함. 따라서 JS 지도를 canvas로 합성해 PNG를 내려주는 기능을 맵샷이 **직접 제공**하는 것은 CORS로 기술적 가능 여부와 상관없이 위반 소지가 큼. 한국은 2026-02-27에 1:5,000 지도 데이터 국외 반출이 조건부 승인됨. 다만 이것이 GMP 도로 지도 품질 개선으로 언제 이어지는지는 확인되지 않음.

### Cited Findings
- JS API Policies: "Content pre-fetching, caching, or storage is generally restricted, but place IDs are exempt". 같은 문서의 "Data storage, caching, and scraping" 절이 §3.2.3(a)(b)를 재확인함. — [Maps JavaScript API Policies](https://developers.google.com/maps/documentation/javascript/policies)
- JS API의 Dynamic Maps는 Essentials, 무료 10,000 로드/월, 이후 1,000건당 $7.00. Embed API는 무제한 무료. — [GMP Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- 한국: 2026-02-27 정부 협의체가 Google의 1:5,000 지도 데이터 국외 반출을 **조건부 승인**함. 조건은 국내 파트너 서버에서 처리, 사전 승인, 등고선 등 민감 정보 제외, 국내 컴플라이언스 담당자 배치 등. — [Korea Times](https://www.koreatimes.co.kr/business/companies/20260227/korea-conditionally-approves-google-request-to-export-map-data), [TechCrunch](https://techcrunch.com/2026/02/27/south-korea-opens-the-door-to-let-google-maps-operate-fully), [JURIST](https://www.jurist.org/news/2026/02/south-korea-conditionally-approves-googles-high-precision-map-data-export/)
- GMP 금지 지역(Prohibited Territories)에 한국(남한)은 없음. 목록은 중국·크림·쿠바·이란·북한·시리아·베트남 등. — [GMP Prohibited Territories](https://cloud.google.com/maps-platform/terms/maps-prohibited-territories)

### Inferences
- 현재 맵샷 방식(JS 지도를 크게 렌더링하고 사용자가 확장 프로그램·DevTools로 캡처)은 내보내기 기능을 맵샷이 구현하지 않고 **사용자의 스크린샷 행위에 맡긴다**는 점이 서버·클라이언트 합성 방식보다 방어적임. 이 경계(맵샷 코드가 픽셀을 추출·인코딩하지 않음)를 지키는 것이 중요함. "원클릭 PNG 다운로드" 버튼을 추가하면 이 경계가 무너짐.
- 위 화면에 Google 로고·저작권 표기가 캡처본에 남도록 유지해야 함(§3.2.2(b)와 지오 가이드라인의 출처 표시 요건). 표기를 숨기는 CSS나 옵션은 금지.
- 한국 데이터 반출 승인으로 앞으로 Google 도로 지도 상세도가 나아질 수 있음. 다만 반영 시점·범위(GMP API에 도로 지도 타일로 노출되는지)는 확인되지 않음.

### Gaps
- Google Maps JS가 쓰는 타일 서버(maps.googleapis.com/khms 등)의 CORS 헤더 실측, html2canvas류로 taint 없이 내보낼 수 있는지 (확인 필요, 실측하지 않음. 원시 타일 서버 직접 호출 자체가 약관 문제라 검증을 보류함).
- 2026-02 승인 이후 Google 지도의 한국 도로 지도 상세도가 실제로 개선됐는지, GMP API 타일에 반영됐는지 (확인 필요).
- 현행 ToS에 "스크린샷" 단어가 들어간 조항은 없음. 스크린샷 허용 근거는 지오 가이드라인(비약관 문서)뿐이고, 둘이 충돌할 때 무엇이 우선하는지 Google이 밝힌 바 없음 (확인 필요).
