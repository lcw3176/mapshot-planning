# 도시뉴스 상세 — 브리핑 읽기 화면 (Vue 3 + Vuetify)

> 대상: 프론트엔드 (Mapshot-Front, Vue 3 + Vuetify 3 + Pinia)
> 작성일: 2026-06-30 / 개정 2026-09-13 (신문 1면 구조로 재설계)
> 백엔드 기획: `backend.md`
> 영향 화면: 도시뉴스 탭 — 상세 (`GET /news/{id}`)

> **개정 메모(2026-09-13).** 1차 UI(카드·칩·오늘의 숫자·키워드 클라우드·관련글)는 "AI 가 만든 페이지"
> 티가 강하고 눈에 들어오는 게 없다는 피드백으로 **신문 1면 구조**로 다시 짰다. 응답 스키마는 그대로지만
> **렌더하지 않는 필드가 여럿** 생겼다(§4). 스키마엔 서버가 채우는 `section.image` 가 추가됐다.

---

## 1. 한눈에 보는 변경점

`GET /news/{id}` 응답이 같은 LLM 1콜에서 **구조화 데이터(`digest`)** 를 함께 준다.
본문 HTML(`content`)은 호환용으로 유지되므로 둘 중 하나를 그린다.

- `digest != null` → **브리핑 UI**(`NewsDigest.vue`)
- `digest == null` → **기존 방식** `content`(HTML) 렌더링 (과거 글/폴백)

목록 API(`GET /news/recent`)는 변경 없음.

### 구현 위치

| 파일 | 역할 |
|---|---|
| `src/views/NewsDetailView.vue` | 컨테이너. 로딩/에러/헤더 + `digest` 분기 + `content` 폴백. `.news-reader` 서체 스코프 |
| `src/components/news/NewsDigest.vue` | 브리핑 UI 본체(리드·톱기사·카테고리 묶음·용어·마치며·출처) |
| `src/store/news.js` | API 호출(변경 없음 — 응답을 그대로 보관) |
| `public/index.html` | Pretendard 동적 서브셋 `<link>` |

---

## 2. API 응답 스키마 (TypeScript 표기)

```ts
interface NewsPostResponse {
  id: number;
  title: string;
  content: string;                 // 호환용 HTML. digest==null 폴백
  digest: NewsDigest | null;       // 구조화 브리핑. 과거 글엔 null
  sources: NewsSource[];
  relatedPosts: NewsRelatedPost[]; // 0~3. 현재 프론트 미표시(§4)
  createdDate: string;             // ISO 8601 (KST)
}

interface NewsDigest {
  intro: string;
  highlight: NewsHighlight | null; // 미표시. 2026-09-13 부터 프롬프트에서 제외 → 새 글엔 null
  sections: NewsDigestSection[];   // 3~9
  keywordCloud: NewsKeywordTag[];  // 미표시. 새 글엔 null/빈 배열
  regionStats: NewsRegionTag[];    // 미표시
  glossary: NewsGlossaryItem[];    // 0~3
  questions: string[];             // 미표시 — §7. 새 글엔 null
  outro: string;
}

interface NewsDigestSection {
  category: string;                // 정책|기술|재생|제도|시장|기타 (unknown 허용)
  title: string;
  body: string;
  whyMatters?: string;             // 미표시. 새 글엔 null (프롬프트에서 제외)
  nextStep?: string;
  regions: string[];               // 지명 텍스트만(좌표 없음)
  entities: string[];              // 미표시
  keywords: string[];              // 미표시
  sources: NewsSource[];           // 이 섹션의 원문 기사
  image?: string | null;           // 서버가 채운 og:image 핫링크. 없을 수 있음
}
interface NewsSource { title: string; url: string; }
```

---

## 3. 렌더링 분기

`NewsDetailView.vue` 가 분기를 책임진다. `digest` 가 있어도 `content` 는 항상 함께 내려오지만
**브리핑 UI를 그릴 땐 `content` 를 같이 그리지 않는다**(중복).

---

## 4. 화면 구성 (신문 1면)

```
① 헤더 (NewsDetailView): 제목 + "발행일 · 출처 N건" 텍스트 메타
② 들어가며:            intro (리드 문단, 본문보다 살짝 큼)
③ 톱기사:              sections[0] — 16:9 큰 이미지(있을 때) + 카테고리 라벨 + 큰 제목 + 본문
④ 카테고리 묶음:        sections[1..] 를 카테고리 첫 등장 순으로 묶고, 묶음명 + 가로선 아래에
                        기사 행(썸네일 + 제목 + 본문 + 지역 한 줄 + 출처 링크)
⑤ 이런 뜻이에요:        glossary — 펼쳐진 <dl> (아코디언 아님)
⑥ 마치며:              outro — 본문과 같은 서체, 박스·아이콘 없음
⑦ 출처 N건 보기:        sources — 접힘 패널
```

**표시하지 않는 것과 이유** (데이터는 그대로 오므로 `v-if` 한 줄로 되살릴 수 있다)

| 필드 | 이유 |
|---|---|
| `highlight`(오늘의 숫자) | 숫자 선택 기준이 없어 무관한 값(예: 대학 수시 경쟁률)이 큰 타일로 박힘. 가장 큰 AI 티 |
| `keywordCloud`, `regionStats` | 본문에 있는 단어를 칩으로 반복할 뿐. 지역은 기사별 한 줄 메타로 대체 |
| `whyMatters` | "~이 중요해지고 있습니다" 류 상투구가 매 꼭지마다 붙어 전체가 생성물처럼 보임 |
| `entities`, `keywords` | 칩 홍수. 본문 중복 |
| `relatedPosts` | 제목이 전부 "도시뉴스 브리핑 (날짜)"라 고를 정보가 없음. 상세→상세 이동 시 `created()` 가 재실행되지 않는 문제도 있었음 |
| `questions` | §7 |

