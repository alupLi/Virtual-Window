import pytest
from tests.conftest import TestingSessionLocal
import models


def seed_location(db, n=1):
    locs = []
    for i in range(n):
        loc = models.Location(
            name=f"Test Loc {i}", country=f"Country {i}",
            latitude=60.0 + i, longitude=10.0 + i,
            timezone="Europe/Oslo", bg_image=f"/static/images/test{i}.jpg"
        )
        db.add(loc)
        db.commit()
        db.refresh(loc)
        locs.append(loc)
    return locs


def seed_scene(db):
    s = models.Scene(
        name="Test Scene", description="A test scene",
        preview_image="/static/images/prev.jpg",
        bg_image="/static/images/bg.gif"
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


class TestLocations:
    def test_get_locations_empty(self, client):
        r = client.get("/locations")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_get_locations_returns_seeded(self, client):
        db = TestingSessionLocal()
        seed_location(db, 2)
        db.close()

        r = client.get("/locations")
        assert r.status_code == 200
        assert len(r.json()) >= 2

    def test_get_location_by_id(self, client):
        db = TestingSessionLocal()
        loc = seed_location(db, 1)[0]
        loc_id = loc.id
        db.close()

        r = client.get(f"/locations/{loc_id}")
        assert r.status_code == 200
        assert r.json()["id"] == loc_id

    def test_get_location_not_found(self, client):
        r = client.get("/locations/99999")
        assert r.status_code == 404

    def test_location_has_required_fields(self, client):
        db = TestingSessionLocal()
        seed_location(db, 1)
        db.close()

        r = client.get("/locations")
        loc = r.json()[0]
        for field in ["id", "name", "country", "latitude", "longitude", "timezone", "bg_image"]:
            assert field in loc


class TestScenes:
    def test_get_scenes_returns_list(self, client):
        r = client.get("/scenes")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_get_scene_by_id(self, client):
        db = TestingSessionLocal()
        scene = seed_scene(db)
        scene_id = scene.id
        db.close()

        r = client.get(f"/scenes/{scene_id}")
        assert r.status_code == 200
        assert r.json()["name"] == "Test Scene"

    def test_get_scene_not_found(self, client):
        r = client.get("/scenes/99999")
        assert r.status_code == 404


class TestSounds:
    def test_get_sounds_all(self, client):
        r = client.get("/sounds")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_get_sounds_by_location(self, client):
        db = TestingSessionLocal()
        loc = seed_location(db, 1)[0]
        snd = models.Sound(
            name="Rain", file_path="/static/sounds/rain.mp3",
            weather_condition="rain", location_id=loc.id
        )
        db.add(snd)
        db.commit()
        loc_id = loc.id
        db.close()

        r = client.get(f"/sounds?location_id={loc_id}")
        assert r.status_code == 200
        sounds = r.json()
        assert any(s["location_id"] == loc_id for s in sounds)

    def test_get_sounds_by_scene(self, client):
        db = TestingSessionLocal()
        scene = seed_scene(db)
        snd = models.Sound(
            name="Forest", file_path="/static/sounds/forest.mp3",
            scene_id=scene.id
        )
        db.add(snd)
        db.commit()
        scene_id = scene.id
        db.close()

        r = client.get(f"/sounds?scene_id={scene_id}")
        assert r.status_code == 200
        sounds = r.json()
        assert any(s["scene_id"] == scene_id for s in sounds)


class TestMusic:
    def test_get_tracks_returns_list(self, client):
        r = client.get("/music")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_tracks_have_required_fields(self, client):
        db = TestingSessionLocal()
        track = models.MusicTrack(
            title="Lofi Track", file_path="/static/music/lofi.mp3", mood_tag="lofi"
        )
        db.add(track)
        db.commit()
        db.close()

        r = client.get("/music")
        t = r.json()[0]
        for field in ["id", "title", "file_path", "mood_tag"]:
            assert field in t
