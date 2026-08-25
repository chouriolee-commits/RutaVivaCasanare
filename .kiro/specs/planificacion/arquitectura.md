# CASANARE EN MOVIMIENTO — Arquitectura del Sistema

**Versión:** 3.0  
**Fecha:** 2026-08-24  
**Metodología:** UML + Spec-Driven Development

---

## 1. Diagrama de Casos de Uso (UML)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SISTEMA: Casanare en Movimiento                       │
│                                                                          │
│   ┌─────────┐                                          ┌─────────────┐  │
│   │         │──── Ver eventos publicados ─────────────►│             │  │
│   │ PÚBLICO │──── Ver detalle de evento ──────────────►│             │  │
│   │ (sin    │──── Ver agenda/programación ────────────►│   Sistema   │  │
│   │ sesión) │──── Seleccionar rol en login ───────────►│             │  │
│   └─────────┘                                          │             │  │
│                                                        │             │  │
│   ┌─────────┐                                          │             │  │
│   │         │──── (hereda acciones de Público) ───────►│             │  │
│   │ CLIENTE │──── Chatear con IA del evento ──────────►│             │  │
│   │ (usuario│──── Ver historial de chat ──────────────►│             │  │
│   │  auth)  │──── Editar su perfil ───────────────────►│             │  │
│   └─────────┘                                          │             │  │
│                                                        │             │  │
│   ┌──────────────┐                                     │             │  │
│   │              │──── Seleccionar su evento ─────────►│             │  │
│   │ EMPRESARIO   │──── Cargar datos del evento ────────►│             │  │
│   │ (organizador │──── Editar datos del evento ────────►│             │  │
│   │  auth)       │──── Gestionar agenda/horarios ──────►│             │  │
│   │              │──── Publicar / despublicar evento ──►│             │  │
│   │              │──── Chatear con IA (dudas gestión) ─►│             │  │
│   │              │──── Ver panel de su evento ─────────►│             │  │
│   └──────────────┘                                     └─────────────┘  │
│                                                                          │
│   ┌─────────┐                                                            │
│   │  n8n    │──── Enviar notificaciones email                           │
│   │ (sistema│──── Procesar consultas IA (LLM)                           │
│   │  auto)  │──── Recordatorios automáticos                             │
│   └─────────┘                                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Diagrama de Flujo General del Sistema

```
                    ┌──────────────────┐
                    │  Pantalla inicio │
                    │  (Eventos públic.)│
                    └────────┬─────────┘
                             │
              ┌──────────────▼──────────────┐
              │         Login Screen         │
              │                              │
              │   ┌──────────┐ ┌──────────┐ │
              │   │ 👤 Soy   │ │ 🏢 Soy  │ │
              │   │ Cliente  │ │Empresario│ │
              │   └────┬─────┘ └────┬─────┘ │
              └────────┼────────────┼────────┘
                       │            │
          ┌────────────▼──┐    ┌────▼──────────────────────────────┐
          │  Auth Cliente  │    │         Auth Empresario            │
          │  email+pass    │    │         email+pass                 │
          └────────┬───────┘    └─────────────────┬─────────────────┘
                   │                              │
          ┌────────▼───────┐         ┌────────────▼────────────────┐
          │ Home — Listado │         │  ¿Tienes un evento creado?   │
          │ de eventos     │         │                              │
          │ publicados     │         │  [Sí, seleccionar mi evento] │
          └────────┬───────┘         │  [No, crear nuevo evento]   │
                   │                 └────────────┬────────────────┘
          ┌────────▼───────┐                      │
          │  Click en un   │         ┌────────────▼────────────────┐
          │  evento        │         │   Panel del Empresario       │
          └────────┬───────┘         │                              │
                   │                 │  ┌─────────────────────────┐│
          ┌────────▼───────┐         │  │ Datos del evento         ││
          │  Detalle del   │         │  │ (título, fecha, lugar,   ││
          │  evento        │         │  │  descripción, imagen)    ││
          │  + Agenda      │         │  └─────────────────────────┘│
          │  + Chat IA 💬  │         │  ┌─────────────────────────┐│
          └────────────────┘         │  │ Agenda/Horarios          ││
                                     │  │ (actividades, ponentes)  ││
                                     │  └─────────────────────────┘│
                                     │  ┌─────────────────────────┐│
                                     │  │ Publicar / Despublicar   ││
                                     │  └─────────────────────────┘│
                                     │  ┌─────────────────────────┐│
                                     │  │ Chat IA 💬 (dudas de    ││
                                     │  │ gestión del evento)      ││
                                     │  └─────────────────────────┘│
                                     └─────────────────────────────┘
```

