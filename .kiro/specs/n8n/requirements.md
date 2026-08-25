# n8n — Requerimientos de Automatización

**Proyecto:** Casanare en Movimiento  
**Tecnología:** n8n (self-hosted)  
**Responsable:** Profesional en Automatización  
**Versión:** 1.0

---

## 1. Alcance de la Automatización

n8n actúa como la capa de integración inteligente del sistema. Su rol es:
1. **Recibir** consultas del backend y conectarlas con el modelo IA (LLM)
2. **Disparar** notificaciones automáticas de email al crear/publicar eventos
3. **Programar** recordatorios automáticos para eventos próximos
4. **Orquestar** cualquier integración futura (redes sociales, WhatsApp, etc.)

---

## 2. Workflows Requeridos

### WF-01 — Chat IA (webhook)
**Trigger:** Webhook HTTP POST  
**URL:** `/webhook/chat-ia`  
**Prioridad:** 🔴 Crítica

**Descripción:** Recibe la pregunta del usuario junto con el contexto del evento, construye un prompt estructurado y lo envía al LLM, retornando la respuesta.

**Payload de entrada:**
```json
{
  "pregunta": "¿Cuándo empieza el festival?",
  "contexto": {
    "titulo": "Festival Llanero 2026",
    "descripcion": "Gran festival de música llanera...",
    "fecha_inicio": "2026-09-15",
    "hora_inicio": "10:00",
    "ubicacion": "Plaza Central, Yopal",
    "municipio": "Yopal",
    "agenda": [
      { "hora": "10:00", "actividad": "Apertura", "ponente": "" },
      { "hora": "11:00", "actividad": "Concierto", "ponente": "Los Llanos Vivos" }
    ]
  },
  "historial": [
    { "rol": "user", "contenido": "Hola" },
    { "rol": "assistant", "contenido": "Hola, ¿en qué te puedo ayudar?" }
  ]
}
```

**Payload de salida:**
```json
{
  "respuesta": "El festival empieza el 15 de septiembre de 2026 a las 10:00 AM en la Plaza Central de Yopal.",
  "tokens_usados": 150
}
```

---

### WF-02 — Notificación de Evento Creado
**Trigger:** Webhook HTTP POST  
**URL:** `/webhook/notificacion-evento`  
**Prioridad:** 🟡 Alta

**Descripción:** Cuando el empresario crea un evento, el backend llama este webhook y n8n envía un email de confirmación al organizador.

**Payload de entrada:**
```json
{
  "tipo": "evento_creado",
  "organizador": {
    "nombre": "Carlos Pérez",
    "email": "carlos@empresa.com"
  },
  "evento": {
    "titulo": "Festival Llanero",
    "fecha_inicio": "2026-09-15",
    "ubicacion": "Plaza Central, Yopal",
    "estado": "borrador"
  }
}
```

---

### WF-03 — Recordatorio 24h Antes del Evento
**Trigger:** Schedule (cron) — Ejecuta diariamente a las 8:00 AM  
**Prioridad:** 🟡 Alta

**Descripción:** Cada día a las 8AM, consulta la BD y envía emails a los usuarios registrados recordándoles los eventos del día siguiente.

**Flujo:**
1. Ejecutar cada día a las 8:00 AM
2. Consultar API del backend: `GET /api/v1/eventos?fecha_inicio={mañana}&estado=publicado`
3. Para cada evento encontrado, enviar email de recordatorio al organizador
4. Opcional: disparar webhook de difusión en redes

---

### WF-04 — Notificación de Evento Publicado
**Trigger:** Webhook HTTP POST  
**URL:** `/webhook/evento-publicado`  
**Prioridad:** 🟢 Media

**Descripción:** Cuando un evento cambia de estado a "publicado", envía confirmación al organizador y puede disparar difusión.

---

## 3. Requerimientos Técnicos

| ID | Descripción |
|----|-------------|
| RNF-N01 | Los webhooks deben responder en ≤ 30 segundos (timeout del backend) |
| RNF-N02 | Autenticación de webhook con header `X-API-Key` |
| RNF-N03 | Los workflows deben tener manejo de errores (nodo de error) |
| RNF-N04 | Los workflows exportados como JSON para versionarlos en Git |
| RNF-N05 | Variables de entorno en n8n para API keys (no hardcodeadas) |
| RNF-N06 | Los emails usan plantillas HTML, no texto plano |

---

## 4. Configuración de Credenciales en n8n

Configurar las siguientes credenciales en la interfaz de n8n:

| Nombre | Tipo | Uso |
|--------|------|-----|
| `OpenAI API` | OpenAI API | LLM para chat IA |
| `SMTP Email` | SMTP | Envío de emails (Gmail / SendGrid) |
| `Backend API` | HTTP Header Auth | Consumir endpoints del backend |

---

## 5. Variables de Entorno de n8n

```env
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=password_seguro_aqui
WEBHOOK_URL=http://n8n:5678
N8N_HOST=0.0.0.0
N8N_PORT=5678
```
