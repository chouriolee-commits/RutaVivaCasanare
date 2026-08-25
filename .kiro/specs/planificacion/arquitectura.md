# CASANARE EN MOVIMIENTO — Arquitectura del Sistema

**Versión:** 1.0  
**Fecha:** 2026-08-24

---

## 1. Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          React SPA (Vite + React 18)                 │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │ Vista Pública│  │ Dashboard    │  │ Chat IA    │  │   │
│  │  │ (Eventos)   │  │ Empresario   │  │ (Asistente)│  │   │
│  │  └─────────────┘  └──────────────┘  └────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS / REST API
┌──────────────────────────▼──────────────────────────────────┐
│                      BACKEND                                 │
│  ┌────────────────────────────────────────────────────┐     │
│  │             FastAPI (Python 3.11)                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │     │
│  │  │ /auth    │  │ /eventos │  │ /ia/chat          │ │     │
│  │  │ /users   │  │ /agenda  │  │ (proxy → n8n)     │ │     │
│  │  └──────────┘  └──────────┘  └──────────────────┘ │     │
│  └──────────────────────────────────────────────────── │     │
│           │                        │                   │     │
│  ┌────────▼──────┐         ┌──────▼────────────────┐  │     │
│  │ MySQL/MariaDB │         │    n8n Webhook         │  │     │
│  │  (SQLAlchemy) │         │    (Automatización)    │  │     │
│  └───────────────┘         └──────────┬────────────┘  │     │
└────────────────────────────────────────┼───────────────┘     │
                                         │
┌────────────────────────────────────────▼───────────────────┐
│                   n8n (Automatización)                      │
│  ┌─────────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Workflow Chat IA │  │ Workflow     │  │ Workflow      │  │
│  │ (recibe query,  │  │ Notificación │  │ Recordatorio  │  │
│  │  llama LLM,     │  │ Email        │  │ 24h antes     │  │
│  │  retorna resp.) │  │ (creación    │  │               │  │
│  └────────┬────────┘  │  evento)     │  └───────────────┘  │
│           │           └──────────────┘                      │
│  ┌────────▼────────┐                                        │
│  │ Modelo IA/LLM   │                                        │
│  │ (OpenAI /       │                                        │
│  │  Ollama local)  │                                        │
│  └─────────────────┘                                        │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Estructura de Base de Datos

```sql
-- Tabla usuarios
users
  id              INT PK AUTO_INCREMENT
  email           VARCHAR(255) UNIQUE NOT NULL
  password_hash   VARCHAR(255) NOT NULL
  nombre          VARCHAR(100)
  telefono        VARCHAR(20)
  rol             ENUM('usuario','empresario') DEFAULT 'usuario'
  activo          BOOLEAN DEFAULT TRUE
  created_at      DATETIME
  updated_at      DATETIME

-- Tabla eventos
eventos
  id              INT PK AUTO_INCREMENT
  titulo          VARCHAR(200) NOT NULL
  descripcion     TEXT NOT NULL
  categoria       ENUM('cultural','deportivo','turistico','gastronomico','otro')
  fecha_inicio    DATE NOT NULL
  fecha_fin       DATE
  hora_inicio     TIME
  hora_fin        TIME
  ubicacion       VARCHAR(300) NOT NULL
  municipio       VARCHAR(100)
  aforo           INT
  imagen_url      VARCHAR(500)
  estado          ENUM('borrador','publicado','cancelado') DEFAULT 'borrador'
  organizador_id  INT FK -> users.id
  created_at      DATETIME
  updated_at      DATETIME

-- Tabla agenda (programación del evento)
agenda_items
  id              INT PK AUTO_INCREMENT
  evento_id       INT FK -> eventos.id
  hora_inicio     TIME NOT NULL
  hora_fin        TIME
  titulo_actividad VARCHAR(200) NOT NULL
  descripcion     TEXT
  ponente         VARCHAR(150)
  orden           INT DEFAULT 0
  created_at      DATETIME

-- Tabla conversaciones IA
ia_conversaciones
  id              INT PK AUTO_INCREMENT
  usuario_id      INT FK -> users.id
  evento_id       INT FK -> eventos.id
  created_at      DATETIME

-- Tabla mensajes IA
ia_mensajes
  id              INT PK AUTO_INCREMENT
  conversacion_id INT FK -> ia_conversaciones.id
  rol             ENUM('user','assistant')
  contenido       TEXT NOT NULL
  created_at      DATETIME
```

