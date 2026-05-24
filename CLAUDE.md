# CLAUDE.md — 몽글마을 (Mongle Village)

> Claude Code가 매 세션 시작 시 이 파일을 자동으로 읽습니다.
> **읽고 시작하세요. 같은 실수 반복하면 시간 낭비입니다.**

---

## 프로젝트 개요

코지팜 마을 + 포모도로 타이머 + 투두 + 알림 통합 웹앱.
**메인 코드는 `web/` 폴더.** 초기 Godot 버전은 `legacy/godot/`에 참고용으로 보관.

- **메인 스택**: React 18 + TypeScript + Vite 5 + Tailwind 3 + Zustand 5
- **시각 기조**: Sparklin "Ninja Adventure" 16×16 CC0 픽셀아트로 합성한 통짜 PNG 배경 + SVG 캐릭터/UI
- **타깃 해상도**: 1920×1080 데스크탑 (모바일 미지원)
- **배포**: `vercel` 한 줄로 정적 호스팅
- **레거시**: Godot 4.3 + GDScript 버전 — `legacy/godot/`

---

## 디렉토리 지도

```
.
├── web/                       # 메인 코드 — 95% 이 안에서 작업
│   ├── src/
│   │   ├── App.tsx           # 최상위 라우터·키보드 단축키
│   │   ├── components/        # Village, Character, Chicken, HUD 패널들
│   │   └── store/             # Zustand (useTimer/useTodos/useChickens 등)
│   └── public/
│       └── village_background.png   # 합성된 배경. 통째로 교체 OK
├── legacy/godot/              # 초기 구현. 참고용. 수정 거의 안 함
│   └── tools/build_village.py # 배경 PNG 합성 스크립트 (필요시 돌림)
├── docs/                      # 작업/배경 문서
├── .claude/skills/            # 커스텀 슬래시 스킬
└── CLAUDE.md                  # 이 파일
```

---

## 절대 시도하지 말 것

| 시도 금지 | 이유 |
|---|---|
| **AI 페인팅 스타일 재현** | 16×16 chibi로는 물리적으로 불가능. 사용자가 페인팅 레퍼런스를 주면 솔직히 한계 명시하고 합의부터. |
| **타일 좌표 추측해서 추가** | 거의 매번 틀림. `build_village.py` 수정 시 항상 단독 크롭 시각 확인. |
| **`legacy/godot/` 안 코드 수정** | 메인 코드는 `web/`. 참고만 하세요. |
| **빌드 검증 없이 커밋** | `cd web && npm run build` 가 깨끗하게 통과해야 함. TS strict. |

---

## 빌드 / 검증 명령

```bash
# 메인 (웹앱) ─ 첫 1회
cd web && npm install

# 개발 서버 (HMR)
cd web && npm run dev                 # → http://localhost:5173

# 프로덕션 빌드 + 타입체크 (커밋 전 필수)
cd web && npm run build               # → dist/ 생성. TS 에러 있으면 실패.

# 빌드 결과 미리보기
cd web && npm run preview             # → http://localhost:4173

# Playwright 스크린샷 (이 컨테이너에 chromium 깔려있음)
node /tmp/shoot.mjs                   # OUT=/tmp/out.png DELAY=2000

# 배경 PNG 재합성 (legacy/godot 안에서)
cd legacy/godot && python3 tools/build_village.py
cp legacy/godot/assets/sprites/village_background.png web/public/
```

---

## 검증된 좌표 (legacy/godot 작업 시만 필요)

`legacy/godot/assets/sparklin/ninja_tileset.png` 28×40 그리드 (16px 타일).
**새 좌표 추가 전 반드시 단독 미리보기 확인.**

