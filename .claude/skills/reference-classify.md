---
name: reference-classify
description: |
  When the user attaches a reference image for the visual look,
  classify it and set realistic expectations BEFORE writing code.
  This is the single highest-leverage skill — we wasted 4 iteration
  rounds in this project trying to match an AI-painted reference
  with 16×16 chibi sprites before classifying it.
allowed-tools: Read
---

# Reference image classifier

User attached an image as a visual target. Don't start building yet.
First, classify the reference into one of three buckets and tell the
user what's achievable.

## Classify into

### Type A: Actual game screenshot
**Signs**: visible UI elements, tile-aligned art, consistent pixel
density across the whole image, sprite seams sometimes visible at
high zoom, characters/objects clearly separable.

**Verdict**: 80–95% achievable. Find the same or similar asset pack
(check itch.io, OpenGameArt, Kenney) and we can build a close match.

### Type B: AI-painted concept art / Midjourney / DALL-E
**Signs**: smooth gradients between objects, soft brush-like edges,
inconsistent rules (some objects have shadows, others don't),
"painterly" texture, dimensional shading on every leaf/roof tile,
objects don't tile-align — they organically merge.

**Verdict**: NOT achievable with low-res pixel art. The painted
look comes from per-pixel hand-shading at high resolution
(~256×256 per object). 16×16 chibi tiles will never reproduce it.

**What to do**: tell the user explicitly. Offer three real paths:
1. Use the reference image AS the literal background (slap it on)
2. Find premium 32×32 or 48×48 asset pack ($5–50)
3. Accept that pixel style has its own charm and aim for Stardew-like

### Type C: Hand-drawn illustration
**Signs**: visible pen strokes, simple cel shading, anime-like
character proportions, soft pastel palette, no UI suggestion.

**Verdict**: Partially achievable. Color palette and composition
transfer, but the line work doesn't.

## What to say to the user

Speak in plain Korean (or the user's language). Pick one of:

> 이건 [A형: 게임 스샷]이에요. 우리 에셋팩 X로 90% 가까이 만들 수 있어요.
> 시작할게요.

> 이건 [B형: AI 페인팅]이에요. 픽셀 게임으로는 100% 매칭이 물리적으로
> 불가능합니다. 어느 방향 가실래요?
>   (A) 이 그림 통째로 배경
>   (B) 유료 에셋팩 ($)
>   (C) 픽셀 스타일 그대로 가서 70% 정도 매칭

> 이건 [C형: 일러스트]에요. 색감/구도는 참고 가능하지만 라인은 못 따라가요.

## Why this exists

In this project's first 4 rounds we tried to procedurally render a
painted-style village in Python+PIL because nobody classified the
reference. Hours wasted. This skill prevents that.
