import io


def test_upload_requires_authentication(client, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        resp = client.post("/upload/", files={"file": ("Iris.csv", f, "text/csv")})
    assert resp.status_code == 401


def test_upload_returns_target_recommendation_not_a_final_choice(client, auth_headers, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        resp = client.post("/upload/", files={"file": ("IrisAnalysisOnly.csv", f, "text/csv")}, headers=auth_headers)
    assert resp.status_code == 200
    analysis = resp.json()["analysis"]

    # MLForge must never silently commit to a target - it only recommends.
    assert analysis["target_confirmed"] is False
    assert analysis["target_recommendation"]["requires_confirmation"] is True
    assert analysis["target_recommendation"]["recommended_column"] in analysis["column_names"]
    assert len(analysis["target_recommendation"]["candidates"]) == len(analysis["column_names"])


def test_upload_rejects_non_csv_extension(client, auth_headers):
    bad_file = io.BytesIO(b"not a real dataset")
    resp = client.post(
        "/upload/",
        files={"file": ("malware.exe", bad_file, "application/octet-stream")},
        headers=auth_headers,
    )
    assert resp.status_code == 400


def test_upload_rejects_dataset_with_too_few_rows(client, auth_headers):
    tiny_csv = io.BytesIO(b"a,b,target\n1,2,3\n4,5,6\n")
    resp = client.post(
        "/upload/",
        files={"file": ("tiny.csv", tiny_csv, "text/csv")},
        headers=auth_headers,
    )
    assert resp.status_code == 400
    assert "rows" in resp.json()["detail"].lower()


def test_train_requires_valid_target_column(client, auth_headers, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        resp = client.post("/upload/", files={"file": ("IrisBadTarget.csv", f, "text/csv")}, headers=auth_headers)
    filename = resp.json()["filename"]

    resp = client.post(
        "/upload/train",
        json={"filename": filename, "target_column": "ThisColumnDoesNotExist", "training_mode": "fast"},
        headers=auth_headers,
    )
    assert resp.status_code == 400


def test_train_classification_produces_a_ranked_leaderboard(trained_classification):
    result = trained_classification
    assert result["analysis"]["problem_type"] in ("Binary Classification", "Multi-Class Classification")
    assert len(result["training"]["models_trained"]) >= 5

    best = result["evaluation"]["best_model"]
    assert best["model_name"] in result["training"]["models_trained"]
    assert 0 <= best["accuracy"]["value"] <= 100


def test_train_regression_produces_r2_scores(trained_regression):
    result = trained_regression
    assert result["analysis"]["problem_type"] == "Regression"
    best = result["evaluation"]["best_model"]
    assert -1 <= best["r2_score"] <= 1


def test_dropped_columns_are_reported_with_reasons(trained_classification):
    dropped = trained_classification["preprocessing"]["dropped_columns"]

    # Iris.csv has an "Id" column, which should be detected as an identifier and dropped with a reason.
    assert any(d["column"].lower() == "id" for d in dropped)
    for entry in dropped:
        assert entry["reason"]


def test_label_encoding_produces_original_class_labels_on_predict(client, auth_headers, trained_classification):
    result = trained_classification
    dataset_name = result["dataset_name"]
    best_model = result["evaluation"]["best_model"]["model_name"]

    details = client.get(f"/models/{dataset_name}/{best_model}", headers=auth_headers).json()
    sample = {f["name"]: f["example"] for f in details["input_schema"]}

    resp = client.post(f"/predict/{dataset_name}/{best_model}", json={"features": sample}, headers=auth_headers)
    assert resp.status_code == 200
    prediction = resp.json()["prediction"]
    # Should be a real species name, not a raw encoded integer like 0/1/2.
    assert isinstance(prediction, str)
    assert prediction.lower().startswith("iris")
