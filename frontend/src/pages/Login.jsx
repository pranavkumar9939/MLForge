import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";
import { Card } from "../components/ui/Primitives";
import Button from "../components/ui/Button";
import "./Auth.css";

function ForgeMark() {
  return (
    <svg width="18" height="18" viewBox="0 0 48 48" fill="none">
      <path d="M12 30h10v6a2 2 0 0 1-2 2h-6a2 2 0 0 1-2-2v-6Z" fill="#f3efe6" />
      <path d="M10 22h16l4 4v2a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2v-6Z" fill="#f3efe6" />
      <path d="M16 22v-3a4 4 0 0 1 4-4h2a4 4 0 0 1 4 4" stroke="#f3efe6" strokeWidth="2.4" strokeLinecap="round" />
      <circle cx="33" cy="14" r="3" fill="#c4501f" />
    </svg>
  );
}

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const redirectTo = location.state?.from?.pathname || "/dashboard";

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await login({ email, password });
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-wrap shell">
      <Card className="auth-card">
        <div className="auth-head">
          <div className="brand-mark"><ForgeMark /></div>
          <h1>Log in to MLForge</h1>
          <p>Pick up where you left off with your datasets and models.</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              className="input"
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              className="input"
              type="password"
              required
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          {error && <div className="auth-error">{error}</div>}

          <Button type="submit" variant="primary" block loading={submitting}>
            Log in
          </Button>
        </form>

        <div className="auth-footer">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </div>
      </Card>
    </main>
  );
}
