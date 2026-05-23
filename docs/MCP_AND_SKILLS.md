# MCP·스킬·서브에이전트 활용 가이드

> 이번 프로젝트에서 **실제 효과 있었던 것** vs **있었으면 좋았을 것** vs
> **우리가 만든 커스텀** 을 정리합니다.

---

## 0. 한 줄 요약

- **이번 노가다의 가장 큰 시간 절약 도구는 "커스텀 스킬"** 이었을 것.
- 시중 MCP들은 게임/시각 작업에 직접 도움 되는 게 거의 없음.
- 슬래시 명령 `/init`, `/run`, `/verify`, `/code-review`는 어디서나 유용.

---

## 1. 실제 효과 있었던 것

### Claude Code 내장 슬래시 명령

| 명령 | 이번 프로젝트에서 효과 |
|---|---|
| `/init` | 사용 안 했지만 첫날 썼으면 CLAUDE.md를 자동 생성받아 함정 회피 가능 |
| `/run` | 게임 실행 자동화 — 우리는 직접 xvfb 명령 짰지만 표준 패턴이면 더 빨랐을 것 |
| `/verify` | "이 수정이 실제로 작동해?" — 시각적 회귀 발견에 좋음 |
| `/code-review` | 큰 변경 (v15 같은) 직전 자기 검토 |
| `/ultrareview` | 마일스톤마다 멀티-에이전트 리뷰. 사용자 트리거 필요 |

### 서브에이전트 (Agent tool)

`Explore` 서브에이전트를 적극적으로 썼다면 좋았던 순간:
- 타일셋에서 잔디·길·집·꽃·돌 좌표 한 번에 다 찾기
- 메인 컨텍스트 더럽히지 않고 결과만 리턴

```
Agent(subagent_type="Explore", 
      description="Find all useful tile coords",
      prompt="이 타일셋에서 (1) 단색 잔디 (2) 갈색 길 (3) 4×3 집들 
              (4) 단일 부쉬 (5) 꽃 좌표를 각각 3개씩 후보로 찾아 
              단독 미리보기 PNG 저장하고 좌표만 보고해줘")
```

이번에는 메인에서 다 했어서 컨텍스트 빨리 차고, 한 번에 못 봐서 시행착오 늘었음.

### 백그라운드 실행 (run_in_background)

게임 빌드/임포트는 백그라운드로 돌릴 수 있는데 우린 항상 동기로 기다림. 
다음엔 임포트 백그라운드 돌리면서 다음 코드 짜는 식.

---

## 2. 도움 됐을 MCP (시중)

### 직접 관련 있는 것

| MCP | 어떤 상황에 |
|---|---|
| **GitHub MCP** | PR/이슈/CI — 우리 이미 적극 사용 |
| **Figma MCP** | UI 디자인이 Figma에 있으면 → 코드 자동 변환. **게임 아트엔 무관**. |
| **Playwright MCP** | HTML5 export 빌드 검증 — 우리 안 함. 웹 배포할 거면 유용 |

### 우리 프로젝트와 무관

대부분의 시중 MCP는 비즈니스 도구(Slack, Notion, DB) 통합용이라 
게임/시각 작업엔 부적합.

### 있으면 좋을 MCP (아직 없는 것)

- **이미지 분석 MCP**: 픽셀 단위로 영역 색상/패턴 분석, 타일셋 자동 인덱싱
- **에셋팩 검색 MCP**: itch.io/OpenGameArt에서 자연어 검색 → CC0 에셋 자동 다운로드
- **게임엔진 컨트롤 MCP**: Godot/Unity 인스턴스 원격 제어 (씬 편집, 노드 추가)

---

## 3. 우리 프로젝트 커스텀 스킬 (`.claude/skills/`)

이번 시행착오에서 만든, 같은 실수 반복 안 하기 위한 3개:

### `/tile-check`
**용도**: 타일 좌표 등록 전 시각 확인 강제  
**막은 함정**:
- "부쉬" (12,11)이 실은 그루터기
- "꽃" (2,9)/(3,9)이 실은 당근
- "해바라기" (3,16)이 실은 복숭아 아이콘

```
/tile-check 3,13
/tile-check 12,16 13,16 14,16   # 후보 3개 비교
/tile-check chunk:4,16,2,2       # 청크
```

### `/village-rebuild`
**용도**: build → import → validate → screenshot 풀 루프 자동화  
**막은 함정**: 4개 명령을 매번 직접 치다 보니 한 단계 빠뜨림

### `/reference-classify`  
**용도**: 사용자가 레퍼런스 이미지 줄 때 분류 + 한계 명시 강제  
**막은 함정**: 4라운드 동안 AI 페인팅 따라잡으려고 헛수고

