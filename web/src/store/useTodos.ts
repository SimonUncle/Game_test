import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface TodoItem {
  id: string;
  text: string;
  done: boolean;
  createdAt: number;
}

interface TodoStore {
  items: TodoItem[];
  add: (text: string) => void;
  toggle: (id: string) => void;
  remove: (id: string) => void;
  clearDone: () => void;
}

export const useTodos = create<TodoStore>()(
  persist(
    (set) => ({
      items: [],

      add: (text: string) => {
        const trimmed = text.trim();
        if (!trimmed) return;
        const id = `${Date.now()}_${Math.floor(Math.random() * 10000)}`;
        set((s) => ({
          items: [
            ...s.items,
            { id, text: trimmed, done: false, createdAt: Date.now() },
          ],
        }));
      },

      toggle: (id: string) =>
        set((s) => ({
          items: s.items.map((it) =>
            it.id === id ? { ...it, done: !it.done } : it,
          ),
        })),

      remove: (id: string) =>
        set((s) => ({
          items: s.items.filter((it) => it.id !== id),
        })),

      clearDone: () =>
        set((s) => ({
          items: s.items.filter((it) => !it.done),
        })),
    }),
    { name: "mongle-todos" },
  ),
);
