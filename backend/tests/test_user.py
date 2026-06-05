import pytest
from tests.conftest import TestingSessionLocal
import models


def make_location(db):
    loc = models.Location(
        name="Fav Loc", country="Test", latitude=50.0, longitude=10.0,
        timezone="UTC", bg_image="/static/images/fav.jpg"
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc


class TestFavorites:
    def test_favorites_requires_auth(self, client):
        r = client.get("/favorites")
        assert r.status_code == 401

    def test_add_favorite_location(self, auth_client):
        db = TestingSessionLocal()
        loc = make_location(db)
        db.close()

        r = auth_client.post("/favorites", json={"location_id": loc.id})
        assert r.status_code == 201
        assert r.json()["location_id"] == loc.id

    def test_get_favorites(self, auth_client):
        r = auth_client.get("/favorites")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_add_duplicate_favorite_fails(self, auth_client):
        db = TestingSessionLocal()
        loc = make_location(db)
        db.close()

        auth_client.post("/favorites", json={"location_id": loc.id})
        r = auth_client.post("/favorites", json={"location_id": loc.id})
        assert r.status_code == 400

    def test_remove_favorite(self, auth_client):
        db = TestingSessionLocal()
        loc = make_location(db)
        db.close()

        add_r = auth_client.post("/favorites", json={"location_id": loc.id})
        fav_id = add_r.json()["id"]

        del_r = auth_client.delete(f"/favorites/{fav_id}")
        assert del_r.status_code == 204

    def test_add_favorite_no_target_fails(self, auth_client):
        r = auth_client.post("/favorites", json={})
        assert r.status_code == 422

    def test_add_favorite_both_targets_fails(self, auth_client):
        r = auth_client.post("/favorites", json={"location_id": 1, "scene_id": 1})
        assert r.status_code == 422


class TestSettings:
    def test_settings_requires_auth(self, client):
        r = client.get("/settings")
        assert r.status_code == 401

    def test_get_settings_defaults(self, auth_client):
        r = auth_client.get("/settings")
        assert r.status_code == 200
        data = r.json()
        assert "volume_sounds" in data
        assert "volume_music" in data

    def test_update_volume(self, auth_client):
        r = auth_client.put("/settings", json={"volume_sounds": 0.5, "volume_music": 0.3})
        assert r.status_code == 200
        data = r.json()
        assert data["volume_sounds"] == 0.5
        assert data["volume_music"] == 0.3

    def test_update_last_location(self, auth_client):
        db = TestingSessionLocal()
        loc = make_location(db)
        db.close()

        r = auth_client.put("/settings", json={"last_location_id": loc.id})
        assert r.status_code == 200
        assert r.json()["last_location_id"] == loc.id