---

## 3. Diagrama de Secuencia — Flujo Cliente

```
Cliente    React SPA    FastAPI    MySQL    n8n/LLM
   │           │           │         │         │
   │──Login──►│           │         │         │
   │           │──POST /auth/login──►│         │
   │           │◄──JWT token────────│         │
   │◄──Redirige a Home──│           │         │
   │                    │           │         │
   │──Ver eventos──────►│           │         │
   │           │──GET /eventos──────►│         │
   │           │◄──Lista eventos────│         │
   │◄──Muestra tarjetas─│           │         │
   │                    │           │         │
   │──Click evento──────►│           │         │
   │           │──GET /eventos/{id}─►│         │
   │           │──GET /eventos/{id}/agenda──►│  │
   │           │◄──Evento + Agenda──│         │
   │◄──Muestra detalle──│           │         │
   │                    │           │         │
   │──Escribe pregunta──►│           │         │
   │           │──POST /ia/chat─────►│         │
   │           │           │──Valida JWT       │
   │           │           │──Obtiene contexto evento
   │           │           │──POST webhook────►│
   │           │           │         │──LLM──►│
   │           │           │         │◄──resp─│
   │           │           │◄──respuesta───────│
   │           │           │──Guarda ia_mensajes
   │           │◄──Respuesta IA──────│         │
   │◄──Muestra en chat──│           │         │
```

---

## 4. Diagrama de Secuencia — Flujo Empresario (Onboarding)

```
Empresario  React SPA    FastAPI    MySQL    n8n
    │           │           │         │       │
    │──Login ──►│           │         │       │
    │  (rol=    │──POST /auth/login──►│       │
    │  empresario)│◄──JWT(rol=empresario)──│  │
    │◄──Redirige a /empresa/inicio
    │           │           │         │       │
    │──Pantalla "¿A qué evento perteneces?"
    │           │           │         │       │
    │  Opción A: Seleccionar evento existente
    │──Selecciona─►│         │         │       │
    │           │──GET /mis-eventos──►│       │
    │           │◄──Lista mis eventos─│       │
    │◄──Elige evento del listado──│   │       │
    │           │──POST /empresa/sesion-evento
    │           │◄──evento_activo guardado    │
    │◄──Redirige a /empresa/panel/{evento_id}
    │           │           │         │       │
    │  Opción B: Crear nuevo evento
    │──Formulario nuevo evento────────────────│
    │           │──POST /eventos─────►│       │
    │           │◄──Evento creado (id)│       │
    │           │           │──Trigger n8n──►│
    │           │           │         │  Email confirmación
    │◄──Redirige a /empresa/panel/{evento_id}
    │           │           │         │       │
    │  ═══ DENTRO DEL PANEL DEL EMPRESARIO ═══
    │           │           │         │       │
    │──Editar datos evento──►│         │       │
    │           │──PUT /eventos/{id}──►│       │
    │           │◄──Evento actualizado│       │
    │◄──Feedback éxito──────│         │       │
    │           │           │         │       │
    │──Gestionar agenda──────►│         │       │
    │           │──POST/PUT/DELETE /agenda/{id}
    │           │◄──Agenda actualizada│       │
    │◄──Timeline actualizado─│         │       │
    │           │           │         │       │
    │──Publicar evento──────►│         │       │
    │           │──PATCH /eventos/{id}/publicar
    │           │◄──estado=publicado──│       │
    │           │           │──Trigger n8n──►│
    │           │           │         │  Email publicación
    │◄──Badge verde en panel─│         │       │
    │           │           │         │       │
    │──Pregunta al chat IA──►│         │       │
    │           │──POST /ia/chat─────►│       │
    │           │           │──n8n/LLM─────►│
    │           │◄──Respuesta IA──────│       │
    │◄──Respuesta sobre gestión evento
```

