import { motion } from "framer-motion";
import { Sun, Play, Pause, RotateCcw } from "lucide-react";
import { useTimer, formatMmss, phaseLabel } from "../store/useTimer";
import { useGameState } from "../store/useGameState";

export function PomodoroPanel() {
  const state = useTimer((s) => s.state);
  const secondsLeft = useTimer((s) => s.secondsLeft);
  const running = useTimer((s) => s.running);
  const start = useTimer((s) => s.start);
  const reset = useTimer((s) => s.reset);
  const totalCycles = useGameState((s) => s.totalCycles);

  return (
    <motion.div
      initial={{ x: -30, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.45, delay: 0.1 }}
      className="absolute top-20 left-6 z-20 w-[360px] glass-panel-strong rounded-lg p-5"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="w-12 h-12 rounded-md bg-cozy-bg/60 border border-cozy-border
                        flex items-center justify-center">
          <Sun className="text-cozy-accent" size={26} />
        </div>
      </div>

      <div className="display-text text-cozy-cream text-7xl leading-none mb-2 tracking-tight">
        {formatMmss(secondsLeft)}
      </div>

      <div className="text-cozy-mute text-xs tracking-[0.25em] mb-1">
        {phaseLabel(state)}
      </div>

      <div className="text-cozy-mute/80 text-xs tracking-wider mb-4">
        ◔ {totalCycles} CYCLES
      </div>

      <div className="flex gap-2">
        <button
          onClick={start}
          className="btn-primary flex items-center gap-1.5"
        >
          {running ? (
            <>
              <Pause size={14} /> PAUSE
            </>
          ) : (
            <>
              <Play size={14} /> {state === "idle" ? "START" : "RESUME"}
            </>
          )}
        </button>

        <button
          onClick={reset}
          className="px-4 py-2 text-sm uppercase tracking-wider rounded
                     bg-cozy-bg/60 text-cozy-cream/85 border border-cozy-border
                     hover:bg-cozy-bg/80 hover:text-cozy-cream transition-colors
                     flex items-center gap-1.5"
        >
          <RotateCcw size={14} /> RESET
        </button>
      </div>
    </motion.div>
  );
}
