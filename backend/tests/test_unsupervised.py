import time


def _run_unsupervised_job(client, headers, csv_path, filename, mode, **kwargs):
    with open(csv_path, "rb") as f:
        upload_resp = client.post("/upload/", files={"file": (filename, f, "text/csv")}, headers=headers)
    assert upload_resp.status_code == 200
    uploaded_filename = upload_resp.json()["filename"]

    job_resp = client.post(
        "/unsupervised/train/start",
        json={"filename": uploaded_filename, "mode": mode, **kwargs},
        headers=headers,
    )
    assert job_resp.status_code == 200, job_resp.text
    job_id = job_resp.json()["job_id"]

    for _ in range(60):
        status_resp = client.get(f"/jobs/{job_id}", headers=headers)
        body = status_resp.json()
        if body["status"] in ("completed", "failed"):
            return body
        time.sleep(0.3)

    raise AssertionError("Unsupervised job did not finish in time")


def test_clustering_job_completes_and_ranks_algorithms(client, auth_headers, sample_csv_path):
    job = _run_unsupervised_job(client, auth_headers, sample_csv_path, "ClusterTest1.csv", "clustering")
    assert job["status"] == "completed", job.get("error")

    result = job["result"]
    assert result["mode"] == "clustering"
    assert result["recommended_k"] >= 2
    assert len(result["results"]) > 0
    assert result["best_algorithm"] is not None

    # scores should be ranked descending by silhouette
    scores = [r["silhouette_score"] for r in result["results"]]
    assert scores == sorted(scores, reverse=True)


def test_clustering_results_are_persisted_and_fetchable(client, auth_headers, sample_csv_path):
    job = _run_unsupervised_job(client, auth_headers, sample_csv_path, "ClusterTest2.csv", "clustering")
    dataset_name = job["result"]["dataset_name"]

    resp = client.get(f"/unsupervised/clustering/{dataset_name}", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["visualization"]["points"]) > 0


def test_dimensionality_reduction_job_completes(client, auth_headers, sample_csv_path):
    job = _run_unsupervised_job(
        client, auth_headers, sample_csv_path, "DRTest1.csv", "dimensionality_reduction", n_components=2
    )
    assert job["status"] == "completed", job.get("error")

    result = job["result"]
    assert result["mode"] == "dimensionality_reduction"
    assert len(result["results"]) > 0

    pca_result = next((r for r in result["results"] if r["algorithm"] == "PCA"), None)
    assert pca_result is not None
    assert len(pca_result["coordinates"]) > 0
    assert pca_result["explained_variance_ratio"] is not None


def test_unsupervised_rejects_invalid_mode(client, auth_headers, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        upload_resp = client.post("/upload/", files={"file": ("DRTest2.csv", f, "text/csv")}, headers=auth_headers)
    filename = upload_resp.json()["filename"]

    resp = client.post(
        "/unsupervised/train/start",
        json={"filename": filename, "mode": "not_a_real_mode"},
        headers=auth_headers,
    )
    assert resp.status_code == 400