---

## 5. Diagrama de Clases UML (Dominio)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DIAGRAMA DE CLASES                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐        ┌──────────────────────────────────────────┐
│        User           │        │              Evento                       │
├──────────────────────┤        ├──────────────────────────────────────────┤
│ + id: int             │        │ + id: int                                 │
│ + email: str          │        │ + titulo: str                             │
│ + password_hash: str  │        │ + descripcion: str                        │
│ + nombre: str         │        │ + categoria: CategoriaEnum                │
│ + telefono: str       │        │ + fecha_inicio: date                      │
│ + rol: RolEnum        │        │ + fecha_fin: date?                        │
│ + activo: bool        │        │ + hora_inicio: time?                      │
│ + created_at: datetime│        │ + hora_fin: time?                         │
│ + updated_at: datetime│        │ + ubicacion: str                          │
├──────────────────────┤        │ + municipio: str?                         │
│ + verificar_pass()    │        │ + aforo: int?                             │
│ + es_empresario()     │        │ + imagen_url: str?                        │
└──────────┬───────────┘        │ + estado: EstadoEnum                      │
           │                    │ + organizador_id: int (FK)                │
           │ 1                  │ + created_at: datetime                    │
           │                    │ + updated_at: datetime                    │
           │ crea/gestiona      ├──────────────────────────────────────────┤
           │                    │ + publicar()                              │
           │ N                  │ + despublicar()                           │
           ▼                    │ + esta_publicado(): bool                  │
    ┌──────────────────────┐    └──────────────┬───────────────────────────┘
    │    SesionEmpresario   │                   │
    ├──────────────────────┤                   │ 1
    │ + user_id: int (FK)  │        tiene      │
    │ + evento_activo_id   │                   │ N
    │ + created_at         │                   ▼
    └──────────────────────┘    ┌──────────────────────────────────────────┐
                                │              AgendaItem                   │
                                ├──────────────────────────────────────────┤
                                │ + id: int                                 │
                                │ + evento_id: int (FK)                     │
                                │ + hora_inicio: time                       │
                                │ + hora_fin: time?                         │
                                │ + titulo_actividad: str                   │
                                │ + descripcion: str?                       │
                                │ + ponente: str?                           │
                                │ + orden: int                              │
                                │ + created_at: datetime                    │
                                └──────────────────────────────────────────┘

┌──────────────────────┐        ┌──────────────────────────────────────────┐
│    IAConversacion     │        │              IAMensaje                    │
├──────────────────────┤        ├──────────────────────────────────────────┤
│ + id: int             │        │ + id: int                                 │
│ + usuario_id: int(FK) │ 1    N │ + conversacion_id: int (FK)               │
│ + evento_id: int (FK) │───────►│ + rol: RolMensajeEnum                     │
│ + rol_usuario: RolEnum│        │   (user | assistant)                      │
│   (cliente|empresario)│        │ + contenido: str                          │
│ + created_at          │        │ + created_at: datetime                    │
└──────────────────────┘        └──────────────────────────────────────────┘

«enumeration»              «enumeration»            «enumeration»
RolEnum                    CategoriaEnum            EstadoEnum
─────────────              ─────────────            ──────────────
usuario                    cultural                 borrador
empresario                 deportivo                publicado
                           turistico                cancelado
                           gastronomico
                           otro
