import { useEffect, useRef } from "react";
import { useChickens } from "../store/useChickens";
import { Chicken } from "./Chicken";

/**
 * Spawns a handful of wandering chickens in the village and runs the
 * AI tick on every animation frame. Each chicken renders at its own
 * world position so it sits with the player/buildings in the camera's
 * transform.
 */
// Spawn in open grass — between houses, away from path crossings.
const SPAWN_POINTS: Array<[number, number]> = [
  [240, 200],   // NW open area
  [880, 200],   // NE open
  [240, 580],   // SW
  [1180, 600],  // SE
  [560, 660],   // south of plaza
];

export function ChickenSwarm() {
  const chickens = useChickens((s) => s.chickens);
  const init = useChickens((s) => s.init);
  const tick = useChickens((s) => s.tick);
  const rafRef = useRef<number | null>(null);
  const lastRef = useRef<number>(performance.now());

  useEffect(() => {
    init(SPAWN_POINTS);
  }, [init]);

  useEffect(() => {
    const loop = (t: number) => {
      const dt = Math.min(60, t - lastRef.current);
      lastRef.current = t;
      tick(dt);
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, [tick]);

  return (
    <>
      {chickens.map((c) => (
        <div
          key={c.id}
          className="absolute"
          style={{
            left: c.x,
            top: c.y,
            transform: "translate(-50%, -75%)",
          }}
        >
          <Chicken flipped={c.facingLeft} step={c.step} />
        </div>
      ))}
    </>
  );
}
