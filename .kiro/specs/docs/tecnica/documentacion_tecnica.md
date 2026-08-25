# Documentación Técnica — Casanare en Movimiento

**Versión:** 1.0  
**Fecha:** Agosto 2026  
**Audiencia:** Desarrolladores, DevOps, mantenedores del sistema

---

## 1. Resumen del Sistema

Casanare en Movimiento es una plataforma web de gestión y descubrimiento de eventos para el departamento de Casanare, Colombia. El sistema consta de tres componentes principales:

| Componente | Tecnología | Puerto |
|-----------|-----------|--------|
| Frontend SPA | React 18 + Vite + Tailwind | 5173 (dev) / 80 (prod) |
| Backend API | Python 3.11 + FastAPI | 8000 |
| Automatización | n8n | 5678 |
| Base de datos | MySQL 8 / MariaDB 10.6 | 3306 |

---

## 2. Prerrequisitos de Instalación

- Docker >= 24.0 y Docker Compose >= 2.20
- Node.js >= 20.0 (desarrollo frontend)
- Python >= 3.11 (desarrollo backend)
- Git

---

## 3. Instalación para Desarrollo

### 3.1 Clonar el repositorio
```bash
git clone https://github.com/tu-org/casanare-en-movimiento.git
cd casanare-en-movimiento
```

### 3.2 Configurar variables de entorno

```bash
# Backend
cp backend/.env.example backend/.env
# Editar backend/.env con tus valores

# Frontend
cp frontend/.env.example frontend/.env
# Editar frontend/.env con VITE_API_BASE_URL
```

### 3.3 Levantar con Docker Compose

```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Detener
docker-compose down
```

### 3.4 Aplicar migraciones de base de datos

```bash
docker-compose exec backend alembic upgrade head
```

### 3.5 Verificar que todo funciona

```bash
# Backend health check
curl http://localhost:8000/health

# Swagger UI (solo en desarrollo)
open http://localhost:8000/docs

# n8n
open http://localhost:5678

# Frontend
open http://localhost:5173
```

---

## 4. Desarrollo Local sin Docker

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Linux/Mac
# o: venv\Scripts\activate        # Windows

pip install -r requirements.txt

# Asegurarse que MySQL corre localmente en 3306
# Crear BD: CREATE DATABASE casanare_eventos;

alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# Disponible en http://localhost:5173
```

---

## 5. Estructura de la Base de Datos

### Diagrama de Relaciones

```
users (1) ────────────── (N) eventos
              organizador_id FK

eventos (1) ─────────── (N) agenda_items
              evento_id FK

users (1) ──────────── (N) ia_conversaciones
              usuario_id FK

eventos (1) ────────── (N) ia_conversaciones
              evento_id FK

ia_conversaciones (1) ── (N) ia_mensajes
              conversacion_id FK
```

### Índices importantes

```sql
-- Para búsquedas frecuentes de eventos públicos
CREATE INDEX idx_eventos_estado_fecha ON eventos(estado, fecha_inicio);
CREATE INDEX idx_eventos_categoria ON eventos(categoria);
CREATE INDEX idx_eventos_municipio ON eventos(municipio);

-- Para agenda de un evento
CREATE INDEX idx_agenda_evento_hora ON agenda_items(evento_id, hora_inicio);

-- Para historial de conversaciones
CREATE INDEX idx_conv_usuario_evento ON ia_conversaciones(usuario_id, evento_id);
CREATE INDEX idx_mensajes_conv ON ia_mensajes(conversacion_id, created_at);
```

### Migraciones con Alembic

```bash
# Generar nueva migración tras cambios en modelos
alembic revision --autogenerate -m "descripcion_del_cambio"

# Aplicar todas las migraciones pendientes
alembic upgrade head

# Rollback una migración
alembic downgrade -1

# Ver historial de migraciones
alembic history
```

---

## 6. API Reference

La documentación interactiva completa está disponible en:
- **Swagger UI:** `GET /docs` (solo en `ENVIRONMENT=development`)
- **ReDoc:** `GET /redoc` (solo en `ENVIRONMENT=development`)

### Autenticación

Todos los endpoints protegidos requieren el header:
```
Authorization: Bearer {access_token}
```

El `access_token` se obtiene en `POST /api/v1/auth/login`.

### Códigos de respuesta comunes

| Código | Significado |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Recurso creado exitosamente |
| 204 | Operación exitosa sin contenido (DELETE) |
| 400 | Datos de entrada inválidos |
| 401 | No autenticado o token inválido/expirado |
| 403 | Autenticado pero sin permisos suficientes |
| 404 | Recurso no encontrado |
| 422 | Error de validación de schema Pydantic |
| 500 | Error interno del servidor |

### Ejemplos de uso

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"password123","nombre":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@test.com","password":"password123"}'

# Listar eventos (público)
curl http://localhost:8000/api/v1/eventos?estado=publicado&page=1&page_size=10

# Crear evento (requiere token de empresario)
curl -X POST http://localhost:8000/api/v1/eventos \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo":"Festival Llanero",
    "descripcion":"Gran festival",
    "categoria":"cultural",
    "fecha_inicio":"2026-09-15",
    "ubicacion":"Plaza Central, Yopal"
  }'

# Chat IA
curl -X POST http://localhost:8000/api/v1/ia/chat \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"evento_id":1,"mensaje":"¿A qué hora empieza?"}'
```