```

---

## 6. Diagrama de Componentes UML

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DIAGRAMA DE COMPONENTES                                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                           <<subsystem>>                                   │
│                        FRONTEND (React SPA)                               │
│                                                                           │
│  ┌───────────────────┐   ┌─────────────────┐   ┌──────────────────────┐ │
│  │   <<module>>      │   │   <<module>>     │   │   <<module>>         │ │
│  │  Auth Module      │   │  Cliente Module  │   │  Empresario Module   │ │
│  │                   │   │                  │   │                      │ │
│  │ LoginPage         │   │ HomePage         │   │ EmpresaInicio        │ │
│  │ RoleSelectScreen  │   │ EventoDetailPage │   │ EventoSelector       │ │
│  │ RegisterPage      │   │ ChatWindow       │   │ EmpresaPanel         │ │
│  │ AuthContext       │   │ AgendaTimeline   │   │ EventoForm           │ │
│  │ ProtectedRoute    │   │ EventFilters     │   │ AgendaManager        │ │
│  └────────┬──────────┘   └────────┬─────────┘   └──────────┬───────────┘ │
│           │                       │                         │             │
│           └───────────────────────┴─────────────────────────┘             │
│                                   │                                        │
│                          ┌────────▼──────────┐                             │
│                          │  <<module>>        │                             │
│                          │  Services Layer    │                             │
│                          │                    │                             │
│                          │ api.js (axios)     │                             │
│                          │ authService        │                             │
│                          │ eventosService     │                             │
│                          │ agendaService      │                             │
│                          │ iaService          │                             │
│                          │ empresaService     │                             │
│                          └────────┬──────────┘                             │
└───────────────────────────────────┼────────────────────────────────────────┘
                                    │ HTTPS REST
┌───────────────────────────────────▼────────────────────────────────────────┐
│                           <<subsystem>>                                      │
│                        BACKEND (FastAPI)                                     │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ <<module>>   │  │ <<module>>   │  │ <<module>>   │  │ <<module>>    │  │
│  │   Auth       │  │  Eventos     │  │  Empresa     │  │   IA Chat     │  │
│  │              │  │              │  │              │  │               │  │
│  │ /auth/login  │  │ /eventos     │  │ /empresa/    │  │ /ia/chat      │  │
│  │ /auth/reg    │  │ /mis-eventos │  │  inicio      │  │ /ia/historial │  │
│  │ /auth/refresh│  │ /agenda      │  │ /empresa/    │  │               │  │
│  └──────┬───────┘  └──────┬───────┘  │  panel       │  └──────┬────────┘  │
│         │                 │          └──────┬───────┘         │           │
│         └─────────────────┴─────────────────┴─────────────────┘           │
│                                     │                                       │
│                     ┌───────────────▼──────────────┐                       │
│                     │       <<module>>              │                       │
│                     │      Services Layer           │                       │
│                     │                               │                       │
│                     │ auth_service                  │                       │
│                     │ evento_service                │                       │
│                     │ empresa_service               │                       │
│                     │ ia_service                    │                       │
│                     └───────────────┬──────────────┘                       │
│                                     │                                       │
│              ┌──────────────────────┼───────────────────────┐              │
│              │                      │                        │              │
│     ┌────────▼──────┐     ┌─────────▼──────┐     ┌─────────▼──────┐      │
│     │ <<database>>  │     │ <<external>>   │     │ <<middleware>>  │      │
│     │    MySQL /    │     │   n8n webhook  │     │  JWT Auth       │      │
│     │   MariaDB     │     │                │     │  CORS           │      │
│     └───────────────┘     └────────────────┘     └────────────────┘      │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
┌───────────────────────────────────▼────────────────────────────────────────┐
│                           <<subsystem>>                                      │
│                        n8n (Automatización)                                  │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐ │
│  │  WF-01 Chat IA   │  │ WF-02 Email      │  │  WF-03 Recordatorio     │ │
│  │  webhook         │  │ Notificación     │  │  diario (cron)          │ │
│  │  → LLM (OpenAI/  │  │ (evento creado/  │  │  → Eventos de mañana   │ │
│  │    Ollama)       │  │  publicado)      │  │  → Email organizador   │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Diagrama de Despliegue UML

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      DIAGRAMA DE DESPLIEGUE                               │
└──────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────┐
  │  <<device>>                  │
  │  Dispositivo del Usuario     │
  │  (móvil / tablet / desktop)  │
  │                              │
  │  ┌──────────────────────┐   │
  │  │ <<artifact>>          │   │
  │  │ React SPA             │   │
  │  │ (Vite build)          │   │
  │  │                       │   │
  │  │ Navegador Web         │   │
  │  └──────────┬────────────┘   │
  └─────────────┼───────────────┘
                │ HTTPS :443
  ┌─────────────▼───────────────────────────────────────────────────┐
  │  <<node>>                                                         │
  │  Servidor (VPS / Docker host)                                     │
  │                                                                   │
  │  ┌───────────────────┐   ┌───────────────────┐                  │
  │  │ <<container>>      │   │ <<container>>      │                  │
  │  │ nginx              │   │ FastAPI            │                  │
  │  │ :443 / :80         │   │ :8000              │                  │
  │  │                    │   │                    │                  │
  │  │ Sirve SPA estática │   │ API REST           │                  │
  │  │ Proxy → FastAPI    │   │ SQLAlchemy ORM     │                  │
  │  │ SSL termination    │   │ JWT Auth           │                  │
  │  └───────────────────┘   └─────────┬──────────┘                  │
  │                                     │                             │
  │  ┌──────────────────────────────────▼─────────────────────────┐  │
  │  │ <<container>>                                                │  │
  │  │ MariaDB 10.6 :3306                                          │  │
  │  │                                                              │  │
  │  │ DB: casanare_eventos                                         │  │
  │  │ Tablas: users, eventos, agenda_items,                        │  │
  │  │         ia_conversaciones, ia_mensajes,                      │  │
  │  │         sesiones_empresa                                     │  │
  │  └──────────────────────────────────────────────────────────────┘  │
  │                                                                   │
  │  ┌──────────────────────────────────┐                             │
  │  │ <<container>>                     │                             │
  │  │ n8n :5678                         │                             │
  │  │                                   │                             │
  │  │ WF-01: Chat IA webhook            │                             │
  │  │ WF-02: Email notificaciones       │                             │
  │  │ WF-03: Cron recordatorios         │                             │
  │  └──────────────────────────────────┘                             │
  └───────────────────────────────────────────────────────────────────┘
                │                          │
  ┌─────────────▼────────────┐  ┌──────────▼──────────────┐
  │ <<external service>>      │  │ <<external service>>     │
  │ OpenAI API                │  │ SMTP / SendGrid          │
  │ (GPT-4o-mini)             │  │ (envío de emails)        │
  └──────────────────────────┘  └─────────────────────────┘
```

