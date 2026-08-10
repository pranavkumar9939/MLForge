def select_top_models(leaderboard, top_n=3):

    sorted_models = sorted(
        leaderboard,
        key = lambda x:
            x["overall_score"],
        reverse = True
    )

    return sorted_models[:top_n]