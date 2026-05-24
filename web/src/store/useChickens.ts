import { create } from "zustand";

export interface ChickenState {
  id: number;
  x: number;
  y: number;
  homeX: number;
  homeY: number;
  targetX: number;
  targetY: number;
  state: "idle" | "walk";
  stateUntil: number;     // ms timestamp when current state ends
  facingLeft: boolean;
  step: 0 | 1;
  stepAccum: number;
}

interface ChickensStore {
  chickens: ChickenState[];
  init: (positions: Array<[number, number]>) => void;
  tick: (dtMs: number) => void;
}

const WANDER_RADIUS = 90;
const SPEED = 18;       // px/sec — slower than player
const IDLE_MIN = 1500;
const IDLE_MAX = 3500;
const WALK_MAX = 5000;

// House rectangles in world coords — must match placements in
// tools/build_village.py. Chickens steer clear of these so they don't
// hop onto roofs. Each house is 64×48 px (4×3 tiles of 16).
const HOUSE_RECTS: Array<[number, number, number, number]> = [
  [128, 96, 192, 144],   // (8, 6) → 8*16=128, 6*16=96
  [288, 80, 352, 128],   // (18, 5)
  [432, 112, 496, 160],  // (27, 7)
  [576, 80, 640, 128],   // (36, 5)
  [752, 96, 816, 144],   // (47, 6)
  [912, 112, 976, 160],  // (57, 7)
  [1072, 80, 1136, 128], // (67, 5)
  [128, 240, 192, 288],  // (8, 15)
  [272, 272, 336, 320],  // (17, 17)
  [896, 256, 960, 304],  // (56, 16)
  [1040, 288, 1104, 336],// (65, 18)
  [112, 448, 176, 496],  // (7, 28)
  [272, 480, 336, 528],  // (17, 30)
  [448, 448, 512, 496],  // (28, 28)
  [608, 480, 672, 528],  // (38, 30)
  [768, 448, 832, 496],  // (48, 28)
  [928, 480, 992, 528],  // (58, 30)
  [1088, 448, 1152, 496],// (68, 28)
];

function clearsHouses(x: number, y: number, margin = 16): boolean {
  for (const [hx0, hy0, hx1, hy1] of HOUSE_RECTS) {
    if (x > hx0 - margin && x < hx1 + margin && y > hy0 - margin && y < hy1 + margin) {
      return false;
    }
  }
  return true;
}

export const useChickens = create<ChickensStore>((set, get) => ({
  chickens: [],

  init: (positions) => {
    const now = performance.now();
    const chickens = positions.map((p, i) => ({
      id: i,
      x: p[0],
      y: p[1],
      homeX: p[0],
      homeY: p[1],
      targetX: p[0],
      targetY: p[1],
      state: "idle" as const,
      stateUntil: now + IDLE_MIN + Math.random() * (IDLE_MAX - IDLE_MIN),
      facingLeft: Math.random() < 0.5,
      step: 0 as 0 | 1,
      stepAccum: 0,
    }));
    set({ chickens });
  },

  tick: (dtMs) => {
    const now = performance.now();
    const dt = dtMs / 1000;
    const next = get().chickens.map((c) => {
      let { x, y, targetX, targetY, state, stateUntil, facingLeft, step, stepAccum } = c;

      if (now >= stateUntil) {
        if (state === "idle") {
          // Pick a new wander target that's not inside a house
          let tries = 0;
          let nx = c.homeX;
          let ny = c.homeY;
          while (tries < 8) {
            const angle = Math.random() * Math.PI * 2;
            const dist = 20 + Math.random() * WANDER_RADIUS;
            nx = c.homeX + Math.cos(angle) * dist;
            ny = c.homeY + Math.sin(angle) * dist;
            if (clearsHouses(nx, ny)) break;
            tries++;
          }
          targetX = nx;
          targetY = ny;
          state = "walk";
          stateUntil = now + WALK_MAX;
        } else {
          state = "idle";
          stateUntil = now + IDLE_MIN + Math.random() * (IDLE_MAX - IDLE_MIN);
        }
      }

      if (state === "walk") {
        const dx = targetX - x;
        const dy = targetY - y;
        const dist = Math.hypot(dx, dy);
        if (dist < 3) {
          state = "idle";
          stateUntil = now + IDLE_MIN + Math.random() * (IDLE_MAX - IDLE_MIN);
        } else {
          const move = Math.min(dist, SPEED * dt);
          x += (dx / dist) * move;
          y += (dy / dist) * move;
          facingLeft = dx < 0;
          stepAccum += dtMs;
          if (stepAccum > 250) {
            step = step === 0 ? 1 : 0;
            stepAccum = 0;
          }
        }
      }

      return { ...c, x, y, targetX, targetY, state, stateUntil, facingLeft, step, stepAccum };
    });
    set({ chickens: next });
  },
}));
