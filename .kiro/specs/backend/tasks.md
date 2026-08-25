# BACKEND — Tareas de Codificación

**Proyecto:** Casanare en Movimiento  
**Desarrollador:** Backend  
**Metodología:** Spec-Driven Development  
**Versión:** 1.0

---

## Instrucciones de uso

Cada tarea tiene:
- **ID**: identificador único
- **Prioridad**: 🔴 Crítica | 🟡 Alta | 🟢 Media
- **Estimado**: horas de desarrollo
- **Dependencias**: tareas que deben completarse primero
- **Criterios de aceptación**: qué debe cumplir para considerarse terminada

---

## SPRINT 0 — Setup del Proyecto

### T-B01 🔴 — Inicializar proyecto FastAPI
**Estimado:** 1h  
**Dependencias:** Ninguna

Pasos:
1. Crear virtualenv Python 3.11
2. Instalar dependencias de `requirements.txt`
3. Crear estructura de carpetas según `design.md §1`
4. Crear `app/main.py` con FastAPI básico + health endpoint
5. Crear `app/core/config.py` con pydantic-settings
6. Crear `.env` basado en `.env.example`
7. Verificar que `uvicorn app.main:app --reload` levanta sin errores

**Criterios de aceptación:**
- [ ] `GET /health` retorna `{"status": "ok"}`
- [ ] Swagger disponible en `GET /docs`

---

### T-B02 🔴 — Configurar base de datos y migraciones
**Estimado:** 1.5h  
**Dependencias:** T-B01

Pasos:
1. Crear `app/core/database.py` con engine SQLAlchemy + `get_db` dependency
2. Crear modelos ORM en `app/models/` (ver `design.md §2`)
3. Inicializar Alembic: `alembic init alembic`
4. Configurar `alembic/env.py` para leer modelos automáticamente
5. Generar primera migración: `alembic revision --autogenerate -m "initial"`
6. Aplicar migración: `alembic upgrade head`
7. Verificar tablas creadas en MySQL

**Criterios de aceptación:**
- [ ] Tablas `users`, `eventos`, `agenda_items`, `ia_conversaciones`, `ia_mensajes` existen en BD
- [ ] Alembic puede hacer downgrade y upgrade sin errores

---

### T-B03 🔴 — Dockerfile y docker-compose
**Estimado:** 1h  
**Dependencias:** T-B02

Contenido `docker-compose.yml`:
```yaml
services:
  db:
    image: mariadb:10.11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: casanare_eventos
      MYSQL_USER: app_user
      MYSQL_PASSWORD: app_pass
    ports: ["3306:3306"]
    volumes: [db_data:/var/lib/mysql]

  backend:
    build: ./backend
    ports: ["8000:8000"]
    env_file: ./backend/.env
    depends_on: [db]

  n8n:
    image: n8nio/n8n
    ports: ["5678:5678"]
    environment:
      N8N_BASIC_AUTH_ACTIVE: "true"
      N8N_BASIC_AUTH_USER: admin
      N8N_BASIC_AUTH_PASSWORD: admin123
    volumes: [n8n_data:/home/node/.n8n]

volumes:
  db_data:
  n8n_data:
```

**Criterios de aceptación:**
- [ ] `docker-compose up` levanta DB + backend + n8n sin errores
- [ ] Backend conecta a la BD dentro del compose

---

## SPRINT 1 — Autenticación

### T-B04 🔴 — Módulo de seguridad (JWT + bcrypt)
**Estimado:** 2h  
**Dependencias:** T-B02

Implementar `app/core/security.py`:
- `hash_password(password)` → string bcrypt
- `verify_password(plain, hashed)` → bool
- `create_access_token(data)` → JWT string
- `create_refresh_token(data)` → JWT string
- `decode_token(token)` → dict payload o HTTPException 401

Implementar `app/dependencies.py`:
- `get_db()` → Session
- `get_current_user()` → User
- `require_empresario()` → User
- `require_evento_owner()` → Evento

**Criterios de aceptación:**
- [ ] Token generado se puede decodificar con la misma SECRET_KEY
- [ ] Token expirado lanza HTTPException 401
- [ ] Contraseña incorrecta retorna False en verify_password

---

### T-B05 🔴 — Schemas de usuario y autenticación
**Estimado:** 1h  
**Dependencias:** T-B04

Crear `app/schemas/user.py`:
- `UserCreate`: email, password (min 8 chars), nombre
- `UserLogin`: email, password
- `UserResponse`: id, email, nombre, rol, created_at (sin password)
- `TokenResponse`: access_token, refresh_token, token_type
- `UserUpdate`: nombre opcional, telefono opcional

**Criterios de aceptación:**
- [ ] `UserCreate` rechaza email inválido
- [ ] `UserCreate` rechaza password menor a 8 caracteres
- [ ] `UserResponse` nunca incluye el campo `password_hash`

---

