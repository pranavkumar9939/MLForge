"""
Assembles a report data structure for a dataset's best model, pulling
exclusively from real evaluation artifacts already on disk - nothing here
is invented or hardcoded.
"""

from app.services.comparison.leaderboard_services import built_leaderboard
from app.services.metrics.metrics_service import get_metrics
from app.services.feature_importance.feature_importance_service import get_feature_importance
from app.services.evaluation.confusion_matrix_service import get_confusion_matrix
from app.services.evaluation.roc_service import get_roc_curve
from app.services.persistence.model_registry import get_model_details
from app.services.hyperparameter.tuning_service import get_tuning_results


def build_report_data(dataset_name: str, model_name: str | None = None) -> dict:
    leaderboard = built_leaderboard(dataset_name)
    if leaderboard is None or not leaderboard["leaderboard"]:
        return None

    is_regression = leaderboard["problem_type"] == "Regression"

    target_model = model_name or leaderboard["best_model"]

    metrics = get_metrics(dataset_name, target_model)
    feature_importance = get_feature_importance(dataset_name, target_model, top_n=10)
    metadata = get_model_details(dataset_name, target_model) or {}
    tuning = get_tuning_results(dataset_name, target_model)

    confusion_matrix = None
    roc_curve = None
    if not is_regression:
        confusion_matrix = get_confusion_matrix(dataset_name, target_model)["confusion_matrix"]
        roc_curve = get_roc_curve(dataset_name, target_model)["roc_curve"]

    return {
        "dataset_name": dataset_name,
        "display_name": metadata.get("display_name", dataset_name),
        "problem_type": leaderboard["problem_type"],
        "target_column": metadata.get("target_column"),
        "generated_for_model": target_model,
        "algorithm": metadata.get("algorithm"),
        "training_date": metadata.get("training_date"),
        "feature_count": metadata.get("feature_count"),
        "mlforge_version": metadata.get("mlforge_version"),
        "leaderboard": leaderboard["leaderboard"],
        "best_model": leaderboard["best_model"],
        "metrics": metrics,
        "feature_importance": feature_importance["feature_importance"],
        "confusion_matrix": confusion_matrix,
        "roc_curve": roc_curve,
        "tuning": tuning,
        "is_regression": is_regression,
    }