---

## 8. Base de Datos — Esquema Actualizado

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
  created_at      DATETIME DEFAULT NOW()
  updated_at      DATETIME DEFAULT NOW() ON UPDATE NOW()

-- Tabla sesión activa del empresario (qué evento está gestionando)
sesiones_empresa
  id              INT PK AUTO_INCREMENT
  user_id         INT FK -> users.id UNIQUE  -- un empresario, un evento activo a la vez
  evento_id       INT FK -> eventos.id
  created_at      DATETIME DEFAULT NOW()
  updated_at      DATETIME DEFAULT NOW() ON UPDATE NOW()

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
  created_at      DATETIME DEFAULT NOW()
  updated_at      DATETIME DEFAULT NOW() ON UPDATE NOW()

-- Tabla agenda/programación del evento
agenda_items
  id                INT PK AUTO_INCREMENT
  evento_id         INT FK -> eventos.id
  hora_inicio       TIME NOT NULL
  hora_fin          TIME
  titulo_actividad  VARCHAR(200) NOT NULL
  descripcion       TEXT
  ponente           VARCHAR(150)
  orden             INT DEFAULT 0
  created_at        DATETIME DEFAULT NOW()

-- Tabla conversaciones IA (una por usuario × evento × rol)
ia_conversaciones
  id              INT PK AUTO_INCREMENT
  usuario_id      INT FK -> users.id
  evento_id       INT FK -> eventos.id
  rol_usuario     ENUM('cliente','empresario')  -- diferencia el contexto del chat
  created_at      DATETIME DEFAULT NOW()

