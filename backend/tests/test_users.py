"""Tests for user accounts and RBAC."""

import pytest


@pytest.mark.anyio
async def test_register_user(client):
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "admin@test.com", "password": "secret123", "role": "admin"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "admin@test.com"
    assert data["role"] == "admin"
    assert data["is_active"] is True


@pytest.mark.anyio
async def test_register_duplicate_email(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dupe@test.com", "password": "pass1"},
    )
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "dupe@test.com", "password": "pass2"},
    )
    assert resp.status_code == 409


@pytest.mark.anyio
async def test_login_success(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "login@test.com", "password": "secret"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "login@test.com", "password": "secret"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "login@test.com"


@pytest.mark.anyio
async def test_login_wrong_password(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "wrong@test.com", "password": "correct"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@test.com", "password": "incorrect"},
    )
    assert resp.status_code == 401


@pytest.mark.anyio
async def test_list_users(client):
    await client.post(
        "/api/v1/auth/register",
        json={"email": "list@test.com", "password": "pass"},
    )
    resp = await client.get("/api/v1/auth/users")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 1


@pytest.mark.anyio
async def test_jwt_token_is_valid():
    """Test JWT creation and verification."""
    from app.services.user_service import _create_jwt, decode_jwt

    token = _create_jwt("user123", "test@test.com", "admin")
    payload = decode_jwt(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["email"] == "test@test.com"
    assert payload["role"] == "admin"
