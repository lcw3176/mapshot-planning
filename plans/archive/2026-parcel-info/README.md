# 필지 정보 조회 (접음)

> **2026-11-25 제거.** 지도 왼쪽 패널의 자리를 도시소식 지도 레이어에 넘겼다. → `decisions/2026-11-25-remove-parcel.md`

지도에서 '필지 선택하기'를 켜고 필지를 누르면 지목·면적·개별공시지가·용도지역을 보여주고,
건축물대장·토지이용규제·실거래가를 붙여 질문에 답하던 기능.

- [pnu-lookup.md](pnu-lookup.md): 브이월드로 좌표 → PNU → 필지 속성 조회, 호출량 통제와 캐시 설계 (원래 `Mapshot-API:docs/parcel-pnu-feature.md`)
- [public-data.md](public-data.md): 공공데이터포털 세 API 연동과 키 설정 (원래 `Mapshot-API:docs/parcel-public-data.md`)

코드는 Mapshot-API·Mapshot-Front 의 git 기록에 남아 있다(제거 직전 커밋: API `dcad888`, Front `ee69a3a`).
