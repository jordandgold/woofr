import pytest
from fastapi.testclient import TestClient

from main import app
from routers import favorites

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_favorites():
    favorites.favorite_ids.clear()
    yield
    favorites.favorite_ids.clear()


def test_favorites_empty_by_default():
    response = client.get("/api/favorites")

    assert response.status_code == 200
    assert response.json() == []


def test_add_and_list_favorite():
    assert client.put("/api/favorites/3").status_code == 204

    data = client.get("/api/favorites").json()

    assert [p["name"] for p in data] == ["Luna"]


def test_add_favorite_is_idempotent():
    client.put("/api/favorites/3")
    client.put("/api/favorites/3")

    assert len(client.get("/api/favorites").json()) == 1


def test_remove_favorite():
    client.put("/api/favorites/3")

    assert client.delete("/api/favorites/3").status_code == 204
    assert client.get("/api/favorites").json() == []


def test_unknown_profile_returns_404():
    assert client.put("/api/favorites/999").status_code == 404
    assert client.delete("/api/favorites/999").status_code == 404
