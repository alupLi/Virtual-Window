import time
import pytest

RESPONSE_TIME_LIMIT = 0.5

class TestResponseTime:

    def _measure(self, fn):
        start = time.perf_counter()
        r = fn()
        elapsed = time.perf_counter() - start
        return r, elapsed

    def test_root_endpoint_response_time(self, client):
        _, elapsed = self._measure(lambda: client.get("/"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET / ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_locations_response_time(self, client):
        _, elapsed = self._measure(lambda: client.get("/locations"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET /locations ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_scenes_response_time(self, client):
        _, elapsed = self._measure(lambda: client.get("/scenes"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET /scenes ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_sounds_response_time(self, client):
        _, elapsed = self._measure(lambda: client.get("/sounds"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET /sounds ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_music_response_time(self, client):
        _, elapsed = self._measure(lambda: client.get("/music"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET /music ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_register_response_time(self, client):
        _, elapsed = self._measure(lambda: client.post("/auth/register", json={
            "username": "perf_user",
            "email": "perf@test.com",
            "password": "perfpass123",
        }))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"POST /auth/register ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_login_response_time(self, client):
        client.post("/auth/register", json={
            "username": "perf2", "email": "perf2@test.com", "password": "pass"
        })
        _, elapsed = self._measure(lambda: client.post("/auth/login", json={
            "email": "perf2@test.com", "password": "pass"
        }))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"POST /auth/login ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_me_response_time(self, auth_client):
        _, elapsed = self._measure(lambda: auth_client.get("/auth/me"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET /auth/me ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )

    def test_settings_response_time(self, auth_client):
        _, elapsed = self._measure(lambda: auth_client.get("/settings"))
        assert elapsed < RESPONSE_TIME_LIMIT, (
            f"GET /settings ответил за {elapsed:.3f}s > {RESPONSE_TIME_LIMIT}s"
        )
