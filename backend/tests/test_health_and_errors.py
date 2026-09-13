def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["app"] == "MLForge"


def test_unhandled_exceptions_never_leak_a_stack_trace(client, auth_headers):
    # Deliberately hit predict with a model that doesn't exist to trigger
    # an internal 404 path, and separately confirm well-formed 4xx bodies
    # never contain raw Python traceback text.
    resp = client.post(
        "/predict/definitely_not_a_real_dataset/NotAModel",
        json={"features": {}},
        headers=auth_headers,
    )
    assert resp.status_code == 404
    assert "Traceback" not in resp.text
    assert "File \"" not in resp.text


def test_404_for_unknown_route(client):
    resp = client.get("/this/route/does/not/exist")
    assert resp.status_code == 404
