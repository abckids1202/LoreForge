import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuthStore } from "../store/auth";

export default function Login() {
  const navigate = useNavigate();
  const setToken = useAuthStore((state) => state.setToken);
  const [email, setEmail] = useState("demo@loreforge.local");
  const [password, setPassword] = useState("DemoPass123!");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const result = await api.login({ email, password });
      setToken(result.access_token);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to sign in");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={submit}>
      <div>
        <span className="eyebrow">Welcome back</span>
        <h2>Sign in to your archive</h2>
        <p>Use the demo account after running the seed command, or register a fresh owner account.</p>
      </div>
      {error && <div className="form-error">{error}</div>}
      <label>
        Email
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
      </label>
      <label>
        Password
        <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
      </label>
      <button className="primary-button" disabled={loading}>
        {loading ? "Signing in..." : "Sign in"}
      </button>
      <small>
        New to LoreForge? <Link to="/register">Create an owner account</Link>
      </small>
    </form>
  );
}
