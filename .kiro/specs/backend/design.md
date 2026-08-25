# BACKEND — Diseño Técnico Detallado

**Proyecto:** Casanare en Movimiento  
**Tecnología:** Python 3.11 + FastAPI + SQLAlchemy 2.0  
**Versión:** 3.0 — Flujo con roles diferenciados + módulo /empresa

---

## 1. Estructura de Módulos

```
backend/
├── app/
│   ├── main.py                    # FastAPI app, routers, CORS, middleware
│   ├── core/
│   │   ├── config.py              # pydantic-settings (lee .env)
│   │   ├── database.py            # Engine, SessionLocal, Base
│   │   └── security.py            # bcrypt, JWT create/decode
│   │
│   ├── models/                    # ORM SQLAlchemy — una clase = una tabla
│   │   ├── __init__.py            # Importa todos los modelos (Alembic los descubre)
│   │   ├── user.py                # User
│   │   ├── evento.py              # Evento
│   │   ├── agenda.py              # AgendaItem
│   │   ├── sesion_empresa.py      # SesionEmpresa (evento activo del empresario)
│   │   └── ia_chat.py             # IAConversacion + IAMensaje
│   │
│   ├── schemas/                   # Pydantic v2 — validación entrada/salida
│   │   ├── auth.py                # LoginRequest, RegisterRequest, TokenResponse
│   │   ├── user.py                # UserCreate, UserResponse, UserUpdate
│   │   ├── evento.py              # EventoCreate, EventoUpdate, EventoResponse
│   │   ├── agenda.py              # AgendaItemCreate, AgendaItemResponse
│   │   ├── empresa.py             # SesionEmpresaCreate, PanelResponse
│   │   └── ia_chat.py             # ChatRequest, ChatResponse, MensajeResponse
│   │
│   ├── routers/                   # Controladores HTTP — uno por dominio
│   │   ├── auth.py                # /auth/*
│   │   ├── users.py               # /users/*
│   │   ├── eventos.py             # /eventos/* (público)
│   │   ├── empresa.py             # /empresa/* (solo empresario)
│   │   └── ia_chat.py             # /ia/* (cliente + empresario)
│   │
│   ├── services/                  # Lógica de negocio desacoplada de HTTP
│   │   ├── auth_service.py
│   │   ├── evento_service.py
│   │   ├── empresa_service.py     # NUEVO: lógica del panel empresario
│   │   └── ia_service.py
│   │
│   └── dependencies.py            # get_db, get_current_user, require_rol
│
├── alembic/
│   ├── env.py
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_eventos.py
│   ├── test_empresa.py            # NUEVO
│   └── test_ia_chat.py
│
├── .env
├── .env.example
├── requirements.txt
└── Dockerfile
```

---

## 2. Modelos ORM — Diseño Completo

### models/user.py
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class RolEnum(str, enum.Enum):
    usuario    = "usuario"
    empresario = "empresario"

class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    email         = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre        = Column(String(100), nullable=False)
    telefono      = Column(String(20))
    rol           = Column(Enum(RolEnum), default=RolEnum.usuario, nullable=False)
    activo        = Column(Boolean, default=True, nullable=False)
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    eventos           = relationship("Evento", back_populates="organizador")
    sesion_empresa    = relationship("SesionEmpresa", back_populates="user",
                                     uselist=False)  # uno a uno
    conversaciones    = relationship("IAConversacion", back_populates="usuario")
