import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/useAuth";
import "./AppShell.css";

function ForgeMark() {
  return (
    <svg width="16" height="16" viewBox="0 0 48 48" fill="none">
      <path d="M12 30h10v6a2 2 0 0 1-2 2h-6a2 2 0 0 1-2-2v-6Z" fill="#f3efe6" />
      <path d="M10 22h16l4 4v2a2 2 0 0 1-2 2H12a2 2 0 0 1-2-2v-6Z" fill="#f3efe6" />
      <path
        d="M16 22v-3a4 4 0 0 1 4-4h2a4 4 0 0 1 4 4"
        stroke="#f3efe6"
        strokeWidth="2.4"
        strokeLinecap="round"
      />
      <circle cx="33" cy="14" r="3" fill="#c4501f" />
    </svg>
  );
}

export function TopNav() {
  const { user, logout, isAuthenticated } = useAuth();

  return (
    <header className="nav">
      <div className="shell nav-inner">
        <NavLink to="/" className="brand">
          <span className="brand-mark">
            <ForgeMark />
          </span>
          <span className="brand-name">
            ML<span>Forge</span>
          </span>
        </NavLink>

        <nav className="nav-links">
          {isAuthenticated && (
            <>
              <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                Dashboard
              </NavLink>
              <NavLink to="/upload" className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}>
                New Experiment
              </NavLink>
            </>
          )}
        </nav>

        {isAuthenticated ? (
          <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
            <span style={{ color: "var(--text-on-inverse-dim)", fontSize: 13 }}>{user?.name}</span>
            <button className="nav-cta" style={{ background: "transparent", border: "1px solid var(--border-inverse)" }} onClick={logout}>
              Log out
            </button>
          </div>
        ) : (
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <NavLink to="/login" className="nav-link">Log in</NavLink>
            <NavLink to="/signup" className="nav-cta">Sign up</NavLink>
          </div>
        )}
      </div>
    </header>
  );
}

export function Footer() {
  return (
    <footer className="footer">
      <div className="shell footer" style={{ borderTop: "none", padding: 0 }}>
        <span>MLForge &mdash; Forge your data into intelligence.</span>
        <span>Developed by Pranav Kumar</span>
      </div>
    </footer>
  );
}

export default function AppShell({ children }) {
  return (
    <>
      <TopNav />
      {children}
      <Footer />
    </>
  );
}
