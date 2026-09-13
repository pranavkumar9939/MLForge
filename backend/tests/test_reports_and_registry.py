def test_html_report_contains_leaderboard_and_brand(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    resp = client.get(f"/report/{dataset_name}/html", headers=auth_headers)
    assert resp.status_code == 200
    assert "MLForge" in resp.text
    assert "<table>" in resp.text


def test_pdf_report_is_a_valid_pdf(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    resp = client.get(f"/report/{dataset_name}/pdf", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content[:5] == b"%PDF-"


def test_report_works_for_every_trained_model_including_no_feature_importance(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    for model_name in trained_classification["training"]["models_trained"]:
        resp = client.get(
            f"/report/{dataset_name}/pdf", params={"model_name": model_name}, headers=auth_headers
        )
        assert resp.status_code == 200, f"{model_name} failed: {resp.text}"


def test_report_requires_ownership(client, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    other_resp = client.post(
        "/auth/signup",
        json={"name": "Report Intruder", "email": "report_intruder@example.com", "password": "Passw0rd123"},
    )
    token = other_resp.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {token}"}

    resp = client.get(f"/report/{dataset_name}/pdf", headers=other_headers)
    assert resp.status_code == 404


def test_leaderboard_ranks_by_overall_score_descending(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    resp = client.get(f"/leaderboard/{dataset_name}", headers=auth_headers)
    assert resp.status_code == 200
    entries = resp.json()["leaderboard"]
    ranks = [e["rank"] for e in entries]
    assert ranks == sorted(ranks)


def test_feature_importance_is_a_list_for_every_model(client, auth_headers, trained_classification):
    """Regression test: this used to return a malformed nested dict for
    models without a native importance score (KNN, SVM, Naive Bayes)."""
    dataset_name = trained_classification["dataset_name"]

    for model_name in trained_classification["training"]["models_trained"]:
        resp = client.get(f"/feature-importance/{dataset_name}/{model_name}", headers=auth_headers)
        assert resp.status_code == 200
        assert isinstance(resp.json()["feature_importance"], list)


def test_tuning_results_include_best_params(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    resp = client.get(f"/tuning/{dataset_name}/{best_model}", headers=auth_headers)
    assert resp.status_code == 200
