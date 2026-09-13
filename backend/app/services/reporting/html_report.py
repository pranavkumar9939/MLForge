import base64
from datetime import datetime

from app.services.reporting.chart_images import (
    feature_importance_chart, confusion_matrix_chart, roc_curve_chart,
)


def _img_tag(png_bytes: bytes, alt: str) -> str:
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f'<img src="data:image/png;base64,{b64}" alt="{alt}" />'


def _leaderboard_table(data: dict) -> str:
    is_reg = data["is_regression"]
    header = (
        "<tr><th>Rank</th><th>Model</th><th>R\u00b2</th><th>MAE</th><th>RMSE</th><th>Status</th></tr>"
        if is_reg else
        "<tr><th>Rank</th><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>Status</th></tr>"
    )
    rows = []
    for m in data["leaderboard"]:
        is_best = m["model_name"] == data["best_model"]
        name_cell = f'{m["model_name"]}{" <span class=\"badge\">Best</span>" if is_best else ""}'
        if is_reg:
            rows.append(
                f'<tr class="{"best" if is_best else ""}"><td>{m["rank"]}</td><td>{name_cell}</td>'
                f'<td>{m["r2_score"]:.3f}</td><td>{m["mae"]:.3f}</td><td>{m["rmse"]:.3f}</td><td>{m["status"]}</td></tr>'
            )
        else:
            rows.append(
                f'<tr class="{"best" if is_best else ""}"><td>{m["rank"]}</td><td>{name_cell}</td>'
                f'<td>{m["accuracy"]:.1f}%</td><td>{m["precision"]:.1f}%</td>'
                f'<td>{m["recall"]:.1f}%</td><td>{m["f1_score"]:.1f}%</td><td>{m["status"]}</td></tr>'
            )
    return f"<table>{header}{''.join(rows)}</table>"


def _metrics_html(data: dict) -> str:
    m = data["metrics"]
    if data["is_regression"]:
        tiles = [
            ("R\u00b2 Score", f"{m['r2_score'] * 100:.1f}%"),
            ("MAE", f"{m['mae']:.3f}"),
            ("RMSE", f"{m['rmse']:.3f}"),
            ("Status", m["status"]),
        ]
    else:
        tiles = [
            ("Accuracy", f"{m['accuracy']:.1f}%"),
            ("Precision", f"{m['precision']:.1f}%"),
            ("Recall", f"{m['recall']:.1f}%"),
            ("F1 Score", f"{m['f1_score']:.1f}%"),
        ]
    tile_html = "".join(f'<div class="tile"><div class="tile-value">{v}</div><div class="tile-label">{k}</div></div>' for k, v in tiles)
    return f'<div class="tiles">{tile_html}</div>'