---

## 3. Flujo de Datos — Chat IA

```
Usuario escribe pregunta
        │
        ▼
React → POST /api/v1/ia/chat
        │
        ▼
FastAPI valida JWT + obtiene contexto del evento
        │
        ▼
FastAPI → POST al webhook de n8n (query + contexto evento)
        │
        ▼
n8n construye prompt con contexto del evento
        │
        ▼
n8n → LLM API (OpenAI / Ollama)
        │
        ▼
n8n retorna respuesta a FastAPI
        │
        ▼
FastAPI guarda en ia_mensajes + retorna al frontend
        │
        ▼
React muestra respuesta en el chat
```

---

## 4. Estructura de Carpetas del Proyecto

```
casanare-en-movimiento/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── evento.py
│   │   │   ├── agenda.py
│   │   │   └── ia_chat.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── evento.py
│   │   │   ├── agenda.py
│   │   │   └── ia_chat.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── eventos.py
│   │   │   ├── agenda.py
│   │   │   └── ia_chat.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── evento_service.py
│   │   │   └── ia_service.py
│   │   └── dependencies.py
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── context/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── n8n/
│   ├── workflows/
│   │   ├── chat_ia.json
│   │   ├── notificacion_evento.json
│   │   └── recordatorio.json
│   └── README.md
├── docker-compose.yml
└── README.md
```

---

## 5. Endpoints API — Resumen

| Método | Ruta | Rol requerido | Descripción |
|--------|------|---------------|-------------|
| POST | /api/v1/auth/register | Público | Registro de usuario |
| POST | /api/v1/auth/login | Público | Login, retorna tokens |
| POST | /api/v1/auth/refresh | Autenticado | Renovar access token |
| GET | /api/v1/eventos | Público | Listar eventos publicados |
| GET | /api/v1/eventos/{id} | Público | Detalle de evento |
| POST | /api/v1/eventos | Empresario | Crear evento |
| PUT | /api/v1/eventos/{id} | Empresario (dueño) | Editar evento |
| DELETE | /api/v1/eventos/{id} | Empresario (dueño) | Eliminar evento |
| PATCH | /api/v1/eventos/{id}/publicar | Empresario (dueño) | Publicar/despublicar |
| GET | /api/v1/eventos/{id}/agenda | Público | Programación del evento |
| POST | /api/v1/eventos/{id}/agenda | Empresario (dueño) | Agregar item a agenda |
| PUT | /api/v1/agenda/{item_id} | Empresario (dueño) | Editar item agenda |
| DELETE | /api/v1/agenda/{item_id} | Empresario (dueño) | Eliminar item agenda |
| POST | /api/v1/ia/chat | Autenticado | Enviar mensaje al asistente |
| GET | /api/v1/ia/conversacion/{evento_id} | Autenticado | Historial de conversación |
| GET | /api/v1/users/me | Autenticado | Perfil propio |
| PUT | /api/v1/users/me | Autenticado | Actualizar perfil |
| PATCH | /api/v1/users/me/rol | Autenticado | Solicitar rol empresario |

---

## 6. Plan de Sprints

| Sprint | Duración | Objetivo |
|--------|----------|----------|
| Sprint 0 | Día 1 | Setup: repo, docker-compose, DB, scaffolding |
| Sprint 1 | Días 2-3 | Auth completa (backend + frontend) |
| Sprint 2 | Días 4-6 | CRUD de eventos (backend + frontend empresario) |
| Sprint 3 | Días 7-9 | Vista pública de eventos + detalle |
| Sprint 4 | Días 10-11 | Integración IA + n8n workflows |
| Sprint 5 | Días 12-13 | Testing + correcciones |
| Sprint 6 | Día 14 | Preparación demo + documentación final |
