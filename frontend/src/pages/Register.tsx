import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api/client";
import { useAuthStore } from "../store/auth";

export default function Register() {
  const navigate = useNavigate();
  const setToken = useAuthStore((state) => state.setToken);
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      setLoading(false);
      return;
    }
    try {
      const cleanEmail = email.trim();
      await api.register({ email: cleanEmail, password, display_name: displayName.trim() });
      const result = await api.login({ email: cleanEmail, password });
      setToken(result.access_token);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to register");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form className="auth-form" onSubmit={submit}>
      <div>
        <span className="eyebrow">Create owner account</span>
        <h2>Start a private world bible</h2>
        <p>Your worlds are private by default and owned by your account.</p>
      </div>
      {error && <div className="form-error">{error}</div>}
      <label>
        Display name
        <input value={displayName} onChange={(event) => setDisplayName(event.target.value)} required minLength={2} />
      </label>
      <label>
        Email
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
      </label>
      <label>
        Password
        <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required minLength={8} autoComplete="new-password" />
      </label>
      <label>
        Re-enter password
        <input
          type="password"
          value={confirmPassword}
          onChange={(event) => setConfirmPassword(event.target.value)}
          required
          minLength={8}
          autoComplete="new-password"
        />
      </label>
      <button className="primary-button" disabled={loading}>
        {loading ? "Creating..." : "Create account"}
      </button>
      <small>
        Already have an account? <Link to="/login">Sign in</Link>
      </small>
    </form>
  );
}
