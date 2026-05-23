# MCP·스킬 정직한 가이드

> 이전 버전은 너무 일반론이었습니다. 이 문서는 **우리가 한 구체적인
> 실수마다 어떤 MCP가 잡을 수 있었는지** 매핑합니다.

---

## 0. 결론 먼저

이번 프로젝트 노가다의 **80%는 이미 존재하는 MCP들로 막을 수 있었어요.**
구체적으로:

- **Godot MCP** (`Coding-Solo/godot-mcp` 등): 우리가 한 xvfb 해킹 + 수동 .tscn 편집 → 불필요
- **Aseprite MCP Pro**: 타일 좌표 추측 + 검은 외곽선 못 본 실수 → 차단
- **PixelLab MCP**: 16×16으로 못 만든 디테일 → AI가 직접 생성

다음 프로젝트는 **이 3개 설치부터 하고 시작하세요.**

---

## 1. 우리 실수 → 막아줬을 MCP 매핑

| 라운드 | 실수 | 잡을 수 있었던 MCP | 어떻게 |
|---|---|---|---|
| v1 | xvfb 명령 직접 작성 + 스크린샷 폴더 헤매기 | **Godot MCP** | `run_project` 도구가 빌트인. 캡처도 한 명령 |
| v2 | 잔디 타일 (12,16)의 1픽셀 검은 외곽선 못 발견 | **Aseprite MCP** | Aseprite에서 픽셀 단위 확대 + 색 분석. 검은 픽셀 1초에 발견 |
| v3 | 집을 5×3로 잘라서 옆집 일부가 끼어들어감 | **Aseprite MCP** | 타일셋에 슬라이스 그리드 그어두면 4×3 즉시 보임 |
| v4 | "부쉬" (12,11)이 사실 그루터기 | **Aseprite MCP** | 타일에 이름 라벨 가능. 또는 PixelLab에서 진짜 "bush" 생성 |
| v5 | "꽃" (2,9)가 사실 당근 | **Aseprite MCP** | 같음. 또는 카테고리 검색 |
| v6 | 손으로 .tscn 작성하다 collision shape 빠뜨림 | **Godot MCP** | `add_node`, `add_collision_shape` 도구로 직접 |
| v7 | 캐릭터 4방향 워크 sheet 좌표 추측 | **Aseprite MCP** + **Godot MCP** | Aseprite로 export → Godot SpriteFrames.tres 자동 생성 |
| v8 | 길 가장자리 직각 + 풀-길 경계 계단 | **PixelLab MCP** | Wang 타일셋 생성 — 경계 자동 처리 (계단 X) |
| v9~v15 | 매번 build → import → screenshot 4명령 반복 | **Godot MCP** | `run_project` 한 명령. 또는 우리 `/village-rebuild` 스킬 |

**모든 라운드의 핵심 시간 손실** = "Claude가 직접 Godot/Aseprite를 조작할 수 없어서 사람이 매개" 였음.

---

## 2. 실제 있는 MCP들 (2025년 5월 현재)

### Godot MCP — 여러 구현체 중 선택

