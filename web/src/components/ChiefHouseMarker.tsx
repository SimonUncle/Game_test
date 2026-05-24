import { useGameState } from "../store/useGameState";

export function ChiefHouseMarker({ x, y }: { x: number; y: number }) {
  const chiefName = useGameState((s) => s.chiefName);
  const initials = getInitials(chiefName);

  return (
    <div
      className="absolute -translate-x-1/2 -translate-y-full pointer-events-none"
      style={{ left: x, top: y }}
    >
      <div className="bg-[#6b3e22] border-2 border-[#3d2110] rounded-md px-3 py-3 shadow-2xl flex flex-col items-center gap-1 min-w-[88px]">
        <div className="bg-[#1a0f08] text-cozy-cream font-bold text-xl w-12 h-12 flex items-center justify-center rounded-sm">
          {initials}
        </div>
        <div className="text-cozy-cream/95 text-[10px] font-semibold tracking-wider text-center leading-tight">
          CHIEF<br />HOUSE
        </div>
      </div>
    </div>
  );
}

function getInitials(name: string): string {
  const trimmed = name.trim();
  if (!trimmed) return "?";
  const parts = trimmed.split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return trimmed.slice(0, 2).toUpperCase();
}
