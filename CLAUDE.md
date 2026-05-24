# CLAUDE.md — 몽글마을 (Mongle Village)

> Claude Code가 매 세션 시작 시 이 파일을 자동으로 읽습니다.
> **읽고 시작하세요. 같은 실수 반복하면 시간 낭비입니다.**

---

## 프로젝트 개요

코지팜 픽셀 게임 + 포모도로/투두/알림 통합. **Godot 4.3** + **GDScript**.

- **시각 기조**: 16×16 chibi 픽셀아트 (Stardew Valley 풍 cozy farm)
- **에셋**: `assets/sparklin/ninja_tileset.png` — Sparklin Labs Ninja Adventure (CC0)
- **마을 배경**: 통짜 PNG (`assets/sprites/village_background.png`), `tools/build_village.py`로 합성
- **타깃 해상도**: 1920×1080, 픽셀-퍼펙트, GL Compatibility 렌더러
- **카메라 줌**: 2.5× (캐릭터를 보이기 위한 값, 바꾸지 마세요)

---

## 절대 시도하지 말 것

| 시도 금지 | 이유 |
|---|---|
| **AI 페인팅 스타일 재현** | 16×16 chibi로는 물리적으로 불가능. 사용자가 페인팅 레퍼런스를 줘도 솔직히 한계 명시하고 합의부터. |
| **타일 좌표 추측해서 추가** | 거의 매번 틀림 (아래 함정 표 참고). 항상 단독 크롭 보고 확인 후 등록. |
| **검은 외곽선 있는 잔디 타일 사용** | `(12, 16)`은 좌측 1px 검은 줄 있음. 깔면 16px마다 수직 줄무늬. |
| **집을 5×3로 자르기** | 4×3입니다. 5×3로 자르면 옆집의 일부가 끼어들어가 "미완성"으로 보임. |
| **에셋 변경 후 검증 없이 커밋** | 빌드→스크린샷 루프 1분 안에 끝나니 항상 캡처 확인 후 커밋. |

---

## 검증된 타일 좌표

신뢰 가능한 것만 등록. **새 좌표 추가하기 전에 반드시 단독 미리보기 확인.**

### 지형
| 용도 | 좌표 | 비고 |
|---|---|---|
| 잔디 기본 | `(14, 16)` | 깨끗함, 외곽선 없음 |
| 잔디 변형 (점박이) | `(13, 16)` | 노란 점박이, sparse blend 용 |
| 흙길 | `(21, 16)` | 적갈색, 균일 |
| 물 | `(20, 8)` | 연못 중심 타일 |

### 건물 (모두 4×3 = 64×48px)
| 청크 | 좌표 |
|---|---|
| `HOUSES[0]` 오렌지 지붕 (3개 입구) | `chunk(0, 0, 4, 3)` |
| `HOUSES[1]` 베이지 지붕 | `chunk(4, 0, 4, 3)` |
| `HOUSES[2]` 오렌지 변형 | `chunk(8, 0, 4, 3)` |
| `HOUSES[3]` 빨간 벽돌 지붕 | `chunk(12, 0, 4, 3)` |

### 식물 (단일 타일)
| 용도 | 좌표 | 함정 |
|---|---|---|
| 작은 부쉬 | `(3, 13)` | ✅ |
| 큰 부쉬 (잎이 무성) | `(9, 15)` | ✅ |
| 풀 다발 | `(4, 15)` | ✅ |
| 해바라기 | `(3, 15)` | ✅ |

### 식물 (2×2 청크)
| 용도 | 청크 |
|---|---|
| 둥근 나무 | `chunk(4, 10, 2, 2)` |
| 어두운 나무 | `chunk(8, 10, 2, 2)` |
| 왼쪽 클럼프 | `chunk(0, 10, 2, 2)` |
| 소나무 | `chunk(6, 10, 2, 2)` |
| 벚꽃 (큰) | `chunk(4, 16, 2, 2)` |
| 벚꽃 (작은) | `chunk(8, 16, 2, 2)` |
| 큰 바위 | `chunk(14, 11, 2, 2)` |

### 절대 쓰지 말 것 (함정)
| 좌표 | 실제로는 |
|---|---|
| `(12, 11)` | 나무 그루터기 (부쉬 아님) |
| `(2, 9)`, `(3, 9)` | 당근 아이콘 (꽃 아님) |
| `(9, 16)` | 벚꽃나무 가장자리 픽셀 (부쉬 아님) |
| `(3, 16)` | 복숭아 식재 아이콘 (해바라기 아님) |
| `(12, 16)` | 잔디인데 검은 1px 외곽선 있음 |

---

## 빌드/검증 명령

### 마을 배경 재합성 (~5초)
```bash
python3 tools/build_village.py
# → assets/sprites/village_background.png 갱신
```

### Godot 임포트 (PNG 새로 생기면 필요, ~10초)
```bash
godot --headless --import --path .
```

### 헤드리스 실행 검증 (에러 체크, ~5초)
```bash
godot --headless --verbose --path . --quit-after 60 scenes/main.tscn 2>&1 \
  | grep -iE "(error|warning|fail)" | grep -v ALSA | grep -v vsync
# exit 0 + 출력 없음 = 깨끗함
```

### 스크린샷 캡처 (xvfb 필요)
```bash
xvfb-run -a -s "-screen 0 1920x1080x24" \
  godot --path . --resolution 1920x1080 tools/screenshot.tscn
# → user://screenshot.png (Linux: ~/.local/share/godot/app_userdata/.../screenshot.png)
```

