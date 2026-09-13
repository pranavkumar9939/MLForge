"""
Test configuration.

CRITICAL: this module sets environment variables BEFORE any `app.*` module
is imported, so the app's settings singleton (and its SQLite DB / upload /
saved_models paths) point at an isolated temp directory instead of the
real development data. This must stay at module level, at the very top,
because pytest imports conftest.py before it imports any test file.
"""

import os
import shutil
import tempfile
import uuid
from pathlib import Path

_TEST_DIR = Path(tempfile.mkdtemp(prefix="mlforge_test_"))

os.environ["UPLOAD_DIR"] = str(_TEST_DIR / "uploads")
os.environ["SAVED_MODELS_DIR"] = str(_TEST_DIR / "saved_models")
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DIR / 'test.db'}"
os.environ["ENVIRONMENT"] = "test"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _cleanup_test_dir():
    yield
    shutil.rmtree(_TEST_DIR, ignore_errors=True)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def unique_email():
    """Function-scoped: each auth test needs its own fresh email."""
    return f"user_{uuid.uuid4().hex[:10]}@example.com"


@pytest.fixture(scope="module")
def auth_headers(client):
    """
    Sign up one user per test module (not per test function) and reuse
    their session everywhere in that module. Real per-test isolation for
    ownership/security tests comes from using distinct users deliberately
    (see test_ownership.py's _second_user_headers), not from re-signing-up
    for every single test.
    """
    email = f"module_user_{uuid.uuid4().hex[:10]}@example.com"
    resp = client.post(
        "/auth/signup",
        json={"name": "Test User", "email": email, "password": "Passw0rd123"},
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="module")
def sample_csv_path():
    """Path to a real sample dataset shipped in the repo's uploads folder."""
    path = Path(__file__).resolve().parents[1] / "uploads" / "Iris.csv"
    assert path.exists(), "Expected sample dataset uploads/Iris.csv to exist"
    return path


@pytest.fixture(scope="module")
def regression_csv_path():
    path = Path(__file__).resolve().parents[1] / "uploads" / "powerplant_data.csv"
    assert path.exists(), "Expected sample dataset uploads/powerplant_data.csv to exist"
    return path


@pytest.fixture(scope="module")
def trained_classification(client, auth_headers, sample_csv_path, request):
    """One shared, fully-trained classification model per test module."""
    filename = f"SharedClassification_{request.module.__name__.split('.')[-1]}.csv"
    return upload_and_train(client, auth_headers, sample_csv_path, filename)


@pytest.fixture(scope="module")
def trained_regression(client, auth_headers, regression_csv_path, request):
    """One shared, fully-trained regression model per test module."""
    filename = f"SharedRegression_{request.module.__name__.split('.')[-1]}.csv"
    return upload_and_train(client, auth_headers, regression_csv_path, filename)


def upload_and_train(client, headers, csv_path, filename, training_mode="fast", target_column=None):
    """Helper: upload a dataset and run synchronous training. Returns the /upload/train response JSON."""
    with open(csv_path, "rb") as f:
        upload_resp = client.post(
            "/upload/",
            files={"file": (filename, f, "text/csv")},
            headers=headers,
        )
    assert upload_resp.status_code == 200, upload_resp.text
    upload_data = upload_resp.json()

    resolved_target = target_column or upload_data["analysis"]["target_recommendation"]["recommended_column"]

    train_resp = client.post(
        "/upload/train",
        json={
            "filename": upload_data["filename"],
            "target_column": resolved_target,
            "training_mode": training_mode,
        },
        headers=headers,
    )
    assert train_resp.status_code == 200, train_resp.text
    return train_resp.json()
