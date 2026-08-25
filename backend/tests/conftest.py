from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models import Empresario, Evento, Producto, Stand  # noqa: F401  (registran las tablas en Base.metadata)

# BD de pruebas: SQLite en memoria, totalmente independiente de la BD real de desarrollo.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _registrar_y_loguear(client: TestClient, email: str) -> str:
    client.post("/api/v1/auth/register", json={"nombre": "Usuario Test", "email": email, "password": "password123"})
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    return resp.json()["access_token"]


@pytest.fixture()
def auth_headers(client: TestClient) -> dict[str, str]:
    token = _registrar_y_loguear(client, "usuario_test@example.com")
    return {"Authorization": f"Bearer {token}"}
