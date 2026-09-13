def test_signup_creates_user_and_returns_token(client, unique_email):
    resp = client.post(
        "/auth/signup",
        json={"name": "Alice", "email": unique_email, "password": "Passw0rd123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]
    assert data["user"]["email"] == unique_email
    assert data["user"]["name"] == "Alice"


def test_signup_rejects_duplicate_email(client, unique_email):
    payload = {"name": "Alice", "email": unique_email, "password": "Passw0rd123"}
    first = client.post("/auth/signup", json=payload)
    assert first.status_code == 200

    second = client.post("/auth/signup", json=payload)
    assert second.status_code == 409


def test_signup_rejects_weak_password(client, unique_email):
    resp = client.post(
        "/auth/signup",
        json={"name": "Alice", "email": unique_email, "password": "short"},
    )
    assert resp.status_code == 422


def test_login_succeeds_with_correct_credentials(client, unique_email):
    client.post("/auth/signup", json={"name": "Bob", "email": unique_email, "password": "Passw0rd123"})

    resp = client.post("/auth/login", json={"email": unique_email, "password": "Passw0rd123"})
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_login_rejects_wrong_password(client, unique_email):
    client.post("/auth/signup", json={"name": "Bob", "email": unique_email, "password": "Passw0rd123"})

    resp = client.post("/auth/login", json={"email": unique_email, "password": "WrongPass1"})
    assert resp.status_code == 401


def test_login_rejects_unknown_email(client):
    resp = client.post("/auth/login", json={"email": "nobody@example.com", "password": "Passw0rd123"})
    assert resp.status_code == 401


def test_me_requires_authentication(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 401


def test_me_returns_current_user(client, auth_headers):
    resp = client.get("/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert "email" in resp.json()


def test_me_rejects_garbage_token(client):
    resp = client.get("/auth/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert resp.status_code == 401
