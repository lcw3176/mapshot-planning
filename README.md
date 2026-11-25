# mapshot-planning

맵샷(kmapshot.com)의 기획·결정·공통 규칙을 모아두는 레포. 코드는 없다.

- 코드 레포: [Mapshot-API](https://github.com/lcw3176/Mapshot-API) (Spring Boot), [Mapshot-Front](https://github.com/lcw3176/Mapshot-Front) (Vue 3)
- 코드 레포에는 기획 문서를 두지 않는다. 각 레포의 `CLAUDE.md` 가 이 레포를 가리킨다.

## 구조

```
mapshot-planning/
├── README.md                 이 파일. 기획 목록도 여기서 관리
├── CLAUDE.md                 사람·AI가 이 레포에서 일할 때의 규칙
├── rules/                    규칙
│   ├── common-rules.md       두 레포 공통 규칙
│   ├── api-code.md           Mapshot-API 코드 규약
│   └── front-code.md         Mapshot-Front 코드 규약
├── architecture/             시스템 구성 소개
│   └── overview.md
├── decisions/                결정 기록. 결정 하나 = 파일 하나
│   └── YYYY-MM-DD-주제.md
├── plans/                    기획. 기획 하나 = 폴더 하나
│   ├── YYYY-MM-주제/
│   │   ├── README.md         기획서(왜·무엇·범위·UI). 폴더의 입구
│   │   ├── flow.md           작동 플로우(필요할 때)
│   │   └── ...               화면 캡처, 평가 데이터 등 그 기획에만 쓰는 것
│   └── archive/              접었거나 제거한 기능
└── templates/                새 기획·결정 문서 틀
```

## 기획 목록

| 기획 | 상태 | 레포 |
|---|---|---|
| [도시소식 지도 레이어](plans/2026-11-city-news-map/README.md) | 구현 완료, 리뷰 대기 | API, Front |
| [도시뉴스 AI 브리핑](plans/2026-06-news-ai-digest/README.md) | 운영 중 | API, Front |
| [필지 정보 조회](plans/archive/2026-parcel-info/README.md) | 제거(2026-11) | API, Front |

## 결정 목록

| 날짜 | 결정 |
|---|---|
| 2026-11-25 | [Grafana 관련 설정과 의존성을 API 에서 뺀다](decisions/2026-11-25-remove-grafana.md) |
| 2026-11-25 | [점검 배너는 프론트 빌드 환경변수로 켠다](decisions/2026-11-25-maintenance-banner.md) |
| 2026-11-25 | [위치정보 규칙은 '사용자 위치'에만 적용한다](decisions/2026-11-25-location-rule-scope.md) |
| 2026-11-25 | [필지 정보 조회 기능을 제거한다](decisions/2026-11-25-remove-parcel.md) |
| 2026-11-25 | [기획·결정 문서를 이 레포로 모은다](decisions/2026-11-25-planning-repo.md) |

새 기획이나 결정을 추가하면 위 표에도 한 줄 넣는다.