| 용도 | 좌표 | 비고 |
|---|---|---|
| 잔디 기본 | `(14, 16)` | 깨끗함, 외곽선 없음 |
| 잔디 변형 | `(13, 16)` | 노란 점박이 |
| 흙길 | `(21, 16)` | |
| 물 (물결) | `(23, 7)` | 물결무늬 있음 |
| 연꽃 | `(23, 8)` | 강의 accent |
| 다리 판자 | `(24, 8)` | 강 가로지름 |
| 집 (모두 4×3) | `chunk(0,0,4,3)` `chunk(4,0,4,3)` `chunk(8,0,4,3)` `chunk(12,0,4,3)` | |
| 둥근 나무 | `chunk(4, 10, 2, 2)` | |
| 어두운 나무 | `chunk(8, 10, 2, 2)` | |
| 큰 부쉬 | `(9, 15)` | 깨끗함 |
| 해바라기 | `(3, 15)` | 베이스에 흙 있음 → `_strip_dirt_base()` 필수 |
| 풀 다발 | `(4, 15)` | 흙 strip 필수 |

### 절대 쓰지 말 것 (함정)
| 좌표 | 실제로는 |
|---|---|
| `(12, 11)` | 나무 그루터기 |
| `(13, 11)` | 갈색 나무 블록 (자갈 아님) |
| `(2, 9)`, `(3, 9)` | 당근 |
| `(14, 11, 2, 2)` | 큰 바위 위 절반만 진짜, 아래 절반은 사막 사장 — 청크로 쓰면 오렌지 사각 같이 박힘 |
| `(12, 16)` | 잔디인데 왼쪽 1px 검은 줄 → 깔면 수직 줄무늬 |
| 임의의 `chunk(c, r, w, h)` | 청크 잘라서 쓰기 전에 단독 미리보기 필수 |

---

## 신규 작업 시 워크플로우

### A. 웹 컴포넌트 추가
```
1. web/src/components/Foo.tsx 작성
2. web/src/store/useFoo.ts 필요하면 작성 (Zustand)
3. App.tsx 또는 Village.tsx에서 마운트
4. npm run build → TS 에러 없는지 확인
5. npm run dev → 브라우저에서 동작 확인
6. Playwright 스크린샷 → 깨진 거 없는지
```

### B. 배경 PNG 변경
```
1. legacy/godot/tools/build_village.py 수정
2. cd legacy/godot && python3 tools/build_village.py
3. cp legacy/godot/assets/sprites/village_background.png web/public/
4. (개발서버 자동 리로드. 안 되면 cd web && npm run build 후 preview)
5. 스크린샷 검증 + 줌인 검증 (사각 깨진 거 있는지)
```

### C. 사용자가 시각 버그 신고
```
1. 사용자가 보낸 스크린샷에서 의심 영역 짚기
2. Playwright로 같은 각도 재현 스크린샷
3. 줌인해서 픽셀 단위 비교
4. 원인 추정 (보통: chunk 좌표 + 다른 영역 포함 / 흙 베이스 / 충돌 부재)
5. 작은 수정 + 재빌드 + 검증
```

### D. 사용자가 레퍼런스 이미지를 주면
**먼저 분류**:
- 실제 게임 스크린샷 → 비슷한 에셋팩 검색 → 가능
- AI 페인팅 / 컨셉아트 → **솔직히 한계 명시**, 합의 후 시작
- 일러스트 → 색감/구도만 참고

분류 안 하고 따라잡으려고 시작하면 시간 폭발.

---

## 자주 까먹는 사실

### 웹 (메인)
- **CanvasModulate 없음**. 시간대는 `mix-blend-mode: multiply` CSS overlay (DayCycle.tsx).
- **카메라 클램프 주의** — 플레이어 위치에 따라 화면이 한쪽으로 쏠림. 스폰 위치가 시각 디자인에 직결됨.
- **localStorage 영속화** — `persist` 미들웨어가 자동. 키: `mongle-todos`, `mongle-game-state`.
- **닭 충돌**: `useChickens.ts`의 `HOUSE_RECTS` 배열이 `build_village.py`의 placements와 동기화돼야 함. 집 위치 바꾸면 둘 다 수정.
- **TS strict** — `any` 금지. `noUnusedLocals`, `noUnusedParameters` 켜져있음.

