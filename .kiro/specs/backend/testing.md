# BACKEND — Guía de Testing

**Proyecto:** Casanare en Movimiento  
**Framework:** pytest + pytest-asyncio + httpx  
**Versión:** 1.0

---

## 1. Stack de Testing

| Herramienta | Uso |
|-------------|-----|
| `pytest` | Runner principal de tests |
| `pytest-asyncio` | Tests de funciones async |
| `httpx.AsyncClient` | Cliente HTTP para tests de endpoints |
| `SQLite en memoria` | BD aislada por test (no toca MySQL real) |
| `pytest-cov` | Reporte de cobertura de código |
| `unittest.mock` | Mock de servicios externos (n8n, email) |

---

## 2. Instalación

```bash
pip install pytest==8.2.0 pytest-asyncio==0.23.6 pytest-cov==5.0.0 httpx==0.27.0
```

---

## 3. Configuración pytest

Crear `pytest.ini` en raíz del backend:
```ini
[pytest]
asyncio_mode = auto
testpaths = tests
filterwarnings = ignore::DeprecationWarning
```

Crear `pyproject.toml` para cobertura:
```toml
[tool.coverage.run]
source = ["app"]
omit = ["app/core/database.py", "alembic/*"]

[tool.coverage.report]
fail_under = 70
show_missing = true
```

---

## 4. Fixture Principal (conftest.py)

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User

# BD SQLite en memoria para tests
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine_test = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def usuario_data():
    return {"email": "test@test.com", "password": "password123", "nombre": "Test User"}

@pytest.fixture
def empresario_data():
    return {"email": "empresa@test.com", "password": "password123", "nombre": "Empresa Test"}

@pytest.fixture
def user_token(db, client, usuario_data):
    # Registrar y obtener token
    client.post("/api/v1/auth/register", json=usuario_data)
    resp = client.post("/api/v1/auth/login", json=usuario_data)
    return resp.json()["access_token"]

@pytest.fixture
def empresario_token(db, client, empresario_data):
    client.post("/api/v1/auth/register", json=empresario_data)
    # Cambiar rol a empresario directamente en BD
    user = db.query(User).filter_by(email=empresario_data["email"]).first()
    user.rol = "empresario"
    db.commit()
    resp = client.post("/api/v1/auth/login", json=empresario_data)
    return resp.json()["access_token"]

@pytest.fixture
def evento_publicado(db, client, empresario_token):
    resp = client.post(
        "/api/v1/eventos",
        json={
            "titulo": "Festival Llanero",
            "descripcion": "Gran festival de música llanera en Yopal",
            "categoria": "cultural",
            "fecha_inicio": "2026-09-15",
            "ubicacion": "Plaza Central, Yopal",
            "municipio": "Yopal"
        },
        headers={"Authorization": f"Bearer {empresario_token}"}
    )
    evento_id = resp.json()["id"]
    # Publicar el evento
    client.patch(
        f"/api/v1/eventos/{evento_id}/publicar",
        headers={"Authorization": f"Bearer {empresario_token}"}
    )
    return resp.json()
```

---

## 5. Ejemplos de Tests por Módulo

### test_auth.py
```python
class TestRegistro:
    def test_registro_exitoso(self, client, usuario_data):
        resp = client.post("/api/v1/auth/register", json=usuario_data)
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == usuario_data["email"]
        assert "password" not in data  # Nunca exponer password

    def test_registro_email_duplicado(self, client, usuario_data):
        client.post("/api/v1/auth/register", json=usuario_data)
        resp = client.post("/api/v1/auth/register", json=usuario_data)
        assert resp.status_code == 400
        assert "email" in resp.json()["detail"].lower()

    def test_registro_password_corto(self, client):
        resp = client.post("/api/v1/auth/register", json={
            "email": "x@x.com", "password": "123", "nombre": "X"
        })
        assert resp.status_code == 422

class TestLogin:
    def test_login_exitoso(self, client, usuario_data):
        client.post("/api/v1/auth/register", json=usuario_data)
        resp = client.post("/api/v1/auth/login", json=usuario_data)
        assert resp.status_code == 200
        assert "access_token" in resp.json()
        assert "refresh_token" in resp.json()

    def test_login_password_incorrecto(self, client, usuario_data):
        client.post("/api/v1/auth/register", json=usuario_data)
        resp = client.post("/api/v1/auth/login", json={
            **usuario_data, "password": "wrongpassword"
        })
        assert resp.status_code == 401
```

### test_eventos.py
```python
class TestListarEventos:
    def test_lista_publica_sin_token(self, client, evento_publicado):
        resp = client.get("/api/v1/eventos")
        assert resp.status_code == 200
        assert isinstance(resp.json()["items"], list)

    def test_solo_retorna_publicados(self, client, db, empresario_token):
        # Crear evento en borrador (no publicado)
        client.post("/api/v1/eventos",
            json={"titulo": "Borrador", "descripcion": "desc", ...},
            headers={"Authorization": f"Bearer {empresario_token}"}
        )
        resp = client.get("/api/v1/eventos")
        for evento in resp.json()["items"]:
            assert evento["estado"] == "publicado"

class TestCrearEvento:
    def test_crear_como_empresario(self, client, empresario_token):
        resp = client.post("/api/v1/eventos",
            json={
                "titulo": "Nuevo evento",
                "descripcion": "Descripción del evento",
                "categoria": "deportivo",
                "fecha_inicio": "2026-10-01",
                "ubicacion": "Estadio, Aguazul"
            },
            headers={"Authorization": f"Bearer {empresario_token}"}
        )
        assert resp.status_code == 201
        assert resp.json()["titulo"] == "Nuevo evento"
        assert resp.json()["estado"] == "borrador"

    def test_crear_como_usuario_normal(self, client, user_token):
        resp = client.post("/api/v1/eventos",
            json={"titulo": "x", "descripcion": "y", ...},
            headers={"Authorization": f"Bearer {user_token}"}
        )
        assert resp.status_code == 403
```

---

## 6. Comandos de Ejecución

```bash
# Correr todos los tests
pytest tests/ -v

# Correr con reporte de cobertura
pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Correr solo tests de autenticación
pytest tests/test_auth.py -v

# Correr tests que fallen primero
pytest tests/ --tb=short -x

# Ver cobertura en navegador
open htmlcov/index.html
```

---

## 7. Checklist de Calidad

Antes de marcar una tarea como completada:

- [ ] Todos los tests de la tarea pasan en verde
- [ ] No hay warnings de deprecación en pytest
- [ ] Cobertura del módulo cumple el mínimo definido en tasks.md
- [ ] Los tests de error (4xx) verifican el código HTTP correcto
- [ ] Los mocks de servicios externos están aislados (no llaman a n8n real)
- [ ] No hay hardcoding de IDs o datos en los tests (usar fixtures)
