import { useCallback, useEffect, useState } from "react";
import { Village } from "./components/Village";
import { TopNav } from "./components/TopNav";
import { PomodoroPanel } from "./components/PomodoroPanel";
import { DateTodoPanel } from "./components/DateTodoPanel";
import { NotificationPanel } from "./components/NotificationPanel";
import { InfoDialog, type DialogContent } from "./components/InfoDialog";
import { useTimer } from "./store/useTimer";
import { useGameState } from "./store/useGameState";

export default function App() {
  const [dialog, setDialog] = useState<DialogContent | null>(null);
  const start = useTimer((s) => s.start);
  const totalCycles = useGameState((s) => s.totalCycles);
  const unlocked = useGameState((s) => s.unlockedResidents);

  const onNav = useCallback(
    (target: string) => {
      switch (target) {
        case "town_info":
          setDialog({
            title: "마을 정보",
            body: `몽글마을 — 지금까지 ${totalCycles}번의 집중 사이클이 쌓였어요.`,
          });
          break;
        case "residents":
          setDialog({
            title: "주민들",
            body: `현재 주민 ${unlocked.length}명. 집중 사이클을 완료할수록 한 명씩 이사 옵니다.`,
          });
          break;
        case "settings":
          setDialog({
            title: "설정",
            body: "환경 설정 화면은 곧 추가될 예정이에요.",
          });
          break;
        case "login":
          setDialog({
            title: "로그인",
            body: "현재 게스트로 플레이 중이에요. 계정 기능은 곧 추가됩니다.",
          });
          break;
      }
    },
    [totalCycles, unlocked.length],
  );

  // Esc starts/pauses focus timer (matches Godot version)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        if (dialog) {
          setDialog(null);
        } else {
          start();
        }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [start, dialog]);

  return (
    <main className="relative w-screen h-screen overflow-hidden bg-cozy-bg">
      <Village minZoom={1.4} />

      <TopNav onAction={onNav} />
      <PomodoroPanel />
      <DateTodoPanel />
      <NotificationPanel />

      <InfoDialog content={dialog} onClose={() => setDialog(null)} />

      {/* Hint footer */}
      <div className="absolute bottom-3 left-1/2 -translate-x-1/2 z-10
                      text-cozy-mute/65 text-xs tracking-wider
                      pointer-events-none select-none">
        WASD / 방향키 — 이동 · ESC — 타이머
      </div>
    </main>
  );
}
