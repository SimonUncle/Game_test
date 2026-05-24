# `web/` — Mongle Village 웹앱

루트 [`../README.md`](../README.md)에서 친구용 안내를 먼저 보세요.
이 문서는 코드 구조 + 개발자용 세부사항입니다.

---

## 명령

```bash
npm install     # 첫 1회
npm run dev     # 개발 서버 (HMR), http://localhost:5173
npm run build   # TS 체크 + 프로덕션 빌드 → dist/
npm run preview # 빌드 결과 미리보기 → http://localhost:4173
```

## 구조

```
src/
├── main.tsx                   # 진입점
├── App.tsx                    # 최상위 — 패널 마운트, 키보드 단축키, 다이얼로그
├── index.css                  # Tailwind + 글래스 패널 + 꽃잎 애니
├── components/
│   ├── Village.tsx            # 카메라 + 배경 + 이동 RAF 루프 + 모든 child 마운트
│   ├── Character.tsx          # SVG 4방향 캐릭터
│   ├── Chicken.tsx            # SVG 닭 (4방향 + 다리 애니)
│   ├── ChickenSwarm.tsx       # 닭 5마리 spawn + tick 루프
│   ├── ChiefHouseMarker.tsx   # 나무 푯말 + 받침대 + 그림자
│   ├── DayCycle.tsx           # 120s 시간대 색 보정
│   ├── CherryPetals.tsx       # 떨어지는 벚꽃잎 (CSS only)
│   ├── TopNav.tsx             # 상단 네비
│   ├── PomodoroPanel.tsx      # 좌상단 25:00 타이머
│   ├── DateTodoPanel.tsx      # 우상단 날짜 + 투두 입력
│   ├── NotificationPanel.tsx  # 우하단 알림 토스트
│   └── InfoDialog.tsx         # 모달 다이얼로그
└── store/
    ├── useTimer.ts            # 포모도로 상태머신 (25/5/15)
    ├── useTodos.ts            # 투두 (localStorage 영속화)
    ├── useGameState.ts        # 사이클 카운트, 촌장 이름 (영속화)
    ├── useNotifications.ts    # 토스트 큐
    ├── usePlayer.ts           # 캐릭터 x/y/방향
    └── useChickens.ts         # 닭 무리 + AI tick
```

## 핵심 동작

### 카메라 (Village.tsx)
- World 1280×768. Viewport 1920×1080 가정.
- `zoom = max(minZoom, fitZoom)` — 최소 1.4배. World가 viewport보다 작으면 fit.
- 카메라는 플레이어를 따라가되, World 가장자리 너머 안 보이게 클램프.

### 이동 입력 (Village.tsx)
- `keydown` / `keyup`을 ref Set에 누적, RAF에서 dt 곱해서 위치 갱신.
- 4-way (대각선 시 normalize). 속도 240 px/s.
- 화면 가장자리 40px 클램프. 객체별 충돌은 없음.

### 시간대 (DayCycle.tsx)
- `<div className="day-tint-layer">` 가 World 위 mix-blend-mode: multiply.
- 120초 동안 dawn → noon → dusk → night 색 보간.
- HUD는 다른 z-index라 영향 안 받음.

### 닭 AI (useChickens.ts)
- 각 닭: home_x/y + target_x/y + state(idle/walk).
- idle → 1.5~3.5s 후 → 새 target 뽑고 walk → 도달 시 idle.
- target은 home 반경 20~90 안에서 random 각도.
- `HOUSE_RECTS` 배열로 집 회피 (집 안엔 target 안 잡힘).
- ⚠️ `HOUSE_RECTS`는 `legacy/godot/tools/build_village.py`의 placements와 손으로 동기화. 집 위치 바꾸면 둘 다 수정.

### 영속화
- Zustand `persist` 미들웨어가 자동.
- localStorage 키: `mongle-todos`, `mongle-game-state`.
- 타이머 상태는 영속화 안 함 — 새로고침하면 idle로.

---

## 디자인 시스템

### Tailwind 커스텀 (`tailwind.config.js`)
- `cozy-bg`, `cozy-panel`, `cozy-border`, `cozy-accent`, `cozy-cream`, `cozy-mute` — 색 팔레트
- `glass-panel`, `glass-panel-strong` — backdrop-blur 클래스
- `pixel-text`, `display-text` — 폰트 변형
- 애니메이션: `bob`, `fade-in`, `slide-up`, `shimmer`

### 폰트 (`index.html`)
- **Press Start 2P** — 픽셀 게임 타이틀
- **VT323** — 타이머 숫자
- **Noto Sans KR** — 한국어 본문

---

## 자주 까먹는 것

1. **HOUSE_RECTS 동기화** — 집 위치 변경 시 `useChickens.ts`도 같이 수정
2. **타입 strict** — `any` 안 됨. `noUnusedLocals` 활성화
3. **z-index 순서** (Village 내부, 위에서 아래로 렌더):
   - 배경 PNG
   - DayCycle 오버레이
   - CherryPetals (z 4)
   - ChickenSwarm
   - ChiefHouseMarker
   - Player
   - (UI는 z 10-30, World 바깥 별도 레이어)
4. **카메라 transform 순서** — `translate(tx, ty) scale(zoom)`. 자식 객체의 local transform은 scale 이후에 적용됨에 주의

---

## 빌드 결과 크기

```
dist/assets/index-*.css   ≈ 16 kB / 4 kB gzipped
dist/assets/index-*.js    ≈ 285 kB / 93 kB gzipped
dist/village_background.png ≈ 700 kB
```

전체 초기 로드 ~1MB. CDN 거치면 충분히 빠름.

---

## 배포 옵션

### Vercel (한 줄)
```bash
npm i -g vercel
vercel
```

### Netlify (드래그)
```bash
npm run build
```
`dist/` 폴더를 [app.netlify.com/drop](https://app.netlify.com/drop)에 드래그.

### GitHub Pages
```bash
npm run build
# dist/ 내용을 gh-pages 브랜치로 push
```

### 자체 서버
`dist/` 통째로 nginx/apache의 정적 디렉토리에 복사. SPA 라우팅 없어서 catch-all 불필요.
