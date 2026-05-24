# 🎮 몽글마을 실행 가이드

총 소요시간: **약 5분** (Godot 다운로드 포함)

---

## 1단계 — Godot 4 다운로드

브라우저에서 https://godotengine.org/download 열기

| OS | 받을 파일 | 크기 |
|---|---|---|
| **Windows** | `Godot_v4.3-stable_win64.exe.zip` | ~70MB |
| **macOS** | `Godot_v4.3-stable_macos.universal.zip` | ~90MB |
| **Linux** | `Godot_v4.3-stable_linux.x86_64.zip` | ~65MB |

> **중요:** "**Godot Engine**" (Standard) 받으세요. ".NET" 버전 말고.

ZIP 풀면 단일 실행파일 하나만 나옵니다. **설치 필요 없음.**

---

## 2단계 — 프로젝트 받기

이 레포를 컴퓨터로 클론:

```bash
git clone https://github.com/simonuncle/game_test.git
cd game_test
git checkout claude/wizardly-dijkstra-FjX9G
```

또는 GitHub 페이지에서 **Code → Download ZIP**으로 받아 푸셔도 됩니다.

---

## 3단계 — 프로젝트 열기

1. Godot 실행 (방금 받은 그 파일 더블클릭)
2. Project Manager가 열림 → **Import** 버튼
3. 방금 클론한 `Game_test` 폴더 안의 `project.godot` 선택
4. **Import & Edit** 클릭
5. 에디터가 뜨면 잠시 기다림 (에셋 임포트 ~5초)

---

## 4단계 — 실행

### 가장 빠른 방법
오른쪽 위 **▶ (Play) 버튼** 클릭. 또는 키보드 **F5**.

처음 실행 시 메인 씬을 물어보면 → `scenes/main.tscn` 선택.

### 빌드해서 친구한테 줄 거면
**Project → Export**:
1. **Add...** → Windows Desktop (또는 Mac/Linux/Web)
2. 첫 번째일 경우 "**Manage Export Templates**" → Download (~600MB, 한 번만)
3. **Export Project** → 저장 경로 지정
4. 결과: 더블클릭만 하면 실행되는 단일 파일

---

## 5단계 — 조작법

| 키 | 동작 |
|---|---|
| **W A S D** 또는 **방향키** | 캐릭터 이동 |
| **Space** | 집/NPC 앞에서 상호작용 (다이얼로그) |
| **Esc** | 포모도로 타이머 시작 / 일시정지 |
| 마우스로 화면 위쪽 **+ 버튼** | 투두 입력창 포커스 |
| **▶ START** | 25분 집중 타이머 시작 |
| 화면 자동 변화 | 90초마다 새벽/낮/노을/밤 사이클 |

---

## 🐛 안 되면

| 증상 | 해결 |
|---|---|
| Godot이 안 열림 | 다운받은 ZIP을 풀었는지 확인. 그냥 압축 안 풀고 실행하면 안 됨. |
| "Main scene not defined" 에러 | F5 누른 직후 팝업에서 `scenes/main.tscn` 선택 |
| 화면이 회색 / 까만색 | Godot 버전 확인. 4.3 이상 필요. 4.1/4.2면 에러 가능 |
| 한글 안 보임 | Korean 폰트가 시스템에 있어야 함. Windows/Mac은 기본 OK. Linux는 `sudo apt install fonts-noto-cjk` |
| 캐릭터가 안 보임 | 화면 한가운데 EJ 마커 위로 살짝 위쪽 봐보기. zoom 2.5x라 작음. |

---

## 📦 프로젝트 구조 (참고)

```
project.godot              ← 첫 실행시 이 파일 선택
scenes/main.tscn           ← 시작 씬
scenes/player.tscn         ← 캐릭터
scenes/ui/                 ← HUD 패널들
scripts/                   ← 로직 (GDScript)
scripts/autoload/          ← 전역 싱글톤 (타이머/투두/저장)
assets/sparklin/           ← CC0 픽셀아트 (Pixel-boy 제작)
assets/sprites/            ← 합성된 마을 배경
tools/build_village.py     ← 마을 배경 PNG 합성 스크립트
tools/screenshot.tscn      ← 헤드리스 스크린샷용
```

---

## 🔄 마을 배경 다시 만들기

마을 PNG는 `tools/build_village.py`로 합성됩니다.
이 파일 수정하면 마을 모양이 바뀝니다.

```bash
# Python 3 + Pillow 필요
pip install Pillow
python3 tools/build_village.py
# → assets/sprites/village_background.png 갱신됨
```

Godot 에디터 다시 열면 자동 임포트됩니다.
