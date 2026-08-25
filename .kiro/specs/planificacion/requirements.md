# CASANARE EN MOVIMIENTO — Requerimientos del Proyecto

**Versión:** 1.0  
**Fecha:** 2026-08-24  
**Equipo:** 1 Frontend · 1 Backend · 1 Automatización n8n · 1 Pitch  
**Hackathon:** Simulacro 02 — Casanare en Movimiento

---

## 1. Visión General

Plataforma web de gestión y descubrimiento de eventos turísticos, culturales y deportivos del departamento de Casanare. Permite a organizadores publicar eventos y a ciudadanos explorarlos y resolver dudas mediante un asistente de IA.

---

## 2. Actores del Sistema

| Actor | Descripción |
|---|---|
| **Usuario / Ciudadano** | Persona que explora eventos disponibles, ve detalles y consulta al asistente IA |
| **Empresario / Organizador** | Persona que crea, edita y gestiona sus eventos dentro de la plataforma |
| **Sistema IA** | Modelo de lenguaje que responde preguntas sobre eventos específicos |
| **n8n (Automatización)** | Capa de workflows que conecta notificaciones, integraciones y el modelo IA |

---

## 3. Requerimientos Funcionales

### RF-01 — Autenticación y Roles
- RF-01.1: El sistema debe permitir registro con email y contraseña
- RF-01.2: El sistema debe soportar login con JWT (access + refresh token)
- RF-01.3: El sistema debe asignar rol `usuario` por defecto al registrarse
- RF-01.4: El sistema debe permitir que un usuario solicite rol `empresario`
- RF-01.5: El sistema debe proteger rutas según el rol del usuario

### RF-02 — Gestión de Eventos (Rol: Empresario)
- RF-02.1: El empresario puede crear un evento con: título, descripción, categoría, fecha inicio, fecha fin, hora, ubicación, aforo, imagen, programación detallada
- RF-02.2: El empresario puede editar sus propios eventos
- RF-02.3: El empresario puede eliminar sus propios eventos
- RF-02.4: El empresario puede ver todos sus eventos en una tabla con filtros
- RF-02.5: El empresario puede gestionar la programación del evento (actividades con hora, ponente, descripción)
- RF-02.6: El empresario puede publicar o despublicar un evento

### RF-03 — Exploración de Eventos (Rol: Usuario)
- RF-03.1: El usuario ve en la pantalla principal todos los eventos publicados
- RF-03.2: El usuario puede filtrar eventos por categoría, fecha y ubicación
- RF-03.3: Al hacer clic en un evento, se muestra detalle completo: info general + programación
- RF-03.4: El detalle del evento incluye un chat con asistente IA para resolver dudas

### RF-04 — Asistente IA
- RF-04.1: El asistente IA responde preguntas sobre el evento seleccionado
- RF-04.2: El asistente usa el contexto del evento (descripción, programación, ubicación, horarios)
- RF-04.3: Las consultas se envían al backend que las enruta via n8n al modelo IA
- RF-04.4: El historial de la conversación persiste durante la sesión del usuario

### RF-05 — Notificaciones (Automatización)
- RF-05.1: Al crear un evento, se envía notificación por email al organizador
- RF-05.2: Al publicar un evento, se puede activar un flujo de difusión
- RF-05.3: Recordatorio automático 24h antes del evento a usuarios registrados

---

## 4. Requerimientos No Funcionales

| ID | Descripción |
|---|---|
| RNF-01 | Tiempo de respuesta del API ≤ 500ms para operaciones CRUD |
| RNF-02 | La plataforma debe ser responsive (mobile-first) |
| RNF-03 | Autenticación segura con tokens JWT firmados (HS256) |
| RNF-04 | Base de datos MySQL/MariaDB con migraciones versionadas |
| RNF-05 | Contraseñas almacenadas con hash bcrypt |
| RNF-06 | API RESTful con documentación OpenAPI/Swagger |
| RNF-07 | Frontend cargando en ≤ 3s en conexión 3G |
| RNF-08 | Cobertura de tests ≥ 70% en backend |

---

## 5. Reglas de Negocio

- Un evento solo puede ser editado/eliminado por su creador
- Un evento debe tener al menos: título, fecha, ubicación y descripción para ser publicado
- El asistente IA solo responde sobre el evento en cuyo detalle está abierto
- Un usuario puede cambiar a rol empresario desde su perfil

---

## 6. Restricciones Técnicas

| Componente | Tecnología |
|---|---|
| Frontend | React 18 + JavaScript (ES2022) |
| Backend | Python 3.11 + FastAPI |
| Base de datos | MySQL 8 / MariaDB 10.6 |
| Automatización | n8n (self-hosted o cloud) |
| ORM | SQLAlchemy 2.0 + Alembic |
| Auth | JWT con python-jose |
| Testing Backend | pytest + httpx |
| Testing Frontend | Vitest + React Testing Library |
| Contenedores | Docker + docker-compose (dev) |
