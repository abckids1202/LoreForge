import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { api } from "../api/client";
import WorldCard from "../components/WorldCard";

export default function Worlds() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { data: worlds = [] } = useQuery({ queryKey: ["worlds"], queryFn: api.worlds });
  const [name, setName] = useState("The Ashen Meridian");
  const [genre, setGenre] = useState("Dark Fantasy");
  const [tone, setTone] = useState("Tragic, political, mythic");
  const [premise, setPremise] = useState("A continent where the sun died once, and every nation claims to be the rightful heir of its light.");
  const [themes, setThemes] = useState("Power, Faith, Memory, Inheritance, Decay");

  const mutation = useMutation({
    mutationFn: api.createWorld,
    onSuccess: (world) => {
      queryClient.invalidateQueries({ queryKey: ["worlds"] });
      navigate(`/worlds/${world.id}`);
    },
  });

  function submit(event: React.FormEvent) {
    event.preventDefault();
    mutation.mutate({
      name,
      genre,
      tone,
      premise,
      themes_json: themes
        .split(",")
        .map((theme) => theme.trim())
        .filter(Boolean),
      default_visibility: "PRIVATE",
      accent_color: "#6f42c1",
      calendar_mode: "YEAR_BASED",
    });
  }

  return (
    <section className="page">
      <header className="page-header">
        <div>
          <span className="eyebrow">World CRUD</span>
          <h1>Create and manage worlds</h1>
        </div>
      </header>
      <div className="split-grid">
        <form className="panel form-stack" onSubmit={submit}>
          <div className="section-heading">
            <h2>New world</h2>
            <Plus size={18} />
          </div>
          {mutation.error && <div className="form-error">{mutation.error.message}</div>}
          <label>
            Name
            <input value={name} onChange={(event) => setName(event.target.value)} required />
          </label>
          <label>
            Genre
            <input value={genre} onChange={(event) => setGenre(event.target.value)} />
          </label>
          <label>
            Tone
            <input value={tone} onChange={(event) => setTone(event.target.value)} />
          </label>
          <label>
            Themes
            <input value={themes} onChange={(event) => setThemes(event.target.value)} />
          </label>
          <label>
            Premise
            <textarea value={premise} onChange={(event) => setPremise(event.target.value)} rows={5} />
          </label>
          <button className="primary-button" disabled={mutation.isPending}>
            {mutation.isPending ? "Creating..." : "Create World"}
          </button>
        </form>

        <section className="panel">
          <div className="section-heading">
            <h2>Existing worlds</h2>
            <span>{worlds.length}</span>
          </div>
          <div className="world-list">
            {worlds.length ? worlds.map((world) => <WorldCard key={world.id} world={world} />) : <p className="muted">No worlds created yet.</p>}
          </div>
        </section>
      </div>
    </section>
  );
}