| 구현 | 도구 수 | 특징 | 가격 |
|---|---|---|---|
| **[Coding-Solo/godot-mcp](https://github.com/Coding-Solo/godot-mcp)** | 기본 | 에디터 실행, 프로젝트 실행, 디버그 캡처, 씬 생성/노드 추가 | MIT 무료 |
| **[hi-godot/godot-ai](https://github.com/hi-godot/godot-ai)** | 120+ | 라이브 에디터 연결, 씬·노드·스크립트·시그널·머티리얼 | 무료 |
| **[tugcantopaloglu/godot-mcp](https://github.com/tugcantopaloglu/godot-mcp)** | 149 | 풀 엔진 제어. 네트워킹/3D/2D/UI/오디오/애니메이션 트리/물리/런타임 코드 실행 | 무료 |
| **[youichi-uda/godot-mcp-pro](https://github.com/youichi-uda/godot-mcp-pro)** | 172 | 프로 버전, 시그널 자동 와이어링, 디버그 향상 | $15 1회 |

설치 예 (Coding-Solo):
```bash
claude mcp add godot -- npx @coding-solo/godot-mcp
```

### Aseprite MCP Pro

[**aseprite-mcp.abyo.net**](https://aseprite-mcp.abyo.net) — 픽셀아트 업계 표준 에디터 Aseprite를 Claude가 직접 제어.

**121 도구** 포함:
- 타일셋 슬라이싱 + 메타데이터 관리
- 픽셀 단위 인스펙션 (검은 외곽선 같은 거 자동 검출)
- 애니메이션 만들기
- **Godot 형식으로 export**: SpriteFrames.tres, AnimationPlayer.tres, TileSet.tres

가격: Aseprite 본체 $20 + MCP는 추정 무료 (확인 필요)

### PixelLab MCP

[**pixellab.ai/mcp**](https://pixellab.ai/mcp) — AI 픽셀아트 생성 (요청 시 캐릭터/타일셋/애니메이션 즉시 생성).

특이 기능:
- **Wang 타일셋 생성** — 경계 타일 자동 처리로 계단 없는 부드러운 전환
- 캐릭터 4방향 워크 시트 한 번에
- 자연어 → 픽셀아트

가격: API 기반 (사용량 과금)

---

## 3. 다음 프로젝트 시작 시 — 30분 셋업

```bash
# 1. Godot MCP 설치 (무료)
claude mcp add godot -- npx @coding-solo/godot-mcp

# 2. Aseprite + Aseprite MCP 설치 ($20 + MCP 설정)
#    https://www.aseprite.org/ + aseprite-mcp.abyo.net 가이드

# 3. PixelLab MCP (선택 — AI 생성 필요할 때만)
#    https://pixellab.ai/mcp 에서 API key

# 4. 검증
claude
> /mcp     # 등록된 MCP 목록 확인
> godot 실행해서 빈 프로젝트 만들어줘
```

설치 후 첫 명령:
- "이 타일셋 분석하고 각 영역 자동 슬라이스해서 클래스 분류해줘"
- "이 캐릭터 4방향 워크 애니메이션 만들고 Godot 씬으로 export"
- "마을 배경에 시냇물 추가하되 Wang 타일로 자연스러운 경계로"

**이번 프로젝트에서 우리가 손으로 다 한 것들 = 한 명령씩으로 끝남.**

---

## 4. 시중 MCP가 아직 못하는 것

정직히, 이런 건 MCP로도 아직 어려움:

| 한계 | 이유 | 우회 |
|---|---|---|
| **AI 페인팅 → 픽셀아트 완벽 변환** | 본질적으로 다른 매체 | 풀 페인팅 게임 → Unity/Unreal + 별도 일러스트레이터 |
| **"이쁘게 만들어줘"** | 미적 기준 정량화 어려움 | 레퍼런스 + 구체적 평가 기준 합의 |
| **에셋팩 발견 (itch.io 자연어 검색)** | 그런 MCP 아직 없음 | WebSearch + 사람 판단 |
| **시각적 "느낌" 판단** | 사람만큼 정확히는 픽셀 차이 못 짚음 | 사용자 피드백 받는 게 빠름 |

---

## 5. 이 프로젝트 자체엔 적용 어려운 이유

이번 세션에서 Godot MCP를 안 쓴 건 환경 제약 때문:
- 컨테이너에 Godot 설치는 됐지만 GUI 없음
- xvfb 가상 디스플레이로 우회
- MCP 서버 따로 띄우는 셋업 안 됨

**로컬 개발자라면 처음부터 Godot MCP 쓰는 게 정답.**

---

## 6. 다른 도메인은 어떤가

게임 외 작업도 도메인 MCP가 있으면 천지차이:

| 도메인 | 도움 되는 MCP |
|---|---|
| **웹 개발** | Playwright MCP (E2E 테스트), Browser MCP |
| **디자인** | Figma MCP, Sketch MCP |
| **데이터** | DuckDB MCP, BigQuery MCP, Postgres MCP |
| **DevOps** | Kubernetes MCP, Terraform MCP |
| **문서** | Notion MCP, Confluence MCP |
| **커뮤니케이션** | Slack MCP, Discord MCP |
| **AI/ML** | Hugging Face MCP, Replicate MCP |

각 도메인마다 "Claude가 직접 도구를 조작할 수 있느냐"가 노가다 결정.

---

## 7. 우리가 만든 커스텀 스킬 — 여전히 가치 있음

Godot MCP가 있어도 **프로젝트별 함정**은 커스텀 스킬로 잡아야 함:

| 스킬 | Godot MCP가 있어도 필요한 이유 |
|---|---|
| `/tile-check` | 우리 타일셋의 특정 함정 좌표는 MCP가 모름. 프로젝트 메모리 |
| `/village-rebuild` | 우리 프로젝트의 정확한 빌드 순서 (build_village.py → import → screenshot) |
| `/reference-classify` | 프로젝트 외적인 판단 로직 (사용자 의도 분석) |

**즉**: MCP는 "도구 조작" 담당, 스킬은 "프로젝트 관례" 담당. 둘 다 필요.

---

## 8. 학생들에게 권장 시작 키트

게임 프로젝트 시작 시:

```yaml
필수 (무료):
  - Godot MCP (Coding-Solo 또는 hi-godot/godot-ai)
  - GitHub MCP (PR/이슈)
  - CLAUDE.md (프로젝트별 함정 메모)
  - .claude/skills/ (반복 작업 자동화)

추천 (유료지만 가치 높음):
  - Aseprite + Aseprite MCP Pro ($20 일회)
  - 픽셀아트 에셋팩: Sprout Lands ($5), Cozy Farm ($25) 등

선택 (필요 시):
  - PixelLab MCP (캐릭터 즉시 생성 필요할 때)
  - Playwright MCP (HTML5 빌드 검증)
```

---

## 9. 정직한 결론

이번 세션을 다시 한다면 — **Godot MCP + Aseprite MCP만 있어도** 똑같은 결과를
**1/3 시간에** 만들었을 거예요. 우리가 했던:
- xvfb로 스크린샷 → MCP 한 명령
- 타일 좌표 추측·확인 반복 → Aseprite에서 직접
- .tscn 손으로 작성 → MCP `add_node`
- build→import→screenshot 4명령 → MCP `run_project`

**노가다는 도구 부재의 증거입니다.** 

같은 실수 2번째부터는 자동화하든 MCP 찾든 처리하세요. 학생들에겐 이 원칙을
첫 시간에 가르치는 게 좋을 것 같습니다.

---

## 참고

- 검색해 본 Godot MCP 10여 개 — 가장 활발한 건 `tugcantopaloglu/godot-mcp` (149 도구)
- 픽셀아트 도구 분야 MCP는 Aseprite MCP가 사실상 표준
- PixelLab은 AI 생성 분야의 거의 유일한 옵션
- 새 MCP는 매주 등장하므로 [mcpservers.org](https://mcpservers.org) 또는 [glama.ai/mcp](https://glama.ai/mcp) 주기적 확인 권장