**썸네일.** `section.image` 가 있으면 톱기사는 16:9 전폭, 일반 기사는 데스크톱 오른쪽 4:3(168px) /
모바일 제목 옆 정사각(88px). 그림은 첫 출처 기사로 가는 링크다. `referrerpolicy="no-referrer"`,
`onerror` 시 `brokenImages` 에 기록해 **칸을 통째로 숨긴다**(핫링크라 깨질 수 있음).
백엔드 배포 전엔 `image` 가 없으므로 텍스트만으로도 성립하게 만들어져 있다.

**출처 링크.** 언론사 파비콘(`https://www.google.com/s2/favicons?domain=…&sz=32`, 키 불필요) + 제목 한 줄
말줄임 + 새 탭. 파비콘 실패도 같은 방식으로 숨긴다.

---

## 5. 디자인 가이드

- 서체: `.news-reader { font-family: 'Pretendard Variable', Pretendard, … }` (뷰 스코프). Vuetify 타이포
  유틸(`text-h5` 등)은 Roboto 를 박아 넣으므로 읽기 화면에선 쓰지 않는다.
- 한글: `word-break: keep-all` + `overflow-wrap: anywhere`. 제목엔 `text-wrap: balance`.
- 색: 액센트는 `--v-theme-success` **하나만**. 카테고리별 5색 매핑은 폐기. 모든 색은 테마 토큰이라 다크 테마 호환.
- 카드 없음. 묶음은 작은 초록 라벨 + 가로선, 기사 사이는 여백(32px)으로만 구분.
- 모션: 썸네일 hover 1.03 확대(링크임을 알리는 피드백)만. `prefers-reduced-motion` 에서 해제.
- 읽기 폭: `md=8 lg=7 xl=6` (목록보다 한 단계 좁게).

---

## 6. 엣지 케이스 / 폴백

| 상황 | 처리 |
|---|---|
| `digest == null` | `content`(HTML) 폴백 |
| `sections` 빈 배열 | 본문 블록 전체 생략(리드·용어·마치며는 각자 `v-if`) |
| `image` 없음 / 로드 실패 | 이미지 칸 숨김, 텍스트만 |
| `glossary` 빈 배열 | 코너 숨김 |
| 알 수 없는 `category` | 라벨은 받은 값 그대로, 색은 동일(카테고리별 색 없음) |
| `nextStep` 누락 | 해당 줄만 숨김 |
| `regions` 빈 배열 | 지역 줄 숨김 |

---

## 7. questions(후속 질문) — 미렌더

`digest.questions` 는 응답에 내려오지만 **렌더링하지 않는다.** 클릭 시 우리 콘텐츠 기반으로 답을 생성하는
후속 Q&A 가 없으면 의미가 없고, 외부 검색으로 내보내는 건 이탈만 유발한다. 백엔드 기획 문서 §6.

---

## 8. 함정 기록 (같은 실수 방지)

- **페이지 내 앵커는 해시 링크로 만들지 말 것.** `<a href="#x">` 는 popstate → `router.beforeEach` 가 돌며
  전역 로딩 오버레이가 깜빡인다. 필요하면 `@click.prevent` + `scrollIntoView`.
- **한 줄 말줄임에 `white-space: nowrap` 을 쓰지 말 것.** flex/grid 조상의 `min-width: auto` 가
  `max-width` 를 이겨 모바일에서 컬럼이 뷰포트 밖으로 밀린다. `-webkit-line-clamp: 1` 을 쓴다.
- **헤드리스 Chrome 스크린샷은 `--window-size=390` 을 무시한다**(최소 창 폭 ~485px). 모바일 검증은 CDP
  `Emulation.setDeviceMetricsOverride` 로 해야 한다. 안 그러면 없는 오버플로를 잡으러 다니게 된다.
- **로컬에서 실 API 를 부르면 CORS 403.** `api.kmapshot.com` 은 `kmapshot.com` 오리진만 허용. 로컬 검증은
  받아둔 JSON 을 CORS 허용(OPTIONS 포함) 목 서버로 서빙한다.

---

## 9. 절대 하지 말 것

1. **좌표·주소를 응답에서 찾지 말 것.** 백엔드가 의도적으로 제외(민감정보). 지명은 텍스트만.
   (사용자 위치정보 기준의 규칙. 행정구역 대표점은 예외 — `decisions/2026-11-25-location-rule-scope.md`)
2. `content` HTML 과 브리핑 UI 를 동시에 그리지 말 것(중복).
3. `category` 를 화이트리스트 enum 으로 강제하지 말 것 — unknown 폴백 필수.
4. `questions` 를 외부 검색 등으로 연결하지 말 것(§7).
5. 썸네일을 우리 서버로 재호스팅하지 말 것(저작권). 핫링크 + 실패 시 숨김이 원칙.

---

## 10. 질문 / 변경 요청

응답 스키마 변경이 필요하거나 모호한 케이스가 생기면 **백엔드에 먼저 알린다.** 스키마 변경 시 이 문서와
`backend.md` 를 함께 갱신한다.
