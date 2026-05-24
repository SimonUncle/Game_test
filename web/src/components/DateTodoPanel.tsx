import { motion } from "framer-motion";
import { Plus, X, Check } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useTodos } from "../store/useTodos";

const WEEKDAYS = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

export function DateTodoPanel() {
  const [now, setNow] = useState(() => new Date());
  const items = useTodos((s) => s.items);
  const add = useTodos((s) => s.add);
  const toggle = useTodos((s) => s.toggle);
  const remove = useTodos((s) => s.remove);
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 30_000);
    return () => clearInterval(id);
  }, []);

  const dateStr = `${now.getFullYear()}.${String(now.getMonth() + 1).padStart(
    2,
    "0",
  )}.${String(now.getDate()).padStart(2, "0")}`;
  const weekday = WEEKDAYS[now.getDay()];

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) return;
    add(text);
    setText("");
  };

  return (
    <motion.div
      initial={{ x: 30, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.45, delay: 0.15 }}
      className="absolute top-20 right-6 z-20 w-[320px] glass-panel-strong rounded-lg p-5"
    >
      {/* Date row */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="text-cozy-mute text-xs tracking-widest mb-0.5">
            {dateStr}
          </div>
          <div className="text-cozy-cream text-2xl font-bold tracking-widest">
            {weekday}
          </div>
        </div>
        <button
          onClick={() => inputRef.current?.focus()}
          className="w-10 h-10 rounded bg-cozy-accent/95 text-cozy-bg
                     hover:bg-yellow-300 transition-colors flex items-center
                     justify-center font-bold text-xl"
          aria-label="Add todo"
        >
          <Plus size={20} />
        </button>
      </div>

      {/* Todo input */}
      <form onSubmit={submit} className="mb-3">
        <input
          ref={inputRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="오늘의 할 일을 추가해보세요"
          className="w-full bg-cozy-bg/50 border border-cozy-border rounded
                     px-3 py-2 text-sm text-cozy-cream placeholder:text-cozy-mute/60
                     outline-none focus:border-cozy-accent/60 transition-colors"
        />
      </form>

      {/* Todo list */}
      <div className="space-y-1 max-h-[260px] overflow-y-auto pr-1">
        {items.length === 0 ? (
          <div className="text-cozy-mute/70 text-center text-xs tracking-[0.3em] py-2">
            PRESS + TO ADD
          </div>
        ) : (
          items.map((it) => (
            <div
              key={it.id}
              className="group flex items-center gap-2 px-2 py-1.5 rounded
                         hover:bg-cozy-bg/40 transition-colors"
            >
              <button
                onClick={() => toggle(it.id)}
                className={`w-4 h-4 rounded border flex items-center justify-center
                            transition-colors flex-shrink-0
                            ${it.done
                              ? "bg-cozy-accent/90 border-cozy-accent text-cozy-bg"
                              : "border-cozy-mute/60 hover:border-cozy-cream"}`}
                aria-label="toggle"
              >
                {it.done && <Check size={11} strokeWidth={3} />}
              </button>
              <span
                className={`flex-1 text-sm leading-tight ${
                  it.done
                    ? "line-through text-cozy-mute"
                    : "text-cozy-cream/95"
                }`}
              >
                {it.text}
              </span>
              <button
                onClick={() => remove(it.id)}
                className="text-cozy-mute/40 hover:text-red-400 opacity-0
                           group-hover:opacity-100 transition-opacity"
                aria-label="remove"
              >
                <X size={14} />
              </button>
            </div>
          ))
        )}
      </div>
    </motion.div>
  );
}