def render_html_report(data: dict) -> str:
    fi_bytes = feature_importance_chart(data["feature_importance"])
    if fi_bytes:
        fi_section = f'<div class="chart-block">{_img_tag(fi_bytes, "Feature importance")}</div>'
    else:
        fi_section = (
            '<p class="muted-note">This model (' + data['best_model'] + ') does not expose a '
            'feature-importance score (only tree-based and linear models do).</p>'
        )

    extra_charts = ""
    if not data["is_regression"] and data["confusion_matrix"]:
        cm_img = _img_tag(confusion_matrix_chart(data["confusion_matrix"]), "Confusion matrix")
        extra_charts += f'<div class="chart-block"><h3>Confusion Matrix</h3>{cm_img}</div>'
    if not data["is_regression"] and data["roc_curve"]:
        roc_img = _img_tag(roc_curve_chart(data["roc_curve"]), "ROC curve")
        extra_charts += f'<div class="chart-block"><h3>ROC Curve</h3>{roc_img}</div>'

    tuning_html = ""
    if data["tuning"] and data["tuning"].get("tuned"):
        params = "".join(f"<li><code>{k}</code>: {v}</li>" for k, v in data["tuning"]["best_params"].items())
        cv_score = data["tuning"].get("best_cv_score")
        tuning_html = f"""
        <section>
          <h2>Hyperparameter Tuning</h2>
          <p>Best cross-validated score: <strong>{f'{cv_score * 100:.2f}%' if cv_score is not None else 'N/A'}</strong></p>
          <ul class="params">{params}</ul>
        </section>
        """

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>MLForge Report — {data['display_name']}</title>
<style>
  :root {{
    --ember: #c4501f; --ember-strong: #a63f16; --ember-wash: #fbf1e8;
    --ink: #201d18; --muted: #63594c; --border: #e4e1d8; --surface: #faf9f6;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--ink); background: var(--surface); margin: 0; padding: 48px;
    max-width: 860px; margin-left: auto; margin-right: auto; line-height: 1.55;
  }}
  header {{ border-bottom: 2px solid var(--ink); padding-bottom: 20px; margin-bottom: 28px; }}
  .brand {{ font-weight: 700; font-size: 14px; letter-spacing: 0.02em; }}
  .brand span {{ color: var(--ember); }}
  h1 {{ font-size: 26px; margin: 10px 0 4px; }}
  .subtitle {{ color: var(--muted); font-size: 13.5px; }}
  h2 {{ font-size: 17px; margin-top: 34px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }}
  h3 {{ font-size: 14px; margin-bottom: 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 12px; }}
  th {{ text-align: left; background: #f2f0ea; padding: 8px 10px; font-size: 11px; text-transform: uppercase;
        letter-spacing: 0.03em; color: var(--muted); border-bottom: 1px solid var(--border); }}
  td {{ padding: 8px 10px; border-bottom: 1px solid var(--border); }}
  tr.best td {{ background: var(--ember-wash); font-weight: 600; }}
  .badge {{ background: var(--ember); color: white; font-size: 10px; padding: 2px 7px; border-radius: 999px; }}
  .tiles {{ display: flex; gap: 14px; margin-top: 14px; flex-wrap: wrap; }}
  .tile {{ border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; flex: 1; min-width: 120px; }}
  .tile-value {{ font-size: 22px; font-weight: 700; color: var(--ember-strong); }}
  .tile-label {{ font-size: 11.5px; color: var(--muted); margin-top: 4px; }}
  .chart-block {{ margin-top: 18px; }}
  .chart-block img {{ max-width: 100%; border: 1px solid var(--border); border-radius: 8px; }}
  .meta-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px 24px; font-size: 13px; margin-top: 10px; }}
  .meta-grid dt {{ color: var(--muted); }}
  .meta-grid dd {{ margin: 0; font-weight: 600; }}
  ul.params {{ font-size: 13px; padding-left: 18px; }}
  code {{ font-family: ui-monospace, monospace; background: #f2f0ea; padding: 1px 5px; border-radius: 3px; }}
  .muted-note {{ color: var(--muted); font-size: 13px; font-style: italic; }}
  footer {{ margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border); color: var(--muted); font-size: 11.5px; display: flex; justify-content: space-between; }}
</style>
</head>
<body>
  <header>
    <div class="brand">ML<span>Forge</span></div>
    <h1>{data['display_name']}</h1>
    <div class="subtitle">{data['problem_type']} &middot; Model report generated {generated_at}</div>
  </header>

  <section>
    <h2>Overview</h2>
    <dl class="meta-grid">
      <dt>Target column</dt><dd>{data['target_column']}</dd>
      <dt>Best model</dt><dd>{data['best_model']}</dd>
      <dt>Algorithm</dt><dd>{data['algorithm']}</dd>
      <dt>Feature count</dt><dd>{data['feature_count']}</dd>
      <dt>Models compared</dt><dd>{len(data['leaderboard'])}</dd>
      <dt>Training date</dt><dd>{data['training_date']}</dd>
    </dl>
  </section>

  <section>
    <h2>Best Model Performance</h2>
    {_metrics_html(data)}
  </section>

  <section>
    <h2>Model Leaderboard</h2>
    {_leaderboard_table(data)}
  </section>

  <section>
    <h2>Feature Importance</h2>
    {fi_section}
  </section>

  {f'<section><h2>Diagnostics</h2>{extra_charts}</section>' if extra_charts else ""}

  {tuning_html}

  <footer>
    <span>Generated by MLForge &mdash; Forge your data into intelligence.</span>
    <span>Developed by Pranav Kumar</span>
  </footer>
</body>
</html>"""
