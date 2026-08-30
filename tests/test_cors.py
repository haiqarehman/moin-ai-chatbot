from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_cors_allows_configured_origin():
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert (
        response.headers["access-control-allow-origin"]
        == "http://localhost:5173"
    )


def test_cors_rejects_unapproved_origin():
    response = client.options(
        "/api/v1/health",
        headers={
            "Origin": "http://malicious.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in response.headers