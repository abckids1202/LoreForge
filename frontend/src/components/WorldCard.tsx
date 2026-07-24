import { ArrowRight, LockKeyhole, Palette } from "lucide-react";
import { Link } from "react-router-dom";
import type { World } from "../types";

export default function WorldCard({ world }: { world: World }) {
  return (
    <article className="world-card" style={{ borderTopColor: world.accent_color }}>
      <div className="world-card-head">
        <div>
          <span>{world.genre ?? "Unclassified world"}</span>
          <h2>{world.name}</h2>
        </div>
        <Palette size={19} style={{ color: world.accent_color }} />
      </div>
      <p>{world.premise || world.description || "No premise written yet."}</p>
      <div className="theme-row">
        {(world.themes_json.length ? world.themes_json : ["Private", "Draft"]).slice(0, 4).map((theme) => (
          <span key={theme}>{theme}</span>
        ))}
      </div>
      <div className="world-footer">
        <span>
          <LockKeyhole size={14} />
          {world.default_visibility}
        </span>
        <Link to={`/worlds/${world.id}`}>
          Open
          <ArrowRight size={15} />
        </Link>
      </div>
    </article>
  );
}
