from tests.conftest import upload_and_train


def _second_user_headers(client):
    resp = client.post(
        "/auth/signup",
        json={"name": "Second User", "email": "second_user_for_ownership@example.com", "password": "Passw0rd123"},
    )
    if resp.status_code == 409:
        resp = client.post(
            "/auth/login",
            json={"email": "second_user_for_ownership@example.com", "password": "Passw0rd123"},
        )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_other_user_cannot_list_my_datasets(client, trained_classification):
    other_headers = _second_user_headers(client)
    resp = client.get("/models/", headers=other_headers)
    assert resp.status_code == 200
    other_names = [d["dataset_name"] for d in resp.json()["datasets"]]
    assert trained_classification["dataset_name"] not in other_names


def test_other_user_cannot_read_my_model_details(client, trained_classification):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    other_headers = _second_user_headers(client)
    resp = client.get(f"/models/{dataset_name}/{best_model}", headers=other_headers)
    assert resp.status_code == 404  # not 403 - existence itself shouldn't be confirmed


def test_other_user_cannot_read_my_leaderboard(client, trained_classification):
    dataset_name = trained_classification["dataset_name"]

    other_headers = _second_user_headers(client)
    resp = client.get(f"/leaderboard/{dataset_name}", headers=other_headers)
    assert resp.status_code == 404


def test_other_user_cannot_predict_with_my_model(client, trained_classification):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    other_headers = _second_user_headers(client)
    resp = client.post(f"/predict/{dataset_name}/{best_model}", json={"features": {}}, headers=other_headers)
    assert resp.status_code == 404


def test_other_user_cannot_export_my_model(client, trained_classification):
    dataset_name = trained_classification["dataset_name"]
    best_model = trained_classification["evaluation"]["best_model"]["model_name"]

    other_headers = _second_user_headers(client)
    resp = client.get(f"/export/{dataset_name}/{best_model}", headers=other_headers)
    assert resp.status_code == 404


def test_other_user_cannot_train_against_my_uploaded_file(client, auth_headers, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        upload_resp = client.post(
            "/upload/", files={"file": ("OwnershipUploadTest.csv", f, "text/csv")}, headers=auth_headers
        )
    filename = upload_resp.json()["filename"]
    target = upload_resp.json()["analysis"]["target_recommendation"]["recommended_column"]

    other_headers = _second_user_headers(client)
    resp = client.post(
        "/upload/train",
        json={"filename": filename, "target_column": target, "training_mode": "fast"},
        headers=other_headers,
    )
    assert resp.status_code == 404


def test_other_user_cannot_poll_my_training_job(client, auth_headers, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        upload_resp = client.post(
            "/upload/", files={"file": ("OwnershipJobTest.csv", f, "text/csv")}, headers=auth_headers
        )
    filename = upload_resp.json()["filename"]
    target = upload_resp.json()["analysis"]["target_recommendation"]["recommended_column"]

    job_resp = client.post(
        "/upload/train/start",
        json={"filename": filename, "target_column": target, "training_mode": "fast"},
        headers=auth_headers,
    )
    job_id = job_resp.json()["job_id"]

    other_headers = _second_user_headers(client)
    resp = client.get(f"/jobs/{job_id}", headers=other_headers)
    assert resp.status_code == 404

    owner_resp = client.get(f"/jobs/{job_id}", headers=auth_headers)
    assert owner_resp.status_code == 200


def test_owner_can_access_their_own_data(client, trained_classification, auth_headers):
    dataset_name = trained_classification["dataset_name"]

    resp = client.get(f"/leaderboard/{dataset_name}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["best_model"]
