# n8n — Diseño de Workflows

**Proyecto:** Casanare en Movimiento  
**Versión:** 1.0

---

## WF-01 — Chat IA: Diseño Nodo a Nodo

```
[Webhook]
  ↓ Recibe: { pregunta, contexto, historial }
  
[Code Node — Construir Prompt]
  ↓ Construye el prompt con contexto estructurado
  
[HTTP Request — LLM API]
  ↓ POST a OpenAI / Ollama
  
[Code Node — Extraer Respuesta]
  ↓ Extrae el texto de la respuesta del LLM
  
[Respond to Webhook]
  → Retorna { respuesta, tokens_usados }
```

### Nodo 1: Webhook
```
Método: POST
Ruta: /chat-ia
Autenticación: Header Auth (X-API-Key)
Responder: Usando el nodo "Respond to Webhook"
```

### Nodo 2: Code — Construir Prompt del Sistema
```javascript
// Construir prompt de sistema con contexto del evento
const { pregunta, contexto, historial } = $input.first().json;

const agenda_texto = (contexto.agenda || [])
  .map(item => `  - ${item.hora}: ${item.actividad}${item.ponente ? ` (${item.ponente})` : ''}`)
  .join('\n');

const sistema_prompt = `Eres un asistente virtual del evento "${contexto.titulo}".
Solo debes responder preguntas relacionadas con este evento.
Si te preguntan algo que no tiene que ver con el evento, redirige amablemente.

INFORMACIÓN DEL EVENTO:
- Nombre: ${contexto.titulo}
- Descripción: ${contexto.descripcion}
- Fecha: ${contexto.fecha_inicio}
- Hora de inicio: ${contexto.hora_inicio || 'Por confirmar'}
- Lugar: ${contexto.ubicacion}, ${contexto.municipio}

PROGRAMACIÓN:
${agenda_texto || 'Programación por confirmar'}

Responde siempre en español, de forma amigable y concisa (máximo 3 párrafos).`;

// Construir mensajes con historial
const mensajes = [
  { role: 'system', content: sistema_prompt },
  ...(historial || []).map(m => ({
    role: m.rol,
    content: m.contenido
  })),
  { role: 'user', content: pregunta }
];

return [{ json: { mensajes, pregunta } }];
```

### Nodo 3: HTTP Request — OpenAI Chat
```
Método: POST
URL: https://api.openai.com/v1/chat/completions
Autenticación: Bearer Token (credencial OpenAI guardada en n8n)

Body (JSON):
{
  "model": "gpt-4o-mini",
  "messages": {{ $json.mensajes }},
  "max_tokens": 500,
  "temperature": 0.7
}
```

**Alternativa con Ollama (local/gratuito):**
```
URL: http://ollama:11434/api/chat
Body:
{
  "model": "llama3",
  "messages": {{ $json.mensajes }},
  "stream": false
}
```

### Nodo 4: Code — Extraer Respuesta
```javascript
// Para OpenAI:
const respuesta = $input.first().json.choices[0].message.content;
const tokens = $input.first().json.usage?.total_tokens || 0;

// Para Ollama:
// const respuesta = $input.first().json.message.content;

return [{ json: { respuesta, tokens_usados: tokens } }];
```

### Nodo 5: Respond to Webhook
```
Respond With: JSON
Response Body: {{ $json }}
Response Code: 200
```

### Nodo 6 (rama de error): Error Handler
```javascript
// Si el LLM falla, retornar mensaje amigable
return [{
  json: {
    respuesta: "Lo siento, no pude procesar tu consulta en este momento. Por favor intenta de nuevo en unos segundos.",
    tokens_usados: 0,
    error: true
  }
}];
```

---

## WF-02 — Notificación Email: Diseño Nodo a Nodo

```
[Webhook]
  ↓ Recibe: { tipo, organizador, evento }
  
[Switch — tipo de notificación]
  ↓ evento_creado        ↓ evento_publicado
  
[Code — Armar Email]    [Code — Armar Email]
  ↓                       ↓
[Send Email (SMTP)]
  ↓
[Respond to Webhook]
```

### Nodo 2: Switch por tipo
```
Condición 1: {{ $json.tipo }} === "evento_creado"   → rama A
Condición 2: {{ $json.tipo }} === "evento_publicado" → rama B
```

