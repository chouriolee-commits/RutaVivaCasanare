from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

# pool_pre_ping evita errores por conexiones muertas (MySQL cierra conexiones
# inactivas); pool_recycle evita el timeout por defecto de MySQL (wait_timeout).
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280,
    pool_size=10,
    max_overflow=20,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """Dependency de FastAPI: una sesión por request, cerrada siempre al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