-- Tabla mensajes dentro de cada conversación
ia_mensajes
  id              INT PK AUTO_INCREMENT
  conversacion_id INT FK -> ia_conversaciones.id
  rol             ENUM('user','assistant')
  contenido       TEXT NOT NULL
  created_at      DATETIME DEFAULT NOW()

-- Índices clave de rendimiento
INDEX idx_eventos_estado_fecha    ON eventos(estado, fecha_inicio)
INDEX idx_eventos_categoria       ON eventos(categoria)
INDEX idx_eventos_municipio       ON eventos(municipio)
INDEX idx_agenda_evento_hora      ON agenda_items(evento_id, hora_inicio)
INDEX idx_conv_usuario_evento_rol ON ia_conversaciones(usuario_id, evento_id, rol_usuario)
INDEX idx_mensajes_conv_fecha     ON ia_mensajes(conversacion_id, created_at)
```

---

## 9. Endpoints API — Tabla Completa Actualizada

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | /api/v1/auth/register | Público | Registro (elige rol al registrarse) |
| POST | /api/v1/auth/login | Público | Login → retorna JWT con `rol` en payload |
| POST | /api/v1/auth/refresh | Auth | Renovar access token |
| GET | /api/v1/eventos | Público | Listar eventos publicados (filtros + paginación) |
| GET | /api/v1/eventos/{id} | Público | Detalle del evento |
| GET | /api/v1/eventos/{id}/agenda | Público | Agenda/programación del evento |
| POST | /api/v1/ia/chat | Auth (cliente) | Chat IA cliente sobre un evento |
| GET | /api/v1/ia/conversacion/{evento_id} | Auth (cliente) | Historial chat cliente |
| GET | /api/v1/users/me | Auth | Perfil del usuario autenticado |
| PUT | /api/v1/users/me | Auth | Actualizar perfil |
| GET | /api/v1/empresa/inicio | Auth (empresario) | Pantalla inicio: lista sus eventos |
| POST | /api/v1/empresa/seleccionar-evento | Auth (empresario) | Guardar evento activo en sesión |
| GET | /api/v1/empresa/panel | Auth (empresario) | Datos del evento activo + agenda |
| PUT | /api/v1/empresa/panel/evento | Auth (empresario) | Editar datos del evento activo |
| PATCH | /api/v1/empresa/panel/publicar | Auth (empresario) | Publicar/despublicar el evento activo |
| GET | /api/v1/empresa/panel/agenda | Auth (empresario) | Listar agenda del evento activo |
| POST | /api/v1/empresa/panel/agenda | Auth (empresario) | Agregar ítem a la agenda |
| PUT | /api/v1/empresa/panel/agenda/{id} | Auth (empresario) | Editar ítem de agenda |
| DELETE | /api/v1/empresa/panel/agenda/{id} | Auth (empresario) | Eliminar ítem de agenda |
| POST | /api/v1/empresa/eventos | Auth (empresario) | Crear nuevo evento |
| POST | /api/v1/ia/empresa/chat | Auth (empresario) | Chat IA empresario (dudas de gestión) |
| GET | /api/v1/ia/empresa/conversacion | Auth (empresario) | Historial chat empresario |

---

## 10. Plan de Sprints Actualizado

| Sprint | Duración | Backend | Frontend |
|--------|----------|---------|----------|
| Sprint 0 | Día 1 | Setup, Docker, BD, migraciones | Setup Vite + Tailwind + routing |
| Sprint 1 | Días 2-3 | Auth + roles + sesión empresa | Login con selección de rol, RegisterPage |
| Sprint 2 | Días 4-5 | CRUD eventos + agenda endpoints | Vista pública: Home + EventoDetail |
| Sprint 3 | Días 6-7 | Módulo /empresa (panel, selección) | Pantalla inicio empresario + selector de evento |
| Sprint 4 | Días 8-9 | IA chat (cliente + empresario) | Panel empresario: form + agenda + chat |
| Sprint 5 | Días 10-11 | Testing backend ≥ 70% cobertura | Testing frontend + responsive final |
| Sprint 6 | Día 12 | Docs Swagger + docker-compose prod | Demo prep + pitch |
