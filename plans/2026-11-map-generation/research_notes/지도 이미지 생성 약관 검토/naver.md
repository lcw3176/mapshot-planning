# 네이버 지도 API(NAVER Cloud Platform Maps) 약관 — 대형 지도 이미지 생성 관점 검토

조사일: 2026-11-25. 1차 근거는 **「네이버 클라우드 플랫폼 Maps 서비스 이용약관」 PDF 원문(v0.4, 부칙: 2025-03-20 시행)** 입니다.
URL: https://xv-ncloud.pstatic.net/images/provision/%5B%EB%AF%BC%EA%B0%84%5DMaps%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%B4%EC%9A%A9%EC%95%BD%EA%B4%80_v0.4_(CLEAN)_1742433558704.pdf
(아래에서는 "Maps 약관"이라고 부릅니다. 이 PDF가 2026-11 현재 최신판인지는 **확인 필요**. 검색 시점에 노출되는 판은 이것뿐이었습니다.)

## 1. 이용약관이 저장·캡처·인쇄·납품물·캐싱·직접 타일 접근·서버 렌더링·상업 이용·합성·출처표시에 대해 말하는 것

### Takeaway
Maps 약관에는 "캡처", "인쇄", "도면", "보고서" 같은 단어가 **아예 나오지 않습니다**. 대신 API **"결과 데이터"는 받은 즉시 1회만 자기 서비스에 쓸 수 있고, 따로 저장·DB화·재사용·가공·배포하면 안 된다**는 포괄 조항(제7조 ⑨·⑪)이 있습니다. 문언대로 읽으면 지도 이미지를 파일로 남기거나, 여러 장을 합성하거나, 서버에서 타일을 긁는 방식은 모두 **회사의 사전 동의 없이는 허용 범위 밖**입니다. 상업·광고 수익 사이트에서 쓰는 것 자체를 금지하는 조항은 없고, 금지 대상은 API/SDK의 **재판매**(제7조 ⑫)입니다.

