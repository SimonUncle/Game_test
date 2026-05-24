import { create } from "zustand";
import { persist } from "zustand/middleware";

interface GameStateStore {
  chiefName: string;
  totalCycles: number;
  dayIndex: number;
  unlockedResidents: string[];

  setChiefName: (name: string) => void;
  registerCycle: () => void;
  advanceDay: () => void;
}

export const useGameState = create<GameStateStore>()(
  persist(
    (set) => ({
      chiefName: "EJ",
      totalCycles: 0,
      dayIndex: 0,
      unlockedResidents: [],

      setChiefName: (name: string) => set({ chiefName: name }),
      registerCycle: () => set((s) => ({ totalCycles: s.totalCycles + 1 })),
      advanceDay: () => set((s) => ({ dayIndex: s.dayIndex + 1 })),
    }),
    { name: "mongle-game-state" },
  ),
);