### T-B06 🔴 — Router de autenticación
**Estimado:** 2h  
**Dependencias:** T-B04, T-B05

Implementar `app/routers/auth.py`:

```
POST /api/v1/auth/register
  - Validar que email no exista → 400 si ya existe
  - Hashear password con bcrypt
  - Crear usuario en BD con rol='usuario'
  - Retornar UserResponse (201)

POST /api/v1/auth/login
  - Buscar usuario por email → 401 si no existe
  - Verificar password → 401 si incorrecto
  - Generar access_token y refresh_token
  - Retornar TokenResponse (200)

POST /api/v1/auth/refresh
  - Validar refresh_token
  - Generar nuevo access_token
  - Retornar nuevo TokenResponse (200)
```

**Criterios de aceptación:**
- [ ] Register con email duplicado retorna 400
- [ ] Login con credenciales correctas retorna tokens JWT
- [ ] Login con credenciales incorrectas retorna 401
- [ ] Refresh con token expirado retorna 401

---

### T-B07 🟡 — Router de usuarios
**Estimado:** 1h  
**Dependencias:** T-B06

Implementar `app/routers/users.py`:
```
GET  /api/v1/users/me        → retorna perfil del usuario autenticado
PUT  /api/v1/users/me        → actualiza nombre y teléfono
PATCH /api/v1/users/me/rol   → cambia rol a 'empresario'
```

**Criterios de aceptación:**
- [ ] Sin token JWT retorna 401
- [ ] Con token válido retorna datos correctos del usuario
- [ ] Cambio de rol persiste en BD

---

## SPRINT 2 — Eventos y Agenda

### T-B08 🔴 — Schemas de eventos
**Estimado:** 1h  
**Dependencias:** T-B02

Crear `app/schemas/evento.py` (ver `design.md §3`):
- `EventoCreate` con validaciones
- `EventoUpdate` (todos opcionales)
- `EventoResponse` con `model_config = ConfigDict(from_attributes=True)`
- `EventoListResponse` (paginado): items, total, page, page_size

**Criterios de aceptación:**
- [ ] `fecha_fin` debe ser >= `fecha_inicio` (validator personalizado)
- [ ] `aforo` debe ser entero positivo si se provee

---

### T-B09 🔴 — Servicio y router de eventos
**Estimado:** 3h  
**Dependencias:** T-B08

Implementar `app/services/evento_service.py`:
- `get_eventos_publicos(db, filtros, page, page_size)` → lista paginada
- `get_evento_by_id(db, id)` → Evento o 404
- `create_evento(db, data, organizador_id)` → Evento
- `update_evento(db, evento, data)` → Evento
- `delete_evento(db, evento)` → None
- `toggle_publicar(db, evento)` → Evento

Implementar `app/routers/eventos.py` con todos los endpoints definidos en `requirements.md §RF-B03`

**Criterios de aceptación:**
- [ ] `GET /eventos` retorna solo eventos con estado='publicado'
- [ ] `GET /eventos?categoria=cultural&municipio=Yopal` filtra correctamente
- [ ] `POST /eventos` sin token retorna 401
- [ ] `POST /eventos` con rol='usuario' retorna 403
- [ ] `DELETE /eventos/{id}` de otro empresario retorna 403
- [ ] `GET /eventos` retorna paginación correcta

---

### T-B10 🟡 — Schemas y router de agenda
**Estimado:** 2h  
**Dependencias:** T-B09

Crear `app/schemas/agenda.py`:
- `AgendaItemCreate`: evento_id, hora_inicio, hora_fin?, titulo_actividad, descripcion?, ponente?, orden?
- `AgendaItemResponse`: todos los campos + id + created_at

Implementar `app/routers/agenda.py`:
```
GET    /api/v1/eventos/{id}/agenda    → lista ordenada por hora_inicio (público)
POST   /api/v1/eventos/{id}/agenda    → crear item (empresario dueño)
PUT    /api/v1/agenda/{item_id}       → editar item (empresario dueño)
DELETE /api/v1/agenda/{item_id}       → eliminar item (empresario dueño)
```

**Criterios de aceptación:**
- [ ] Agenda retorna items ordenados por `hora_inicio` ASC
- [ ] No se puede agregar agenda a evento de otro organizador (403)
- [ ] `hora_fin` debe ser > `hora_inicio` si se provee

---

## SPRINT 4 — Integración IA

### T-B11 🔴 — Servicio y router de IA Chat
**Estimado:** 2.5h  
**Dependencias:** T-B09, n8n configurado

Implementar `app/services/ia_service.py` (ver `design.md §5`)

Crear `app/schemas/ia_chat.py`:
- `ChatRequest`: evento_id (int), mensaje (str, min 1, max 500)
- `ChatResponse`: respuesta (str), conversacion_id (int)
- `MensajeResponse`: id, rol, contenido, created_at

