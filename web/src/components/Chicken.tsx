/**
 * Cute SVG chicken. Drawn at 20×16 logical units. Walking animation
 * driven by a `step` boolean that flips every ~250ms (alternating leg
 * positions).
 */
interface ChickenProps {
  flipped?: boolean;     // facing left if true
  step?: 0 | 1;          // walk frame
}

export function Chicken({ flipped = false, step = 0 }: ChickenProps) {
  const bodyShadowY = 14;

  return (
    <svg
      viewBox="0 0 20 18"
      width={36}
      height={32}
      className="drop-shadow-[0_2px_3px_rgba(0,0,0,0.45)]"
      style={{
        shapeRendering: "crispEdges",
        transform: flipped ? "scaleX(-1)" : undefined,
      }}
    >
      {/* Ground shadow */}
      <ellipse cx="10" cy={bodyShadowY + 2} rx="6" ry="1.5"
               fill="rgba(0,0,0,0.32)" />

      {/* Body — round white blob */}
      <ellipse cx="9" cy="9" rx="6" ry="5" fill="#f5f5f0" />
      <ellipse cx="9" cy="10" rx="6" ry="4" fill="#eaeae0" />

      {/* Head — slightly smaller blob on top-right */}
      <ellipse cx="14" cy="6" rx="3" ry="2.6" fill="#f5f5f0" />

      {/* Eye */}
      <rect x="14" y="5" width="1" height="1" fill="#1a1410" />

      {/* Beak */}
      <polygon points="16,6 18,6 16,7" fill="#f5a623" />

      {/* Comb (red) */}
      <rect x="13" y="3" width="1" height="1" fill="#c54a3a" />
      <rect x="14" y="3" width="1" height="1.2" fill="#c54a3a" />

      {/* Legs (animated) */}
      {step === 0 ? (
        <>
          <line x1="7" y1="13" x2="6" y2="15" stroke="#f5a623" strokeWidth="0.8" />
          <line x1="11" y1="13" x2="12" y2="15" stroke="#f5a623" strokeWidth="0.8" />
        </>
      ) : (
        <>
          <line x1="7" y1="13" x2="8" y2="15" stroke="#f5a623" strokeWidth="0.8" />
          <line x1="11" y1="13" x2="10" y2="15" stroke="#f5a623" strokeWidth="0.8" />
        </>
      )}
    </svg>
  );
}
