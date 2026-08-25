# BACKEND — Diseño Técnico Detallado

**Proyecto:** Casanare en Movimiento  
**Tecnología:** Python 3.11 + FastAPI + SQLAlchemy 2.0  
**Versión:** 1.0

---

## 1. Estructura de Módulos

```
backend/
├── app/
│   ├── main.py                    # Entrada: crea FastAPI app, registra routers, CORS
│   ├── core/
│   │   ├── config.py              # Settings con pydantic-settings (lee .env)
│   │   ├── database.py            # Engine SQLAlchemy, SessionLocal, Base
│   │   └── security.py            # hash_password, verify_password, create_token, decode_token
│   ├── models/                    # ORM SQLAlchemy (tablas)
│   │   ├── user.py                # Modelo User
│   │   ├── evento.py              # Modelo Evento
│   │   ├── agenda.py              # Modelo AgendaItem
│   │   └── ia_chat.py             # Modelos Conversacion + Mensaje
│   ├── schemas/                   # Pydantic v2 (validación entrada/salida)
│   │   ├── user.py
│   │   ├── evento.py
│   │   ├── agenda.py
│   │   └── ia_chat.py
│   ├── routers/                   # Controladores HTTP
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── eventos.py
│   │   ├── agenda.py
│   │   └── ia_chat.py
│   ├── services/                  # Lógica de negocio desacoplada
│   │   ├── auth_service.py
│   │   ├── evento_service.py
│   │   ├── agenda_service.py
│   │   └── ia_service.py
│   └── dependencies.py            # get_db, get_current_user, require_empresario
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── conftest.py                # Fixtures: client, db de prueba, usuarios mock
│   ├── test_auth.py
│   ├── test_eventos.py
│   ├── test_agenda.py
│   └── test_ia_chat.py
├── .env
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 2. Diseño de Modelos ORM

### modelo: User
```python
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    email         = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre        = Column(String(100))
    telefono      = Column(String(20))
    rol           = Column(Enum("usuario", "empresario"), default="usuario")
    activo        = Column(Boolean, default=True)
    created_at    = Column(DateTime, default=func.now())
    updated_at    = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    eventos       = relationship("Evento", back_populates="organizador")
    conversaciones = relationship("IAConversacion", back_populates="usuario")
```

### modelo: Evento
```python
class Evento(Base):
    __tablename__ = "eventos"

    id             = Column(Integer, primary_key=True, index=True)
    titulo         = Column(String(200), nullable=False)
    descripcion    = Column(Text, nullable=False)
    categoria      = Column(Enum("cultural","deportivo","turistico","gastronomico","otro"))
    fecha_inicio   = Column(Date, nullable=False)
    fecha_fin      = Column(Date)
    hora_inicio    = Column(Time)
    hora_fin       = Column(Time)
    ubicacion      = Column(String(300), nullable=False)
    municipio      = Column(String(100))
    aforo          = Column(Integer)
    imagen_url     = Column(String(500))
    estado         = Column(Enum("borrador","publicado","cancelado"), default="borrador")
    organizador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at     = Column(DateTime, default=func.now())
    updated_at     = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relaciones
    organizador    = relationship("User", back_populates="eventos")
    agenda_items   = relationship("AgendaItem", back_populates="evento",
                                  order_by="AgendaItem.hora_inicio")
```

### modelo: AgendaItem
```python
class AgendaItem(Base):
    __tablename__ = "agenda_items"

    id                = Column(Integer, primary_key=True)
    evento_id         = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    hora_inicio       = Column(Time, nullable=False)
    hora_fin          = Column(Time)
    titulo_actividad  = Column(String(200), nullable=False)
    descripcion       = Column(Text)
    ponente           = Column(String(150))
    orden             = Column(Integer, default=0)
    created_at        = Column(DateTime, default=func.now())

    evento            = relationship("Evento", back_populates="agenda_items")
```

---

## 3. Diseño de Schemas Pydantic

### schemas/evento.py (ejemplo clave)
```python
from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional
from enum import Enum

