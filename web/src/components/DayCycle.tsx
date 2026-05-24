import { useEffect, useState } from "react";

const CYCLE_DURATION = 120; // seconds for full cycle in demo

const PHASES = [
  { name: "DAWN", tint: "rgba(255, 220, 180, 0.18)", time: "06:00" },
  { name: "NOON", tint: "rgba(255, 255, 255, 0.00)", time: "12:00" },
  { name: "DUSK", tint: "rgba(255, 150, 90, 0.30)", time: "18:00" },
  { name: "NIGHT", tint: "rgba(40, 60, 130, 0.55)", time: "00:00" },
];

export function DayCycle() {
  const [tint, setTint] = useState(PHASES[0].tint);

  useEffect(() => {
    let elapsed = 0;
    let raf: number;
    let last = performance.now();

    const tick = (t: number) => {
      const dt = (t - last) / 1000;
      last = t;
      elapsed = (elapsed + dt) % CYCLE_DURATION;
      const pos = (elapsed / CYCLE_DURATION) * PHASES.length;
      const a = Math.floor(pos) % PHASES.length;
      const b = (a + 1) % PHASES.length;
      const frac = smoothstep(pos - Math.floor(pos));
      setTint(mixColors(PHASES[a].tint, PHASES[b].tint, frac));
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  return <div className="day-tint-layer" style={{ background: tint }} />;
}

function smoothstep(t: number): number {
  return t * t * (3 - 2 * t);
}

// Naive mixer: parses two rgba() strings and interpolates each channel.
function mixColors(a: string, b: string, t: number): string {
  const ca = parseRgba(a);
  const cb = parseRgba(b);
  const r = Math.round(ca[0] + (cb[0] - ca[0]) * t);
  const g = Math.round(ca[1] + (cb[1] - ca[1]) * t);
  const bl = Math.round(ca[2] + (cb[2] - ca[2]) * t);
  const al = ca[3] + (cb[3] - ca[3]) * t;
  return `rgba(${r}, ${g}, ${bl}, ${al.toFixed(3)})`;
}

function parseRgba(s: string): [number, number, number, number] {
  const m = s.match(/rgba?\(([^)]+)\)/);
  if (!m) return [0, 0, 0, 0];
  const parts = m[1].split(",").map((p) => parseFloat(p.trim()));
  return [parts[0] || 0, parts[1] || 0, parts[2] || 0, parts[3] ?? 1];
}
