# Grafana(Loki·Prometheus·Tempo) 관련 설정과 의존성을 API 에서 뺀다

> 날짜: 2026-11-25 · 영향 레포: API / 운영

## 계기

Grafana 모니터링 서버를 이미 내렸는데, API 레포에 연결용 설정과 의존성이 남아 있었다.
`otelagent/opentelemetry-javaagent.jar`(20MB)가 레포에 들어 있었고, `docker-compose.yml` 은 Loki 로그 드라이버를 쓰고 있었다.

## 결정

- 지운 것 (브랜치 `feat/grafana-제거`)
  - `otelagent/opentelemetry-javaagent.jar`
  - `micrometer-registry-prometheus`, `opentelemetry-api`, `opentelemetry-context` 의존성. 코드에서 쓰는 곳은 없었다.
  - `docker-compose.yml` 의 OTEL 환경변수, `application.yml` 의 주석 처리된 `management`(prometheus) 블록
- 바꾼 것
  - `docker-compose.yml` 로그 드라이버: Loki → `json-file`(10MB x 5개 회전). 회전이 없으면 컨테이너 로그가 디스크를 채운다.
  - `LoggingFilter` 의 로그 제외 경로: `/actuator/prometheus` → `/actuator/health`
- 남긴 것: `spring-boot-starter-actuator`. 기본으로 `/actuator/health` 만 열린다.
  외부 모니터링이 헬스체크로 이 경로를 부르고 있을 가능성이 있다(운영자 기억, 확인 필요). 확인 전엔 지우지 않는다.
- 모니터링은 Sentry(에러·로그)와 Slack(서버 예외, 수집 실패 알림)으로 한다.

## 버린 선택지

- actuator 까지 같이 제거: 운영 서버나 외부 업타임 체크가 `/actuator/health` 를 부르고 있으면 깨진다. 확인 전이라 보류.

## 이 결정을 다시 볼 조건

- 메트릭·트레이스가 다시 필요해질 때(응답 지연 추적 등). 그때는 무료 범위 안에서 Sentry 트레이싱을 먼저 본다.
- 운영 서버의 실제 `docker-compose.yml` 은 레포 파일과 따로 관리된다. 서버 쪽 Loki 드라이버 설정은 운영자가 직접 바꿔야 한다(확인 필요).
