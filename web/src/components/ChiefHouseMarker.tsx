import { useGameState } from "../store/useGameState";

/**
 * Wooden sign post that names the chief's house. Designed to feel like
 * an in-world object (pixel-art wooden plaque + post + dropped shadow)
 * rather than a HUD rectangle floating over the village.
 */
export function ChiefHouseMarker({ x, y }: { x: number; y: number }) {
  const chiefName = useGameState((s) => s.chiefName);
  const initials = getInitials(chiefName);

  return (
    <div
      className="absolute pointer-events-none flex flex-col items-center"
      style={{
        left: x,
        top: y,
        transform: "translate(-50%, -100%)",
      }}
    >
      {/* The plaque */}
      <div
        className="relative flex items-center gap-2 px-3 py-2 rounded-sm"
        style={{
          background: "linear-gradient(180deg, #8a5230 0%, #6b3e22 100%)",
          border: "2px solid #3a1f10",
          boxShadow:
            "inset 0 1px 0 rgba(255,200,140,0.25), 0 4px 0 #2a160a, 0 8px 12px rgba(0,0,0,0.45)",
        }}
      >
        {/* Avatar square */}
        <div
          className="flex items-center justify-center font-bold text-sm"
          style={{
            width: 26,
            height: 26,
            background: "#1a0f08",
            color: "#f5d068",
            border: "1px solid #3a1f10",
            borderRadius: 2,
          }}
        >
          {initials}
        </div>
        <div
          className="text-[10px] font-semibold tracking-wider leading-tight"
          style={{ color: "#f7eccd" }}
        >
          CHIEF<br />HOUSE
        </div>
      </div>

      {/* Wooden post — anchors the sign to the ground */}
      <div className="flex flex-col items-center">
        <div
          style={{
            width: 6,
            height: 14,
            background: "linear-gradient(90deg, #4a2a14 0%, #6b3e22 50%, #4a2a14 100%)",
            borderLeft: "1px solid #2a160a",
            borderRight: "1px solid #2a160a",
          }}
        />
        {/* Ground shadow ellipse */}
        <div
          style={{
            width: 32,
            height: 6,
            marginTop: -2,
            borderRadius: "50%",
            background:
              "radial-gradient(ellipse at center, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 70%)",
          }}
        />
      </div>
    </div>
  );
}

function getInitials(name: string): string {
  const trimmed = name.trim();
  if (!trimmed) return "?";
  const parts = trimmed.split(/\s+/);
  if (parts.length >= 2) return (parts[0][0] + parts[1][0]).toUpperCase();
  return trimmed.slice(0, 2).toUpperCase();
}
