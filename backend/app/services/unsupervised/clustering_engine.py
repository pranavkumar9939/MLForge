"""
Clustering engine: runs a library of clustering algorithms against a
preprocessed feature matrix and scores each with Silhouette, Davies-Bouldin,
and Calinski-Harabasz.

Approach (kept deliberately bounded so this stays computationally
reasonable on real datasets):
  1. Use a quick KMeans sweep over a small k range to pick a recommended
     number of clusters via silhouette score.
  2. Run every candidate algorithm once, using that recommended k where the
     algorithm takes one (density-based algorithms use their own logic).
  3. Any algorithm that fails, or produces a degenerate labeling (fewer
     than 2 clusters, or every point in its own cluster) is skipped with a
     stated reason rather than silently dropped.
"""

import numpy as np
from sklearn.cluster import (
    KMeans, MiniBatchKMeans, AgglomerativeClustering, DBSCAN, OPTICS,
    SpectralClustering, Birch,
)
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# Algorithms whose runtime/memory scales poorly (O(n^2) or worse) - skipped
# above this many rows to keep training bounded.
EXPENSIVE_ROW_LIMIT = 8000


def _recommend_k(X: np.ndarray, k_range: range) -> int:
    best_k, best_score = k_range[0], -1.0
    for k in k_range:
        try:
            labels = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)
            if len(set(labels)) < 2:
                continue
            score = silhouette_score(X, labels)
            if score > best_score:
                best_k, best_score = k, score
        except Exception:
            continue
    return best_k


def _score(X, labels) -> dict | None:
    unique_labels = set(labels)
    unique_labels.discard(-1)  # DBSCAN/OPTICS noise label
    if len(unique_labels) < 2 or len(unique_labels) >= len(labels):
        return None
    try:
        return {
            "silhouette_score": float(silhouette_score(X, labels)),
            "davies_bouldin_score": float(davies_bouldin_score(X, labels)),
            "calinski_harabasz_score": float(calinski_harabasz_score(X, labels)),
        }
    except Exception:
        return None


def _cluster_sizes(labels) -> dict:
    values, counts = np.unique(labels, return_counts=True)
    return {str(int(v)): int(c) for v, c in zip(values, counts)}


def build_candidates(n_samples: int, k: int):
    """Return the list of (name, estimator) candidates for this dataset size."""
    candidates = [
        ("K-Means", KMeans(n_clusters=k, n_init=10, random_state=42)),
        ("MiniBatch K-Means", MiniBatchKMeans(n_clusters=k, n_init=10, random_state=42)),
        ("Gaussian Mixture", GaussianMixture(n_components=k, random_state=42)),
        ("Birch", Birch(n_clusters=k)),
        ("DBSCAN", DBSCAN(eps=0.8, min_samples=5)),
    ]

    if n_samples <= EXPENSIVE_ROW_LIMIT:
        candidates.append(("Agglomerative Clustering", AgglomerativeClustering(n_clusters=k)))
        candidates.append(("Spectral Clustering", SpectralClustering(n_clusters=k, random_state=42, affinity="nearest_neighbors")))
        candidates.append(("OPTICS", OPTICS(min_samples=5)))

    return candidates


def run_clustering(X: np.ndarray, k: int | None = None, on_progress=None) -> dict:
    n_samples = X.shape[0]

    if k is None:
        max_k = min(10, max(2, n_samples // 5))
        k = _recommend_k(X, range(2, max_k + 1)) if max_k >= 2 else 2

    candidates = build_candidates(n_samples, k)
    total = len(candidates)

    results = []
    skipped = []

    for i, (name, estimator) in enumerate(candidates, start=1):
        if on_progress:
            on_progress(f"Clustering with {name} ({i}/{total})", i - 1, total)

        try:
            labels = estimator.fit_predict(X)
        except Exception as exc:
            skipped.append({"algorithm": name, "reason": f"Failed to fit: {exc}"})
            continue

        metrics = _score(X, labels)
        if metrics is None:
            skipped.append({
                "algorithm": name,
                "reason": "Produced fewer than 2 real clusters (or degenerate labeling) on this data.",
            })
            continue

        results.append({
            "algorithm": name,
            "model": estimator,
            "labels": labels,
            "n_clusters_found": len(set(labels)) - (1 if -1 in labels else 0),
            "cluster_sizes": _cluster_sizes(labels),
            "noise_points": int(np.sum(labels == -1)) if -1 in labels else 0,
            **metrics,
        })

    if on_progress:
        on_progress("Ranking clustering algorithms", total, total)

    results.sort(key=lambda r: r["silhouette_score"], reverse=True)

    return {
        "recommended_k": k,
        "results": results,
        "skipped": skipped,
        "best_algorithm": results[0]["algorithm"] if results else None,
    }
