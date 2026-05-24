import { useMemo } from "react";

/** Drifting cherry blossom petals across the world. Pure CSS animation. */
export function CherryPetals({ count = 18 }: { count?: number }) {
  const petals = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => ({
        left: `${(i * 73) % 100}%`,
        delay: `${(i * 0.7) % 12}s`,
        duration: `${10 + (i * 1.3) % 8}s`,
        scale: 0.5 + ((i * 13) % 100) / 200,
      })),
    [count],
  );

  return (
    <>
      {petals.map((p, i) => (
        <div
          key={i}
          className="petal"
          style={{
            left: p.left,
            animationDelay: p.delay,
            animationDuration: p.duration,
            transform: `scale(${p.scale})`,
          }}
        />
      ))}
    </>
  );
}
