from __future__ import annotations

from fastapi.testclient import TestClient


def register_and_login(client: TestClient, email: str = "writer@example.com") -> str:
    response = client.post("/api/v1/auth/register", json={"email": email, "password": "StrongPass123!", "display_name": "Worldwright"})
    assert response.status_code == 201
    login = client.post("/api/v1/auth/login", json={"email": email, "password": "StrongPass123!"})
    assert login.status_code == 200
    return login.json()["access_token"]


def test_register_login_and_create_world(client: TestClient) -> None:
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "name": "Clockwork Atlas",
        "genre": "Science Fantasy",
        "tone": "Elegant, dangerous, hopeful",
        "premise": "A sky-city archive predicts wars before anyone declares them.",
        "themes_json": ["Memory", "Power", "Identity"],
    }
    response = client.post("/api/v1/worlds", json=payload, headers=headers)
    assert response.status_code == 201
    body = response.json()
    assert body["slug"] == "clockwork-atlas"
    assert body["default_visibility"] == "PRIVATE"

    worlds = client.get("/api/v1/worlds", headers=headers)
    assert worlds.status_code == 200
    assert len(worlds.json()) == 1


def test_world_dashboard_requires_owner(client: TestClient) -> None:
    owner_token = register_and_login(client, "owner@example.com")
    other_token = register_and_login(client, "other@example.com")
    world = client.post("/api/v1/worlds", json={"name": "Hidden Coast"}, headers={"Authorization": f"Bearer {owner_token}"}).json()

    forbidden = client.get(f"/api/v1/worlds/{world['id']}/dashboard", headers={"Authorization": f"Bearer {other_token}"})
    assert forbidden.status_code == 404

    allowed = client.get(f"/api/v1/worlds/{world['id']}/dashboard", headers={"Authorization": f"Bearer {owner_token}"})
    assert allowed.status_code == 200
    assert allowed.json()["stats"]["total_entries"] == 0


def test_validation_rejects_short_password(client: TestClient) -> None:
    response = client.post("/api/v1/auth/register", json={"email": "bad@example.com", "password": "short", "display_name": "Bad"})
    assert response.status_code == 422


def test_login_accepts_trimmed_email(client: TestClient) -> None:
    token = register_and_login(client, "trimmed@example.com")
    assert token
    login = client.post("/api/v1/auth/login", json={"email": "  trimmed@example.com  ", "password": "StrongPass123!"})
    assert login.status_code == 200
