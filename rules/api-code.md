# Mapshot-API 코드 규약

> 2026-11-25 `master` 코드를 보고 정리했다. 새 코드는 이 규약을 따르고, 기존 코드가 규약과 다르면 손볼 때 같이 맞춘다.
> 공통 규칙은 [common-rules.md](common-rules.md).

## 1. 패키지와 레이어

```
com.mapshot.api
├── presentation/<기능>   컨트롤러, 요청 DTO(*Request)
├── application/<기능>    기능 단위 서비스(*Service), 응답 DTO(*Response, *Dto), 스케줄러(*Scheduler)
├── domain/<기능>         엔티티, 리포지토리(*Repository), enum
└── infra/               외부 클라이언트, 설정, 인증, 예외, 로깅, 레이트리밋, 유틸
```

- 의존 방향은 `presentation → application → domain` 한 방향이다. `infra` 는 어느 레이어에서 써도 된다.
  - 컨트롤러는 리포지토리를 직접 부르지 않는다. 서비스를 거친다.
  - `domain` 은 `application`·`presentation` 을 모른다.
- 기능 이름으로 패키지를 나누고, 세 레이어에서 같은 이름을 쓴다. 예: `presentation/news`, `application/news`, `domain/news`.
- 외부 API 클라이언트는 `infra/client/<서비스명>/` 에 두고, 요청·응답 모델은 그 아래 `model/` 에 둔다.

## 2. 컨트롤러 (presentation)

- `@RestController` + `@RequestMapping("/<기능>")` + `@RequiredArgsConstructor`(생성자 주입).
- 반환은 `ResponseEntity<XxxResponse>`. 응답 DTO 는 서비스가 만들어 넘긴다.
- 입력 검증은 컨트롤러에서 한다.
  - 경로·쿼리 값: 클래스에 `@Validated`, 파라미터에 `@Positive`, `@PositiveOrZero` 등.
  - 요청 본문: `*Request` DTO 에 `@NotBlank` 등을 달고 `@Valid` 로 받는다.
- 인증이 필요한 메서드는 `@PreAuth(...)` 를 붙인다. 검사는 `infra/auth/AuthInterceptor` 가 한다.
- `/map/**` 처럼 호출량을 막아야 하는 경로는 `infra/rateLimit` 의 인터셉터에 경로를 등록한다.
- 지도 템플릿처럼 HTML 을 내려주는 경우만 Thymeleaf(`src/main/resources/templates/`)를 쓴다.

## 3. 서비스와 DTO (application)

- 서비스는 `@Service` + `@RequiredArgsConstructor`. 메서드 이름은 조회 `getXxx`, 그 밖은 동작을 드러내는 동사.
- 응답 DTO 는 Lombok `@Getter @NoArgsConstructor @AllArgsConstructor @Builder` 로 만든다. 엔티티를 그대로 응답에 싣지 않는다.
- 엔티티 → DTO 변환은 DTO 의 `static fromEntity(Entity)` 에 둔다.
- 설정값(페이지 크기, 외부 URL, cron 등)은 코드에 박지 않고 `application.yml` 에 두고 `@Value("${...}")` 로 읽는다.
  - 비밀값(API 키 등)은 `application.yml` 에 `${환경변수}` 로만 적고, 값은 서버 환경변수로 넣는다.
- 스케줄러(`*Scheduler`)는 `@Scheduled(cron = "${...}", zone = "${...}")` 로 cron 을 설정에 뺀다.
  - 켜고 끄는 플래그도 설정에 둔다. 테스트에서는 꺼서 테스트 중에 외부 호출이 나가지 않게 한다.
  - 실패해도 예외를 스케줄러 밖으로 던지지 않는다. 로그를 남기고 Slack 으로 알린 뒤 다음 회차에 다시 한다.

## 4. 엔티티와 리포지토리 (domain)

