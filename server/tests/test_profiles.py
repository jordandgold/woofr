from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_profiles():
    response = client.get("/api/profiles")

    assert response.status_code == 200
    
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) == 24

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

    assert len(data) == 16
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
        assert response.headers["content-type"].startswith("image/jpeg")


VALID_FORM = {
    "name": "Pickles",
    "breed": "Dalmatian",
    "age": "3",
    "distanceMiles": "1.5",
    "available": "true",
    "energyLevel": "high",
    "bio": "Spotted and ready to play.",
}


def test_create_profile_without_photo_uses_default_image():
    response = client.post("/api/profiles", data=VALID_FORM)

    assert response.status_code == 201

    created = response.json()

    assert created["id"] == "25"
    assert created["name"] == "Pickles"
    assert created["favorited"] is False
    assert created["imageUrl"] == "/api/static/dogs/default.svg"
    assert len(client.get("/api/profiles").json()) == 25


def test_create_profile_with_photo_saves_file(tmp_path, monkeypatch):
    from routers import profiles

    monkeypatch.setattr(profiles, "UPLOADS_DIR", tmp_path)

    response = client.post(
        "/api/profiles",
        data=VALID_FORM,
        files={"photo": ("../evil.png", b"\x89PNG fake", "image/png")},
    )

    assert response.status_code == 201

    saved = list(tmp_path.iterdir())

    assert len(saved) == 1
    assert saved[0].suffix == ".png"
    assert "evil" not in saved[0].name
    assert response.json()["imageUrl"] == f"/api/static/dogs/uploads/{saved[0].name}"


def test_create_profile_rejects_non_image(tmp_path, monkeypatch):
    from routers import profiles

    monkeypatch.setattr(profiles, "UPLOADS_DIR", tmp_path)

    response = client.post(
        "/api/profiles",
        data=VALID_FORM,
        files={"photo": ("notes.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 415
    assert list(tmp_path.iterdir()) == []
    assert len(client.get("/api/profiles").json()) == 24


def test_create_profile_validates_fields():
    response = client.post("/api/profiles", data={**VALID_FORM, "energyLevel": "extreme"})

    assert response.status_code == 422
    assert len(client.get("/api/profiles").json()) == 24


def test_profiles_include_created_at_and_new_ones_are_newest():
    profiles = client.get("/api/profiles").json()

    assert all(p["created_at"].endswith("Z") for p in profiles)

    created = client.post("/api/profiles", data=VALID_FORM).json()

    assert created["created_at"] > max(p["created_at"] for p in profiles)

