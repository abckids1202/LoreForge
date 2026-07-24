import { create } from "zustand";
import type { User } from "../types";

interface AuthState {
  token: string | null;
  user: User | null;
  setToken: (token: string | null) => void;
  setUser: (user: User | null) => void;
  logout: () => void;
}

const storedToken = localStorage.getItem("loreforge_token");

export const useAuthStore = create<AuthState>((set) => ({
  token: storedToken,
  user: null,
  setToken: (token) => {
    if (token) {
      localStorage.setItem("loreforge_token", token);
    } else {
      localStorage.removeItem("loreforge_token");
    }
    set({ token });
  },
  setUser: (user) => set({ user }),
  logout: () => {
    localStorage.removeItem("loreforge_token");
    set({ token: null, user: null });
  },
}));
