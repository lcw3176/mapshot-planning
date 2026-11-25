# 도시뉴스 AI 디지스트 — 기능 기획서 (백엔드)

> 대상: 백엔드 / 기획
> 작성일: 2026-06-30
> 관련 프론트 문서: `frontend.md`
> 영향 범위: 뉴스 수집·요약 파이프라인, 공개 도시뉴스 조회 API(`/news/*`)

---

## 1. 무엇을 만드는가

도시공학·도시계획 뉴스를 매일 모아서, **LLM 1회 호출로 구조화된 '도시뉴스 브리핑'** 을 만들어
공개 도시뉴스 탭에 발행한다. 핵심은 자유 텍스트 한 덩어리가 아니라, 프론트가 풍부한 UI를
그릴 수 있도록 **정해진 스키마의 JSON(digest)** 을 함께 내려주는 것.

기존에는 `GET /news/{id}` 가 `content`(HTML) 한 덩어리만 줬다. 이번 기획으로 같은 LLM
응답에서 카테고리·하이라이트·키워드·지명·용어풀이 등을 구조화해 `digest` 필드로 함께 제공한다.
`content`(HTML)는 호환용으로 계속 내려가며, `digest == null` 인 과거 글/폴백은 프론트가
`content` 로 폴백한다.

### 설계 원칙

- **1요청 1콜.** 기사마다 LLM을 호출하면 레이트리밋에 걸린다. 개별 기사는 네이버가 준
  요약(`description`)을 그대로 저장하고, 발행용 종합 요약만 전체 기사를 모아 **한 번** 호출한다.
- **구조화 우선.** 프론트 UX(컬러 칩, 키워드 클라우드, 용어 아코디언 등)를 백엔드가 한 번에
  추출해 내려준다. 프론트는 렌더링만 책임진다.
- **폴백 안전.** LLM 호출 실패 / JSON 파싱 실패에도 게시는 멈추지 않는다. 제목만 묶은
  폴백 디지스트로라도 발행한다.
- **위치정보 제외.** 좌표·주소는 응답에 절대 넣지 않는다(민감정보 정책). 지명은 텍스트만.
  > 2026-11-25 범위 정리: 이 규칙은 **사용자 위치정보**를 막으려는 것이다. 행정구역(시군구) 대표점처럼 사용자와 무관한
  > 대략 좌표는 허용한다. → `decisions/2026-11-25-location-rule-scope.md`

---

## 2. 파이프라인

```
[NewsScheduler] (cron, 매일)
      │
      ▼
[NewsCollectService.collectAndSummarize()]
  1) 키워드별 네이버 뉴스 검색 (news.collect.keywords)
  2) urlHash 로 신규 기사만 필터 → NewsArticle 저장
     · 개별 LLM 요약 안 함. description 을 그대로 summary 로 저장
  3) 이번에 새로 모인 기사들을 종합해 publishDigest()
      │
      ▼
[publishDigest()]
  buildDigest()   : 전체 기사(제목+요약) → LLM 1콜 → 구조화 JSON 파싱(NewsDigest)
                    실패 시 fallbackDigest()(제목만 묶음)
  digestToHtml()  : 호환용 content(HTML) 생성
  buildSourcesJson(): 출처 목록을 본문과 분리해 JSON 배열로
  PostService.publish(title, html, sources, digestJson, "도시뉴스")
      │
      ▼
[Post] 저장 (writer="도시뉴스", content=HTML, sources=JSON, digestJson=구조화 JSON)
```

조회 경로:

```
GET /news/recent  → NewsFeedService.getRecentNewsPosts() → 경량 목록(제목·미리보기·발행일)
GET /news/{id}    → NewsFeedService.getNewsPost(id)
                     · 조회수 +1
                     · digestJson 파싱 → digest
                     · sources 파싱
                     · 토큰 매칭으로 relatedPosts 계산(0~3건)
```

> 원본 수집 기사(NewsArticle)는 공개하지 않는다. 사용자에겐 LLM이 발행한 도시뉴스 게시글만 노출한다.

---

## 3. 응답 스키마 (공개 API 계약)

`GET /news/{id}` → `NewsPostResponse`

| 필드 | 타입 | 설명 |
|---|---|---|
| `id` | number | 게시글 ID |
| `title` | string | 제목 |
| `content` | string(HTML) | 호환용 본문. `digest==null` 일 때 폴백 렌더링 |
| `digest` | `NewsDigest \| null` | 구조화 브리핑. 과거 글/파싱실패 시 null |
| `sources` | `NewsSource[]` | 본문과 분리된 출처 목록 |
| `relatedPosts` | `NewsRelatedPost[]` | 같은 주제 과거 브리핑 추천(0~3) |
| `createdDate` | string(ISO, KST) | 발행 시각 |