- 엔티티는 `@Entity` + Lombok `@Getter @NoArgsConstructor @AllArgsConstructor @Builder`. setter 는 두지 않는다.
  - 값을 바꿀 때는 `update(...)` 같은 의미 있는 메서드를 엔티티에 둔다.
  - 생성 시각이 필요하면 `infra/db/BaseTimeEntity` 를 상속한다(`createdDate`).
  - enum 컬럼은 `@Enumerated(EnumType.STRING)`.
- 리포지토리는 Spring Data `JpaRepository` 를 상속하고, 가능하면 메서드 이름 쿼리로 쓴다.
- 스키마는 `src/main/resources/schema.sql` 에 직접 쓴다(`ddl-auto: none`). 규칙은 공통 규칙 8번.

## 5. 예외와 응답 코드

- 서비스에서 실패를 알릴 때는 `throw new ApiException(ErrorCode.XXX)`.
  - 새 실패 상황이면 `infra/exception/status/ErrorCode` 에 HTTP 상태와 한국어 메시지를 같이 추가한다.
  - 조회 실패는 `repository.findById(id).orElseThrow(() -> new ApiException(ErrorCode.NO_SUCH_XXX))` 형태로 쓴다.
- 외부 API 호출은 `ApiHandler.handle(() -> ...)` 로 감싼다. 실패하면 `ErrorCode.EXTERNAL_API_FAILED` 로 바뀐다.
  - 외부 실패를 로그에 남길 때 요청 URL 과 인증키는 넣지 않는다.
- 예외를 HTTP 응답으로 바꾸는 일은 `GlobalExceptionHandler` 한 곳에서만 한다. 컨트롤러에서 try/catch 로 응답을 만들지 않는다.
  - 처리하지 못한 예외는 거기서 로그 + Slack + Sentry 로 보낸다.

## 6. 외부 호출

- HTTP 클라이언트는 `infra/client/ExternalApiClient` 가 만드는 `RestClient` 빈 하나를 주입받아 쓴다.
- 클라이언트 클래스는 `@Component` + `@RequiredArgsConstructor`, URL·키는 `@Value` 로 받는다.
- 쿼리 문자열은 `UriComponentsBuilder` 로 만들고 `.encode()` 한다. 문자열 이어붙이기로 만들지 않는다.
- 외부 응답 오류는 `.onStatus(HttpStatusCode::isError, ...)` 에서 잡는다. 로그·예외 메시지에 키나 인증 헤더를 넣지 않는다.
- 호출량 제한, 캐시, 폴백 같은 원칙은 공통 규칙 4~6번.

## 7. 로깅

- 로그는 Lombok `@Slf4j`. 요청마다 `LoggingFilter` 가 `traceId` 를 MDC 에 넣으므로 따로 만들지 않는다.
- 로그에 비밀값, 사용자 위치(공통 규칙 7번)를 남기지 않는다. 남겨야 하는 외부 실패는 `source=`, `stage=` 처럼 키=값으로 쓴다.

## 8. 테스트

- JUnit 5 + AssertJ. 테스트 패키지는 `src/main` 과 같은 경로에 `XxxTest` 로 둔다.
- 테스트 메서드 이름은 한국어 + 밑줄로 무엇을 확인하는지 쓴다. 예: `없는_공지사항_가져오면_예외()`.
- 레이어별 방식
  - domain: 스프링 없이 순수 단위 테스트. `// given`, `// when`, `// then` 으로 나눈다.
  - application: `@SpringBootTest` 로 테스트용 H2 에 데이터를 넣어 확인한다. `@BeforeEach` 에서 넣고 `@AfterEach` 에서 `deleteAll()`.
  - presentation: `@SpringBootTest @AutoConfigureMockMvc` + MockMvc. Slack 은 `SlackMockExtension` 을 상속해 막는다.
    API 문서는 공개하지 않는다. REST Docs(`document(...)`)는 쓰지 않는다(Mapshot-API PR #138 에서 제거).
- 외부 API 는 실제로 부르지 않는다. 응답 JSON 파싱은 저장해둔 예시 JSON 으로 테스트한다.
- 실행: `./gradlew test`. JDK 17 로 돌린다(Gradle 7.6 이라 JDK 21 기본이면 빌드 스크립트 단계에서 실패한다).
