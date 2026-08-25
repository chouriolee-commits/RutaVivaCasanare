# PITCH DECK — Casanare en Movimiento

**Hackathon:** Simulacro 02 — Casanare en Movimiento  
**Equipo:** 4 personas  
**Tiempo de presentación:** ~5-8 minutos  
**Versión:** 1.0

---

## SLIDE 1 — Portada

**Título:** Casanare en Movimiento  
**Subtítulo:** Tu plataforma inteligente de eventos del departamento  
**Tagline:** *"Descubre, vive y conecta con Casanare"*

Visual sugerido: Foto de los llanos orientales + logo de la plataforma  
Incluir: Logo del Hackathon, nombre del equipo, fecha

---

## SLIDE 2 — El Problema

**Título:** ¿Cuál es el problema que resolvemos?

**Pain points identificados:**

🗓️ **Para el ciudadano:**
- La información de eventos en Casanare está dispersa (redes sociales, voz a voz, volantes físicos)
- No hay un punto centralizado donde conocer toda la oferta cultural, deportiva y turística del departamento
- Las personas no saben cómo contactar a los organizadores para resolver dudas

🏢 **Para el organizador:**
- No tienen una herramienta digital para gestionar y publicar sus eventos profesionalmente
- La difusión de eventos depende de esfuerzos manuales costosos en tiempo
- Dificultad para comunicar la programación detallada a los asistentes

**Cifra clave:** Casanare tiene +19 municipios con actividades culturales y deportivas que hoy no tienen visibilidad digital unificada.

---

## SLIDE 3 — La Solución

**Título:** Presentamos: Casanare en Movimiento

**Una plataforma web con dos roles:**

| 👤 Para el Ciudadano | 🏢 Para el Organizador |
|---------------------|----------------------|
| Explorar todos los eventos del departamento | Panel de gestión completo |
| Ver agenda detallada de cada evento | Crear y publicar eventos en minutos |
| Consultar dudas con un asistente IA | Gestionar la programación del evento |
| Filtrar por municipio y categoría | Recibir notificaciones automáticas |

**El plus:** Un asistente IA integrado que responde preguntas sobre cada evento específico — disponible 24/7, sin necesidad de contactar al organizador.

---

## SLIDE 4 — Demo / Flujo del Producto

**Título:** ¿Cómo funciona?

**Flujo del Ciudadano:**
```
Abre la plataforma
     ↓
Ve eventos publicados (con fotos, fechas, municipios)
     ↓
Hace clic en un evento
     ↓
Ve la agenda detallada hora por hora
     ↓
Tiene una duda → chatea con el asistente IA
     ↓
La IA responde basándose en la info del evento
```

**Flujo del Organizador:**
```
Se registra como empresario
     ↓
Crea su evento (título, fecha, ubicación, foto)
     ↓
Agrega la programación (actividades, ponentes, horarios)
     ↓
Publica con un clic → aparece en la plataforma
     ↓
Recibe email de confirmación automático (n8n)
```

Visual sugerido: Capturas de pantalla o mockups de la plataforma

---

## SLIDE 5 — Arquitectura Tecnológica

**Título:** Stack Tecnológico

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   FRONTEND   │    │   BACKEND   │    │     n8n     │
│             │    │             │    │             │
│  React 18   │◄──►│   Python    │◄──►│ Automatiza  │
│  JavaScript │    │   FastAPI   │    │ notif. email│
│  Tailwind   │    │             │    │ Chat IA     │
└─────────────┘    └──────┬──────┘    └──────┬──────┘
                          │                   │
                   ┌──────▼──────┐    ┌──────▼──────┐
                   │  MySQL /    │    │  Modelo IA  │
                   │  MariaDB    │    │  (LLM)      │
                   └─────────────┘    └─────────────┘
