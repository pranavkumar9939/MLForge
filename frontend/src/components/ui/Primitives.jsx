import "./ui.css";

export function Card({ children, className = "", padded = false, ...rest }) {
  return (
    <div className={`card ${padded ? "card-padded" : ""} ${className}`} {...rest}>
      {children}
    </div>
  );
}

export function CardHeader({ title, action, subtitle }) {
  return (
    <div className="card-header">
      <div>
        <h3>{title}</h3>
        {subtitle && (
          <p style={{ fontSize: 12.5, color: "var(--text-tertiary)", marginTop: 3 }}>
            {subtitle}
          </p>
        )}
      </div>
      {action}
    </div>
  );
}

export function CardBody({ children, className = "" }) {
  return <div className={`card-body ${className}`}>{children}</div>;
}

export function Badge({ tone = "neutral", children }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

export function ProgressBar({ value = 0 }) {
  return (
    <div className="progress-track">
      <div className="progress-fill" style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
    </div>
  );
}

export function Spinner() {
  return <span className="spinner" aria-hidden="true" />;
}

export function EmptyState({ icon, title, description, action }) {
  return (
    <div className="empty-state">
      {icon}
      <h4>{title}</h4>
      {description && <p>{description}</p>}
      {action}
    </div>
  );
}
