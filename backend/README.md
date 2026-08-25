# Backend — Casanare en Movimiento

API REST en **FastAPI + SQLAlchemy 2.0** sobre la base de datos MySQL/MariaDB
`eventos_culturales` (ya existente en phpMyAdmin/XAMPP). Gestiona empresarios,
eventos, stands, productos e inventario (movimientos de stock).

> Los specs en `.kiro/specs/backend` describen un dominio distinto (eventos +
> agenda + chat IA) que no corresponde al esquema real de la base de datos.
> Este backend se construyó contra el **esquema real** (`usuarios`,
> `empresarios`, `eventos`, `stands`, `productos`, `movimientos_stock`) — ver
> decisión de alcance documentada en la conversación con el equipo.

---

## 1. Arranque local

```bash
# 1. Activar el venv (ya existe en la raíz del proyecto, c:\...\simulacro\venv)
..\..\venv\Scripts\activate        # PowerShell: ..\..\venv\Scripts\Activate.ps1

# 2. Instalar dependencias (ya instaladas si vienes de esta sesión)
pip install -r requirements-dev.txt

# 3. Copiar/ajustar variables de entorno
copy .env.example .env             # ya existe un .env con las credenciales de XAMPP

# 4. Levantar el servidor
uvicorn app.main:app --reload
```

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## 2. Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Conexión a MySQL/MariaDB (XAMPP local) |
| `SECRET_KEY` | Clave de firma JWT — nunca la subas al repo |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` / `REFRESH_TOKEN_EXPIRE_DAYS` | Vigencia de tokens |
| `ENVIRONMENT` | `development` habilita `/docs`; `production` los deshabilita |
| `CORS_ORIGINS` | Orígenes permitidos, separados por coma (URLs del frontend) |

## 3. Modelo de autorización

- **Público (sin token):** `GET /api/v1/eventos`, `GET /api/v1/eventos/{id}`.
- **Todo lo demás requiere `Authorization: Bearer <access_token>`.**
- No existe un sistema de roles: cualquier `usuario` autenticado puede
  gestionar empresarios, stands, productos e inventario. Es un panel de
  gestión interna (organizadores), no una plataforma multi-tenant — la
  tabla `empresarios` no tiene FK hacia `usuarios`.

## 4. Endpoints

### Auth (`/api/v1/auth`)
| Método | Ruta | Auth | Body |
|---|---|---|---|
| POST | `/register` | No | `{nombre, email, password, telefono?}` → `201` |
| POST | `/login` | No | `{email, password}` → `{access_token, refresh_token, token_type}` |
| POST | `/refresh` | No | `{refresh_token}` → nuevo par de tokens |

### Usuarios (`/api/v1/usuarios`)
| Método | Ruta | Auth |
|---|---|---|
| GET | `/me` | Sí |
| PUT | `/me` | Sí — `{nombre?, telefono?}` |

### Empresarios / Eventos / Stands / Productos
Todos con el mismo patrón CRUD + paginación:

```
GET    /api/v1/{recurso}?page=1&page_size=20&<filtros>
GET    /api/v1/{recurso}/{id}
POST   /api/v1/{recurso}
PUT    /api/v1/{recurso}/{id}
DELETE /api/v1/{recurso}/{id}   → 204
```

Filtros disponibles por recurso:
- `empresarios`: `tipo_producto`
- `eventos`: `estado` (`planeado`|`en_curso`|`finalizado`)
- `stands`: `id_evento`, `id_empresario`, `estado` (`pendiente`|`confirmado`|`cancelado`)
- `productos`: `id_stand`

Respuesta de listado (todas paginadas igual):
```json
{ "items": [...], "total": 42, "page": 1, "page_size": 20 }
```

### Inventario (`/api/v1`)
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/productos/{producto_id}/movimientos` | Registra `{cantidad_cambio, tipo_movimiento}` |
| GET | `/productos/{producto_id}/movimientos` | Historial paginado de ese producto |
| GET | `/movimientos?id_producto=` | Historial general, filtro opcional |

**Semántica de `cantidad_cambio` según `tipo_movimiento`:**
- `venta` / `reposicion`: entero **positivo** (magnitud). `venta` resta del
  stock, `reposicion` suma.
- `ajuste`: entero con signo (positivo o negativo, nunca 0), se aplica
  directo al stock.

El endpoint rechaza con `422` cualquier movimiento que deje `stock_actual`
negativo. La operación es atómica (bloqueo de fila `FOR UPDATE`), segura
ante ventas concurrentes sobre el mismo producto.

La respuesta de `POST /movimientos` incluye `stock_resultante` (el stock
justo después de aplicar ese movimiento). En los listados históricos ese
campo queda en `null` — solo se calcula con certeza en el momento de
registrar el movimiento.

## 5. Migraciones (Alembic)

El esquema ya existe en la BD (creado manualmente). Alembic está
inicializado con una migración baseline (no-op) ya aplicada (`alembic
stamp head`). Para cambios futuros al esquema:

```bash
# 1. Modifica el modelo en app/models/
# 2. Genera la migración
alembic revision --autogenerate -m "descripcion del cambio"
# 3. Revisa el archivo generado en alembic/versions/ antes de aplicar
alembic upgrade head
```

> Nota: `alembic revision --autogenerate` puede mostrar diffs cosméticos
> heredados del esquema original (nullability de columnas con
> `server_default`, nombre del índice único de `usuarios.email`) — son
> conocidos y no afectan el funcionamiento; no los apliques a menos que
> vayas a limpiar el esquema intencionalmente.

## 6. Tests

```bash
pytest tests/ -v
```

28 tests sobre SQLite en memoria (independiente de la BD real): auth,
eventos y las reglas de negocio de inventario (venta/reposición/ajuste,
stock insuficiente, concurrencia lógica, historial).

## 7. Notas para integrar el frontend

- Todas las fechas van en formato ISO (`YYYY-MM-DD`), horas en
  `YYYY-MM-DDTHH:MM:SS`.
- `precio` es un string decimal (`"3500.00"`) para no perder precisión.
- Los IDs de recursos son `id_<recurso>` (p. ej. `id_evento`,
  `id_producto`), no `id` genérico — así están en la BD real.
- Errores de negocio devuelven `{"detail": "mensaje"}` con el status code
  correspondiente (`400`/`404`/`409`/`422`); errores de validación de
  Pydantic devuelven la forma estándar de FastAPI
  (`{"detail": [{"loc": [...], "msg": ...}]}`).
- El `access_token` dura poco (30 min por defecto) — el frontend debe
  usar `/api/v1/auth/refresh` con el `refresh_token` (7 días) para
  renovarlo sin pedir login de nuevo.
