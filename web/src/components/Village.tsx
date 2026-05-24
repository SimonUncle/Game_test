import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { usePlayer } from "../store/usePlayer";
import { Character } from "./Character";
import { ChiefHouseMarker } from "./ChiefHouseMarker";
import { DayCycle } from "./DayCycle";
import { CherryPetals } from "./CherryPetals";

const WORLD_W = 1280;
const WORLD_H = 768;
const PLAYER_SPEED = 240; // px/sec

/**
 * Village viewport. World is WORLD_W × WORLD_H. We scale the stage so it
 * fills the viewport (with min-zoom to never show empty area beyond world)
 * and let the camera follow the player when zoom > fit-zoom.
 */
export function Village({ minZoom = 1.4 }: { minZoom?: number }) {
  const { x, y, setPosition, setDirection, setMoving } = usePlayer();
  const keysRef = useRef<Set<string>>(new Set());
  const rafRef = useRef<number | null>(null);
  const lastTimeRef = useRef<number>(performance.now());
  const [viewport, setViewport] = useState({
    w: typeof window === "undefined" ? 1920 : window.innerWidth,
    h: typeof window === "undefined" ? 1080 : window.innerHeight,
  });

  // Track viewport size
  useEffect(() => {
    const onResize = () =>
      setViewport({ w: window.innerWidth, h: window.innerHeight });
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  // Keyboard input
  useEffect(() => {
    const onDown = (e: KeyboardEvent) => {
      const k = e.key.toLowerCase();
      if (
        ["w", "a", "s", "d", "arrowup", "arrowdown", "arrowleft", "arrowright"]
          .includes(k)
      ) {
        keysRef.current.add(k);
        e.preventDefault();
      }
    };
    const onUp = (e: KeyboardEvent) => {
      keysRef.current.delete(e.key.toLowerCase());
    };
    window.addEventListener("keydown", onDown);
    window.addEventListener("keyup", onUp);
    return () => {
      window.removeEventListener("keydown", onDown);
      window.removeEventListener("keyup", onUp);
    };
  }, []);

  // Movement RAF loop
  useEffect(() => {
    const tick = (t: number) => {
      const dt = Math.min(0.05, (t - lastTimeRef.current) / 1000);
      lastTimeRef.current = t;

      const k = keysRef.current;
      const up = k.has("w") || k.has("arrowup");
      const down = k.has("s") || k.has("arrowdown");
      const left = k.has("a") || k.has("arrowleft");
      const right = k.has("d") || k.has("arrowright");

      let dx = 0;
      let dy = 0;
      if (up) dy -= 1;
      if (down) dy += 1;
      if (left) dx -= 1;
      if (right) dx += 1;

      const mag = Math.hypot(dx, dy);
      if (mag > 0) {
        dx /= mag;
        dy /= mag;
        const { x: px, y: py } = usePlayer.getState();
        const nx = Math.max(40, Math.min(WORLD_W - 40, px + dx * PLAYER_SPEED * dt));
        const ny = Math.max(40, Math.min(WORLD_H - 40, py + dy * PLAYER_SPEED * dt));
        setPosition(nx, ny);
        setMoving(true);
        if (Math.abs(dx) > Math.abs(dy)) {
          setDirection(dx < 0 ? "left" : "right");
        } else {
          setDirection(dy < 0 ? "up" : "down");
        }
      } else {
        setMoving(false);
      }

      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
    };
  }, [setPosition, setDirection, setMoving]);

  // Camera math: zoom = max(minZoom, fitZoom) so we never see empty area.
  const fitZoom = Math.max(viewport.w / WORLD_W, viewport.h / WORLD_H);
  const zoom = Math.max(minZoom, fitZoom);

  const halfWWorld = viewport.w / 2 / zoom;
  const halfHWorld = viewport.h / 2 / zoom;
  const camX =
    halfWWorld > WORLD_W / 2
      ? WORLD_W / 2
      : Math.max(halfWWorld, Math.min(WORLD_W - halfWWorld, x));
  const camY =
    halfHWorld > WORLD_H / 2
      ? WORLD_H / 2
      : Math.max(halfHWorld, Math.min(WORLD_H - halfHWorld, y));

  // Translate world so camera point lands at viewport center.
  const tx = -camX * zoom + viewport.w / 2;
  const ty = -camY * zoom + viewport.h / 2;

  return (
    <div className="absolute inset-0 overflow-hidden vignette">
      <div
        style={{
          width: WORLD_W,
          height: WORLD_H,
          transform: `translate(${tx}px, ${ty}px) scale(${zoom})`,
          transformOrigin: "0 0",
          position: "absolute",
          top: 0,
          left: 0,
        }}
      >
        {/* Background image. Drop a higher-quality image at
            public/village_background.png to replace the placeholder. */}
        <img
          src="/village_background.png"
          alt=""
          className="absolute inset-0 w-full h-full select-none pointer-events-none"
          style={{
            imageRendering: "auto",
            filter: "saturate(115%) contrast(105%)",
          }}
          draggable={false}
        />

        {/* Day cycle color overlay (only over the village world) */}
        <DayCycle />

        {/* Cherry petals drift across the foreground */}
        <CherryPetals />

        {/* Chief house marker — sits over the village in world coords */}
        <ChiefHouseMarker x={640} y={400} />

        {/* Player */}
        <motion.div
          className="absolute"
          style={{ left: x, top: y }}
          animate={{ left: x, top: y }}
          transition={{ type: "tween", duration: 0.05, ease: "linear" }}
        >
          <div className="-translate-x-1/2 -translate-y-3/4">
            <Character />
          </div>
        </motion.div>
      </div>
    </div>
  );
}
