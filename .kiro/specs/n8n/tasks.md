# n8n — Tareas de Automatización

**Proyecto:** Casanare en Movimiento  
**Responsable:** Profesional en Automatización n8n  
**Versión:** 1.0

---

## SPRINT 0 — Setup de n8n

### T-N01 🔴 — Levantar n8n con Docker
**Estimado:** 30min | **Dependencias:** Docker instalado

```bash
# El docker-compose.yml del proyecto ya incluye n8n
docker-compose up n8n -d

# Acceder a: http://localhost:5678
# Usuario: admin | Password: admin123 (cambiar en producción)
```

**Criterios de aceptación:**
- [ ] n8n accesible en http://localhost:5678
- [ ] Login con credenciales funciona
- [ ] Interfaz carga correctamente

---

### T-N02 🔴 — Configurar credenciales
**Estimado:** 30min | **Dependencias:** T-N01

En n8n → Settings → Credentials → New:

1. **OpenAI API**
   - Tipo: OpenAI API
   - API Key: (tu clave de OpenAI)
   - Nombre: "OpenAI Casanare"

2. **SMTP Email** (usar Mailtrap para desarrollo)
   - Tipo: SMTP
   - Host: smtp.mailtrap.io (dev) / smtp.gmail.com (prod)
   - Puerto: 2525 (dev) / 587 (prod)
   - Usuario y contraseña de Mailtrap
   - Nombre: "Email Casanare"

3. **Backend API Key** (para WF-03)
   - Tipo: HTTP Header Auth
   - Header: Authorization
   - Value: Bearer {token_del_backend}
   - Nombre: "Backend Casanare"

**Criterios de aceptación:**
- [ ] Credencial OpenAI guarda sin error
- [ ] Credencial SMTP puede enviar email de prueba
- [ ] Variables de entorno `BACKEND_URL` configuradas en n8n

---

## SPRINT 4 — Workflows

### T-N03 🔴 — Construir WF-01: Chat IA
**Estimado:** 3h | **Dependencias:** T-N02, Credencial OpenAI configurada

Pasos:
1. New Workflow → nombre: "Chat IA — Casanare"
2. Agregar nodo **Webhook**:
   - HTTP Method: POST
   - Path: chat-ia
   - Authentication: Header Auth
   - Respond: Using 'Respond to Webhook' node
3. Agregar nodo **Code** "Construir Prompt":
   - Copiar código de `workflows.md §WF-01 Nodo 2`
4. Agregar nodo **HTTP Request** "Llamar LLM":
   - Configurar según `workflows.md §WF-01 Nodo 3`
   - Credencial: OpenAI Casanare
5. Agregar nodo **Code** "Extraer Respuesta":
   - Copiar código de `workflows.md §WF-01 Nodo 4`
6. Agregar nodo **Respond to Webhook**
7. Agregar rama de **Error Handler**:
   - Conectar desde nodo HTTP Request → Error Output
   - Code node con mensaje de error amigable
   - → Respond to Webhook

**Prueba del workflow:**
```bash
curl -X POST http://localhost:5678/webhook/chat-ia \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_api_key" \
  -d '{
    "pregunta": "¿A qué hora empieza el evento?",
    "contexto": {
      "titulo": "Festival Llanero",
      "descripcion": "Gran festival de música",
      "fecha_inicio": "2026-09-15",
      "hora_inicio": "10:00",
      "ubicacion": "Plaza Central, Yopal",
      "municipio": "Yopal",
      "agenda": []
    },
    "historial": []
  }'
```

**Criterios de aceptación:**
- [ ] Webhook activo y accesible
- [ ] Respuesta contiene campo `respuesta` con texto del LLM
- [ ] Tiempo de respuesta < 15 segundos
- [ ] Error del LLM retorna mensaje amigable (no error 500)
- [ ] Workflow exportado como `n8n/workflows/chat_ia.json`

---

### T-N04 🔴 — Construir WF-02: Notificaciones Email
**Estimado:** 2h | **Dependencias:** T-N02, Credencial SMTP configurada

Pasos:
1. New Workflow → nombre: "Notificaciones Email — Casanare"
2. Agregar nodo **Webhook**:
   - Path: notificacion-evento
   - Method: POST