---

## 7. n8n — Integración Técnica

### Comunicación Backend → n8n

El backend llama a n8n via HTTP usando `httpx`:

```python
# En ia_service.py
POST http://n8n:5678/webhook/chat-ia
Headers: { "X-API-Key": settings.N8N_API_KEY }
Body: { "pregunta": str, "contexto": dict, "historial": list }
```

### Variables de entorno del backend relacionadas a n8n

```env
N8N_WEBHOOK_CHAT_URL=http://n8n:5678/webhook/chat-ia
N8N_WEBHOOK_NOTIFICACION_URL=http://n8n:5678/webhook/notificacion-evento
N8N_API_KEY=clave_compartida_segura
```

### Seguridad del webhook

Todos los webhooks de n8n validan el header `X-API-Key`. Configurar en n8n:
- Tipo de autenticación: **Header Auth**
- Header Name: `X-API-Key`
- Header Value: mismo valor que `N8N_API_KEY` en el backend

---

## 8. Despliegue en Producción

### Consideraciones de seguridad

```bash
# Generar SECRET_KEY segura
python -c "import secrets; print(secrets.token_hex(32))"

# Generar N8N_API_KEY
openssl rand -hex 32
```

### Variables de entorno en producción

```env
# Backend — producción
ENVIRONMENT=production          # Deshabilita /docs y /redoc
DATABASE_URL=mysql+pymysql://user:pass@db-host:3306/casanare_prod
SECRET_KEY=clave_generada_securely
CORS_ORIGINS=https://tu-dominio.com
```

### Checklist de producción

- [ ] `ENVIRONMENT=production` (deshabilita Swagger)
- [ ] `SECRET_KEY` generada con `secrets.token_hex(32)` — NUNCA la misma que dev
- [ ] Base de datos con usuario dedicado (no root)
- [ ] n8n con contraseña segura (no la default)
- [ ] CORS configurado solo para el dominio real
- [ ] SSL/HTTPS en el servidor web (nginx/caddy)
- [ ] `.env` en `.gitignore` — nunca en el repositorio
- [ ] Backup de base de datos configurado
- [ ] Logs centralizados

---

## 9. Ejecución de Tests

### Backend
```bash
cd backend
source venv/bin/activate

# Correr todos los tests
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=app --cov-report=html

# Solo un módulo
pytest tests/test_auth.py -v

# Verificar que la cobertura pasa el umbral mínimo (70%)
pytest tests/ --cov=app --cov-fail-under=70
```

### Frontend
```bash
cd frontend

# Correr tests una vez (modo CI)
npm run test -- --run

# Con cobertura
npm run test -- --run --coverage

# Modo watch (desarrollo)
npm run test
```

---

## 10. Guía de Contribución

### Flujo de trabajo Git

```bash
# Crear rama de feature
git checkout -b feature/nombre-de-la-feature

# Hacer cambios y commits
git add archivo.py
git commit -m "feat: descripción breve del cambio"

# Antes de hacer PR, asegurarse que los tests pasan
pytest tests/ --cov=app
npm run test -- --run

# Push y abrir Pull Request
git push origin feature/nombre-de-la-feature
```

### Convención de commits

```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
test: agregar o modificar tests
refactor: refactorización sin cambio funcional
chore: cambios de configuración/build
```

### Estándares de código

**Backend (Python):**
- Formateo: Black
- Linting: flake8 o ruff
- Type hints en todas las funciones de servicio

**Frontend (JavaScript):**
- ESLint con configuración de React
- Prettier para formateo
- PropTypes o JSDoc para documentar props de componentes

---

## 11. Monitoreo y Logs

### Logs del backend

```python
# En producción, el backend usa logging estándar de Python
# Nivel WARNING en producción, INFO en desarrollo

# Ver logs en Docker
docker-compose logs -f backend

# Filtrar errores
docker-compose logs backend 2>&1 | grep ERROR
```

### Health checks

```bash
# Backend
curl http://localhost:8000/health
# Respuesta: {"status": "ok", "version": "1.0.0"}

# Base de datos (desde dentro del contenedor)
docker-compose exec db mysqladmin ping -u root -p

# n8n
curl http://localhost:5678/healthz
```

---

## 12. Troubleshooting Común

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| Backend no conecta a BD | `DATABASE_URL` incorrecto o BD no levantó | Verificar `docker-compose logs db` |
| 401 en endpoints protegidos | Token expirado o mal formado | Hacer refresh del token o re-login |
| Chat IA no responde | n8n no levantó o API Key inválida | Verificar `docker-compose logs n8n` |
| CORS error en frontend | `CORS_ORIGINS` no incluye el origen del frontend | Actualizar la variable en `.env` |
| Migraciones fallan | Modelo tiene cambio incompatible | Revisar migración generada antes de aplicar |
| n8n webhook 404 | Workflow no activado o URL incorrecta | Activar workflow en n8n y verificar URL |
