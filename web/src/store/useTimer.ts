import { create } from "zustand";
import { useNotifications } from "./useNotifications";
import { useGameState } from "./useGameState";

export type TimerState = "idle" | "focus" | "break_short" | "break_long";

const FOCUS_DURATION = 25 * 60;
const SHORT_BREAK = 5 * 60;
const LONG_BREAK = 15 * 60;
const LONG_BREAK_EVERY = 4;

interface TimerStore {
  state: TimerState;
  secondsLeft: number;
  cyclesInSet: number;
  running: boolean;
  intervalId: number | null;

  start: () => void;
  pause: () => void;
  reset: () => void;
  tick: () => void;
}

export const useTimer = create<TimerStore>((set, get) => ({
  state: "idle",
  secondsLeft: FOCUS_DURATION,
  cyclesInSet: 0,
  running: false,
  intervalId: null,

  start: () => {
    const { state, running, intervalId } = get();
    if (running) {
      get().pause();
      return;
    }

    // Resume or start fresh focus
    if (state === "idle") {
      set({ state: "focus", secondsLeft: FOCUS_DURATION });
    }

    if (intervalId !== null) window.clearInterval(intervalId);
    const id = window.setInterval(() => get().tick(), 1000);
    set({ running: true, intervalId: id });
  },

  pause: () => {
    const { intervalId } = get();
    if (intervalId !== null) window.clearInterval(intervalId);
    set({ running: false, intervalId: null });
  },

  reset: () => {
    const { intervalId } = get();
    if (intervalId !== null) window.clearInterval(intervalId);
    set({
      state: "idle",
      secondsLeft: FOCUS_DURATION,
      running: false,
      intervalId: null,
    });
  },

  tick: () => {
    const { secondsLeft, state, cyclesInSet } = get();
    const next = secondsLeft - 1;

    if (next > 0) {
      set({ secondsLeft: next });
      return;
    }

    // Phase ended — advance state machine
    if (state === "focus") {
      const newCycles = cyclesInSet + 1;
      useGameState.getState().registerCycle();
      useNotifications.getState().push({
        title: "집중 완료!",
        body: "한 사이클 끝냈어요. 잠시 쉬어가요 🌿",
        kind: "focus_done",
      });
      const isLong = newCycles % LONG_BREAK_EVERY === 0;
      set({
        state: isLong ? "break_long" : "break_short",
        secondsLeft: isLong ? LONG_BREAK : SHORT_BREAK,
        cyclesInSet: newCycles,
      });
    } else if (state === "break_short" || state === "break_long") {
      useNotifications.getState().push({
        title: "휴식 끝",
        body: "다시 시작할 준비 됐어요. 몽글마을이 응원해요.",
        kind: "break_done",
      });
      get().reset();
    }
  },
}));

export function formatMmss(secs: number): string {
  const m = Math.floor(secs / 60);
  const s = secs % 60;
  return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

export function phaseLabel(state: TimerState): string {
  switch (state) {
    case "focus":
      return "<<  FOCUS TIME  >>";
    case "break_short":
      return "<<  SHORT BREAK  >>";
    case "break_long":
      return "<<  LONG BREAK  >>";
    default:
      return "<<  FOCUS TIME  >>";
  }
}
