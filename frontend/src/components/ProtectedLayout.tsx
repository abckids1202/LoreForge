import { BookOpenText, LayoutDashboard, LogOut, Plus, ScrollText } from "lucide-react";
import { useEffect } from "react";
import { NavLink, Navigate, Outlet, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import { useAuthStore } from "../store/auth";

export default function ProtectedLayout() {
  const token = useAuthStore((state) => state.token);
  const setUser = useAuthStore((state) => state.setUser);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();
  const { data, isError } = useQuery({ queryKey: ["me"], queryFn: api.me, enabled: Boolean(token) });

  useEffect(() => {
    if (data) setUser(data);
  }, [data, setUser]);

  if (!token || isError) return <Navigate to="/login" replace />;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup compact">
          <div className="brand-mark">
            <BookOpenText size={23} />
          </div>
          <div>
            <strong>LoreForge</strong>
            <span>Private world bible</span>
          </div>
        </div>
        <nav className="nav-list">
          <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/worlds" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
            <ScrollText size={18} />
            <span>Worlds</span>
          </NavLink>
        </nav>
        <button className="sidebar-action" onClick={() => navigate("/worlds")}>
          <Plus size={17} />
          New World
        </button>
        <button className="logout-button" onClick={logout}>
          <LogOut size={17} />
          Sign out
        </button>
      </aside>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}
