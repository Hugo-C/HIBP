from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_api_return_404_on_missing_prefix():
    response = client.get("/api/v1/haveibeenrocked/")
    assert response.status_code == 404


def test_api_return_400_on_prefix_too_short():
    response = client.get("/api/v1/haveibeenrocked/123")
    assert response.status_code == 422
    assert "detail" in response.json()  # error message is quite specific so we don't assert it


def test_api_return_400_on_prefix_too_long():
    response = client.get("/api/v1/haveibeenrocked/123456")
    assert response.status_code == 422


def test_api_return_400_on_prefix_not_hexadecimal():
    response = client.get("/api/v1/haveibeenrocked/12xyz")
    assert response.status_code == 422