`NewsDigest`

| 필드 | 타입 | 분량 | 비고 |
|---|---|---|---|
| `intro` | string | 2~3문장 | 도입 |
| `highlight` | `NewsHighlight \| null` | — | **프롬프트에서 제외(2026-09-13)**. 과거 글에만 값 있음. §6 |
| `sections` | `NewsDigestSection[]` | 3~6 | 본문 섹션 |
| `keywordCloud` | `{text,count}[]` | — | **프롬프트에서 제외(2026-09-13)**. 과거 글에만 값 있음. §6 |
| `regionStats` | `{name,count}[]` | 0~6 | 지명 빈도(좌표 없음). 관련글 토큰 매칭에 사용 |
| `glossary` | `{term,explanation}[]` | 0~3 | 용어 풀이 |
| `questions` | `string[]` | — | **프롬프트에서 제외(2026-09-13)**. §6 |
| `outro` | string | 2~3문장 | 마무리 |

`NewsDigestSection`: `category`(정책/기술/재생/제도/시장/기타), `title`, `body`,
`whyMatters?`, `nextStep?`, `regions[]`, `entities[]`, `keywords[]`,
`sources[]`(이 섹션의 원문 출처 `{title,url}` — 프론트가 카드별 '기사 원문' 링크로 렌더),
`image?`(섹션 대표 이미지 URL — 서버가 채움, 아래 참조).

### 섹션 썸네일(`image`)

네이버 뉴스 검색 API 는 썸네일을 주지 않는다. 그래서 `resolveSectionSources` 가 출처를 해석한 직후
`findThumbnail` 이 그 섹션의 출처 기사 페이지를 **순서대로 최대 2건** 열어(Jsoup, 건당 4초 타임아웃)
처음 발견한 `og:image`(없으면 `twitter:image`)를 `section.image` 에 넣는다. 없거나 전부 실패하면 `null`.

- **LLM 출력이 아니다.** 프롬프트/스키마엔 없고, 저장 직전 서버가 채운다. `digestJson` 에 같이 저장되므로
  조회 시 추가 작업이 없다.
- **핫링크.** 언론사 CDN URL 을 그대로 내려주며 우리가 재호스팅하지 않는다(저작권·저장 비용 회피).
  대신 언제든 깨질 수 있어 프론트는 `onerror` 시 이미지 칸을 통째로 숨긴다.
- **로고 제외.** 기사 사진이 없을 때 언론사 로고를 og:image 로 두는 사이트가 있어(`.../image/logo/...png`)
  URL 에 `logo` 가 들어가면 건너뛴다(`looksLikeLogo`). 단순 휴리스틱이라 놓치는 경우가 있으면 조건을 보강한다.
- **실패해도 발행은 진행.** 어떤 예외도 삼키고 `null` 로 둔다. 하루 1회 배치라 섹션 9개 × 최대 8초여도 괜찮다.
- 폴백 디지스트(`fallbackDigest`)는 출처 매핑이 없으므로 썸네일도 없다.

### 섹션별 원문 출처 매핑

각 섹션은 근거가 된 원문 기사로 연결되는 링크를 갖는다. 구현:

1. LLM은 각 섹션에 `sourceRefs`(입력 기사 목록의 1-based 번호 1~3개)를 출력한다.
   프롬프트가 번호는 사용자 입력의 `1.`, `2.` … 와 정확히 일치하도록 강제한다.
2. 백엔드(`NewsCollectService.resolveSectionSources`)가 그 번호를 **우리가 넘긴 기사 목록**에
   매핑해 실제 `{title,url}` 로 변환하고 `section.sources` 에 채운다. LLM이 URL을 지어내지
   못하게 번호→URL 해석은 서버가 한다. 범위를 벗어난 번호는 무시, 없으면 빈 목록(링크 생략).
3. `sourceRefs` 는 내부용이라 프론트는 `section.sources` 만 사용한다.

> 전체 TS 인터페이스와 예시 JSON, 렌더링 규칙은 `frontend.md` 참조.
> 응답 스키마를 바꿀 때는 두 문서를 함께 갱신한다.

---

## 4. LLM 호출 설계

- 클라이언트: `GeminiClient.chat(system, user, maxTokens)` — `maxOutputTokens=5000`, `temperature=0.15`.
  Google AI Studio(Gemini) generateContent 를 **직접 호출**한다. 엔드포인트는
  `{client.gemini.url}/{model}:generateContent`, 인증은 `x-goog-api-key` 헤더.
