# 알아두면 좋은 것 / Known Issues

> 친구한테 보내기 전에 이거 한 번 훑어보세요. 의도된 한계와 진짜
> 버그를 구분해 적었습니다.

---

## 🟡 의도된 한계 (버그 아님)

### 1. 모바일에서 깨짐
- 1920×1080 데스크탑 화면 기준으로 디자인됨.
- 모바일/태블릿에서 열면 UI 위치 깨지고 캐릭터 너무 작음.
- **워크어라운드**: 데스크탑/노트북에서 열기.
- **고치려면**: `web/src/App.tsx` 의 패널 위치를 Tailwind `md:` 브레이크포인트 추가.

### 2. 다리에 콜리전 없음
- 강을 가로지르는 나무 다리는 **순수 시각용**이에요.
- 강물 위로 걸어다녀도 안 막힙니다.
- **고치려면**: 충돌 영역을 React 상에 두지 않고 있어서, 추가하려면
  Village.tsx에 collision rect 배열 + 플레이어 이동 코드에 boundary
  체크 추가 필요. 현재는 화면 가장자리(40px)만 클램프.

### 3. 캐릭터가 집/나무 통과
- 배경이 통짜 PNG라 객체별 충돌이 없음.
- 캐릭터 + 닭이 집 / 나무 통과 가능 (시각만).
- **고치려면**: TileMap 변환 후 객체별 collision 정의. 큰 작업.

### 4. 사운드 없음
- BGM, 효과음, 타이머 알림음 전부 미구현.
- **추가 방법**: `web/public/sounds/` 폴더 만들고 `howler.js` 같은 라이브러리로 재생.

### 5. localStorage 영속화의 함정
- 투두 + 사이클 카운트는 브라우저 localStorage에 저장.
- **시크릿 모드** / **다른 브라우저** / **캐시 클리어** → 다 사라짐.
- 디바이스 간 동기화 안 됨.
- **클라우드 동기화 원하면**: Supabase MCP 또는 Firebase 추가.

### 6. 시간대 사이클이 실시간 기준
- 120초마다 새벽→낮→노을→밤 한 바퀴.
- 데모용. 실제 출시면 시스템 시간 기반(`new Date().getHours()`)으로 바꿔야.
- **위치**: `web/src/components/DayCycle.tsx`의 `CYCLE_DURATION`.

### 7. 배경 이미지 크기 고정
- `village_background.png`는 1280×768 가정.
- 다른 크기로 교체하면 카메라 클램프가 어색해질 수 있음.
- **고치려면**: `web/src/components/Village.tsx` 의 `WORLD_W` / `WORLD_H` 상수 수정.

### 8. Korean 폰트 의존
- Noto Sans KR을 Google Fonts에서 로드. 인터넷 끊기면 시스템 폰트로 폴백.
- 영어만 쓸 거면 `index.html` 에서 폰트 링크 정리 가능.

---

## 🔴 실제 버그 (재현되는 이슈)

지금까지는 **알려진 게 없음** (검증된 v15 기준).

발견하시면:
- 어디서 어떻게 발견됐는지 + 재현 단계 + 브라우저/OS
- 가능하면 스크린샷
- [GitHub Issues](https://github.com/simonuncle/game_test/issues)에 등록

---

## 🚧 트러블슈팅

### `npm install` 실패
```bash
# Node 버전 확인
node --version    # v18 이상이어야 함
# 안 되면 nvm 사용 권장
nvm install 20
nvm use 20
cd web && rm -rf node_modules package-lock.json && npm install
```

### 빌드는 되는데 실행 시 화면 까만색
- 브라우저 콘솔(F12) 열고 빨간 에러 확인.
- `react`/`react-dom` 버전 충돌일 가능성.
  ```bash
  cd web && npm install react@18 react-dom@18
  ```

### 캐릭터 안 움직임
- **게임 화면을 한 번 클릭**해서 포커스 줘야 키보드 입력 받음.
- 한국어 IME(한글 입력기) 켜져있으면 키가 안 먹힐 수 있음 — 영문으로 전환.

### 배경 이미지 회색
- `village_background.png`가 `public/`에 없음.
- `cd web && ls public/` 으로 확인. 없으면 `legacy/godot/tools/build_village.py` 돌려서 재생성:
  ```bash
  cd legacy/godot
  python3 tools/build_village.py
  cp assets/sprites/village_background.png ../../web/public/
  ```

### 한글 깨져 보임
- 시스템에 한글 폰트 설치돼있는지 확인.
- Windows/Mac은 기본 설치. Ubuntu/Linux는:
  ```bash
  sudo apt install fonts-noto-cjk
  ```

### vercel 배포에서 폰트 안 보임
- Google Fonts CDN 차단된 지역? `index.html`의 폰트 link 제거하고
  로컬 woff2 파일 받아서 자체 호스팅하면 해결.

---

## 🔮 미구현 (다음에 할 만한 거)

우선순위 순:

1. **모바일 반응형** — Tailwind `md:` 브레이크포인트
2. **사운드** — 타이머 ding, 환경음 (시냇물/새소리)
3. **클라우드 동기화** — Supabase 무료티어 + 로그인
4. **TileMap 마이그레이션** — 통짜 PNG → 진짜 타일맵 (편집 가능)
5. **NPC 마을사람** — 닭 패턴 재사용해서 사람 NPC + 대화
6. **계절감** — 봄(현재), 여름, 가을(단풍), 겨울(눈)
7. **PWA** — 설치 가능 + 오프라인 동작
8. **타이머 데스크탑 알림** — Notification API
9. **다국어 i18n** — 한국어/영어 토글

각 항목 자세한 구현은 [`docs/CLAUDE_CODE_WORKFLOW.md`](CLAUDE_CODE_WORKFLOW.md)
패턴에 따라 Claude Code로 추가 가능.

---

## 🔧 코드 컨벤션 (PR 받을 때)

- TypeScript strict mode 켜져있음. `any` 안 됨.
- 컴포넌트는 PascalCase, 훅은 `use*`, 스토어는 `use*Store` 안 쓰고 `useThing`.
- 상태는 모두 Zustand에. React Context 사용 안 함.
- 스타일은 Tailwind. 인라인 style은 동적 값(좌표, transform)에만.
- 한국어 코드 주석/이름 OK. UI 텍스트는 한국어/영어 혼용 의도적.