### 레거시 (Godot, 거의 안 만지지만)
- 5개 싱글톤 모두 autoload: `GameState`, `TimeManager`, `TodoManager`, `NotificationBus`, `SaveManager`.
- 닭 NPC 콜리전 레이어 4. 플레이어 2, 건물 1.
- `user://save.json`으로 저장.

---

## 깨끗한 PR 체크리스트

커밋 전 확인:
- [ ] `cd web && npm run build` 통과 (TS 에러 0건)
- [ ] 신규 컴포넌트면 `App.tsx` 또는 부모에서 마운트됐는지
- [ ] 신규 스토어면 `persist` 미들웨어 필요한지 판단
- [ ] 비주얼 변경이면 Playwright 스크린샷 + 줌인 검증
- [ ] 한국어 UI 텍스트 깨짐 없는지
- [ ] `localStorage` 키 추가했으면 기존 키와 안 겹치는지

---

## ⚠️ 다음 프로젝트는 — MCP 먼저 설치하고 시작

이번 프로젝트는 환경 제약으로 컨테이너 안에서 다 했지만, 로컬 개발이라면 **무조건**:

```bash
# 1. 웹앱 시각 검증 자동화
claude mcp add playwright -- npx @playwright/mcp

# 2. AI 이미지 생성 (배경 페인팅 즉시 생성)
claude mcp add flux -- npx replicate-flux-mcp

# 3. (Godot 작업 시) Godot MCP — 손 .tscn 편집 불필요
claude mcp add godot -- npx @coding-solo/godot-mcp
```

상세: [`docs/MCP_AND_SKILLS.md`](docs/MCP_AND_SKILLS.md)

---

## 이 프로젝트의 커스텀 스킬

`.claude/skills/` 폴더에 3개. **새 작업 시작 전 활용:**

- `/tile-check c,r` — 타일 좌표 등록 전 시각 확인 (legacy/godot 작업 시)
- `/village-rebuild` — build_village.py → 임포트 → 캡처 풀 루프
- `/reference-classify` — 사용자가 레퍼런스 이미지 줄 때 분류 + 한계 명시

상세: [`docs/MCP_AND_SKILLS.md`](docs/MCP_AND_SKILLS.md)

---

## 참고 문서

- 친구용 / 일반 사용자용: [`README.md`](README.md)
- 알려진 한계 + 트러블슈팅: [`docs/KNOWN_ISSUES.md`](docs/KNOWN_ISSUES.md)
- 작업 패턴/회고: [`docs/CLAUDE_CODE_WORKFLOW.md`](docs/CLAUDE_CODE_WORKFLOW.md)
- MCP/스킬 매핑: [`docs/MCP_AND_SKILLS.md`](docs/MCP_AND_SKILLS.md)
- 웹앱 vs 게임엔진 결정: [`docs/WEB_APP_ALTERNATIVE.md`](docs/WEB_APP_ALTERNATIVE.md)
- 웹 내부 구조: [`web/README.md`](web/README.md)
- Godot 버전 (참고): [`legacy/godot/HOW_TO_RUN.md`](legacy/godot/HOW_TO_RUN.md)

---

## 마지막 — 작업 정신

1. **추측 금지**: 좌표/크기/한계 — 항상 검증 먼저.
2. **루프 1분 안에**: 빌드→캡처→판정. 늦으면 인프라부터 고치기.
3. **솔직함**: 안 되는 건 안 된다고 말하기. 헛수고 1라운드 = 30분 손해.
4. **위치 단일 진실원**: 집 위치 같은 데이터는 한 곳에만 (build_village.py의 placements). 닭 같은 다른 시스템이 참조할 땐 동기화 의무 명시.