class CategoriaEnum(str, Enum):
    cultural     = "cultural"
    deportivo    = "deportivo"
    turistico    = "turistico"
    gastronomico = "gastronomico"
    otro         = "otro"

class EstadoEnum(str, Enum):
    borrador   = "borrador"
    publicado  = "publicado"
    cancelado  = "cancelado"

class EventoCreate(BaseModel):
    titulo:       str = Field(..., min_length=3, max_length=200)
    descripcion:  str = Field(..., min_length=10)
    categoria:    CategoriaEnum
    fecha_inicio: date
    fecha_fin:    Optional[date] = None
    hora_inicio:  Optional[time] = None
    hora_fin:     Optional[time] = None
    ubicacion:    str = Field(..., min_length=5)
    municipio:    Optional[str] = None
    aforo:        Optional[int] = Field(None, gt=0)
    imagen_url:   Optional[str] = None

class EventoUpdate(EventoCreate):
    titulo:       Optional[str] = None
    descripcion:  Optional[str] = None
    categoria:    Optional[CategoriaEnum] = None
    fecha_inicio: Optional[date] = None
    ubicacion:    Optional[str] = None

class EventoResponse(EventoCreate):
    id:             int
    estado:         EstadoEnum
    organizador_id: int
    created_at:     datetime

    model_config = ConfigDict(from_attributes=True)
```

---

## 4. Diseño de Seguridad

### core/security.py
```python
# Funciones clave a implementar:

def hash_password(password: str) -> str:
    # Usa passlib CryptContext con bcrypt, rounds=12
    ...

def verify_password(plain: str, hashed: str) -> bool:
    # Verifica contra el hash bcrypt
    ...

def create_access_token(data: dict) -> str:
    # Expira en ACCESS_TOKEN_EXPIRE_MINUTES
    # Payload: sub=user_id, rol=user.rol, exp=...
    ...

def create_refresh_token(data: dict) -> str:
    # Expira en REFRESH_TOKEN_EXPIRE_DAYS
    ...

def decode_token(token: str) -> dict:
    # Decodifica y valida, lanza HTTPException 401 si inválido
    ...
```

### dependencies.py
```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Decodifica JWT → busca usuario en BD → retorna User
    ...

async def require_empresario(
    current_user: User = Depends(get_current_user)
) -> User:
    # Valida rol == "empresario", lanza HTTPException 403 si no
    ...

async def require_evento_owner(
    evento_id: int,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
) -> Evento:
    # Busca evento, valida que organizador_id == current_user.id
    ...
```

---

## 5. Diseño del Servicio IA

### services/ia_service.py
```python
import httpx
from app.core.config import settings

async def enviar_consulta_ia(
    pregunta: str,
    contexto_evento: dict,
    historial: list[dict]
) -> str:
    """
    Construye el payload para n8n y retorna la respuesta del LLM.

    contexto_evento = {
        "titulo": str,
        "descripcion": str,
        "fecha_inicio": str,
        "ubicacion": str,
        "municipio": str,
        "agenda": [{"hora": str, "actividad": str, "ponente": str}]
    }
    historial = [{"rol": "user"|"assistant", "contenido": str}]
    """
    payload = {
        "pregunta": pregunta,
        "contexto": contexto_evento,
        "historial": historial[-10:]  # Últimos 10 mensajes para no exceder contexto
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            settings.N8N_WEBHOOK_CHAT_URL,
            json=payload,
            headers={"X-API-Key": settings.N8N_API_KEY}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("respuesta", "No pude generar una respuesta.")
```

---

## 6. main.py — Estructura

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, eventos, agenda, ia_chat

app = FastAPI(
    title="Casanare en Movimiento API",
    version="1.0.0",
    description="API para la plataforma de eventos de Casanare"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,    prefix="/api/v1/auth",    tags=["Autenticación"])
app.include_router(users.router,   prefix="/api/v1/users",   tags=["Usuarios"])
app.include_router(eventos.router, prefix="/api/v1",         tags=["Eventos"])
app.include_router(agenda.router,  prefix="/api/v1",         tags=["Agenda"])
app.include_router(ia_chat.router, prefix="/api/v1/ia",      tags=["IA Chat"])

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
```