- 모델(페일오버): `client.gemini.models`(콤마 구분, 기본 `gemini-2.5-flash,gemini-2.5-flash-lite`,
  환경변수 `geminiModels` 로 override). 키는 `geminiApiKey` 환경변수.
- **모델 페일오버 체인.** 나열한 순서대로 호출을 시도하고, 한 모델이 실패(**503 과부하**·429
  레이트리밋·빈 응답 등)하면 **자동으로 다음 모델로 넘어간다.** 모든 모델이 실패해야 예외가 나고
  상위(buildDigest)가 폴백 디지스트로 처리한다. 성공하면 즉시 반환(뒤 모델은 호출 안 함).
- **키 미설정 안전장치.** `geminiApiKey` 가 비어 있으면 앱은 정상 부팅하되 LLM 호출만 건너뛰고
  폴백 디지스트로 발행한다(부팅 실패 방지).
- **thinking 비활성화(`thinkingBudget=0`).** 2.5 계열은 기본적으로 사고 토큰을 쓰는데,
  `maxOutputTokens` 예산을 사고가 잠식하면 JSON 이 잘려 파싱이 실패한다. 구조화 추출에서는
  사고를 꺼서 출력 토큰을 JSON 생성에 온전히 쓴다.
- 시스템 프롬프트(`NewsCollectService.DIGEST_SYSTEM_PROMPT`)가 페르소나('맵샷AI'), 톤(따뜻한
  존댓말), 출력 스키마, 분량 가이드를 강제한다. `systemInstruction` 으로 전달하며
  **JSON 객체 단독 출력**을 요구한다.
- 파싱 보정: 모델이 코드펜스/머리말을 붙여도 첫 `{` ~ 마지막 `}` 만 잘라 파싱한다.
  모델별 호환을 위해 `@JsonIgnoreProperties(ignoreUnknown=true)` 로 알 수 없는 필드는 무시.

### 왜 OpenRouter 가 아니라 Gemini 직접 호출인가

OpenRouter 의 `:free` 모델은 여러 사용자가 공유하는 무료 풀이라, 우리 호출이 하루 1건이어도
업스트림 포화 시 429(rate limit)가 잦았다. Google AI Studio 무료 티어(약 1,500 req/day,
15 rpm)를 **직접** 쓰면 우리 프로젝트 전용 할당량이 적용돼 그 문제를 피한다. 배치가
하루 1콜이라 무료 한도로 충분하다.

> 참고: 무료 티어는 입력이 모델 학습에 사용될 수 있다(공개 뉴스 요약이라 민감도 낮음).
> `OpenRouterClient` 는 롤백/대체 용도로 코드에 남겨 두었으나 현재 배선되지 않는다.

### 실패 처리 단계

1. LLM 호출 예외 → 로그(root cause) 남기고 `raw=null`.
2. 파싱 실패 → `fallbackDigest()`(제목만 섹션화).
3. 발행 자체 실패 → 예외 흡수. 뉴스 수집 트랜잭션은 막지 않음.

---

## 5. 관련글(relatedPosts) 추천 — LLM 없이

추가 LLM 호출 없이 **토큰 매칭**으로 계산한다(`NewsFeedService.findRelated`).

1. 현재 글 digest 에서 토큰 수집: `keywordCloud`, `regionStats`, 각 섹션의 `keywords`/`regions`
   (2자 이상).
2. 최근 30건의 다른 도시뉴스 글 본문/제목에 토큰이 몇 개 등장하는지로 점수화.
3. 점수 내림차순(동점 시 최신 우선) 상위 3건.

장점: 비용 0, 결정적. 한계: 표면적 문자열 매칭이라 동의어/문맥은 못 잡음 → 향후 개선 후보(§7).

---

## 6. 프롬프트에서 뺀 필드 (2026-09-13) — highlight / keywordCloud / whyMatters / questions

프론트가 그리지 않는 필드는 출력 토큰만 쓰므로 **프롬프트 스키마와 분량 가이드에서 뺐다.**
모델 필드는 nullable 로 그대로 두어 과거 글(값이 있는 digestJson)은 계속 파싱된다(무중단).