### Cited Findings
- **결과 데이터 복제·저장·가공·배포 금지 (제7조 ⑨):** "'고객'은 '회사'의 사전 동의 없이 '본 서비스'의 결과 데이터를 본 약관에서 허용한 범위를 넘어서서 무단으로 복제, 저장, 가공, 배포하거나 제3자에게 제공해서는 안됩니다." — [Maps 약관 PDF](https://xv-ncloud.pstatic.net/images/provision/%5B%EB%AF%BC%EA%B0%84%5DMaps%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%B4%EC%9A%A9%EC%95%BD%EA%B4%80_v0.4_(CLEAN)_1742433558704.pdf)
- **즉시 1회 사용 원칙, 별도 저장·DB화·재사용 금지 (제7조 ⑪):** 결과 데이터는 "받은 즉시 자신의 서비스에서 사용하는 것이 아니라" 별도로 저장하면 안 되며, "모든 Maps API의 결과 데이터는 값을 리턴 받는 즉시 1회 자신의 서비스에서 사용하는 것만 허용". 조항이 드는 예시는 좌표 데이터를 모아 API 호출 없이 재사용하는 경우(“엄격히 금지”)입니다. 지도 이미지를 따로 지칭하지는 않습니다. — [Maps 약관 PDF](https://xv-ncloud.pstatic.net/images/provision/%5B%EB%AF%BC%EA%B0%84%5DMaps%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%B4%EC%9A%A9%EC%95%BD%EA%B4%80_v0.4_(CLEAN)_1742433558704.pdf)
- **권리 귀속 (제7조 ①):** 고객은 허용 범위 안에서 쓸 권리만 갖고, 지식재산권이나 "결과 데이터에 대한 권리의 취득을 의미하지 않습니다." — 같은 PDF
- **로고·표시 게재 의무 (제7조 ⑩):** 회사는 "고객이 '본 서비스'를 이용하여 산출한 모든 결과 데이터 또는 '애플리케이션 등'에 '회사'의 로고 또는 '회사'가 지정한 표시의 게재를 요청할 수 있으며", 고객은 이를 따라야 합니다. 결과 데이터(=이미지)에도 표시를 요구할 수 있다는 뜻입니다. — 같은 PDF
- **재판매 금지 (제7조 ⑫):** "API 및 SDK 자체를 그대로 혹은 리패키징하여 재판매할 수는 없습니다." 광고 수익이나 상업 서비스 자체를 금지하는 문구는 없습니다. — 같은 PDF
- **산출물·외부 송출 모니터링 (제7조 ⑬):** 회사는 "산출물 등 결과물 및 외부 송출 내역을 모니터링할 수 있으며", 문제가 확인되면 결과물을 삭제하고 서비스 이용을 중단시킬 수 있습니다. — 같은 PDF
- **가이드 준수 의무 (제7조 ⑦):** 홈페이지의 'Maps 사용 가이드'와 'API 가이드'를 지켜야 합니다. 가이드의 기술적 제약도 계약 내용이 된다는 뜻입니다. — 같은 PDF
- **자동화·우회 접근은 이용 제한 사유 (제8조 ①4, ①6):** "자동화 프로그램 등을 통해 기계적인 접근을 하거나", 시스템에 부당하게 접근하는 경우, "허용된 접근권한을 넘어 접근하는 경우", "대량의 신호 또는 데이터를 보내"는 경우. 공식 SDK나 API를 거치지 않은 타일 직접 수집, 서버 측 대량 호출에 해당할 소지가 큽니다. — 같은 PDF
- **저작권 등 제3자 권리 침해는 중단 사유 (제8조 ①2):** — 같은 PDF
- **명칭 임의 변경 금지:** 개발 가이드는 네이버 Maps의 기능과 서비스 명칭을 "임의로 변경할 수 없으며" 안내된 명칭대로 표기하라고 합니다(검색 요약 기준, 원문 위치는 **확인 필요**). — [Maps 사용 가이드(검색 결과)](https://guide.ncloud-docs.com/docs/application-maps-procedure)
- **구 이용 약관 링크:** JS v3 문서는 여전히 옛 "Terms of Service" 링크 `http://developer.naver.com/wiki/pages/mapAgreement`를 겁니다. 현재 유효한 약관은 NCP Maps 약관입니다. — [NAVER Maps JS v3 Getting Started](https://navermaps.github.io/maps.js.ncp/docs/tutorial-2-Getting-Started.html)
- **2차 자료의 해석:** 한 GitHub 이슈는 제7조 ⑨·⑪을 근거로 "네이버 NCP Maps ❌ 금지 (사전 동의 시 예외 가능성)"라고 정리했습니다. 좌표·주소 저장 맥락입니다. — [woowacourse-teams/2026-jachwi-sunbae #250](https://github.com/woowacourse-teams/2026-jachwi-sunbae/issues/250)
- **오래된 비공식 견해:** 2019년 OSM 한국 메일링리스트 글은 "편집하지 않고 출처를 밝히면 네이버 지도 스크린샷이 허용된다"고 적었습니다. 현행 NCP 약관을 근거로 한 글이 아니어서 신뢰도가 낮습니다. — [talk-ko 2019-06](https://lists.openstreetmap.org/pipermail/talk-ko/2019-June/000456.html)

### Inferences
- **현재 방식(공식 JS v3로 최대 5000×5000 지도를 띄우고 이용자가 직접 캡처):** 약관상 의무를 지는 주체는 '고객'(맵샷 운영자)입니다. 화면에 지도를 보여 주는 것 자체는 결과 데이터를 "즉시 1회 자신의 서비스에서 사용"하는 정상 범위입니다. 하지만 맵샷의 **목적 자체가 이용자가 이미지를 저장해 도면 배경으로 쓰게 하는 것**이라는 점이 문제입니다. 캡처 방법을 안내하는 것까지 고려하면 제7조 ⑨의 "복제·저장·배포"를 사실상 유도한다고 볼 여지가 있습니다. **회색지대**입니다. 서버 스티칭보다는 확실히 약관 문언과의 거리가 가깝지만, "명시적으로 허용됨"이라고 할 근거는 찾지 못했습니다.
- **과거 방식(서버에서 원시 타일 스티칭):** 제7조 ⑨(복제·저장·가공), ⑪(별도 저장), 제8조 ①4(자동화 기계적 접근), ①6가(허용된 접근권한 초과)에 동시에 걸립니다. 2024-09에 이 방식을 중단한 판단은 약관 문언과 맞습니다.
- **헤드리스 브라우저로 서버에서 렌더링한 뒤 PNG로 돌려주는 방식:** SDK를 쓰더라도 결과물을 서버가 생성·저장·배포하는 구조라 ⑨·⑪에 해당하고, 제8조 ①4의 "자동화 프로그램"에도 걸릴 소지가 큽니다. **권장하지 않습니다.**
- **여러 장을 합성해 큰 이미지 하나로 만들기:** "가공" + "저장"이므로 ⑨에 정면으로 해당합니다. 사전 동의 없이는 불가능하다고 보는 것이 안전합니다.
- **납품물(보고서·도면)에 쓰는 행위:** 최종 이용자의 행위라 약관 직접 적용 대상은 아닙니다. 다만 지도 저작권은 네이버(및 위성영상 공급자)에 있고(제7조 ①), 이용자에게 이를 허락할 권한이 맵샷에는 없습니다. 맵샷이 "납품물에 써도 된다"고 안내하면 안 되고, 이용자 책임과 출처 표기를 고지하는 정도가 한계입니다.
- **광고(AdSense) 수익 사이트:** 약관에 금지 조항이 없으므로 상업 이용 자체는 문제가 되지 않는 것으로 보입니다. 쟁점은 저장·가공입니다.
- **실질 리스크:** 제재 수단은 서비스 중단과 결과물 삭제(제7조 ⑬, 제8조)이고, 회사는 "외부 송출 내역"을 모니터링할 수 있다고 명시했습니다. 키 차단이 가장 현실적인 리스크입니다.
- **가장 확실한 해법:** 제7조 ⑨는 "회사의 사전 동의 없이"라고 쓰여 있으므로, **NCP 고객지원에 서면 문의해 사전 동의를 받는 것**이 약관 문언상 열려 있는 정식 경로입니다(비용 없음).

### Gaps
- NCP 사이트의 별도 "Maps 서비스 이용 정책/운영정책" 문서는 찾지 못했습니다. 제8조 ①10이 "운영정책, 공지사항"을 언급하므로 존재 가능성이 있습니다(**확인 필요**).
- 네이버 클라우드 공식 FAQ나 포럼에서 "지도 이미지 인쇄·저장·캡처 가능 여부"에 공식 답변한 글은 찾지 못했습니다. 포럼(ncloud-forums.com)은 접속 시 DNS 오류가 났고, 관련 질문 글([topic/560](https://www.ncloud-forums.com/topic/560), [topic/573](https://www.ncloud-forums.com/topic/573/))도 검색 결과에서는 답변이 보이지 않았습니다(**확인 필요**).
- 지도 하단 저작권 표시나 로고를 캡처물에 반드시 남겨야 하는지에 대한 구체 가이드는 찾지 못했습니다. 제7조 ⑩은 "요청할 수 있다"는 형식입니다.
- 이 PDF가 2025-03-20 이후 개정됐는지는 **확인 필요**합니다.

## 2. Static Map API — 크기·배율·지도 유형·저장·모자이크·요금

### Takeaway
Static Map은 **w·h 최대 1,024px**, `scale=2`(고해상도, 같은 영역을 2배 픽셀로)를 지원하고, 위성(`satellite`, `satellite_base`)을 포함합니다. 따라서 이미지 한 장으로는 5000×5000 같은 대형 출력이 불가능합니다. 여러 장을 이어 붙이면 약관 제7조 ⑨의 "가공·저장"에 해당하므로, **Static Map으로 대형 이미지를 "정당하게" 만드는 길은 약관상 사실상 없습니다**(사전 동의를 받는 경우는 예외). 요금은 과거 **2원/건**이었고 2026 현재 신규 Maps의 무료 이용량 수치는 공식 원문으로 확인하지 못했습니다.

### Cited Findings
- **크기:** `w`, `h` 필수, "1~1,024 픽셀 지원". — [Static Map API 문서](https://api.ncloud-docs.com/docs/ai-naver-mapsstaticmap-raster)
- **배율:** `scale` 값은 1(기본) 또는 2입니다. 1이면 256×256 타일 기반, 2면 512×512 타일 기반으로 "같은 영역을 2배 픽셀"로 만듭니다. — 같은 문서. 결과 이미지가 w×h 그대로인지 2w×2h인지는 **확인 필요**입니다(최대 2048px 출력 가능 여부).
- **지도 유형:** `basic`(기본), `traffic`, `satellite`, `satellite_base`, `terrain`. "hybrid"라는 이름은 없고, 위성+라벨이 `satellite`, 라벨 없는 위성이 `satellite_base`로 추정됩니다(**확인 필요**). — 같은 문서
- **기타:** `level` 0~20, `format` jpg(85%)/png8/png, `crs` 기본 EPSG:4326(EPSG:3857, 5179 등 지원), 마커 최대 20개. — 같은 문서
- **인증:** `GET /raster`(ID·KEY 헤더 인증)와 `GET /raster-cors`(HTTP Referer 인증, 웹 서비스 URL 등록 필요). 문서상 base URL은 `https://naveropenapi.apigw.ntruss.com/map-static/v2/`입니다. 신규 Maps 상품의 호스트 변경 여부는 공지 [notice/all/1570](https://www.ncloud.com/support/notice/all/1570)을 보라고 안내합니다(**확인 필요**). — 같은 문서; [Maps 개요](https://guide.ncloud-docs.com/docs/application-maps-overview)
- **캐시 관련 기술 기능:** "이미지 캐싱으로 인한 오래된 배경 타일" 문제를 피하려고 `dataversion` 파라미터와 Data Version API(`/lastversion`)를 제공하며, 개요 문서는 이를 "CDN 캐시 무효화"용으로 설명합니다. 즉 **고객 측 CDN 캐싱이 존재한다는 것을 기술 문서가 전제**하고 있습니다. 약관 제7조 ⑪과 어떻게 조화되는지는 문서에 설명이 없습니다. — [Static Map API 문서](https://api.ncloud-docs.com/docs/ai-naver-mapsstaticmap-raster); [Maps 개요](https://guide.ncloud-docs.com/docs/application-maps-overview)
- **최종 이용자 저장 허용 여부:** 문서에 언급이 없습니다. 약관 제7조 ⑨·⑪이 적용됩니다(1절 참조).
- **요금(과거, AI NAVER API 기준):** 2023-01부터 "Static Map 2원/건, 월 3,000,000건 무료"(대표 계정 1개). — [NCP 포럼 공지: Maps API 요금 변경 사전 안내('23.1~)](https://www.ncloud-forums.com/topic/99/) (검색 요약 기준. 포럼 직접 접속은 실패해 **원문 확인 필요**)
- **2025-07-01 무료 이용량 종료(구 상품):** "[수정 공지] AI NAVER API ▶ 지도 API 무료 이용량 제공 종료 안내"(등록 2025-05-28, 최종 수정 2025-06-23). AI NAVER API 안의 지도 API 7종(Static Map 포함)의 월 무료 이용량이 끝나고 100% 유료 과금됩니다. — [NCP 공지 528](https://www.gov-ncloud.com/support/notice/all/528) (본문 표는 검색 요약 기준)
- **신규 Maps:** "Web Dynamic Map API, Static Map API, Geocoding API, Reverse Geocoding API는 대표 계정에 한하여 무료이용량을 제공"합니다. 대표 계정은 Maps API를 가장 먼저 쓴 계정이고, 개인은 휴대폰 번호, 사업자는 사업자번호당 1개입니다. "대표 계정이 아닐 경우에는 API 호출 시 과금" — [Maps 개요(2026-11-24 갱신)](https://guide.ncloud-docs.com/docs/application-maps-overview)
- **신규 Maps의 수치는 출처마다 다릅니다:** NCP 요금 페이지 검색 요약에는 "Web Dynamic Map 0.1원/건, Static Map 2원/건"이 대표 계정 무료 이용량과 함께 표시됩니다. — [ncloud 요금 페이지(검색 결과)](https://www.ncloud.com/charge/region/de). 2026 가이드 글은 "월 최소 3,000건에서 최대 6,000,000건"이라고만 씁니다. — [api-academy (2026-09 수정)](https://api-academy.kr/naver-maps-api-guide/). 공식 FAQ "Maps API의 무료이용량 정책이 어떻게 되나요?"는 본문이 렌더링되지 않았습니다. — [NCP FAQ 2828](https://ncloud.com/support/faq/all/2828)

### Inferences
- 5000×5000 위성지도를 Static Map으로 만들려면 scale=1 기준 1024px 타일이 최소 25장 필요합니다. 이걸 이어 붙이는 것은 "가공·저장"이라 약관 문언에 정면으로 걸립니다. **Static Map은 맵샷의 대형 이미지 요구에 대한 합법적 대안이 되지 못합니다.**
- 비용도 걸립니다. 2원/건이 유지된다고 가정하면 5000px 한 장에 25건 이상이 들고, 무료 이용량을 넘기면 과금이 붙습니다. 유료화가 사전 승인 대상인 운영 원칙상 불리합니다.
- 1024px(또는 scale=2로 더 선명한) **단일 이미지를 화면에 표시**하는 용도로는 문제가 없습니다.

### Gaps
- 신규 Maps 상품의 Static Map **월 무료 건수와 초과 단가(2026)**. 요금 페이지가 JS로 렌더링돼 원문을 확인하지 못했습니다(**확인 필요**, NCP 콘솔 > Maps > 요금 또는 FAQ 2828에서 직접 확인).
- scale=2일 때 실제 출력 픽셀 크기(**확인 필요**).
- 신규 Maps에서 Static Map 엔드포인트 호스트가 바뀌었는지(공지 1570, **확인 필요**).

## 3. Dynamic Map JS v3 — 무료 이용량, 스크린샷 조항, 타일 CORS

### Takeaway
JS v3는 이제 `ncpKeyId` 파라미터로 로드합니다(구 `ncpClientId`/`govClientId`/`finClientId`는 폐기 흐름). 과금 단위는 **지도 로드 1건당 0.1원**으로 보이고, 대표 계정 무료 이용량은 **월 600만 건(1,000만 건이라는 자료도 있음)** 으로 소개됩니다. 공식 원문 수치는 **확인 필요**합니다. 스크린샷을 직접 다룬 조항은 없습니다. 타일 CORS 허용 여부를 공식 문서에서 확인하지 못했습니다.

### Cited Findings
- **로딩:** `https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=YOUR_CLIENT_ID`. 기존 `ncpClientId`, `govClientId`, `finClientId`에서 `ncpKeyId`로 통일됐고, "공공기관용 및 금융기관용 콘솔은 중단될 예정이며, 개인/일반 기업용 콘솔로 통합"됐습니다. 인증 실패는 `window.navermap_authFailure`로 감지합니다. — [JS v3 Getting Started](https://navermaps.github.io/maps.js.ncp/docs/tutorial-2-Getting-Started.html)
- **상품 개편 일정:** 신규 Maps 상품은 2025-03 출시, 구 AI NAVER API 신규 가입은 2025-04-17 중단. 기사 기준으로 구 상품은 2024-11에 무료량이 웹·모바일 각 600만 건으로 축소됐고(종전 웹 1,000만/모바일 1억), 초과분은 0.1원/건. 같은 기사는 신규 Maps 무료량을 "월 600건"이라고 적었는데, 다른 자료와 크게 달라 **오기 가능성이 높습니다(확인 필요)**. — [다음 뉴스 2025-04-16](https://v.daum.net/v/20250416153003092)
- **구 상품 무료량 종료:** 2025-07-01부터 AI NAVER API의 Web/Mobile Dynamic Map 무료량이 끝났고, 신규 Maps로 전환해야 무료량을 받습니다. — [NCP 공지 528](https://www.gov-ncloud.com/support/notice/all/528); [toktokhan 2026-05-22](https://www.toktokhan.dev/insight/%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%A7%80%EB%8F%84-api-%EC%82%AC%EC%9A%A9%EB%B2%95)
- **신규 Maps Dynamic Map 무료량:** "Dynamic Map은 대표 계정 기준 월 600만 건". 여러 Application이 하나의 무료량을 공유하므로 '한도 및 알림 설정'으로 상한을 걸라고 권합니다. — [toktokhan 2026-05-22](https://www.toktokhan.dev/insight/%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%A7%80%EB%8F%84-api-%EC%82%AC%EC%9A%A9%EB%B2%95). 반면 600만에서 1,000만으로 상향됐다는 보도도 있습니다. — [매일일보(검색 결과)](https://www.m-i.kr/news/articleView.html?idxno=259010) (시점 **확인 필요**)
- **콘솔 한도:** 일별·월별 이용 한도를 설정할 수 있습니다. — [Maps Application 가이드(검색 결과)](https://guide.ncloud-docs.com/docs/maps-app)
- **스크린샷 조항:** JS v3 문서와 Maps 약관 어디에도 "스크린샷/캡처"라는 단어는 없습니다. 적용되는 것은 제7조 ⑨·⑪의 결과 데이터 일반 조항입니다. — [Maps 약관 PDF](https://xv-ncloud.pstatic.net/images/provision/%5B%EB%AF%BC%EA%B0%84%5DMaps%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%B4%EC%9A%A9%EC%95%BD%EA%B4%80_v0.4_(CLEAN)_1742433558704.pdf)

### Inferences
- 맵샷은 5000×5000 지도 한 장을 1회 로드하므로, 과금 단위가 "지도 로드 1건"이라면 요청당 비용이 아주 작습니다(0.1원 수준). 월 600만 건 무료량이면 사실상 무료 범위입니다. 단, 대표 계정이 맞는지, 새 `ncpKeyId`가 신규 Maps 상품의 Application인지 콘솔에서 확인해야 합니다. 구 AI NAVER API 키라면 2025-07 이후 전량 유료입니다.
- **canvas export(toDataURL)로 서버 캡처를 대체하는 방식:** 타일 서버가 CORS를 허용하지 않으면 canvas가 오염(tainted)돼 내보내기가 불가능합니다. 허용하더라도 결과 데이터를 "저장"하는 기능을 맵샷이 직접 제공하는 셈이라 약관상 현재 방식(이용자 캡처)보다 리스크가 큽니다.

### Gaps
- 네이버 지도 타일 서버(pstatic 계열)가 `Access-Control-Allow-Origin`을 보내는지. 공식 문서에 기재가 없고, 이번 조사에서 실측하지 않았습니다(**확인 필요**: DevTools Network에서 타일 응답 헤더 확인).
- 신규 Maps Web Dynamic Map의 공식 무료량(600만 vs 1,000만)과 과금 단위(로드 1건 정의) — 공식 요금 페이지 원문 **확인 필요**.
- 대형(5000px) 지도 로드가 타일 수와 무관하게 1건으로 집계되는지 공식 설명을 찾지 못했습니다(**확인 필요**).

## 4. 위성영상 공급자 저작권 표기

### Takeaway
Maps 약관과 조사한 API 문서에는 **위성영상 공급자(예: 항공사진 제공처)를 명시한 저작권 조항이 없습니다.** 약관은 저작권 등 제3자 권리 침해를 이용 중단 사유로만 일반적으로 규정합니다.

### Cited Findings
- 제8조 ①2: "저작권 등 제 3 자의 권리를 침해한 경우" 이용 중단. 제8조 ①1은 저작권법 위반을 명시합니다. — [Maps 약관 PDF](https://xv-ncloud.pstatic.net/images/provision/%5B%EB%AF%BC%EA%B0%84%5DMaps%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%B4%EC%9A%A9%EC%95%BD%EA%B4%80_v0.4_(CLEAN)_1742433558704.pdf)
- 제7조 ①: 결과 데이터에 대한 권리를 고객이 취득하지 않습니다. — 같은 PDF

### Inferences
- 위성/항공영상의 원저작권자 표기는 지도 하단 저작권 문구(지도 컨트롤)에 나타나는 것으로 보입니다. 캡처본에 이 표기를 남기도록 안내하는 것이 안전합니다(약관 근거라기보다 저작권 일반 원칙).

### Gaps
- 네이버 위성지도 영상의 공급처와, 공급처별 재배포 제한이 있는지 공식 자료를 찾지 못했습니다(**확인 필요**: 지도 우하단 저작권 표기 텍스트를 직접 확인).

## 5. 이미지 인쇄·저장에 대한 NAVER Cloud 공식 FAQ·포럼 답변

### Takeaway
**공식 답변을 찾지 못했습니다.** 관련 FAQ는 무료량 정책뿐이고, 포럼의 이미지 저작권 질문 글은 답변을 확인할 수 없었습니다.

### Cited Findings
- 포럼 "장소이미지 저작권관련 문의": 캡처한 이미지를 비영리 내부 DB에 저장해도 되는지 묻는 글입니다. 검색 결과에는 질문만 보였습니다. — [ncloud-forums topic/560](https://www.ncloud-forums.com/topic/560)
- 포럼 "네이버 지도 타겟 썸네일 이미지관련 문의": 지도 썸네일 이미지를 얻을 방법을 묻는 글로, 답변은 미확인입니다. — [ncloud-forums topic/573](https://www.ncloud-forums.com/topic/573/)
- FAQ 948(무료 이용량 프로모션)과 2828(무료이용량 정책)은 질문만 렌더링됐습니다. — [FAQ 948](https://www.ncloud.com/support/faq/all/948); [FAQ 2828](https://ncloud.com/support/faq/all/2828)

### Inferences
- 약관 문언(제7조 ⑨ "사전 동의 없이")상 **NCP 고객지원 1:1 문의로 "도시계획 도면 배경용 대형 지도 이미지를 이용자가 브라우저에서 캡처해 쓰는 서비스" 사용에 대한 서면 동의나 해석을 받는 것**이 유일하게 확실한 확인 방법입니다. 무료이고 되돌릴 수 있는 조치라 우선순위가 높습니다.

### Gaps
- 포럼 답변 본문(ncloud-forums.com 접속 실패) — **확인 필요**.
