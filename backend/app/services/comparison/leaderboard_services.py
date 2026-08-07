from .comparison_service import compare_models

def built_leaderboard(dataset_name):

    result = compare_models(dataset_name)

    if result is None:
        return None

    models = result["models"]

    ranked = []

    for idx, model in enumerate(models, start = 1):

        model["rank"] = idx

        ranked.append(model)

    return {
        "dataset": dataset_name,
        "best_model": result["best_model"],
        "problem_type": result["problem_type"],
        "leaderboard": ranked
    }