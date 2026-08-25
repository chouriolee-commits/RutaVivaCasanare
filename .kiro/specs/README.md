# Casanare en Movimiento — Spec Driven Development

**Hackathon:** Simulacro 02 — Casanare en Movimiento  
**Equipo:** Frontend · Backend · Automatización n8n · Pitch  
**Versión:** 1.0 | Fecha: Agosto 2026

---

## ¿Qué es este directorio?

Este directorio `.kiro/specs/` contiene toda la documentación spec-driven del proyecto, organizada por área de trabajo. Cada miembro del equipo tiene su propia carpeta con todo lo que necesita para trabajar de forma autónoma.

---

## Estructura de Carpetas

```
.kiro/specs/
│
├── planificacion/          ← LEER PRIMERO — Arquitectura general
│   ├── requirements.md     Requerimientos funcionales y no funcionales
│   └── arquitectura.md     Diagramas, BD, endpoints, plan de sprints
│
├── backend/                ← Para el desarrollador Backend
│   ├── requirements.md     Qué construir (endpoints, reglas de negocio)
│   ├── design.md           Cómo construirlo (modelos, schemas, servicios)
│   ├── tasks.md            Lista de tareas ordenadas por sprint
│   └── testing.md          Guía completa de testing con pytest
│
├── frontend/               ← Para el desarrollador Frontend
│   ├── requirements.md     Páginas, componentes, funcionalidades
│   ├── design.md           Estructura, componentes, Context, Axios
│   ├── tasks.md            Lista de tareas ordenadas por sprint
│   └── testing.md          Guía completa de testing con Vitest
│
├── n8n/                    ← Para el profesional en Automatización
│   ├── requirements.md     Workflows requeridos y specs técnicas
│   ├── workflows.md        Diseño nodo a nodo de cada workflow
│   └── tasks.md            Lista de tareas con criterios de aceptación
│
├── pitch/                  ← Para el presentador
│   └── pitch_deck.md       Estructura completa del pitch (10 slides)
│
└── docs/
    ├── cliente/
    │   └── manual_usuario.md    Manual de uso para ciudadanos y organizadores
    └── tecnica/
        └── documentacion_tecnica.md  Guía técnica para desarrolladores
```

---

## Ciclo de Desarrollo (SDLC)

```
PLANEACIÓN          ANÁLISIS            DISEÑO
requirements.md  →  arquitectura.md  →  design.md (backend/frontend)
     ↓                                       ↓
CODIFICACIÓN                           TESTING
tasks.md          ←────────────────── testing.md
     ↓
PRODUCCIÓN
docs/tecnica/documentacion_tecnica.md §8
```

---

## Cómo usar este spec driven

### Para cada desarrollador:

1. **Lee primero** `planificacion/arquitectura.md` para entender el sistema completo
2. **Lee** los `requirements.md` de tu área para saber qué tienes que construir
3. **Lee** el `design.md` de tu área para saber cómo construirlo
4. **Sigue** las tareas de `tasks.md` en orden (tienen dependencias explícitas)
5. **Escribe tests** siguiendo la guía en `testing.md`
6. **Marca** cada criterio de aceptación cuando lo cumplas

### Regla de oro:
> Una tarea está **terminada** solo cuando todos sus criterios de aceptación están cumplidos y los tests relevantes pasan en verde.

---

## Stack Tecnológico Resumido

| Área | Tecnología |
|------|-----------|
| Frontend | React 18 + Vite + JavaScript + Tailwind CSS |
| Backend | Python 3.11 + FastAPI + SQLAlchemy 2.0 + Alembic |
| Base de Datos | MySQL 8 / MariaDB 10.6 |
| Automatización | n8n (self-hosted) |
| IA / LLM | OpenAI GPT o Ollama (local) via n8n |
| Auth | JWT (access + refresh token) con python-jose |
| Testing Backend | pytest + httpx + pytest-asyncio |
| Testing Frontend | Vitest + React Testing Library |
| Infraestructura | Docker + docker-compose |

---

## Contacto por Área

| Área | Responsable | Archivos principales |
|------|-------------|---------------------|
| Backend | Dev Backend | `backend/tasks.md` |
| Frontend | Dev Frontend | `frontend/tasks.md` |
| Automatización | Prof. n8n | `n8n/tasks.md` |
| Presentación | Pitch | `pitch/pitch_deck.md` |
