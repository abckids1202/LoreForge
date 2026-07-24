import { useAuthStore } from "../store/auth";
import type { User, World, WorldDashboard } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = useAuthStore.getState().token;
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers ?? {}),
    },
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Request failed" }));
    if (typeof body.detail === "string") {
      throw new Error(body.detail);
    }
    if (Array.isArray(body.detail)) {
      const message = body.detail
        .map((item: { loc?: string[]; msg?: string }) => {
          const field = item.loc?.filter((part) => part !== "body").join(".");
          return field ? `${field}: ${item.msg}` : item.msg;
        })
        .filter(Boolean)
        .join(" ");
      throw new Error(message || "Request failed");
    }
    throw new Error("Request failed");
  }
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export const api = {
  register: (payload: { email: string; password: string; display_name: string }) =>
    request<User>("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  login: (payload: { email: string; password: string }) =>
    request<{ access_token: string; token_type: string }>("/auth/login", { method: "POST", body: JSON.stringify(payload) }),
  me: () => request<User>("/auth/me"),
  worlds: () => request<World[]>("/worlds"),
  createWorld: (payload: Partial<World> & { name: string }) => request<World>("/worlds", { method: "POST", body: JSON.stringify(payload) }),
  worldDashboard: (worldId: number) => request<WorldDashboard>(`/worlds/${worldId}/dashboard`),
};
