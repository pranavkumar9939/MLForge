"""
Dimensionality reduction engine: projects a preprocessed feature matrix
down to 2 components (for visualization) using several algorithms.

NMF requires non-negative input, which the standard-scaled pipeline output
is not (StandardScaler centers to mean 0), so NMF is run on a separately
min-max-scaled copy of X rather than skipped outright.
"""

import numpy as np
from sklearn.decomposition import PCA, TruncatedSVD, KernelPCA, FastICA, NMF
from sklearn.manifold import TSNE
from sklearn.preprocessing import MinMaxScaler

# t-SNE is O(n^2) - skip it above this many rows to stay computationally reasonable.
TSNE_ROW_LIMIT = 5000


def run_dimensionality_reduction(X: np.ndarray, n_components: int = 2, on_progress=None) -> dict:
    n_samples, n_features = X.shape
    max_components = min(n_components, n_features, n_samples - 1)

    candidates = [
        ("PCA", lambda: PCA(n_components=max_components, random_state=42), X),
        ("Truncated SVD", lambda: TruncatedSVD(n_components=max_components, random_state=42), X),
        ("Kernel PCA", lambda: KernelPCA(n_components=max_components, kernel="rbf", random_state=42), X),
        ("ICA", lambda: FastICA(n_components=max_components, random_state=42, max_iter=500), X),
        ("NMF", lambda: NMF(n_components=max_components, random_state=42, max_iter=500), MinMaxScaler().fit_transform(X)),
    ]

    if n_samples <= TSNE_ROW_LIMIT:
        perplexity = min(30, max(5, n_samples // 4))
        candidates.append(
            ("t-SNE", lambda: TSNE(n_components=max_components, random_state=42, perplexity=perplexity), X)
        )

    total = len(candidates)
    results = []
    skipped = []

    for i, (name, make_estimator, data) in enumerate(candidates, start=1):
        if on_progress:
            on_progress(f"Running {name} ({i}/{total})", i - 1, total)

        try:
            estimator = make_estimator()
            coords = estimator.fit_transform(data)
        except Exception as exc:
            skipped.append({"algorithm": name, "reason": f"Failed to fit: {exc}"})
            continue

        entry = {
            "algorithm": name,
            "coordinates": coords[:, :2].tolist(),  # always return 2D for plotting
        }

        if hasattr(estimator, "explained_variance_ratio_"):
            entry["explained_variance_ratio"] = [
                float(v) for v in estimator.explained_variance_ratio_[:2]
            ]
            entry["total_explained_variance"] = float(
                sum(estimator.explained_variance_ratio_)
            )

        results.append(entry)

    if on_progress:
        on_progress("Finalizing projections", total, total)

    return {
        "n_components": max_components,
        "results": results,
        "skipped": skipped,
    }
