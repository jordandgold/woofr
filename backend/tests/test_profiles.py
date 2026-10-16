from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_profiles():
    response = client.get("/api/profiles")

    assert response.status_code == 200
    
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 12

def test_get_search_by_name():
    response = client.get("/api/profiles?search=Luna")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Luna"

def test_get_search_by_breed():
    response = client.get("/api/profiles?search=Lab")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Teddy"

def test_get_multi_filter():
    response = client.get("/api/profiles?search=Lab&availableOnly=true")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 0

    response = client.get("/api/profiles?search=Lab&availableOnly=false")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Teddy"

def test_filter_search_by_name_case_insensitive():
    response = client.get("/api/profiles?search=bIsCuIt")

    assert response.status_code == 200
    
    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Biscuit"

def test_filter_available_only_true():
    response = client.get("/api/profiles?availableOnly=true")

    assert response.status_code == 200
    
    data = response.json()

    assert len(data) == 8
    for profile in data:
        assert profile["available"] is True

def test_return_empty_array_no_matches():
    response = client.get("/api/profiles?search=NonExistentDogBreed")
    
    assert response.status_code == 200
    
    data = response.json()
    assert data == []

def test_profiles_have_image_urls():
    data = client.get("/api/profiles").json()

    for profile in data:
        response = client.get(profile["imageUrl"])
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("image/svg+xml")