Implementar `app/routers/ia_chat.py`:
```
POST /api/v1/ia/chat
  1. Validar evento existe y está publicado
  2. Obtener/crear conversación del usuario para ese evento
  3. Guardar mensaje del usuario en ia_mensajes
  4. Construir contexto del evento (título, desc, agenda, ubicación)
  5. Obtener historial de la conversación (últimos 10 msgs)
  6. Llamar ia_service.enviar_consulta_ia(...)
  7. Guardar respuesta del asistente en ia_mensajes
  8. Retornar ChatResponse

GET /api/v1/ia/conversacion/{evento_id}
  → Retorna historial completo de mensajes de esa conversación
```

**Criterios de aceptación:**
- [ ] Sin token JWT retorna 401
- [ ] Evento inexistente retorna 404
- [ ] Evento no publicado retorna 400
- [ ] Timeout de n8n maneja correctamente con mensaje de error amigable
- [ ] Historial retorna mensajes en orden cronológico

---

## SPRINT 5 — Testing

### T-B12 🔴 — Setup de tests y fixtures
**Estimado:** 1.5h  
**Dependencias:** T-B06

Crear `tests/conftest.py`:
```python
# Fixtures:
# - client: TestClient con BD SQLite en memoria
# - db_session: sesión de prueba
# - user_token: token JWT de usuario normal
# - empresario_token: token JWT de empresario
# - evento_publicado: evento fixture en BD
```

**Criterios de aceptación:**
- [ ] `pytest tests/` corre sin errores de configuración
- [ ] BD de prueba es independiente de la BD de desarrollo

---

### T-B13 🔴 — Tests de autenticación
**Estimado:** 2h  
**Dependencias:** T-B12

Crear `tests/test_auth.py`:

| Test | Caso |
|------|------|
| `test_register_success` | Registro con datos válidos → 201 |
| `test_register_duplicate_email` | Email duplicado → 400 |
| `test_register_weak_password` | Password < 8 chars → 422 |
| `test_login_success` | Credenciales correctas → 200 + tokens |
| `test_login_wrong_password` | Password incorrecto → 401 |
| `test_login_nonexistent_user` | Email no registrado → 401 |
| `test_refresh_token` | Refresh válido → nuevo access token |
| `test_protected_without_token` | Sin token → 401 |

**Criterios de aceptación:**
- [ ] Todos los tests pasan (verde)
- [ ] Cobertura del módulo auth ≥ 80%

---

### T-B14 🔴 — Tests de eventos
**Estimado:** 2h  
**Dependencias:** T-B12, T-B09

Crear `tests/test_eventos.py`:

| Test | Caso |
|------|------|
| `test_list_events_public` | GET /eventos sin token → 200 |
| `test_list_events_only_published` | Solo retorna publicados |
| `test_filter_by_categoria` | Filtro funciona |
| `test_create_event_empresario` | Empresario crea → 201 |
| `test_create_event_usuario` | Usuario normal → 403 |
| `test_create_event_no_token` | Sin auth → 401 |
| `test_update_own_event` | Empresario edita el suyo → 200 |
| `test_update_other_event` | Editar el de otro → 403 |
| `test_delete_own_event` | Empresario elimina el suyo → 204 |
| `test_publish_toggle` | Publicar/despublicar → cambia estado |

**Criterios de aceptación:**
- [ ] Todos los tests pasan
- [ ] Cobertura del módulo eventos ≥ 75%

---

### T-B15 🟡 — Tests de IA Chat
**Estimado:** 1.5h  
**Dependencias:** T-B12, T-B11

Crear `tests/test_ia_chat.py` con mock de httpx para n8n:

| Test | Caso |
|------|------|
| `test_chat_sin_token` | Sin JWT → 401 |
| `test_chat_evento_inexistente` | evento_id inválido → 404 |
| `test_chat_evento_no_publicado` | evento borrador → 400 |
| `test_chat_success` | Mock n8n retorna respuesta → 200 |
| `test_chat_n8n_timeout` | n8n falla → error amigable |
| `test_historial_vacio` | Primera consulta, historial vacío → 200 |
| `test_historial_con_mensajes` | Historial retorna mensajes correctos |

**Criterios de aceptación:**
- [ ] Todos los tests pasan con mock de n8n
- [ ] No se hacen llamadas reales a n8n en tests

---

## SPRINT 6 — Preparación Producción

### T-B16 🟡 — Configuración de producción
**Estimado:** 1h  
**Dependencias:** Todos los tests pasando

- Separar `requirements.txt` y `requirements-dev.txt`
- Configurar Dockerfile multi-stage
- Agregar `ENVIRONMENT=production` que deshabilita `/docs` y `/redoc`
- Configurar logging con nivel WARNING en producción
- Revisar que SECRET_KEY nunca esté hardcodeada

**Criterios de aceptación:**
- [ ] `/docs` no accesible en producción
- [ ] `.env` no está en el repositorio (`.gitignore`)
- [ ] Docker image construye sin errores
