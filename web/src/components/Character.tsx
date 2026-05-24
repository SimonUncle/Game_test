import { usePlayer } from "../store/usePlayer";

/**
 * Chief character — SVG so it scales cleanly and we can color-tint via CSS.
 * 4 directions × idle/walking, with subtle bob animation when idle.
 *
 * Drawn at 32×40 logical units, scaled up via CSS so it sits well on the
 * 1280×768 village background.
 */
export function Character() {
  const { direction, moving } = usePlayer();

  return (
    <div className={moving ? "" : "animate-bob"}>
      <svg
        viewBox="0 0 32 40"
        width={48}
        height={60}
        className="pixelated drop-shadow-[0_4px_6px_rgba(0,0,0,0.55)]"
        style={{ shapeRendering: "crispEdges" }}
      >
        {/* Shadow under feet */}
        <ellipse cx="16" cy="38" rx="9" ry="2.5" fill="rgba(0,0,0,0.32)" />
        <CharacterBody direction={direction} />
      </svg>
    </div>
  );
}

function CharacterBody({ direction }: { direction: string }) {
  // Skin / hair / shirt / pants palette — warm cozy farmer vibe.
  const skin = "#f1c39d";
  const hair = "#5a3a23";
  const shirt = "#c84d3a";
  const shirtDark = "#9a3328";
  const pants = "#3d4a6a";
  const boots = "#2a1810";
  const eye = "#1a0f0a";

  const facingDown = direction === "down";
  const facingUp = direction === "up";
  const facingLeft = direction === "left";

  // For left, mirror the right-facing pose
  const flipH = facingLeft ? "scale(-1, 1) translate(-32 0)" : "";

  return (
    <g transform={flipH}>
      {/* Hair (back) */}
      <rect x="9" y="8" width="14" height="9" fill={hair} />
      {/* Head */}
      <rect x="10" y="11" width="12" height="9" fill={skin} />
      {/* Hair (top) */}
      <rect x="9" y="8" width="14" height="3" fill={hair} />
      <rect x="10" y="11" width="2" height="2" fill={hair} />
      <rect x="20" y="11" width="2" height="2" fill={hair} />
      {/* Ears */}
      <rect x="9" y="14" width="1" height="2" fill={skin} />
      <rect x="22" y="14" width="1" height="2" fill={skin} />

      {/* Eyes - direction dependent */}
      {facingDown && (
        <>
          <rect x="13" y="15" width="2" height="2" fill={eye} />
          <rect x="17" y="15" width="2" height="2" fill={eye} />
        </>
      )}
      {facingUp && (
        <>
          {/* Back of head — no eyes */}
          <rect x="9" y="11" width="14" height="6" fill={hair} />
        </>
      )}
      {!facingDown && !facingUp && (
        <>
          {/* Side view — single eye */}
          <rect x="18" y="15" width="2" height="2" fill={eye} />
        </>
      )}

      {/* Neck */}
      <rect x="14" y="20" width="4" height="2" fill={skin} />

      {/* Shirt body */}
      <rect x="10" y="22" width="12" height="9" fill={shirt} />
      {/* Shirt highlight + shadow */}
      <rect x="10" y="22" width="12" height="1" fill="#e26d59" />
      <rect x="10" y="30" width="12" height="1" fill={shirtDark} />
      {/* Shirt collar */}
      <rect x="14" y="22" width="4" height="2" fill={shirtDark} />

      {/* Arms */}
      <rect x="8" y="23" width="2" height="7" fill={shirt} />
      <rect x="22" y="23" width="2" height="7" fill={shirt} />
      {/* Hands */}
      <rect x="8" y="29" width="2" height="2" fill={skin} />
      <rect x="22" y="29" width="2" height="2" fill={skin} />

      {/* Pants */}
      <rect x="10" y="31" width="12" height="5" fill={pants} />
      {/* Belt */}
      <rect x="10" y="30" width="12" height="1" fill="#1a1410" />

      {/* Legs / boots */}
      <rect x="11" y="36" width="4" height="2" fill={boots} />
      <rect x="17" y="36" width="4" height="2" fill={boots} />
    </g>
  );
}