---

## 4. 워크플로우에 어떻게 박는가

### A. 매 세션 시작
```
1. CLAUDE.md 자동 로드 → 함정 표 + 검증된 좌표 기억남
2. 작업 시작 전 ToolSearch로 필요한 deferred 도구 로드:
   - WebFetch / WebSearch (에셋 검색)
   - GitHub MCP 도구 (PR 작업)
```

### B. 새 시각 작업 받으면
```
1. /reference-classify  ← 레퍼런스 분류 + 한계 합의
2. /tile-check  ← 좌표 후보 검증
3. build_village.py 수정
4. /village-rebuild  ← 전체 루프 자동
5. 결과 확인 → OK면 커밋
```

### C. 막힐 때
```
1. /verify로 정말 작동하는지 명시 검증
2. 진단 → 작은 수정 → /village-rebuild → 확인
3. 1라운드 헛돌면 사용자 진단 요청 (이미지 + 빨간 동그라미)
```

### D. PR 만들 때
```
1. /code-review  ← 자기검토
2. /ultrareview  ← (사용자 트리거) 멀티 에이전트 리뷰
3. PR 본문에 visual diff 첨부 (전/후 스크린샷)
```

---

## 5. 슬래시 명령 자체 만들기

스킬은 `.claude/skills/<name>.md` 파일로 정의하면 끝. 프론트매터에:

```yaml
---
name: my-skill
description: |
  When to invoke (Claude reads this to decide if your skill matches)
allowed-tools: Bash, Read, Edit   # 이 스킬이 호출 가능한 도구
---

# 내용 (Claude가 따를 지침)

1. 단계
2. 단계
```

사용자가 `/my-skill <args>` 입력 시 Claude가 자동 호출.

**팁**: description은 "언제 이걸 쓸지" 명확히 쓰세요. Claude는 이걸 보고 매칭함.

---

## 6. 다른 프로젝트로 옮기는 법

### 게임 프로젝트라면
이 레포의 `.claude/skills/` 폴더를 통째로 복사 후:
1. `tile-check`: 자기 프로젝트 타일셋 경로로 수정
2. `village-rebuild`: 자기 빌드 명령으로 교체
3. `reference-classify`: 그대로 사용 가능

### 일반 코드 프로젝트라면
다음 패턴이 어디서나 유용:
- **검증 자동화 스킬**: 우리의 village-rebuild처럼 "변경→빌드→테스트→스샷" 한 방
- **함정 표 스킬**: CLAUDE.md에 "절대 시도하지 말 것" 추가
- **레퍼런스 분류 스킬**: 시각 작업이라면 거의 동일하게 적용 가능

---

## 7. 솔직한 한계

이번 프로젝트에서 **MCP/스킬로도 해결 안 된** 진짜 문제:

1. **시각적 미세 판단**: "그림이 깨져 보인다" — Claude는 픽셀 단위 차이를 
   사람만큼 정확히 짚지 못함. 결국 사용자 피드백 + 픽셀 확대 보기로 해결.
2. **에셋 한계**: 16×16 chibi로 AI 페인팅 못 만듦 — 어떤 도구로도.
3. **에셋팩 발견**: itch.io 자동 검색 MCP가 없어서 일일이 WebFetch로 시도.

이런 부분은 도구가 발전하기 전까지 사람-AI 협업이 답.

---

## 8. 추천 다음 단계

이 프로젝트에 추가하면 좋을 거:

```bash
# 1. CLAUDE.md (이미 함)
# 2. .claude/skills/  (이미 3개 만듦)
# 3. .claude/settings.json — 도구 허용 목록 (permission prompt 줄임)
```

`.claude/settings.json`은 `/fewer-permission-prompts` 스킬로 자동 생성 가능:

```bash
claude
> /fewer-permission-prompts
```

이번 세션에서 자주 호출한 Bash 명령(`python3 tools/build_village.py`, 
`godot --headless ...`)을 자동 허용 목록에 추가하면 다음 세션에서 
permission 팝업 사라짐.

---

## 마치며

| 핵심 | 이유 |
|---|---|
| **CLAUDE.md** | 매 세션 함정 기억 (자동 로드) |
| **`.claude/skills/`** | 반복 작업 한 명령으로 (3개 만듦) |
| **서브에이전트** | 긴 탐색은 위임해서 컨텍스트 절약 |
| **`/init` `/verify` `/code-review`** | 어디서나 표준 패턴 |

스킬 만드는 데 든 시간 < 같은 명령 10번 반복하는 시간.  
**한 번 만들면 평생 씁니다.**