```

### models/evento.py
```python
from sqlalchemy import (Column, Integer, String, Text, Date, Time,
                        Boolean, DateTime, Enum, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class CategoriaEnum(str, enum.Enum):
    cultural     = "cultural"
    deportivo    = "deportivo"
    turistico    = "turistico"
    gastronomico = "gastronomico"
    otro         = "otro"

class EstadoEnum(str, enum.Enum):
    borrador   = "borrador"
    publicado  = "publicado"
    cancelado  = "cancelado"

class Evento(Base):
    __tablename__ = "eventos"

    id             = Column(Integer, primary_key=True, index=True)
    titulo         = Column(String(200), nullable=False)
    descripcion    = Column(Text, nullable=False)
    categoria      = Column(Enum(CategoriaEnum), nullable=False)
    fecha_inicio   = Column(Date, nullable=False)
    fecha_fin      = Column(Date)
    hora_inicio    = Column(Time)
    hora_fin       = Column(Time)
    ubicacion      = Column(String(300), nullable=False)
    municipio      = Column(String(100))
    aforo          = Column(Integer)
    imagen_url     = Column(String(500))
    estado         = Column(Enum(EstadoEnum), default=EstadoEnum.borrador, nullable=False)
    organizador_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    organizador  = relationship("User", back_populates="eventos")
    agenda_items = relationship("AgendaItem", back_populates="evento",
                                order_by="AgendaItem.hora_inicio",
                                cascade="all, delete-orphan")
    sesiones     = relationship("SesionEmpresa", back_populates="evento")
```

### models/sesion_empresa.py  ← NUEVO
```python
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class SesionEmpresa(Base):
    """
    Registra cuál evento está gestionando activamente cada empresario.
    Un empresario solo puede tener UN evento activo a la vez.
    Se actualiza cada vez que el empresario selecciona un evento diferente.
    """
    __tablename__ = "sesiones_empresa"

    id        = Column(Integer, primary_key=True)
    user_id   = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones
    user   = relationship("User", back_populates="sesion_empresa")
    evento = relationship("Evento", back_populates="sesiones")
```

### models/agenda.py
```python
from sqlalchemy import Column, Integer, String, Text, Time, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class AgendaItem(Base):
    __tablename__ = "agenda_items"

    id               = Column(Integer, primary_key=True)
    evento_id        = Column(Integer, ForeignKey("eventos.id",
                              ondelete="CASCADE"), nullable=False)
    hora_inicio      = Column(Time, nullable=False)
    hora_fin         = Column(Time)
    titulo_actividad = Column(String(200), nullable=False)
    descripcion      = Column(Text)
    ponente          = Column(String(150))
    orden            = Column(Integer, default=0)
    created_at       = Column(DateTime, server_default=func.now())

    evento = relationship("Evento", back_populates="agenda_items")
```

### models/ia_chat.py
```python
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class RolMensajeEnum(str, enum.Enum):
    user      = "user"
    assistant = "assistant"

class RolUsuarioChat(str, enum.Enum):
    cliente    = "cliente"
    empresario = "empresario"

class IAConversacion(Base):
    """
    Una conversación por (usuario × evento × rol_usuario).
    Permite que el mismo usuario tenga conversaciones separadas
    como cliente (preguntas del evento) y como empresario (dudas de gestión).
    """
    __tablename__ = "ia_conversaciones"

    id          = Column(Integer, primary_key=True)
    usuario_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    evento_id   = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    rol_usuario = Column(Enum(RolUsuarioChat), nullable=False)
    created_at  = Column(DateTime, server_default=func.now())

    usuario  = relationship("User", back_populates="conversaciones")
    mensajes = relationship("IAMensaje", back_populates="conversacion",
                            order_by="IAMensaje.created_at",
                            cascade="all, delete-orphan")

class IAMensaje(Base):
    __tablename__ = "ia_mensajes"

    id              = Column(Integer, primary_key=True)
    conversacion_id = Column(Integer, ForeignKey("ia_conversaciones.id",
                             ondelete="CASCADE"), nullable=False)
    rol             = Column(Enum(RolMensajeEnum), nullable=False)
    contenido       = Column(Text, nullable=False)
    created_at      = Column(DateTime, server_default=func.now())

    conversacion = relationship("IAConversacion", back_populates="mensajes")
```

---

## 3. Schemas Pydantic — Diseño Completo

### schemas/auth.py
```python
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email:    EmailStr
    password: str = Field(..., min_length=8)

class RegisterRequest(BaseModel):
    nombre:   str      = Field(..., min_length=2, max_length=100)
    email:    EmailStr
    password: str      = Field(..., min_length=8)
    rol:      str      = Field(..., pattern="^(usuario|empresario)$")

class TokenResponse(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"
    rol:           str  # incluido para que el frontend sepa a dónde redirigir
```

### schemas/empresa.py  ← NUEVO
```python
from pydantic import BaseModel
from app.schemas.evento import EventoResponse
from app.schemas.agenda import AgendaItemResponse
from typing import Optional

class SeleccionarEventoRequest(BaseModel):
    evento_id: int

class PanelEmpresarioResponse(BaseModel):
    """Respuesta unificada del panel del empresario."""
    evento:        EventoResponse
    agenda:        list[AgendaItemResponse]
    tiene_evento:  bool = True

class InicioEmpresarioResponse(BaseModel):
    """Respuesta para la pantalla de inicio del empresario."""
    mis_eventos:   list[EventoResponse]
    evento_activo: Optional[EventoResponse] = None
    tiene_evento:  bool
```

### schemas/ia_chat.py
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class ChatRequest(BaseModel):
    evento_id: int
    mensaje:   str = Field(..., min_length=1, max_length=1000)
    # rol_chat se toma del JWT — no lo envía el cliente
    # "cliente": preguntas sobre el evento
    # "empresario": preguntas sobre gestión

class ChatResponse(BaseModel):
    respuesta:        str
    conversacion_id:  int

class MensajeResponse(BaseModel):
    id:         int
    rol:        Literal["user", "assistant"]
    contenido:  str
    created_at: datetime

    model_config = {"from_attributes": True}
```

---

## 4. Diseño de Routers

### routers/auth.py
```python
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Registro unificado. El campo `rol` en el body determina
    si se registra como usuario o empresario.
    Lanza 400 si el email ya existe.
    """

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login unificado.
    El JWT retornado incluye `rol` en el payload.
    El frontend usa ese rol para redirigir:
      - rol='usuario'    → /
      - rol='empresario' → /empresa/inicio
    """

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str, db: Session = Depends(get_db)):
    """Renueva el access_token usando el refresh_token."""
```

### routers/empresa.py  ← NUEVO (módulo central del empresario)
```python
router = APIRouter(dependencies=[Depends(require_empresario)])

@router.get("/inicio", response_model=InicioEmpresarioResponse)
async def inicio_empresario(
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    Pantalla de inicio del empresario.
    Retorna:
      - mis_eventos: lista de todos sus eventos
      - evento_activo: el evento de su sesión activa (si tiene)
      - tiene_evento: bool de conveniencia para el frontend
    """

@router.post("/seleccionar-evento", response_model=PanelEmpresarioResponse)
async def seleccionar_evento(
    data: SeleccionarEventoRequest,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    El empresario elige qué evento va a gestionar.
    Crea o actualiza la fila en sesiones_empresa.
    Retorna el PanelEmpresarioResponse con los datos del evento + agenda.
    """

@router.get("/panel", response_model=PanelEmpresarioResponse)
async def get_panel(
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    Datos completos del panel del empresario:
    evento activo + agenda actualizada.
    Lanza 404 si no tiene evento activo seleccionado.
    """

@router.put("/panel/evento", response_model=EventoResponse)
async def actualizar_evento(
    data: EventoUpdate,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """Actualiza los datos del evento activo del empresario."""

@router.patch("/panel/publicar", response_model=EventoResponse)
async def toggle_publicar(
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    Alterna el estado del evento activo entre 'publicado' y 'borrador'.
    Un evento publicado se hace visible para todos los usuarios.
    """

@router.get("/panel/agenda", response_model=list[AgendaItemResponse])
async def get_agenda(
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """Retorna agenda ordenada por hora_inicio del evento activo."""

@router.post("/panel/agenda", response_model=AgendaItemResponse, status_code=201)
async def agregar_agenda(
    data: AgendaItemCreate,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """Agrega un ítem de agenda al evento activo."""

@router.put("/panel/agenda/{item_id}", response_model=AgendaItemResponse)
async def editar_agenda(
    item_id: int,
    data: AgendaItemCreate,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """Edita un ítem de agenda. Verifica que pertenezca al evento activo."""

@router.delete("/panel/agenda/{item_id}", status_code=204)
async def eliminar_agenda(
    item_id: int,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """Elimina un ítem de agenda. Verifica que pertenezca al evento activo."""

@router.post("/eventos", response_model=EventoResponse, status_code=201)
async def crear_evento(
    data: EventoCreate,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo evento y automáticamente lo establece como evento
    activo en la sesión del empresario. Dispara notificación via n8n.
    """
```

### routers/ia_chat.py  (cliente + empresario)
```python
router = APIRouter()

# ── Endpoints del CLIENTE ──────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat_cliente(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Chat del cliente sobre un evento específico.
    Contexto del prompt: info del evento + agenda.
    System prompt: 'Eres el asistente del evento X. Responde dudas sobre el evento.'
    """

@router.get("/conversacion/{evento_id}", response_model=list[MensajeResponse])
async def historial_cliente(
    evento_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Historial de la conversación cliente sobre ese evento."""

# ── Endpoints del EMPRESARIO ───────────────────────────────────────────

@router.post("/empresa/chat", response_model=ChatResponse)
async def chat_empresario(
    data: ChatRequest,
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    Chat del empresario sobre su propio evento (dudas de gestión).
    Contexto del prompt: info del evento + agenda actual.
    System prompt diferente: 'Eres un asistente de gestión de eventos.
    Ayuda al organizador con dudas sobre cómo gestionar su evento X.'
    """

@router.get("/empresa/conversacion", response_model=list[MensajeResponse])
async def historial_empresario(
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """Historial del chat del empresario sobre su evento activo."""
```

---

## 5. Servicio Empresa — Lógica Central

### services/empresa_service.py
```python
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.sesion_empresa import SesionEmpresa
from app.models.evento import Evento
from app.models.user import User

def get_evento_activo(db: Session, user_id: int) -> Evento:
    """
    Obtiene el evento activo de la sesión del empresario.
    Lanza 404 si no tiene evento seleccionado.
    """
    sesion = db.query(SesionEmpresa).filter_by(user_id=user_id).first()
    if not sesion:
        raise HTTPException(
            status_code=404,
            detail="No tienes un evento activo. Selecciona o crea uno primero."
        )
    evento = db.query(Evento).filter_by(id=sesion.evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="El evento activo ya no existe.")
    return evento

def seleccionar_evento(db: Session, user_id: int, evento_id: int) -> Evento:
    """
    Establece el evento activo del empresario.
    Si ya tiene sesión, la actualiza. Si no, la crea.
    Verifica que el evento pertenezca al empresario.
    """
    # Validar ownership
    evento = db.query(Evento).filter_by(
        id=evento_id, organizador_id=user_id
    ).first()
    if not evento:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso sobre este evento."
        )
    # Upsert de sesión
    sesion = db.query(SesionEmpresa).filter_by(user_id=user_id).first()
    if sesion:
        sesion.evento_id = evento_id
    else:
        sesion = SesionEmpresa(user_id=user_id, evento_id=evento_id)
        db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return evento

def get_mis_eventos(db: Session, user_id: int) -> list[Evento]:
    """Lista todos los eventos del empresario, ordenados por fecha desc."""
    return (
        db.query(Evento)
        .filter_by(organizador_id=user_id)
        .order_by(Evento.created_at.desc())
        .all()
    )

def crear_evento_y_seleccionar(
    db: Session,
    data: dict,
    user_id: int
) -> Evento:
    """
    Crea un nuevo evento y automáticamente lo establece como activo.
    Retorna el evento creado.
    """
    evento = Evento(**data, organizador_id=user_id)
    db.add(evento)
    db.flush()  # obtener el id sin commit
    # Establecer como evento activo
    seleccionar_evento(db, user_id, evento.id)
    db.commit()
    db.refresh(evento)
    return evento
```

---

## 6. Servicio IA — Contextos Diferenciados

### services/ia_service.py
```python
import httpx
from app.core.config import settings
from app.models.evento import Evento
from app.models.agenda import AgendaItem

def construir_contexto_evento(evento: Evento, agenda: list[AgendaItem]) -> dict:
    """Construye el dict de contexto que se envía a n8n."""
    return {
        "titulo":      evento.titulo,
        "descripcion": evento.descripcion,
        "fecha_inicio": str(evento.fecha_inicio),
        "hora_inicio":  str(evento.hora_inicio) if evento.hora_inicio else None,
        "ubicacion":   evento.ubicacion,
        "municipio":   evento.municipio,
        "aforo":       evento.aforo,
        "agenda": [
            {
                "hora":       str(item.hora_inicio),
                "actividad":  item.titulo_actividad,
                "ponente":    item.ponente or "",
                "descripcion": item.descripcion or ""
            }
            for item in agenda
        ]
    }

SYSTEM_PROMPTS = {
    "cliente": (
        "Eres el asistente virtual del evento '{titulo}'. "
        "Solo respondes preguntas sobre este evento. "
        "Si te preguntan algo ajeno al evento, redirige amablemente. "
        "Responde en español, de forma amigable y concisa."
    ),
    "empresario": (
        "Eres un asistente experto en gestión de eventos para el organizador de '{titulo}'. "
        "Ayudas al organizador con dudas sobre cómo gestionar, publicar y organizar su evento. "
        "Conoces todos los detalles del evento y su agenda actual. "
        "Responde en español, de forma práctica y directa."
    )
}

async def enviar_consulta_ia(
    pregunta: str,
    contexto_evento: dict,
    historial: list[dict],
    rol_usuario: str  # "cliente" | "empresario"
) -> str:
    """
    Envía la consulta a n8n con el prompt y contexto adecuados según el rol.
    """
    titulo = contexto_evento.get("titulo", "")
    system_prompt = SYSTEM_PROMPTS[rol_usuario].format(titulo=titulo)

    payload = {
        "system_prompt": system_prompt,
        "pregunta":      pregunta,
        "contexto":      contexto_evento,
        "historial":     historial[-10:],
        "rol_usuario":   rol_usuario
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            settings.N8N_WEBHOOK_CHAT_URL,
            json=payload,
            headers={"X-API-Key": settings.N8N_API_KEY}
        )
        resp.raise_for_status()
        return resp.json().get("respuesta", "No pude generar una respuesta.")
```

---

## 7. Dependencies — Guards de Autorización

### dependencies.py
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, RolEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Valida JWT y retorna el usuario. Lanza 401 si inválido."""
    payload = decode_token(token)
    user = db.query(User).filter_by(id=int(payload["sub"])).first()
    if not user or not user.activo:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo.")
    return user

async def require_empresario(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verifica que el usuario sea empresario. Lanza 403 si no."""
    if current_user.rol != RolEnum.empresario:
        raise HTTPException(
            status_code=403,
            detail="Acceso restringido a organizadores de eventos."
        )
    return current_user

async def get_evento_activo_dep(
    current_user: User = Depends(require_empresario),
    db: Session = Depends(get_db)
):
    """
    Dependency que obtiene el evento activo del empresario.
    Combina require_empresario + get_evento_activo del service.
    """
    from app.services.empresa_service import get_evento_activo
    return get_evento_activo(db, current_user.id)
```

---

## 8. main.py — Registro de Routers

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, users, eventos, empresa, ia_chat

app = FastAPI(
    title="Casanare en Movimiento API",
    version="3.0.0",
    description="Plataforma de eventos para el departamento de Casanare",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas públicas y de usuario
app.include_router(auth.router,    prefix="/api/v1/auth",    tags=["Auth"])
app.include_router(users.router,   prefix="/api/v1/users",   tags=["Usuarios"])
app.include_router(eventos.router, prefix="/api/v1/eventos", tags=["Eventos — Público"])

# Rutas exclusivas del empresario
app.include_router(empresa.router, prefix="/api/v1/empresa", tags=["Empresa — Panel"])

# Rutas de IA (cliente + empresario — diferenciadas internamente)
app.include_router(ia_chat.router, prefix="/api/v1/ia",      tags=["IA Chat"])

@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "version": "3.0.0"}
```

---

## 9. Flujo de Datos — Chat IA Diferenciado

```
ROL CLIENTE:
─────────────────────────────────────────────────────────────
POST /ia/chat  { evento_id, mensaje }
        │
        ▼
Valida JWT → obtiene user (rol=usuario)
        │
        ▼
Busca/crea IAConversacion { usuario_id, evento_id, rol_usuario="cliente" }
        │
        ▼
Obtiene historial de ia_mensajes de esa conversación
        │
        ▼
Construye contexto = { titulo, descripcion, fecha, ubicacion, agenda[] }
        │
        ▼
ia_service.enviar_consulta_ia(
    pregunta, contexto, historial, rol_usuario="cliente"
)
System prompt: "Eres el asistente del evento X. Responde dudas..."
        │
        ▼
Guarda mensaje usuario + respuesta asistente en ia_mensajes
        │
        ▼
Retorna { respuesta, conversacion_id }


ROL EMPRESARIO:
─────────────────────────────────────────────────────────────
POST /ia/empresa/chat  { mensaje }  (sin evento_id — usa el activo)
        │
        ▼
Valida JWT → obtiene user (rol=empresario)
        │
        ▼
Obtiene evento activo de sesiones_empresa
        │
        ▼
Busca/crea IAConversacion { usuario_id, evento_id, rol_usuario="empresario" }
        │
        ▼
Construye contexto = { titulo, descripcion, fecha, ubicacion, agenda[] }
        │
        ▼
ia_service.enviar_consulta_ia(
    pregunta, contexto, historial, rol_usuario="empresario"
)
System prompt: "Eres asistente de gestión de eventos para el organizador de X..."
        │
        ▼
Guarda + retorna respuesta
```

---

## 10. Variables de Entorno (.env.example)

```env
# ── Base de datos ─────────────────────────────────────────────
DATABASE_URL=mysql+pymysql://app_user:app_pass@db:3306/casanare_eventos

# ── Seguridad JWT ─────────────────────────────────────────────
SECRET_KEY=genera_con__python_-c_"import secrets; print(secrets.token_hex(32))"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ── n8n ───────────────────────────────────────────────────────
N8N_WEBHOOK_CHAT_URL=http://n8n:5678/webhook/chat-ia
N8N_WEBHOOK_NOTIFICACION_URL=http://n8n:5678/webhook/notificacion-evento
N8N_API_KEY=genera_con__openssl_rand_-hex_32

# ── App ────────────────────────────────────────────────────────
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173
```