| 필드 | 프론트에서 안 그리는 이유 |
|---|---|
| `highlight`(오늘의 숫자) | 수치 선택 기준이 없어 무관한 값(대학 수시 경쟁률 등)이 큰 타일로 박혔다 |
| `keywordCloud` | 본문 단어의 반복. 관련글 매칭은 `regionStats`/섹션 `keywords`/`regions` 만으로 충분 |
| `whyMatters` | "~이 중요해지고 있습니다" 류 상투구가 매 섹션에 붙어 전체가 생성물처럼 보였다 |
| `questions` | 아래 결정 참고 |

`digestToHtml` 은 이 필드들이 있을 때만 그리므로 과거 글의 호환 HTML 도 그대로다.

### questions(후속 질문) — 미사용 결정

**결정:** 스키마/저장값에는 유지하되, **프론트는 렌더링하지 않는다.**

근거:
- `questions` 는 "독자가 더 알고 싶을 후속 질문" 칩이다. 의미가 있으려면 클릭 시 **우리 콘텐츠
  기반으로 답을 생성**하는 후속 Q&A(LLM 재호출/RAG)가 있어야 한다. 1차 범위가 아니다.
- 답을 못 주면서 외부 검색(네이버 등)으로 내보내는 건 이탈만 유발하는 나쁜 UX다.
  "차라리 노출하지 않는" 편이 낫다.

운영 방침:
- 모델 필드 `NewsDigest.questions` 는 유지(향후 Q&A 기능 대비 reserved), 프롬프트 생성은 2026-09-13 에 뺐다.
- 진짜 후속 Q&A 기능을 도입할 때 프롬프트에 항목을 되살리고 이 필드를 그대로 재활용한다.

---

## 7. 알려진 한계 / 향후 확장 후보

| 항목 | 현재 | 향후 |
|---|---|---|
| 관련글 매칭 | 표면 문자열 매칭 | 임베딩 유사도/태그 인덱스 |
| 청크 처리 | 단일 콜(기사 많으면 토큰 압박) | 기사 과다 시 분할 요약 후 병합 |
| questions | 미사용(reserved) | 콘텐츠 기반 후속 Q&A |
| 카테고리 | 프롬프트 enum + 기타 | 사용 통계 기반 재정의 |
| 목록 API | 제목·미리보기만 | (선택) 대표 카테고리/키워드 미리보기, 톱기사 썸네일 |
| 섹션 썸네일 | og:image 핫링크 + `logo` 문자열 휴리스틱 | 이미지 크기 검사(너무 작으면 제외), 만료 시 재조회 |
| relatedPosts | 토큰 매칭으로 계산, **프론트는 미표시**(제목이 전부 "도시뉴스 브리핑 (날짜)"라 고를 정보가 없음) | 표시하려면 주제 요약 한 줄이 함께 필요 |
| 어드민 상세 | 공개 `/news/{id}` 재사용(조회수 +1) | 조회수 미증가 어드민 전용 `GET /admin/post/{id}` |

> 어드민 상세 화면은 공개와 같은 카드뷰를 위해 `/news/{id}` 를 재사용한다(digest 포함). 다만
> 조회 시 조회수가 증가해 대시보드 통계가 소폭 오염된다. 무증가가 필요하면 조회수 미증가
> 어드민 전용 엔드포인트로 분리하면 된다.

---

## 8. 설정 키 (application.yml)

| 키 | 의미 |
|---|---|
| `news.collect.enabled` | 스케줄러 on/off |
| `news.collect.cron` / `news.collect.zone` | 수집 주기/타임존 |
| `news.collect.keywords` | 검색 키워드 CSV |
| `news.collect.display` / `news.collect.sort` | 네이버 검색 표시 수/정렬 |
| `client.gemini.url` | Gemini generateContent 베이스 URL |
| `client.gemini.models` (`geminiModels`) | 페일오버 모델 목록, 콤마 구분 (기본 `gemini-2.5-flash,gemini-2.5-flash-lite`) |
| `client.gemini.key` (`geminiApiKey`) | Google AI Studio API 키 (미설정 시 앱은 뜨고 LLM만 건너뜀) |
| `client.openrouter.*` | (레거시) 미배선. 롤백용으로 유지 |

---

## 9. 변경 시 체크리스트

- [ ] `NewsDigest` 등 응답 스키마 변경 시 → 본 문서 §3 + `frontend.md` 동시 갱신
- [ ] 프롬프트(`DIGEST_SYSTEM_PROMPT`) 변경 시 → 스키마/분량 가이드 일치 확인
- [ ] 파싱 모델(`NewsDigestJsonTest`) 회귀 테스트 통과
- [ ] 폴백 경로(LLM/파싱 실패) 동작 확인
- [ ] 응답에 좌표·주소가 새지 않는지 확인
