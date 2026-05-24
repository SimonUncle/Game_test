# 몽글마을 — Web App

Stardew/Cozy 풍 마을 + 포모도로 타이머 + 투두 + 알림. React 18 + Vite + Tailwind.

## 🚀 실행

```bash
cd web
npm install      # 첫 1회만
npm run dev      # 개발 서버 (HMR)
# → http://localhost:5173
```

빌드:
```bash
npm run build    # → dist/ 정적 파일
npm run preview  # 빌드 결과 미리보기
```

## 🎮 조작

- **WASD / 방향키** — 캐릭터 이동
- **Esc** — 포모도로 타이머 시작/정지 (다이얼로그 열려있으면 닫기)
- **+ 버튼 / 입력창 클릭** — 투두 추가
- **TOWN INFO / RESIDENTS / SETTINGS / LOGIN** — 상단 네비

## 🖼 배경 이미지 교체 (그래픽 업그레이드)

기본은 우리 픽셀 마을 PNG. **레퍼런스급 페인팅** 사용하려면:

```bash
# 원하는 1280×768 이상 이미지를 그대로
cp ~/your_painted_village.png public/village_background.png

# 또는 임의 크기 → npm run dev 가 알아서 채움
```

권장 비율: **4:3 또는 16:9** (1920×1080도 OK)  
권장 스타일: 위에서 본 시점, 마을 + 자연 풍경

AI로 생성하려면 (Midjourney/DALL-E):
```
top-down 2.5D cozy village painting, red roof log cabins, 
small wooden bridge over creek, dense pine forest border, 
sunny afternoon, Studio Ghibli + Stardew Valley vibe,
1920x1280 ratio, no UI overlays, no text
```

## 🏗 구조

```
web/
├── index.html                  # 진입점 (Korean 폰트 preload)
├── public/
│   ├── village_background.png  # 여기를 갈아끼우면 됩니다
│   └── favicon.svg
├── src/
│   ├── App.tsx                 # 최상위
│   ├── components/
│   │   ├── Village.tsx         # 배경 + 카메라 + 캐릭터 컨테이너
│   │   ├── Character.tsx       # SVG 캐릭터 (4방향 + 아이들 흔들림)
│   │   ├── ChiefHouseMarker.tsx
│   │   ├── DayCycle.tsx        # 120초 주기 색 보정
│   │   ├── CherryPetals.tsx    # 떨어지는 꽃잎 (CSS)
│   │   ├── TopNav.tsx
│   │   ├── PomodoroPanel.tsx
│   │   ├── DateTodoPanel.tsx
│   │   ├── NotificationPanel.tsx
│   │   └── InfoDialog.tsx
│   ├── store/                  # Zustand (자동 저장: useTodos, useGameState)
│   │   ├── useTimer.ts
│   │   ├── useTodos.ts         # localStorage 영속화
│   │   ├── useNotifications.ts
│   │   ├── useGameState.ts     # localStorage 영속화
│   │   └── usePlayer.ts
│   └── index.css               # Tailwind + 글래스 패널 + 꽃잎 애니
├── tailwind.config.js          # cozy 색상 팔레트, 폰트, 애니메이션
└── vite.config.ts
```

## 🎨 디자인 결정

- **글래스모피즘 HUD** — `backdrop-blur` + 반투명 다크 배경 + 황금 보더
- **Press Start 2P + VT323** 폰트 — 픽셀 게임 느낌
- **시간대 색 보정** — 120초 주기로 새벽/낮/노을/밤 (`mix-blend-mode: multiply`)
- **떨어지는 꽃잎** — pure CSS 애니메이션, GPU 가속
- **Vignette** — 가장자리 비네팅으로 시네마틱
- **Framer Motion** — 패널 페이드인/슬라이드업

## 🚢 배포

### Vercel (제일 빠름)
```bash
npm i -g vercel
vercel
```

### Netlify
```bash
npm run build
# dist/ 폴더를 netlify drop에 드래그
```

### GitHub Pages
```bash
npm run build
# dist/ 내용을 gh-pages 브랜치로
```

## 🔄 Godot 버전과 차이

| 항목 | Godot | 웹 (지금) |
|---|---|---|
| 그래픽 | 16×16 픽셀아트 (Sparklin CC0) | 자유 (PNG/SVG/CSS, 픽셀이든 페인팅이든) |
| 캐릭터 | AtlasTexture region 스왑 | SVG + Framer Motion |
| 시간대 | CanvasModulate 노드 | CSS overlay + `mix-blend-mode` |
| 상태저장 | `user://save.json` | localStorage (Zustand persist) |
| 배포 | exe/dmg/web export | `vercel` 한 줄 |
| 모바일 | 별도 export | 반응형 (지금은 데스크탑 최적) |
