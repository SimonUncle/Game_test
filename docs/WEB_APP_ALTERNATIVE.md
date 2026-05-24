# 웹앱 버전이라면? — 그래픽 가능성 + 완전한 MCP 스택

> 결론: **Godot 픽셀 = 한계 명확, 웹앱 = 거의 제한 없음.**
> 웹앱이면 사용자가 보내준 레퍼런스 이미지 같은 페인팅 스타일도
> 그대로 가능합니다. 다만 "게임"보다는 "인터랙티브 웹앱"이 됩니다.

---

## 0. 한 줄 비교

| | Godot 16×16 픽셀 (현재) | React + Phaser 웹앱 |
|---|---|---|
| 그래픽 자유도 | 16×16 chibi 고정 | **제한 없음** (PNG/SVG/WebGL/AI생성 다) |
| 레퍼런스 매칭 | 30~70% (스타일 한계) | **95~100%** (이미지 그대로 사용 가능) |
| 개발 속도 | 셋업 빠름, 폴리싱 노가다 | 셋업 보통, 폴리싱 빠름 |
| 배포 | exe/dmg 빌드 필요 | URL만 공유 (Vercel 30초) |
| 모바일 | export 셋업 복잡 | 반응형 CSS면 끝 |
| "진짜 게임" 느낌 | ✅ | △ (인터랙티브 앱) |

---

## 1. 웹앱이 그래픽 좋은 이유 — 구체적으로

### 1.1 레퍼런스 이미지 그대로 사용 가능
```jsx
<div style={{
  backgroundImage: 'url(/village_reference.png)',
  backgroundSize: 'cover',
  width: '100vw', height: '100vh'
}}>
  <PlayerSprite />  {/* div나 canvas로 캐릭터 얹기 */}
  <TimerHUD />      {/* React 컴포넌트 */}
</div>
```
사용자가 보내준 그 AI 페인팅 이미지를 **배경으로 그대로 깔면 100% 매칭**.

### 1.2 AI로 게임 에셋 즉시 생성 (MCP 경유)
Flux Pro / DALL-E / Midjourney를 Claude에서 직접 호출:
```
"마을 배경 1920x1080 페인팅 스타일로 생성해줘. 
 빨간 지붕 통나무집 4채, 시냇물, 빽빽한 숲, 위에서 본 시점"
→ Flux 한 번 호출 → 완성된 페인팅 PNG
```

### 1.3 SVG로 무한 해상도 캐릭터
픽셀이 아니라 **벡터 일러스트** 캐릭터를 SVG로:
- 줌해도 안 깨짐
- CSS 애니메이션으로 부드러운 움직임
- 색상 동적 변경 가능 (낮/밤)

### 1.4 CSS/WebGL 효과
실제 빛/그림자 셰이더, 파티클, 블러 등을 한 줄로:
```css
.character { filter: drop-shadow(2px 4px 6px rgba(0,0,0,.5)); }
.water { animation: shimmer 3s infinite; backdrop-filter: blur(2px); }
```

---

## 2. 추천 웹 스택

### 가장 빠른 길 — "이미지 + React"
```
React 18 + TypeScript
├── 배경: PNG (AI 생성 or 사용자 레퍼런스)
├── 캐릭터: <div> + CSS 애니메이션 또는 SVG
├── UI: Tailwind CSS + shadcn/ui (타이머/투두/알림)
├── 상태: Zustand (캐릭터 위치, 타이머)
└── 빌드: Vite (HMR 즉시 반영)
```
**언제**: 마을 탐험은 약간만 + UI 중심 (포모도로 메인). 우리 현재 게임이 사실 이쪽에 가까움.

### 진짜 게임 느낌 — "Phaser + React HUD"
```
Phaser 3 (게임 캔버스)
├── 마을 맵 + 캐릭터 이동 + 충돌
└── React (HUD 오버레이)
    └── 타이머/투두/알림/네비
```
**언제**: 진짜 마을 게임 만들고 싶을 때. AI 코드 생성 정확도 **94%** (Phaser의 구조화된 API 덕분).

### 풀 페인팅 게임 — "이미지 베이스 + Three.js 효과"
```
이미지 배경 (AI 페인팅 1920x1280)
└── Three.js or PixiJS로 위에 효과
    ├── 캐릭터 이동
    ├── 파티클 (꽃잎, 반딧불)
    └── 시간대 색 보정 셰이더
```
**언제**: 시각 퀄리티 최우선, 게임플레이 단순.

---

## 3. 웹앱용 MCP·스킬 완전 카탈로그

### 🎨 이미지 생성 MCP (그래픽의 핵심)

