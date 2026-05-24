import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";

export interface DialogContent {
  title: string;
  body: string;
}

interface InfoDialogProps {
  content: DialogContent | null;
  onClose: () => void;
}

export function InfoDialog({ content, onClose }: InfoDialogProps) {
  return (
    <AnimatePresence>
      {content && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 z-30 flex items-center justify-center"
          onClick={onClose}
        >
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />
          <motion.div
            initial={{ scale: 0.95, y: 10 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.95, y: 10 }}
            transition={{ duration: 0.2 }}
            className="relative glass-panel-strong rounded-xl p-6 max-w-md w-full mx-4"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={onClose}
              className="absolute top-3 right-3 text-cozy-mute hover:text-cozy-cream"
            >
              <X size={18} />
            </button>
            <h2 className="text-cozy-cream font-bold text-xl mb-3 tracking-wide">
              {content.title}
            </h2>
            <p className="text-cozy-cream/85 leading-relaxed">
              {content.body}
            </p>
            <button
              onClick={onClose}
              className="btn-primary mt-5"
            >
              확인
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
