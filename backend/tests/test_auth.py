from fastapi.testclient import TestClient


def test_register_success(client: TestClient) -> None:
    r = client.post("/api/v1/auth/register", json={"nombre": "Ana", "email": "ana@example.com", "password": "password123"})
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "ana@example.com"
    assert "contrasena_hash" not in body
    assert "password" not in body


def test_register_duplicate_email(client: TestClient) -> None:
    payload = {"nombre": "Ana", "email": "ana@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    r = client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 409


def test_register_weak_password(client: TestClient) -> None:
    r = client.post("/api/v1/auth/register", json={"nombre": "Ana", "email": "ana@example.com", "password": "123"})
    assert r.status_code == 422


def test_login_success(client: TestClient) -> None:
    payload = {"nombre": "Ana", "email": "ana@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    r = client.post("/api/v1/auth/login", json={"email": "ana@example.com", "password": "password123"})
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_login_wrong_password(client: TestClient) -> None:
    payload = {"nombre": "Ana", "email": "ana@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    r = client.post("/api/v1/auth/login", json={"email": "ana@example.com", "password": "otra_clave"})
    assert r.status_code == 401


def test_login_nonexistent_user(client: TestClient) -> None:
    r = client.post("/api/v1/auth/login", json={"email": "no_existe@example.com", "password": "password123"})
    assert r.status_code == 401


def test_refresh_token(client: TestClient) -> None:
    payload = {"nombre": "Ana", "email": "ana@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    login = client.post("/api/v1/auth/login", json={"email": "ana@example.com", "password": "password123"})
    refresh_token = login.json()["refresh_token"]

    r = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_refresh_with_access_token_rejected(client: TestClient) -> None:
    """Un access_token no debe servir como refresh_token (evita escalarlo)."""
    payload = {"nombre": "Ana", "email": "ana@example.com", "password": "password123"}
    client.post("/api/v1/auth/register", json=payload)
    login = client.post("/api/v1/auth/login", json={"email": "ana@example.com", "password": "password123"})
    access_token = login.json()["access_token"]

    r = client.post("/api/v1/auth/refresh", json={"refresh_token": access_token})
    assert r.status_code == 401


def test_protected_without_token(client: TestClient) -> None:
    r = client.get("/api/v1/usuarios/me")
    assert r.status_code == 401
