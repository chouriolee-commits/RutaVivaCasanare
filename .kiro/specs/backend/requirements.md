# BACKEND — Requerimientos Funcionales y Técnicos

**Proyecto:** Casanare en Movimiento  
**Tecnología:** Python 3.11 + FastAPI  
**Base de Datos:** MySQL 8 / MariaDB 10.6  
**Responsable:** Desarrollador Backend  
**Versión:** 1.0

---

## 1. Alcance del Backend

El backend es una API REST construida con FastAPI que:
- Gestiona autenticación y autorización por roles (JWT)
- Expone endpoints CRUD para eventos y agenda
- Actúa como proxy seguro hacia los workflows de n8n (IA)
- Persiste toda la información en MySQL/MariaDB via SQLAlchemy 2.0

---

## 2. Requerimientos Funcionales del Backend

### RF-B01 — Módulo de Autenticación
- RF-B01.1: `POST /api/v1/auth/register` — Registrar nuevo usuario con email, contraseña y nombre
- RF-B01.2: `POST /api/v1/auth/login` — Autenticar usuario, retornar access_token (15 min) y refresh_token (7 días)
- RF-B01.3: `POST /api/v1/auth/refresh` — Renovar access_token usando refresh_token válido
- RF-B01.4: `POST /api/v1/auth/logout` — Invalidar refresh_token (blacklist en BD)
- RF-B01.5: Contraseñas hasheadas con bcrypt (cost factor 12)
- RF-B01.6: JWT firmado con HS256 usando SECRET_KEY desde variables de entorno

### RF-B02 — Módulo de Usuarios
- RF-B02.1: `GET /api/v1/users/me` — Retornar datos del usuario autenticado
- RF-B02.2: `PUT /api/v1/users/me` — Actualizar nombre y teléfono del perfil
- RF-B02.3: `PATCH /api/v1/users/me/rol` — Cambiar rol propio a `empresario`

### RF-B03 — Módulo de Eventos
- RF-B03.1: `GET /api/v1/eventos` — Listar eventos publicados (público, con paginación y filtros)
- RF-B03.2: `GET /api/v1/eventos/{id}` — Detalle completo de un evento (público)
- RF-B03.3: `POST /api/v1/eventos` — Crear evento (rol: empresario)
- RF-B03.4: `PUT /api/v1/eventos/{id}` — Editar evento propio (rol: empresario, dueño)
- RF-B03.5: `DELETE /api/v1/eventos/{id}` — Eliminar evento propio (rol: empresario, dueño)
- RF-B03.6: `PATCH /api/v1/eventos/{id}/publicar` — Toggle publicar/despublicar (rol: empresario, dueño)
- RF-B03.7: `GET /api/v1/mis-eventos` — Listar eventos propios del empresario autenticado

### RF-B04 — Módulo de Agenda
- RF-B04.1: `GET /api/v1/eventos/{id}/agenda` — Listar items de agenda de un evento (público)
- RF-B04.2: `POST /api/v1/eventos/{id}/agenda` — Agregar item a la agenda (empresario, dueño)
- RF-B04.3: `PUT /api/v1/agenda/{item_id}` — Editar item de agenda (empresario, dueño)
- RF-B04.4: `DELETE /api/v1/agenda/{item_id}` — Eliminar item de agenda (empresario, dueño)
- RF-B04.5: Los items se ordenan automáticamente por `hora_inicio`

### RF-B05 — Módulo de IA / Chat
- RF-B05.1: `POST /api/v1/ia/chat` — Recibir mensaje del usuario para el evento, enviar a n8n y retornar respuesta
- RF-B05.2: `GET /api/v1/ia/conversacion/{evento_id}` — Historial de conversación del usuario en ese evento
- RF-B05.3: El endpoint construye el contexto del evento (título, descripción, agenda, ubicación) antes de enviarlo a n8n
- RF-B05.4: Los mensajes se persisten en `ia_mensajes` vinculados a `ia_conversaciones`

---

## 3. Requerimientos No Funcionales

| ID | Descripción |
|----|-------------|
| RNF-B01 | Respuesta ≤ 500ms para endpoints CRUD (sin llamadas externas) |
| RNF-B02 | Documentación automática Swagger en `/docs` y ReDoc en `/redoc` |
| RNF-B03 | CORS configurado para permitir solo el origen del frontend |
| RNF-B04 | Variables de entorno manejadas con `pydantic-settings` |
| RNF-B05 | Migraciones de base de datos con Alembic (no DDL manual) |
| RNF-B06 | Manejo centralizado de excepciones con HTTPException |
| RNF-B07 | Logs estructurados (nivel INFO en desarrollo, WARNING en producción) |

---

## 4. Dependencias Python

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
alembic==1.13.1
pymysql==1.1.0
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
httpx==0.27.0
pytest==8.2.0
pytest-asyncio==0.23.6
```

---

## 5. Variables de Entorno (.env)

```env
# Base de datos
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/casanare_eventos

# JWT
SECRET_KEY=tu_clave_secreta_muy_larga_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# n8n
N8N_WEBHOOK_CHAT_URL=http://localhost:5678/webhook/chat-ia
N8N_WEBHOOK_NOTIFICACION_URL=http://localhost:5678/webhook/notificacion-evento
N8N_API_KEY=tu_api_key_n8n

# App
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173
```