### Nodo 3A: Code — Email Creación
```javascript
const { organizador, evento } = $input.first().json;

const html = `
<div style="font-family: Arial; max-width: 600px; margin: auto;">
  <div style="background: #16A34A; padding: 20px; border-radius: 8px 8px 0 0;">
    <h1 style="color: white; margin: 0;">🎉 Evento Creado</h1>
  </div>
  <div style="padding: 20px; background: #f9f9f9;">
    <p>Hola <strong>${organizador.nombre}</strong>,</p>
    <p>Tu evento ha sido creado exitosamente en la plataforma <strong>Casanare en Movimiento</strong>.</p>
    <div style="background: white; padding: 15px; border-radius: 8px; margin: 15px 0;">
      <h3 style="color: #16A34A;">${evento.titulo}</h3>
      <p>📅 Fecha: ${evento.fecha_inicio}</p>
      <p>📍 Lugar: ${evento.ubicacion}</p>
      <p>Estado: <span style="color: #D97706;">Borrador</span></p>
    </div>
    <p>Cuando estés listo, publícalo desde tu dashboard.</p>
    <a href="http://tu-dominio.com/dashboard" 
       style="background: #16A34A; color: white; padding: 10px 20px; 
              border-radius: 6px; text-decoration: none; display: inline-block;">
      Ir al Dashboard
    </a>
  </div>
  <div style="padding: 10px; text-align: center; color: #888; font-size: 12px;">
    Casanare en Movimiento — Gobernación de Casanare
  </div>
</div>
`;

return [{ json: {
  to: organizador.email,
  subject: `✅ Tu evento "${evento.titulo}" fue creado`,
  html
}}];
```

### Nodo 4: Send Email
```
Credencial: SMTP configurada en n8n
From: noreply@casanaraenmovimiento.gov.co
To: {{ $json.to }}
Subject: {{ $json.subject }}
HTML: {{ $json.html }}
```

---

## WF-03 — Recordatorio Diario: Diseño Nodo a Nodo

```
[Schedule Trigger — 8:00 AM diario]
  ↓
[Code — Calcular fecha mañana]
  ↓
[HTTP Request — GET /api/v1/eventos?fecha=mañana]
  ↓
[IF — ¿Hay eventos?]
  ↓ Sí
[Split in Batches — Por cada evento]
  ↓
[Send Email — Recordatorio al organizador]
  ↓
[Merge]
```

### Nodo 1: Schedule Trigger
```
Cron: 0 8 * * *   (8:00 AM todos los días)
```

### Nodo 2: Code — Fecha Mañana
```javascript
const manana = new Date();
manana.setDate(manana.getDate() + 1);
const fecha = manana.toISOString().split('T')[0]; // "2026-09-15"
return [{ json: { fecha_manana: fecha } }];
```

### Nodo 3: HTTP Request — Consultar eventos
```
Método: GET
URL: {{ $env.BACKEND_URL }}/api/v1/eventos
Parámetros:
  fecha_inicio: {{ $json.fecha_manana }}
  estado: publicado
Headers:
  Authorization: Bearer {{ $env.BACKEND_API_KEY }}
```

---

## Instrucciones de Instalación y Export

### Exportar workflows para Git
1. En n8n, ir a cada workflow
2. Click en menú → "Download" → guarda como JSON
3. Guardar en `n8n/workflows/` del repositorio:
   - `chat_ia.json`
   - `notificacion_evento.json`
   - `recordatorio_diario.json`

### Importar en nueva instancia
1. En n8n, ir a "Workflows" → "Import from file"
2. Seleccionar cada JSON del repositorio
3. Configurar las credenciales (no se exportan por seguridad)
4. Activar los workflows

---

## Checklist de Testing de Workflows

### WF-01 Chat IA
- [ ] Webhook responde con `respuesta` correcta cuando llega payload válido
- [ ] Maneja correctamente evento con agenda vacía
- [ ] Timeout de LLM retorna mensaje de error amigable
- [ ] Autenticación: requests sin `X-API-Key` retornan 401

### WF-02 Notificaciones
- [ ] Email llega al organizador tras crear evento (probar con Mailtrap)
- [ ] HTML del email se renderiza correctamente
- [ ] Switch diferencia correctamente `evento_creado` vs `evento_publicado`

### WF-03 Recordatorio
- [ ] Trigger cron se puede activar manualmente para probar
- [ ] Cuando no hay eventos mañana, el workflow termina sin errores
- [ ] Email de recordatorio llega correctamente
