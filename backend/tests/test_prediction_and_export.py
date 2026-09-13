import io

import pandas as pd


def test_single_prediction_returns_confidence_and_explanation(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    details = client.get(f"/models/{dataset_name}/{best_model}", headers=auth_headers).json()
    sample = {f["name"]: f["example"] for f in details["input_schema"]}

    resp = client.post(f"/predict/{dataset_name}/{best_model}", json={"features": sample}, headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "prediction" in body
    assert "explanation" in body


def test_predict_rejects_unknown_model(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    resp = client.post(f"/predict/{dataset_name}/NotARealModel", json={"features": {}}, headers=auth_headers)
    assert resp.status_code == 404


def test_batch_prediction_appends_prediction_column(client, auth_headers, trained_classification, sample_csv_path):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    iris_df = pd.read_csv(sample_csv_path).drop(columns=["Id", "Species"]).head(5)
    csv_bytes = iris_df.to_csv(index=False).encode()

    resp = client.post(
        f"/predict/{dataset_name}/{best_model}/batch",
        files={"file": ("batch.csv", csv_bytes, "text/csv")},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/csv")

    out_df = pd.read_csv(io.BytesIO(resp.content))
    assert "prediction" in out_df.columns
    assert len(out_df) == 5


def test_batch_prediction_rejects_missing_required_columns(client, auth_headers, trained_classification):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    bad_csv = pd.DataFrame({"only_one_column": [1, 2, 3]}).to_csv(index=False).encode()
    resp = client.post(
        f"/predict/{dataset_name}/{best_model}/batch",
        files={"file": ("bad.csv", bad_csv, "text/csv")},
        headers=auth_headers,
    )
    assert resp.status_code == 400
    assert "missing" in resp.json()["detail"].lower()


def test_export_returns_a_valid_zip_with_expected_files(client, auth_headers, trained_classification):
    import zipfile

    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    resp = client.get(f"/export/{dataset_name}/{best_model}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/zip"

    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    names = zf.namelist()
    for expected in ("model.pkl", "pipeline.pkl", "metadata.json", "evaluation.json", "README.txt"):
        assert expected in names
