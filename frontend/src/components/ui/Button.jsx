import "./ui.css";

export default function Button({
  variant = "primary",
  size,
  block,
  loading,
  children,
  className = "",
  disabled,
  ...rest
}) {
  const classes = [
    "btn",
    `btn-${variant}`,
    size === "sm" ? "btn-sm" : "",
    size === "lg" ? "btn-lg" : "",
    block ? "btn-block" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button className={classes} disabled={disabled || loading} {...rest}>
      {loading && <span className="spinner" aria-hidden="true" />}
      {children}
    </button>
  );
}
