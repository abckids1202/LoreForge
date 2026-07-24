import type { RecentEntry } from "../types";

export default function EntryList({ entries, emptyText }: { entries: RecentEntry[]; emptyText: string }) {
  if (!entries.length) return <p className="muted">{emptyText}</p>;
  return (
    <div className="entry-list">
      {entries.map((entry) => (
        <article className="entry-row" key={entry.id}>
          <div>
            <strong>{entry.title}</strong>
            <span>{entry.entry_type.replace("_", " ")}</span>
          </div>
          <div className="badge-row">
            <span className="badge">{entry.status}</span>
            <span className="badge quiet">{entry.importance_level}</span>
          </div>
        </article>
      ))}
    </div>
  );
}
