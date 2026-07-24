import { BookOpenText } from "lucide-react";
import { Outlet } from "react-router-dom";

export default function AuthLayout() {
  return (
    <main className="auth-page">
      <section className="auth-art">
        <div className="brand-lockup">
          <div className="brand-mark">
            <BookOpenText size={28} />
          </div>
          <div>
            <strong>LoreForge</strong>
            <span>Build worlds, connect lore, and keep your universe consistent.</span>
          </div>
        </div>
        <div className="world-preview">
          <span>The Ashen Meridian</span>
          <h1>A private operating system for fictional universes.</h1>
          <p>Track worlds, canon states, secrets, relationships, timeline foundations, and future consistency checks from one structured workspace.</p>
        </div>
      </section>
      <section className="auth-panel">
        <Outlet />
      </section>
    </main>
  );
}