### 시간대 4단계 캡처
```bash
xvfb-run godot --path . tools/screenshot_phases.tscn
# → phase_dawn.png, phase_noon.png, phase_dusk.png, phase_night.png
```

---

## 신규 작업 시 워크플로우

### A. 새 타일 좌표 추가하려면
```
1. Python으로 단독 크롭 → 128×128 확대 저장
   python3 -c "from PIL import Image; ...; im.crop(...).resize((128,128), Image.NEAREST).save('/tmp/preview.png')"
2. 보고 "정말 이거 맞나?" 시각 확인
3. 그 후에야 build_village.py에 등록
```

### B. 마을 배경 수정하려면
```
1. build_village.py 수정
2. python3 tools/build_village.py 빌드
3. godot --headless --import --path . 임포트
4. xvfb-run godot ... screenshot.tscn 캡처
5. 결과 확인 → OK면 커밋, 깨졌으면 step 1
```

### C. 사용자가 레퍼런스 이미지를 줬을 때 (필수)
**먼저 분류**:
- 실제 게임 스샷 → 비슷한 에셋팩 찾기
- AI 페인팅 / 컨셉아트 → **솔직히 한계 명시**, 방향 합의
- 일러스트 → 색감/구도만 참고

분류 안 하고 따라잡으려고 시작하면 시간 폭발합니다.

### D. 시각적 버그 ("뭔가 깨져 보임")
**픽셀 단위 진단 먼저**:
1. 의심 영역 3곳 짚기 (확대 크롭 저장)
2. 각 영역의 원인 후보
3. 가장 작은 수정 한 가지부터 (한 번에 큰 변경 X)

이번 프로젝트에서 큰 변경 한 번에 → 더 망가지는 일 반복했음.

---

## 자주 까먹는 사실

- **CanvasModulate (DayCycle)는 World 위에만 적용**. UI는 별도 CanvasLayer라 영향 안 받음.
- **AnimatedSprite**대신 **AtlasTexture + region 변경**으로 4방향 워크 구현 중. `scripts/player.gd` 참고.
- **자동저장 30초 + 윈도우 닫을 때** — `scripts/autoload/save_manager.gd`. `user://save.json`.
- **5개 싱글톤 모두 autoload**: `GameState`, `TimeManager`, `TodoManager`, `NotificationBus`, `SaveManager`. `project.godot` 참고.
- **닭 NPC는 별도 콜리전 레이어 4** — 플레이어(2), 건물(1), 닭(4) 겹치지 않음.

---

## 깨끗한 PR 체크리스트

커밋 전 확인:
- [ ] `tools/build_village.py` 수정 시 → 빌드 + 임포트 + 60프레임 헤드리스 실행 → exit 0
- [ ] 새 씬 추가 시 → 인스턴스로 부모 씬에 등록되어 있는지
- [ ] 새 스크립트 → autoload 필요한 경우 `project.godot`에 등록
- [ ] PNG 변경 시 → `.import` 파일도 같이 커밋 (Godot이 자동 생성)
- [ ] 비주얼 변경 시 → 스크린샷 캡처해서 PR 본문에 첨부

---

## ⚠️ 다음 프로젝트는 — MCP 먼저 설치하고 시작

이번 프로젝트는 환경 제약으로 다 손으로 했지만, 로컬 개발이라면 **무조건**:

```bash
# 1. Godot 직접 제어 (xvfb 해킹 + 수동 .tscn 편집 불필요)
claude mcp add godot -- npx @coding-solo/godot-mcp

# 2. (있으면) Aseprite MCP — 타일 좌표 추측 사라짐
#    https://aseprite-mcp.abyo.net
```

이번 세션 노가다 80%는 이 두 MCP만 있어도 사라졌을 거예요.
상세: [`docs/MCP_AND_SKILLS.md`](docs/MCP_AND_SKILLS.md)

## 이 프로젝트의 커스텀 스킬

`.claude/skills/` 폴더에 3개 있음. **새 작업 시작 전 활용:**

- `/tile-check c,r` — 타일 좌표를 build_village.py에 등록하기 전 시각 확인
- `/village-rebuild` — build → import → validate → screenshot 풀 루프
- `/reference-classify` — 사용자가 레퍼런스 이미지 줄 때 분류 + 한계 명시

상세: [`docs/MCP_AND_SKILLS.md`](docs/MCP_AND_SKILLS.md)

## 참고 문서

- 상세 작업 패턴: [`docs/CLAUDE_CODE_WORKFLOW.md`](docs/CLAUDE_CODE_WORKFLOW.md)
- MCP/스킬 가이드: [`docs/MCP_AND_SKILLS.md`](docs/MCP_AND_SKILLS.md)
- **웹앱 버전 가능성 검토**: [`docs/WEB_APP_ALTERNATIVE.md`](docs/WEB_APP_ALTERNATIVE.md)
- 사용자용 실행 가이드: [`HOW_TO_RUN.md`](HOW_TO_RUN.md)
- 프로젝트 소개: [`README.md`](README.md)

---

## 마지막 — 작업 정신

1. **추측 금지**: 좌표든 크기든 한계든 — 항상 검증 먼저.
2. **루프 1분 안에**: 빌드→캡처→판정. 늦으면 인프라부터 고치기.
3. **솔직함**: 안 되는 건 안 된다고 말하기. 헛수고 1라운드 = 30분 손해.