```

**Decisiones técnicas:**
- **FastAPI** → API rápida, documentación automática, ideal para integraciones
- **React** → SPA fluida, experiencia de usuario moderna
- **n8n** → Automatización sin código, fácil de mantener y expandir
- **MySQL** → Robusto, confiable, amplio soporte en la industria

---

## SLIDE 6 — Diferenciadores (¿Por qué somos diferentes?)

**Título:** Nuestra propuesta de valor única

✅ **IA Contextual por Evento**  
No es un chatbot genérico. Cada evento tiene su propio asistente entrenado con su información específica.

✅ **Gestión Todo-en-Uno para Organizadores**  
Desde crear el evento hasta gestionar la agenda con horarios y ponentes, en una sola plataforma.

✅ **Automatización desde el Día 1**  
n8n maneja notificaciones, recordatorios y puede escalar a difusión en WhatsApp, Telegram o redes sociales sin cambiar el backend.

✅ **Hecho para Casanare**  
Categorías, municipios y terminología adaptada al departamento. No es una solución genérica importada.

---

## SLIDE 7 — Impacto Esperado

**Título:** ¿Qué impacto genera?

**Para el Departamento:**
- Mayor visibilidad de la oferta cultural y turística de Casanare
- Digitalización de la gestión de eventos del sector público y privado
- Herramienta de base para el turismo interno departamental

**Para los Organizadores:**
- Reducción del tiempo de gestión y difusión de eventos en ~70%
- Canal digital propio sin depender de redes sociales de terceros
- Datos de interés (cuántas personas consultaron, qué preguntan)

**Para los Ciudadanos:**
- Acceso centralizado a toda la agenda del departamento
- Información clara y actualizada antes de asistir a un evento
- Resolución de dudas en tiempo real con IA

---

## SLIDE 8 — Roadmap

**Título:** ¿Qué sigue?

| Fase | Descripción | Tiempo |
|------|-------------|--------|
| **MVP (actual)** | Plataforma funcional con 2 roles + IA + email | Sprint 1-6 |
| **Fase 2** | App móvil (React Native), inscripciones en línea | Mes 2-3 |
| **Fase 3** | Integración WhatsApp Business via n8n, mapas interactivos | Mes 4-5 |
| **Fase 4** | Dashboard de analíticas para organizadores, panel admin | Mes 6 |
| **Fase 5** | Integración con agenda oficial de la Gobernación de Casanare | Mes 7+ |

---

## SLIDE 9 — El Equipo

**Título:** Nuestro equipo

| Rol | Responsabilidad |
|-----|----------------|
| 🖥️ **Frontend Developer** | UI/UX, React, experiencia del usuario |
| ⚙️ **Backend Developer** | API, base de datos, seguridad, lógica de negocio |
| 🤖 **Automatización n8n** | Workflows IA, notificaciones, integraciones |
| 📊 **Pitch / Producto** | Visión del producto, presentación, estrategia |

---

## SLIDE 10 — Demo en Vivo / Cierre

**Título:** ¡Lo vimos funcionar!

**Llamado a la acción:**
> "Casanare tiene cultura, tiene deporte, tiene turismo.  
> Lo que le faltaba era una plataforma que lo lleve a todos.  
> **Casanare en Movimiento** es esa plataforma."

**Preguntas y respuestas**

---

## Notas para el Presentador

### Tips clave:
1. **Empezar con el problema** — generar empatía antes de mostrar la solución
2. **Mostrar la demo en vivo** si el ambiente lo permite (tener backup con video)
3. **Enfatizar el asistente IA** — es el elemento diferenciador más visible
4. **Hablar del impacto local** — los jueces de hackathon valoran la pertinencia regional
5. **Slide de equipo humaniza** — nombrar brevemente qué hizo cada persona

### Preguntas frecuentes del jurado:
- *¿Cómo escala la solución?* → n8n facilita integraciones sin tocar el backend
- *¿Qué pasa si el LLM da respuestas incorrectas?* → Solo usa información del evento, no inventa
- *¿Quién administra la plataforma?* → Panel de admin (roadmap Fase 4)
- *¿Cuánto cuesta operar?* → Infraestructura Docker básica + costo de API de LLM por uso
- *¿Está disponible offline?* → No, requiere conexión (roadmap Fase 2 considera caché)

### Tiempo sugerido por slide:
| Slide | Tiempo |
|-------|--------|
| 1 - Portada | 15 seg |
| 2 - Problema | 60 seg |
| 3 - Solución | 60 seg |
| 4 - Demo/Flujo | 90 seg |
| 5 - Tecnología | 45 seg |
| 6 - Diferenciadores | 45 seg |
| 7 - Impacto | 45 seg |
| 8 - Roadmap | 30 seg |
| 9 - Equipo | 20 seg |
| 10 - Cierre | 30 seg |
| **Total** | **~8 min** |
