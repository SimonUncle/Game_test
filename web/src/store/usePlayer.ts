import { create } from "zustand";

export type Direction = "down" | "up" | "left" | "right";

interface PlayerStore {
  // position in world coords (px). World = 1280×768 (matches background).
  x: number;
  y: number;
  direction: Direction;
  moving: boolean;

  setPosition: (x: number, y: number) => void;
  setDirection: (dir: Direction) => void;
  setMoving: (m: boolean) => void;
}

export const usePlayer = create<PlayerStore>((set) => ({
  x: 640,
  y: 520,
  direction: "down",
  moving: false,

  setPosition: (x, y) => set({ x, y }),
  setDirection: (dir) => set({ direction: dir }),
  setMoving: (m) => set({ moving: m }),
}));
