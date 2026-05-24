import { AnimatePresence, motion } from "framer-motion";
import { Bell, X } from "lucide-react";
import { useEffect } from "react";
import { useNotifications } from "../store/useNotifications";

export function NotificationPanel() {
  const current = useNotifications((s) => s.current);
  const dismiss = useNotifications((s) => s.dismiss);

  // Auto-dismiss after 8s
  useEffect(() => {
    if (!current) return;
    const t = setTimeout(() => dismiss(), 8000);
    return () => clearTimeout(t);
  }, [current, dismiss]);

  return (
    <AnimatePresence>
      {current && (
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: 30, opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="absolute bottom-6 right-6 z-20 w-[360px]
                     glass-panel-strong rounded-lg p-4"
        >
          <div className="flex items-center gap-2 mb-2">
            <Bell size={14} className="text-cozy-accent" />
            <span className="text-cozy-cream/85 text-xs tracking-wider">알림</span>
            <div className="flex-1" />
            <button
              onClick={dismiss}
              className="text-cozy-mute/60 hover:text-cozy-cream"
            >
              <X size={14} />
            </button>
          </div>

          <div className="text-cozy-cream font-semibold mb-1 text-[15px]">
            {current.title}
          </div>
          <div className="text-cozy-cream/75 text-sm leading-snug">
            {current.body}
          </div>

          <div className="flex items-center justify-between mt-3 pt-2
                          border-t border-cozy-border">
            <span className="text-cozy-mute/70 text-[10px] tracking-wider">
              몽글마을 주민회
            </span>
            <span className="text-cozy-mute/70 text-[10px]">방금 전</span>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