3. Agregar nodo **Switch** con dos condiciones:
   - `$json.tipo === "evento_creado"` → Rama A
   - `$json.tipo === "evento_publicado"` → Rama B
4. Rama A: nodo **Code** "Email Creación" (ver `workflows.md §WF-02`)
5. Rama B: nodo **Code** "Email Publicación" (template similar pero diferente mensaje)
6. Ambas ramas → nodo **Send Email** con credencial SMTP
7. → nodo **Respond to Webhook** (200 OK)

**Prueba:**
```bash
curl -X POST http://localhost:5678/webhook/notificacion-evento \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "evento_creado",
    "organizador": { "nombre": "Carlos", "email": "test@mailtrap.io" },
    "evento": { "titulo": "Mi Evento", "fecha_inicio": "2026-09-15", "ubicacion": "Yopal" }
  }'
```

**Criterios de aceptación:**
- [ ] Email llega a Mailtrap tras ejecutar el curl
- [ ] HTML del email se visualiza correctamente en Mailtrap
- [ ] Switch enruta correctamente por tipo
- [ ] Workflow exportado como `n8n/workflows/notificacion_evento.json`

---

### T-N05 🟡 — Construir WF-03: Recordatorio Diario
**Estimado:** 1.5h | **Dependencias:** T-N02, Backend corriendo

Pasos:
1. New Workflow → nombre: "Recordatorio Diario — Casanare"
2. Agregar nodo **Schedule Trigger**:
   - Mode: Every day
   - Hour: 8, Minute: 0
3. Agregar nodo **Code** "Fecha Mañana"
4. Agregar nodo **HTTP Request** "Consultar Eventos"
5. Agregar nodo **IF** "¿Hay eventos?"
6. Agregar nodo **Split in Batches**
7. Agregar nodo **Send Email** por cada evento

**Criterios de aceptación:**
- [ ] Workflow se puede ejecutar manualmente (botón "Execute Workflow")
- [ ] Cuando hay eventos mañana, envía emails
- [ ] Cuando no hay eventos, termina limpiamente sin errores
- [ ] Workflow exportado como `n8n/workflows/recordatorio_diario.json`

---

## SPRINT 5 — Testing de Workflows

### T-N06 🔴 — Testing WF-01 Chat IA
**Estimado:** 1h | **Dependencias:** T-N03, Backend con endpoint /ia/chat activo

Casos de prueba:

| # | Escenario | Input | Resultado Esperado |
|---|-----------|-------|-------------------|
| 1 | Pregunta simple sobre horario | pregunta: "¿A qué hora?" | Respuesta mencionando la hora del evento |
| 2 | Pregunta sobre agenda | pregunta: "¿Quién actúa?" | Respuesta mencionando el ponente |
| 3 | Pregunta fuera del tema | pregunta: "¿Cómo está el tiempo?" | Redirige amablemente al evento |
| 4 | Pregunta con historial | Con 5 mensajes previos | Mantiene coherencia del contexto |
| 5 | LLM timeout | Desconectar red momentáneamente | Retorna mensaje de error amigable |
| 6 | Sin API key | Omitir header X-API-Key | 401 Unauthorized |

---

### T-N07 🟡 — Testing WF-02 Notificaciones
**Estimado:** 45min | **Dependencias:** T-N04

Casos de prueba:

| # | Escenario | Verificar en Mailtrap |
|---|-----------|----------------------|
| 1 | evento_creado | Email recibido con asunto correcto |
| 2 | evento_publicado | Email diferente recibido |
| 3 | tipo desconocido | Workflow termina sin enviar email |
| 4 | Email inválido | Manejo de error sin romper el flujo |

---

## SPRINT 6 — Documentación y Export

### T-N08 🟡 — Documentar y versionar workflows
**Estimado:** 1h | **Dependencias:** T-N03, T-N04, T-N05

1. Exportar cada workflow desde n8n como JSON
2. Guardar en `n8n/workflows/`:
   - `chat_ia.json`
   - `notificacion_evento.json`
   - `recordatorio_diario.json`
3. Crear `n8n/README.md` con instrucciones de instalación
4. Documentar las variables de entorno necesarias

**Criterios de aceptación:**
- [ ] Los 3 archivos JSON están en el repositorio
- [ ] Otro desarrollador puede importar y activar los workflows siguiendo el README
- [ ] Las credenciales NO están en los archivos exportados
