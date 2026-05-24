import { create } from "zustand";

export interface Notif {
  id: string;
  kind: string;
  title: string;
  body: string;
  createdAt: number;
}

interface NotificationStore {
  current: Notif | null;
  history: Notif[];
  push: (n: Omit<Notif, "id" | "createdAt">) => void;
  dismiss: () => void;
}

export const useNotifications = create<NotificationStore>((set) => ({
  current: {
    id: "welcome",
    kind: "welcome",
    title: "오늘도 힘내세요!",
    body: "하나씩 해나가면 돼요. 몽글마을이 응원합니다.",
    createdAt: Date.now(),
  },
  history: [],

  push: (n) => {
    const notif: Notif = {
      id: `${Date.now()}_${Math.floor(Math.random() * 10000)}`,
      createdAt: Date.now(),
      ...n,
    };
    set((s) => ({
      current: notif,
      history: [notif, ...s.history].slice(0, 20),
    }));
  },

  dismiss: () => set({ current: null }),
}));
