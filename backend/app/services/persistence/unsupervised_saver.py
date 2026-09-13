import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(__file__)
        )
    )
)

MODEL_DIR = os.path.join(BASE_DIR, "saved_models")


def save_clustering_results(dataset_name, metadata, clustering_result, visualization):
    folder = os.path.join(MODEL_DIR, dataset_name, "clustering")
    os.makedirs(folder, exist_ok=True)

    # Strip the non-serializable fitted estimator; labels (already converted
    # to plain ints by the caller) stay so the frontend can recolor the
    # shared 2D projection per algorithm.
    serializable_results = [
        {k: v for k, v in r.items() if k != "model"}
        for r in clustering_result["results"]
    ]

    payload = {
        "metadata": metadata,
        "recommended_k": clustering_result["recommended_k"],
        "best_algorithm": clustering_result["best_algorithm"],
        "results": serializable_results,
        "skipped": clustering_result["skipped"],
        "visualization": visualization,
    }

    with open(os.path.join(folder, "results.json"), "w") as f:
        json.dump(payload, f, indent=2)


def load_clustering_results(dataset_name):
    path = os.path.join(MODEL_DIR, dataset_name, "clustering", "results.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def save_dimensionality_reduction_results(dataset_name, metadata, dr_result):
    folder = os.path.join(MODEL_DIR, dataset_name, "dimensionality_reduction")
    os.makedirs(folder, exist_ok=True)

    payload = {
        "metadata": metadata,
        "n_components": dr_result["n_components"],
        "results": dr_result["results"],
        "skipped": dr_result["skipped"],
    }

    with open(os.path.join(folder, "results.json"), "w") as f:
        json.dump(payload, f, indent=2)


def load_dimensionality_reduction_results(dataset_name):
    path = os.path.join(MODEL_DIR, dataset_name, "dimensionality_reduction", "results.json")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)
