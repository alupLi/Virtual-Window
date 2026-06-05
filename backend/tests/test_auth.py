import pytest
import time


class TestAuthRegister:
    def test_register_success(self, client):
        r = client.post("/auth/register", json={
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "password123",
        })
        assert r.status_code == 201
        data = r.json()
        assert data["email"] == "newuser@test.com"
        assert data["username"] == "newuser"
        assert "password_hash" not in data

    def test_register_duplicate_email(self, client):
        payload = {"username": "u1", "email": "dup@test.com", "password": "pass"}
        client.post("/auth/register", json=payload)
        r = client.post("/auth/register", json=payload)
        assert r.status_code == 400
        assert "already" in r.json()["detail"].lower()

    def test_register_invalid_email(self, client):
        r = client.post("/auth/register", json={
            "username": "u2", "email": "not-an-email", "password": "pass"
        })
        assert r.status_code == 422

    def test_register_missing_fields(self, client):
        r = client.post("/auth/register", json={"username": "u3"})
        assert r.status_code == 422


class TestAuthLogin:
    def test_login_success(self, client):
        client.post("/auth/register", json={
            "username": "loginuser", "email": "login@test.com", "password": "pass123"
        })
        r = client.post("/auth/login", json={
            "email": "login@test.com", "password": "pass123"
        })
        assert r.status_code == 200
        assert r.json()["email"] == "login@test.com"

    def test_login_wrong_password(self, client):
        client.post("/auth/register", json={
            "username": "lu2", "email": "lu2@test.com", "password": "correctpass"
        })
        r = client.post("/auth/login", json={
            "email": "lu2@test.com", "password": "wrongpass"
        })
        assert r.status_code == 401
        assert "invalid" in r.json()["detail"].lower()

    def test_login_nonexistent_user(self, client):
        r = client.post("/auth/login", json={
            "email": "ghost@test.com", "password": "pass"
        })
        assert r.status_code == 401

    def test_login_sets_cookie(self, client):
        client.post("/auth/register", json={
            "username": "ck", "email": "ck@test.com", "password": "pass"
        })
        r = client.post("/auth/login", json={"email": "ck@test.com", "password": "pass"})
        assert "access_token" in r.cookies


class TestAuthMe:
    def test_me_unauthenticated(self, client):
        r = client.get("/auth/me")
        assert r.status_code == 401

    def test_me_authenticated(self, auth_client):
        r = auth_client.get("/auth/me")
        assert r.status_code == 200
        assert "email" in r.json()

    def test_logout_clears_session(self, auth_client):
        auth_client.post("/auth/logout")
        r = auth_client.get("/auth/me")
        assert r.status_code == 401
