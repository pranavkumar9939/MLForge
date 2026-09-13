import io

import matplotlib
matplotlib.use("Agg")  # no display server needed - pure image rendering
import matplotlib.pyplot as plt

EMBER = "#c4501f"
GRAPHITE = "#201d18"
SERIES = ["#c4501f", "#3a6b8a", "#6b7a3e", "#8a5a3a", "#7a5a8a", "#3c7a4f", "#b8791a", "#5a6570"]


def _fig_to_png_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def feature_importance_chart(feature_importance: list[dict]) -> bytes | None:
    if not feature_importance:
        return None

    items = sorted(feature_importance, key=lambda x: x["importance"], reverse=True)[:10]
    items = list(reversed(items))  # largest at top

    fig, ax = plt.subplots(figsize=(6, 0.4 * len(items) + 1))
    ax.barh([i["feature"] for i in items], [i["importance"] for i in items], color=EMBER)
    ax.set_xlabel("Importance", color=GRAPHITE, fontsize=9)
    ax.tick_params(colors=GRAPHITE, labelsize=8)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    return _fig_to_png_bytes(fig)


def confusion_matrix_chart(confusion_matrix: dict) -> bytes:
    labels = confusion_matrix["labels"]
    matrix = confusion_matrix["matrix"]

    fig, ax = plt.subplots(figsize=(4.5, 4))
    im = ax.imshow(matrix, cmap="Oranges")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8, color=GRAPHITE)
    ax.set_yticklabels(labels, fontsize=8, color=GRAPHITE)
    ax.set_xlabel("Predicted", fontsize=9, color=GRAPHITE)
    ax.set_ylabel("Actual", fontsize=9, color=GRAPHITE)

    max_val = max(max(row) for row in matrix) if matrix else 1
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            color = "white" if val > max_val * 0.55 else GRAPHITE
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=9)

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    return _fig_to_png_bytes(fig)


def roc_curve_chart(roc_curve: dict) -> bytes:
    curves = roc_curve["curves"]

    fig, ax = plt.subplots(figsize=(5, 4))
    for i, curve in enumerate(curves):
        ax.plot(
            curve["fpr"], curve["tpr"],
            color=SERIES[i % len(SERIES)], linewidth=1.8,
            label=f"{curve['class']} (AUC {curve['auc']:.3f})",
        )
    ax.plot([0, 1], [0, 1], linestyle="--", color="#d3cfc2", linewidth=1)
    ax.set_xlabel("False Positive Rate", fontsize=9, color=GRAPHITE)
    ax.set_ylabel("True Positive Rate", fontsize=9, color=GRAPHITE)
    ax.tick_params(colors=GRAPHITE, labelsize=8)
    ax.legend(fontsize=7.5, loc="lower right")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    return _fig_to_png_bytes(fig)
