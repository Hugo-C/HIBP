from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)

PREFIX_CHECKED = "123AB"


def test_api_return_no_results(kvrocks):
    response = client.get(f"/api/v1/haveibeenrocked/{PREFIX_CHECKED}")

    assert response.status_code == 200
    assert response.json() == {PREFIX_CHECKED: []}


def test_api_return_one_result(kvrocks, password_storage):
    expected_password = "some password"
    password_storage.add_password(prefix=PREFIX_CHECKED, password=expected_password)

    response = client.get(f"/api/v1/haveibeenrocked/{PREFIX_CHECKED}")

    assert response.status_code == 200
    assert response.json() == {PREFIX_CHECKED: [expected_password]}


def test_api_return_multiple_results(kvrocks, password_storage):
    expected_passwords = {
        "some password 1",
        "some password 2",
        "some password 3",
    }
    for password in expected_passwords:
        password_storage.add_password(prefix=PREFIX_CHECKED, password=password)

    response = client.get(f"/api/v1/haveibeenrocked/{PREFIX_CHECKED}")

    assert response.status_code == 200
    json_response = response.json()
    assert set(json_response.pop(PREFIX_CHECKED)) == expected_passwords
    assert len(json_response) == 0  # no other keys
