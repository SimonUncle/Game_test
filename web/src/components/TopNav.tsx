import { motion } from "framer-motion";

interface TopNavProps {
  onAction: (target: string) => void;
}

export function TopNav({ onAction }: TopNavProps) {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="absolute top-0 inset-x-0 z-20 px-6 py-3 flex items-center
                 glass-panel border-b border-cozy-border"
    >
      <nav className="flex items-center gap-6">
        <button onClick={() => onAction("town_info")} className="btn-ghost">
          TOWN INFO
        </button>
        <button onClick={() => onAction("residents")} className="btn-ghost">
          RESIDENTS
        </button>
        <button onClick={() => onAction("settings")} className="btn-ghost">
          SETTINGS
        </button>
      </nav>

      <div className="flex-1 text-center">
        <h1 className="text-cozy-cream/95 text-lg font-bold tracking-[0.3em]">
          몽글마을
        </h1>
      </div>

      <div className="flex items-center gap-3">
        <span className="text-cozy-mute text-sm tracking-widest">GUEST</span>
        <button onClick={() => onAction("login")} className="btn-primary">
          LOGIN
        </button>
      </div>
    </motion.header>
  );
}
