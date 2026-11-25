# Mapshot-Front 코드 규약

> 2026-11-25 `master` 코드를 보고 정리했다. 새 코드는 이 규약을 따르고, 기존 코드가 규약과 다르면 손볼 때 같이 맞춘다.
> 공통 규칙은 [common-rules.md](common-rules.md).

## 1. 폴더 구조

```
src/
├── main.js              앱 생성: Pinia, Router, Vuetify, Sentry 등록
├── App.vue              레이아웃(상단 바/하단 내비), 전역 로더, 점검 배너
├── router/index.js      라우트 정의
├── views/               라우트 하나 = 화면 하나 (*View.vue)
├── components/<기능>/   화면 안에서 쓰는 조각. 기능 이름 폴더로 묶는다 (news/, map/, manual/, ads/ ...)
├── store/               Pinia 스토어. 기능 하나 = 파일 하나
└── assets/              css/, img/, js/(지도 캡처 계산 등 순수 JS)
```

- 화면 컴포넌트는 `XxxView.vue`, 조각은 하는 일을 드러내는 이름(`NewsDigest.vue`, `AdSlot.vue`). 파일 이름은 PascalCase.
- 여러 화면에서 같이 쓰는 조각은 `components/` 바로 아래나 그 성격의 폴더(`ads/`)에 둔다.

## 2. 상태 관리 (Pinia)

- 화면이 쓰는 데이터와 API 호출은 스토어에 둔다. 컴포넌트에서 axios 를 직접 부르지 않는다.
- 스토어 파일 `store/<기능>.js` 에서 `export const useXxxStore = defineStore('<id>', { state, getters, actions })` 로 만든다(Options 스토어).
  - 스토어 id 는 파일 이름과 같게 쓴다. 예: `store/news.js` → `defineStore('news', ...)`.
    지금 `news.js`(`'newsStore'`), `notice.js`(`'noticeStore'`)만 다르다. 손볼 때 맞춘다.
- API 호출 모양
  - 스토어 파일 위쪽에서 `axios.create(...)` 로 그 스토어 전용 인스턴스를 만들고, `const apiUrl = process.env.VUE_APP_API_URL` 로 주소를 붙인다.
  - 실제 요청은 파일 안의 `async function getXxx ()` 로 빼고, 액션은 그걸 불러 상태만 바꾼다.
  - 액션은 `isLoading` / `isError` 같은 플래그를 `try / catch / finally` 로 관리한다. 화면은 플래그를 보고 로딩·에러를 그린다.
  - 실패해도 화면이 멈추지 않게 빈 값으로 되돌린다(예: `this.posts = []`).
- 여러 스토어가 같이 쓰는 상태는 그 상태를 가진 스토어를 액션 안에서 불러 쓴다(`useParcelStore()` 처럼). 상태를 복사해 두지 않는다.
- 브라우저에 남겨야 하는 설정은 스토어 액션에서 `localStorage` 로 저장·복원한다. 키는 `mapshot_` 접두 상수로 두고, 읽을 때는 `try/catch` 로 감싼다(값이 깨져도 기본값으로 뜨게).
- 전역 로딩 오버레이는 `useLoaderStore().isLoading` 하나로 켠다.

## 3. 컴포넌트

- Options API 로 쓴다(`export default { ... }`). 지금 `<script setup>` 을 쓰는 파일은 없다.
- 스토어는 `setup()` 에서 불러 돌려주고, 나머지는 `data`·`computed`·`methods`·생명주기 훅에서 `this.xxxStore` 로 쓴다.
  ```js
  setup () {
    const newsStore = useNewsStore()
    return { newsStore }
  },
  created () {
    this.newsStore.loadRecent()
  },
  ```
- 화면에 처음 필요한 데이터는 `created()` 에서 스토어 액션으로 불러온다.
- 경로 값(`:id` 등)은 라우터에서 `props: true` 로 넘겨 `props` 로 받는다. 컴포넌트 안에서 `$route.params` 를 직접 읽지 않는다.
- UI 는 Vuetify 3 컴포넌트를 먼저 쓴다. 반응형 분기는 `useDisplay()`(`mdAndUp` 등)로 한다.

## 4. 라우터

- 모든 화면은 지연 로딩한다: `component: () => import(/* webpackChunkName: "<이름>" */ '../views/XxxView.vue')`.
- 라우트마다 `name` 을 단다. 화면 분기(광고를 띄울지 등)는 경로 문자열이 아니라 `$route.name` 으로 판단한다.
- 없는 경로는 `/404`(`NotFoundView`)로 보낸다.

## 5. 스타일

- 컴포넌트 전용 스타일은 `<style scoped>`.
- 카카오맵 오버레이처럼 `#map` 안에 그려지는 요소는 scoped 가 닿지 않는다. `src/assets/css/map.css` 에 `.map_wrap #map ...` 접두로 쓴다.
- `public/index.html` 의 전역 글자 크기 규칙 때문에 글자 크기가 상속되지 않는다. 글자 요소마다 크기를 직접 준다.
- 색은 Vuetify 테마 색(`primary`, `success` 등, `main.js`)을 먼저 쓴다.

## 6. 설정과 외부 스크립트

- 빌드 환경변수는 `VUE_APP_` 접두. 지금 쓰는 것: `VUE_APP_API_URL`, 점검 배너(`VUE_APP_MAINTENANCE_*`).
  - 환경변수는 빌드 때 박히므로 값을 바꾸면 Cloudflare Pages 를 다시 배포해야 한다.
  - 프론트 환경변수에 비밀 키를 넣지 않는다(공통 규칙 4번).
- 로컬 실행은 `npm run serve`(8081). API 경로는 `vue.config.js` 프록시로 `localhost:8080` 에 붙는다.
- 외부 SDK(카카오맵, 애드센스, GA)는 `public/index.html` 에서 한 번만 로드한다. 컴포넌트가 `<script>` 를 다시 꽂지 않는다.
- 광고 규칙은 공통 규칙 3번.

## 7. 코드 모양

- 들여쓰기 2칸, 세미콜론 없음, 작은따옴표, 함수 이름 뒤 공백(`created ()`) — `package.json` 의 `@vue/standard` 기준.
  - 다만 지금 lint 가 돌지 않는다(`lintOnSave: false`, `eslint-plugin-vue` 미설치). 자동 검사는 없으니 손으로 맞춘다.
- 코드 주석에는 "왜 이렇게 했는지"를 쓴다(공통 규칙 1번). 함정이 있던 곳(애드센스 push, 지도 오버레이 스타일 등)은 그 자리에 주석을 남긴다.