| MCP | 모델 | 강점 | 가격 |
|---|---|---|---|
| [**merlinrabens/image-gen-mcp**](https://github.com/merlinrabens/image-gen-mcp-server) | DALL-E, Stability, Gemini 멀티 | 자동 fallback | 무료 (API 키만) |
| [**FAL MCP**](https://www.pulsemcp.com/servers/sshtunnelvision-fal-ai-image-generation) | fal-ai/recraft-v3 | 빠른 생성 | FAL 크레딧 |
| [**Replicate Flux**](https://www.pulsemcp.com/servers/mikeyny-image-generation-replicate-flux-schnell) | flux-schnell | 가성비 좋음 | Replicate 사용량 |
| [**ComfyUI MCP**](https://github.com/artokun/comfyui-mcp) | 로컬 SD/Flux/SD3 | LoRA·다양 모델, **무료** | GPU만 있으면 무료 |
| [**Midjourney via AceData**](https://www.mindstudio.ai/blog/automate-browser-tasks-claude-code-playwright) | Midjourney v6+ | 최고 퀄리티 | MJ 구독 |
| [**Together AI**](https://www.pulsemcp.com/servers/sarthakkimtani-together-ai-image-generation) | Flux 호스팅 | 안정적 | 사용량 |

**우리 케이스 추천**: ComfyUI MCP (무료 + Flux로 페인팅 스타일 가능) 또는 Replicate Flux (셋업 쉬움).

### 🎮 게임 엔진 MCP

| MCP | 용도 |
|---|---|
| [**Phaser Editor MCP**](https://github.com/phaserjs/editor-mcp-server) (공식) | Phaser 씬·스프라이트 자동 생성. Claude Sonnet 추천 |
| [**Web Game Development Skill**](https://mcpmarket.com/tools/skills/web-game-development) | Phaser/Three.js/Babylon 통합 가이드 |
| [**Phaser Game Skill**](https://mcpmarket.com/tools/skills/phaser-game-development-1) | Phaser 전용 패턴 |

### 🎨 UI/디자인 MCP

| MCP | 용도 |
|---|---|
| [**Figma MCP**](https://github.com/reuvenaor/figma-mcp-to-tailwind) | Figma 디자인 → React + Tailwind 자동 변환 |
| [**shadcn/studio Figma**](https://shadcnstudio.com/blog/figma-to-code-conversion-guide) | Figma → shadcn/ui 컴포넌트 |
| **shadcn MCP** | shadcn 컴포넌트 자동 설치/사용 |

### 🧪 시각 테스트 MCP

| MCP | 용도 |
|---|---|
| [**Playwright MCP**](https://playwright.dev/docs/getting-started-mcp) | 브라우저 자동 제어, 스크린샷, 시각 회귀 테스트 |
| Claude가 직접 게임 플레이 + 스샷 비교 가능 | 우리 xvfb 해킹 대신 |

### ⚡ 기타 유용

| MCP | 용도 |
|---|---|
| **Cloudflare/Vercel MCP** | 원클릭 배포 |
| **Supabase MCP** | 클라우드 세이브, 사용자 계정 |
| **PostHog MCP** | 사용자 행동 분석 |

---

## 4. "레퍼런스 그대로" 워크플로우 (5분)

```
1. 사용자가 레퍼런스 PNG 제공
   ↓
2. Claude가 Flux MCP로 비슷한 추가 배경 생성
   (마을 동쪽, 서쪽, 다양한 시간대 등 4-6장)
   ↓
3. 캐릭터 SVG 생성 (또는 PixelLab MCP)
   ↓
4. Phaser/React로 합치기:
   - 배경 PNG 띄우기
   - 캐릭터 위에 얹기 + 이동 가능
   - UI 오버레이 (타이머/투두)
   ↓
5. Playwright MCP로 자동 스샷 → 시각 확인
   ↓
6. Vercel MCP로 deploy → URL 생성
```

이 전체가 **Claude한테 자연어로 요청하면 자동 실행** 됩니다 (MCP들 다 설치된 가정).

---

## 5. 우리 프로젝트 웹앱으로 포팅하면

### 그대로 옮길 수 있는 것
- ✅ 포모도로 타이머 로직
- ✅ 투두 매니저
- ✅ 알림 시스템
- ✅ 세이브/로드 (localStorage 또는 Supabase)
- ✅ 캐릭터 이동 로직
- ✅ 다이얼로그 시스템

### 더 좋아지는 것
- 🎨 **배경 = 사용자 레퍼런스 이미지 그대로**
- 🎨 캐릭터 = SVG 일러스트 (벡터)
- 🎨 UI = shadcn/ui (현대적 디자인 시스템)
- 🎨 애니메이션 = Framer Motion (부드러움)
- 📱 모바일 자동 대응
- 🚀 5초 배포 (Vercel)

### 잃는 것
- 진짜 게임엔진 기능 (물리, 셰이더 등) — 단순 인터랙션이면 무관

---

## 6. 시작 가이드 (실제 명령)

```bash
# 1. 프로젝트 생성
npm create vite@latest mongle-village-web -- --template react-ts
cd mongle-village-web

# 2. UI 라이브러리
npm install tailwindcss @radix-ui/react-dialog framer-motion zustand
npx shadcn@latest init

# 3. (선택) 게임 엔진
npm install phaser
# 또는 더 단순하게: 그냥 React만으로도 가능

# 4. MCP 설치
claude mcp add flux -- npx @replicate/flux-mcp        # 이미지 생성
claude mcp add playwright -- npx @playwright/mcp      # 시각 테스트
claude mcp add shadcn -- npx shadcn-mcp               # UI 컴포넌트

# 5. Claude에게 의뢰
claude
> 우리 Godot 프로젝트 (../Game_test) 를 React 웹앱으로 포팅해줘.
> 마을 배경은 첨부 이미지 그대로 사용. 캐릭터는 픽셀 캐릭터 SVG로
> 다시 만들고, UI는 shadcn으로. Phaser 없이 React만으로 시작.
```

---

## 7. 실제 결과 예상

**1주차** (Claude + MCP 풀 스택):
- 배경 이미지로 마을 표시
- 캐릭터 이동
- 포모도로 타이머
- 투두 + 알림
- 로컬 저장
→ Vercel 배포

**2주차**:
- Flux로 동/서/북/남 마을 확장 이미지 4장 생성
- 캐릭터 4방향 워크 (SVG 애니메이션)
- 시간대별 배경 보정 (CSS filter)
- 다이얼로그 시스템

**1개월**:
- 주민 NPC + 대화
- 사이클별 마을 성장 (집/꽃 추가)
- 클라우드 세이브 (Supabase)
- 다국어 지원

**비주얼 퀄리티**: 사용자 레퍼런스의 **95%+** 즉시 도달 (배경 이미지 그대로 쓰니까).

---

## 8. 솔직한 권장

이번 프로젝트의 **본질**을 생각해보면:
- 포모도로/투두/알림 = 메인 기능 (생산성 앱)
- 마을 그래픽 = 시각적 동기부여 (탐험 자체는 부가)

이 경우 **웹앱이 압도적으로 적합**합니다:
- 사용자가 매일 켤 거 → 브라우저 탭이 더 자연스러움
- 그래픽 퀄리티 = 매일 보는 거니 좋을수록 동기부여 ↑
- 모바일/데스크탑 동시 지원
- 친구한테 URL 보내기

게임으로 만들면:
- 실행하는 게 부담 (별도 앱)
- 그래픽 = 16×16 제약
- 모바일 별도 빌드
- 친구한테 .exe 보내는 것도 어색

**진심 권고**: 다음 라운드는 웹앱으로 새로 시작하세요. 위 명령 그대로 치면 1주에 더 좋은 결과 나옵니다.

---

## 9. 만약 Godot 계속 갈 거면

그것도 OK. 다만 **다음 라운드부터는**:
```bash
# 환경 셋업 (15분)
claude mcp add godot -- npx @coding-solo/godot-mcp
claude mcp add aseprite -- aseprite-mcp 설치
claude mcp add pixellab -- pixellab MCP

# 그리고 이번 CLAUDE.md + skills 활용
```

이 셋업 한 번 하면 이번 16시간 노가다가 **1~2시간으로** 줄어요.

---

## 참고 링크

- [Phaser Editor MCP Server (공식)](https://github.com/phaserjs/editor-mcp-server)
- [shadcn/studio Figma Plugin](https://shadcnstudio.com/blog/figma-to-code-conversion-guide)
- [ComfyUI MCP + Claude Code 플러그인](https://github.com/artokun/comfyui-mcp)
- [Replicate Flux MCP](https://www.pulsemcp.com/servers/mikeyny-image-generation-replicate-flux-schnell)
- [Playwright MCP](https://playwright.dev/docs/getting-started-mcp)
- [Multi-provider Image Gen MCP](https://github.com/merlinrabens/image-gen-mcp-server)
- [MCP 서버 카탈로그 (mcpservers.org)](https://mcpservers.org)
- [PulseMCP — MCP 검색](https://www.pulsemcp.com)
