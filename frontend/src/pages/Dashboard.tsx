import { useQuery } from "@tanstack/react-query";
import { BookMarked, GitBranch, LibraryBig, Plus, ShieldAlert } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import MetricCard from "../components/MetricCard";
import WorldCard from "../components/WorldCard";
import { useAuthStore } from "../store/auth";

export default function Dashboard() {
  const navigate = useNavigate();
  const user = useAuthStore((state) => state.user);
  const { data: worlds = [], isLoading } = useQuery({ queryKey: ["worlds"], queryFn: api.worlds });

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">Owner workspace</span>
          <h1>{user ? `${user.display_name}'s worlds` : "World dashboard"}</h1>
        </div>
        <button className="primary-button" onClick={() => navigate("/worlds")}>
          <Plus size={18} />
          Create World
        </button>
      </header>

      <div className="metric-grid">
        <MetricCard label="Worlds" value={String(worlds.length)} hint="Private creative spaces" icon={<LibraryBig size={20} />} />
        <MetricCard label="Canon posture" value="Private" hint="No public publishing in MVP" icon={<BookMarked size={20} />} />
        <MetricCard label="Relationship model" value="Ready" hint="Phase 4 foundation tables" icon={<GitBranch size={20} />} />
        <MetricCard label="Contradictions" value="Manual" hint="AI checks remain opt-in later" icon={<ShieldAlert size={20} />} />
      </div>

      <section className="panel">
        <div className="section-heading">
          <h2>World library</h2>
          <span>{isLoading ? "Loading..." : `${worlds.length} worlds`}</span>
        </div>
        {worlds.length === 0 ? (
          <div className="empty-state">
            <h3>No worlds yet</h3>
            <p>Create your first world workspace to begin tracking premise, themes, canon, and future lore entries.</p>
            <button className="primary-button" onClick={() => navigate("/worlds")}>
              <Plus size={18} />
              New World
            </button>
          </div>
        ) : (
          <div className="world-grid">
            {worlds.map((world) => (
              <WorldCard key={world.id} world={world} />
            ))}
          </div>
        )}
      </section>
    </section>
  );
}
