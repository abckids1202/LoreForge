import { useQuery } from "@tanstack/react-query";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { AlertTriangle, BookOpenText, Boxes, GitBranch, ScrollText } from "lucide-react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import EntryList from "../components/EntryList";
import MetricCard from "../components/MetricCard";

export default function WorldDashboard() {
  const { worldId = "0" } = useParams();
  const id = Number(worldId);
  const { data, isLoading, error } = useQuery({ queryKey: ["world-dashboard", id], queryFn: () => api.worldDashboard(id), enabled: id > 0 });

  if (isLoading) return <section className="page">Loading world dashboard...</section>;
  if (error || !data) return <section className="page">World not found.</section>;

  const chartData = [
    { name: "Characters", value: data.stats.characters },
    { name: "Factions", value: data.stats.factions },
    { name: "Locations", value: data.stats.locations },
    { name: "Events", value: data.stats.events },
    { name: "Artifacts", value: data.stats.artifacts },
  ];

  return (
    <section className="page">
      <header className="world-hero" style={{ borderColor: data.world.accent_color }}>
        <div>
          <span className="eyebrow">{data.world.genre ?? "World workspace"}</span>
          <h1>{data.world.name}</h1>
          <p>{data.world.premise || "No premise written yet."}</p>
          <div className="theme-row">
            {data.world.themes_json.map((theme) => (
              <span key={theme}>{theme}</span>
            ))}
          </div>
        </div>
      </header>

      <div className="metric-grid">
        <MetricCard label="Entries" value={String(data.stats.total_entries)} hint="Structured lore records" icon={<BookOpenText size={20} />} />
        <MetricCard label="Relationships" value={String(data.stats.relationships)} hint="First-class graph data" icon={<GitBranch size={20} />} />
        <MetricCard label="Drafts" value={String(data.stats.draft_entries)} hint="Needs canon decision" icon={<ScrollText size={20} />} />
        <MetricCard label="Contradictions" value={String(data.stats.open_contradictions)} hint="Manual flags open" icon={<AlertTriangle size={20} />} />
      </div>

      <div className="split-grid">
        <section className="panel">
          <div className="section-heading">
            <h2>Entry distribution</h2>
            <Boxes size={18} />
          </div>
          <div className="chart-panel">
            <ResponsiveContainer width="100%" height={270}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#ddd4c4" />
                <XAxis dataKey="name" tickLine={false} axisLine={false} />
                <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
                <Tooltip />
                <Area type="monotone" dataKey="value" stroke="#6f42c1" fill="#ded0f1" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel">
          <div className="section-heading">
            <h2>Major entries</h2>
            <span>{data.major_entries.length}</span>
          </div>
          <EntryList entries={data.major_entries} emptyText="Major lore entries arrive in Phase 2." />
        </section>
      </div>

      <section className="panel">
        <div className="section-heading">
          <h2>Recently updated</h2>
          <span>{data.recent_entries.length} records</span>
        </div>
        <EntryList entries={data.recent_entries} emptyText="No lore entries yet. Phase 2 adds the lore library and Markdown editor." />
      </section>
    </section>
  );
}
