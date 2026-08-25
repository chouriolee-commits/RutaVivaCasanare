# FRONTEND — Diseño Técnico + Responsive + Paleta Temática

**Proyecto:** Casanare en Movimiento  
**Tecnología:** React 18 + JavaScript + Vite + Tailwind CSS  
**Versión:** 3.0 — Flujos diferenciados por rol + Mobile-First

---

## 1. Paleta de Colores — Temática de Eventos Casanare

La paleta se inspira en la identidad visual del departamento: los llanos orientales,
el amanecer sobre el río Meta, las fiestas culturales y la naturaleza exuberante.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        PALETA PRINCIPAL                                   │
│                                                                           │
│  VERDE LLANO       DORADO AMANECER    TIERRA CASANARE   CIELO SABANA     │
│  #1B7A3E           #E8A020            #8B4513           #4A90D9          │
│  Verde oscuro      Naranja dorado     Marrón tierra     Azul cielo       │
│  Naturaleza,       Amanecer llanero,  Tradición,        Río Meta,        │
│  CTA primarios     acentos cálidos    raíces            tranquilidad     │
│                                                                           │
│  FONDO CLARO       TEXTO OSCURO       ÉXITO             ERROR            │
│  #F9F5EE           #1C1C1E            #16A34A           #DC2626          │
│  Beige suave       Casi negro         Verde menta       Rojo alerta      │
│  Fondo de página   Texto principal    Confirmaciones    Errores          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Colores por Categoría de Evento

```
Cultural     → Morado       #7C3AED  bg-purple-700  (arte, música, tradición)
Deportivo    → Azul         #1D4ED8  bg-blue-700    (deporte, competencia)
Turístico    → Verde agua   #0D9488  bg-teal-600    (naturaleza, viaje)
Gastronómico → Naranja      #EA580C  bg-orange-600  (comida, sabor)
Otro         → Gris         #374151  bg-gray-700    (general)
```

### tailwind.config.js — Configuración Completa

```javascript
const colors = require('tailwindcss/colors');

module.exports = {
  content: ['./src/**/*.{js,jsx}'],
  theme: {
    screens: {
      sm:  '320px',
      md:  '768px',
      lg:  '1024px',
      xl:  '1280px',
      '2xl': '1536px',
    },
    extend: {
      colors: {
        // Marca principal
        primary: {
          50:      '#F0FAF4',
          100:     '#D1F7E0',
          200:     '#A3EFC1',
          300:     '#6DDEA0',
          400:     '#3EC87D',
          DEFAULT: '#1B7A3E',   // Verde llano — acciones principales
          600:     '#166332',
          700:     '#114D27',
          800:     '#0C371C',
          900:     '#072212',
        },
        // Acento cálido
        golden: {
          50:      '#FFF9EC',
          100:     '#FEF0C7',
          200:     '#FEDD89',
          300:     '#FEC84B',
          DEFAULT: '#E8A020',   // Dorado amanecer — badges, highlights
          500:     '#C9891A',
          600:     '#A97215',
        },
        // Tierra
        earth: {
          DEFAULT: '#8B4513',   // Marrón tierra — detalles decorativos
          light:   '#C4844A',
          dark:    '#5C2D0D',
        },
        // Cielo
        sky: {
          DEFAULT: '#4A90D9',   // Azul cielo — info, links
          light:   '#7BB3E8',
          dark:    '#2C6BAA',
        },
        // Fondo
        sand: {
          DEFAULT: '#F9F5EE',   // Beige arena — fondo de página
          dark:    '#EDE8DD',
        },
        // Texto
        ink: {
          DEFAULT: '#1C1C1E',   // Texto principal
          light:   '#5C5C60',
          muted:   '#9CA3AF',
        },
        // Categorías de eventos
        categoria: {
          cultural:     '#7C3AED',
          deportivo:    '#1D4ED8',
          turistico:    '#0D9488',
          gastronomico: '#EA580C',
          otro:         '#374151',
        },
      },
      fontFamily: {
        sans:    ['Inter', 'system-ui', 'sans-serif'],
        display: ['Playfair Display', 'Georgia', 'serif'], // títulos de eventos
      },
      backgroundImage: {
        'hero-gradient':    'linear-gradient(135deg, #1B7A3E 0%, #166332 50%, #E8A020 100%)',
        'card-gradient':    'linear-gradient(180deg, transparent 50%, rgba(28,28,30,0.85) 100%)',
        'llanos-pattern':   "url('/patterns/llanos-dots.svg')",
      },
      boxShadow: {
        'card':    '0 2px 8px rgba(27, 122, 62, 0.08)',
        'card-hover': '0 8px 24px rgba(27, 122, 62, 0.18)',
        'panel':   '0 4px 20px rgba(0,0,0,0.10)',
      },
      keyframes: {
        'slide-up':   { '0%': { transform: 'translateY(100%)' }, '100%': { transform: 'translateY(0)' } },
        'fade-in':    { '0%': { opacity: '0' },                  '100%': { opacity: '1' } },
        'fade-scale': { '0%': { opacity: '0', transform: 'scale(0.95)' }, '100%': { opacity: '1', transform: 'scale(1)' } },
        'bounce-dot': { '0%, 100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-5px)' } },
      },
      animation: {
        'slide-up':   'slide-up 0.35s cubic-bezier(0.32, 0.72, 0, 1)',
        'fade-in':    'fade-in 0.25s ease-out',
        'fade-scale': 'fade-scale 0.2s ease-out',
        'bounce-dot': 'bounce-dot 1s ease-in-out infinite',
      },
    },
  },
  plugins: [],
};
```

### CSS Global (src/index.css)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html   { font-family: 'Inter', system-ui, sans-serif; }
  body   { background-color: #F9F5EE; color: #1C1C1E; }
  h1,h2  { font-family: 'Playfair Display', Georgia, serif; }
  *      { -webkit-tap-highlight-color: transparent; }
}

@layer components {
  /* Botón primario reutilizable */
  .btn-primary {
    @apply bg-primary text-white font-semibold px-4 py-2 rounded-xl
           hover:bg-primary-600 active:scale-95
           transition-all duration-150 disabled:opacity-50;
  }
  /* Badge de categoría base */
  .badge-categoria {
    @apply inline-flex items-center px-2.5 py-1 rounded-full
           text-xs font-semibold uppercase tracking-wide text-white;
  }
}

@layer utilities {
  .scrollbar-none          { scrollbar-width: none; }
  .scrollbar-none::-webkit-scrollbar { display: none; }
  .text-display            { font-family: 'Playfair Display', Georgia, serif; }
  .bg-sand                 { background-color: #F9F5EE; }
}
```

---

## 2. Estructura de Carpetas

```
frontend/src/
├── main.jsx
├── App.jsx                          # Router + providers
├── index.css
│
├── context/
│   └── AuthContext.jsx              # user, rol, login, logout, isEmpresario
│
├── hooks/
│   ├── useAuth.js
│   ├── useEventos.js
│   ├── useChat.js
│   ├── useEmpresa.js                # NUEVO: estado panel empresario
│   └── useMediaQuery.js
│
├── services/
│   ├── api.js                       # axios + interceptores
│   ├── authService.js
│   ├── eventosService.js
│   ├── agendaService.js
│   ├── empresaService.js            # NUEVO: /empresa/* endpoints
│   └── iaService.js
│
├── components/
│   ├── layout/
│   │   ├── Navbar.jsx               # Adaptado: logo + links según rol
│   │   ├── MobileMenu.jsx           # Drawer hamburguesa
│   │   ├── Footer.jsx
│   │   ├── PageContainer.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── EmpresarioRoute.jsx
│   ├── ui/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Textarea.jsx
│   │   ├── Select.jsx
│   │   ├── Badge.jsx                # Usa colores de la paleta temática
│   │   ├── Modal.jsx                # Bottom-sheet en móvil
│   │   ├── Spinner.jsx
│   │   ├── SkeletonCard.jsx
│   │   ├── EmptyState.jsx
│   │   └── Toast.jsx
│   ├── events/
│   │   ├── EventCard.jsx            # Tarjeta con gradiente de imagen
│   │   ├── EventFilters.jsx
│   │   └── AgendaTimeline.jsx
│   └── chat/
│       ├── ChatWindow.jsx           # Reutilizado: cliente y empresario
│       ├── ChatFAB.jsx
│       ├── ChatMessage.jsx
│       └── ChatInput.jsx
│
└── pages/
    ├── HomePage.jsx                 # Vista pública de eventos
    ├── EventoDetailPage.jsx         # Detalle + agenda + chat cliente
    ├── LoginPage.jsx                # Con selector de rol
    ├── RegisterPage.jsx             # Con selector de rol
    ├── PerfilPage.jsx
    └── empresa/                     # NUEVO: módulo empresario
        ├── EmpresaInicio.jsx        # ¿A qué evento perteneces?
        ├── EmpresaPanel.jsx         # Panel principal de gestión
        ├── EventoForm.jsx           # Crear / editar evento
        └── AgendaManager.jsx        # Gestión de agenda
```

---

## 3. Flujo de Navegación por Rol

```
/login ──── elige rol ────────────────────────────────────────────────┐
                                                                       │
       rol = 'usuario'                       rol = 'empresario'        │
             │                                       │                 │
             ▼                                       ▼                 │
       / (HomePage)                    /empresa/inicio                 │
       Lista eventos                   ┌──────────────────────┐        │
       publicados                      │ ¿Tienes un evento?   │        │
             │                         │                       │        │
             ▼                         │ [Seleccionar] [Crear] │        │
       /eventos/:id                    └──────────────────────┘        │
       Detalle + agenda                        │                       │
       + Chat IA cliente 💬                   ▼                       │
                                  /empresa/panel                       │
                                  Panel de gestión del evento          │
                                  ├─ Editar datos del evento           │
                                  ├─ Gestionar agenda/horarios         │
                                  ├─ Publicar / despublicar            │
                                  └─ Chat IA empresario 💬             │
                                                                       │
Rutas protegidas — sin sesión → /login ◄──────────────────────────────┘
```

---

## 4. AuthContext — Diseño con Roles

```jsx
// src/context/AuthContext.jsx

export function AuthProvider({ children }) {
  const [user, setUser]       = useState(null);  // { id, nombre, email, rol }
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      const payload = parseJwtPayload(token);
      if (payload?.exp > Date.now() / 1000) {
        setUser({ id: payload.sub, nombre: payload.nombre,
                  email: payload.email, rol: payload.rol });
      } else {
        silentRefresh();
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email, password) => {
    const data = await authService.login(email, password);
    localStorage.setItem('access_token',  data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    const payload = parseJwtPayload(data.access_token);
    const userData = { id: payload.sub, nombre: payload.nombre,
                       email: payload.email, rol: data.rol };
    setUser(userData);
    // Retorna el rol para que LoginPage sepa a dónde redirigir
    return data.rol;
  };

  const logout = () => {
    localStorage.clear();
    setUser(null);
  };

  const isEmpresario = () => user?.rol === 'empresario';
  const isCliente    = () => user?.rol === 'usuario';

  return (
    <AuthContext.Provider value={{
      user, isLoading, login, logout, isEmpresario, isCliente
    }}>
      {children}
    </AuthContext.Provider>
  );
}
```

---

## 5. LoginPage — Selector de Rol

```jsx
// src/pages/LoginPage.jsx

function LoginPage() {
  const { login }  = useAuth();
  const navigate   = useNavigate();
  const [rolSeleccionado, setRolSeleccionado] = useState(null); // 'usuario' | 'empresario'
  const [step, setStep]  = useState('seleccion'); // 'seleccion' | 'formulario'
  const [error, setError] = useState('');

  const handleRol = (rol) => {
    setRolSeleccionado(rol);
    setStep('formulario');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const { email, password } = formData;
    try {
      const rol = await login(email, password);
      // Redirigir según rol real del backend
      navigate(rol === 'empresario' ? '/empresa/inicio' : '/');
    } catch {
      setError('Credenciales incorrectas. Verifica tu email y contraseña.');
    }
  };

  return (
    <div className="min-h-screen bg-sand flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-sm md:max-w-md bg-white rounded-2xl shadow-panel p-6 md:p-8">

        {/* Logo y título */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 mx-auto mb-3 rounded-2xl bg-hero-gradient
                          flex items-center justify-center text-3xl shadow-card">
            🌿
          </div>
          <h1 className="text-display text-2xl font-bold text-ink">
            Casanare en Movimiento
          </h1>
          <p className="text-ink-light text-sm mt-1">Inicia sesión para continuar</p>
        </div>

        {/* PASO 1: Selector de rol */}
        {step === 'seleccion' && (
          <div>
            <p className="text-center text-ink font-medium mb-5">¿Cómo ingresas hoy?</p>
            <div className="grid grid-cols-2 gap-4">

              {/* Tarjeta Cliente */}
              <button
                onClick={() => handleRol('usuario')}
                className="group flex flex-col items-center gap-3 p-5 rounded-2xl
                           border-2 border-gray-100 hover:border-primary
                           hover:bg-primary-50 transition-all duration-200"
              >
                <div className="w-14 h-14 rounded-full bg-primary-50 group-hover:bg-primary-100
                                flex items-center justify-center text-3xl transition-colors">
                  👤
                </div>
                <div className="text-center">
                  <p className="font-semibold text-ink text-sm">Soy Cliente</p>
                  <p className="text-xs text-ink-muted mt-0.5">Explorar eventos</p>
                </div>
              </button>

              {/* Tarjeta Empresario */}
              <button
                onClick={() => handleRol('empresario')}
                className="group flex flex-col items-center gap-3 p-5 rounded-2xl
                           border-2 border-gray-100 hover:border-golden
                           hover:bg-golden-50 transition-all duration-200"
              >
                <div className="w-14 h-14 rounded-full bg-golden-50 group-hover:bg-golden-100
                                flex items-center justify-center text-3xl transition-colors">
                  🏢
                </div>
                <div className="text-center">
                  <p className="font-semibold text-ink text-sm">Soy Organizador</p>
                  <p className="text-xs text-ink-muted mt-0.5">Gestionar mi evento</p>
                </div>
              </button>
            </div>

            <p className="text-center text-sm text-ink-light mt-6">
              ¿No tienes cuenta?{' '}
              <Link to="/register" className="text-primary font-medium hover:underline">
                Regístrate aquí
              </Link>
            </p>
          </div>
        )}

        {/* PASO 2: Formulario de credenciales */}
        {step === 'formulario' && (
          <form onSubmit={handleSubmit} noValidate>
            {/* Indicador del rol seleccionado */}
            <div className={`
              flex items-center gap-2 mb-5 px-3 py-2 rounded-xl text-sm font-medium
              ${rolSeleccionado === 'usuario'
                ? 'bg-primary-50 text-primary-700'
                : 'bg-golden-50 text-golden-600'
              }
            `}>
              <span>{rolSeleccionado === 'usuario' ? '👤' : '🏢'}</span>
              <span>
                Ingresando como {rolSeleccionado === 'usuario' ? 'Cliente' : 'Organizador'}
              </span>
              <button
                type="button"
                onClick={() => setStep('seleccion')}
                className="ml-auto text-xs underline opacity-70 hover:opacity-100"
              >
                Cambiar
              </button>
            </div>

            <div className="flex flex-col gap-4">
              <Input label="Email" type="email" name="email" required />
              <Input label="Contraseña" type="password" name="password" required />
            </div>

            {error && (
              <p className="text-red-600 text-sm mt-3 bg-red-50 px-3 py-2 rounded-lg">
                {error}
              </p>
            )}

            <Button type="submit" variant="primary" className="w-full mt-6">
              Ingresar
            </Button>

            <p className="text-center text-sm text-ink-light mt-4">
              ¿No tienes cuenta?{' '}
              <Link to="/register" className="text-primary font-medium hover:underline">
                Regístrate
              </Link>
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
```

---

## 6. RegisterPage — Con selector de rol

```jsx
// src/pages/RegisterPage.jsx
// Mismo patrón de LoginPage: paso 1 = selección de rol, paso 2 = formulario

// En el formulario de registro se incluye:
// <input type="hidden" name="rol" value={rolSeleccionado} />
// Campos: nombre, email, password, confirmar password

// Colores del selector:
// rol = 'usuario'    → borde primary, icono 👤
// rol = 'empresario' → borde golden, icono 🏢
```

---

## 7. EmpresaInicio — Pantalla "¿A qué evento perteneces?"

```jsx
// src/pages/empresa/EmpresaInicio.jsx

function EmpresaInicio() {
  const { misEventos, eventoActivo, isLoading } = useEmpresa();
  const navigate = useNavigate();

  // Si ya tiene evento activo → redirigir al panel directamente
  useEffect(() => {
    if (eventoActivo) navigate('/empresa/panel');
  }, [eventoActivo]);

  return (
    <div className="min-h-screen bg-sand">

      {/* Header de bienvenida */}
      <div className="bg-hero-gradient text-white py-10 px-4">
        <PageContainer>
          <h1 className="text-display text-2xl md:text-3xl font-bold">
            Bienvenido, organizador 👋
          </h1>
          <p className="mt-2 text-white/80 text-sm md:text-base">
            Selecciona el evento que vas a gestionar hoy
          </p>
        </PageContainer>
      </div>

      <PageContainer className="py-8">

        {/* Botón crear nuevo evento — siempre visible arriba */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/empresa/evento/nuevo')}
            className="w-full md:w-auto flex items-center justify-center gap-2
                       bg-golden text-white font-semibold px-6 py-3 rounded-xl
                       hover:bg-golden-500 transition-colors shadow-card"
          >
            ✨ Crear nuevo evento
          </button>
        </div>

        {/* Lista de eventos existentes */}
        {misEventos.length > 0 && (
          <div>
            <h2 className="text-ink font-semibold mb-3">Mis eventos anteriores</h2>
            <div className="flex flex-col gap-3">
              {misEventos.map(evento => (
                <EventoSelectorCard
                  key={evento.id}
                  evento={evento}
                  onSeleccionar={() => handleSeleccionar(evento.id)}
                />
              ))}
            </div>
          </div>
        )}

        {/* Estado vacío: no tiene eventos */}
        {misEventos.length === 0 && !isLoading && (
          <EmptyState
            icon="📅"
            title="Aún no tienes eventos"
            description="Crea tu primer evento para comenzar a gestionar tu agenda"
          />
        )}
      </PageContainer>
    </div>
  );
}

// Tarjeta de evento en el selector
function EventoSelectorCard({ evento, onSeleccionar }) {
  return (
    <button
      onClick={onSeleccionar}
      className="w-full flex items-center gap-4 bg-white rounded-xl p-4
                 border-2 border-transparent hover:border-primary
                 shadow-card hover:shadow-card-hover
                 transition-all duration-200 text-left"
    >
      <div className="w-12 h-12 rounded-xl bg-primary-50 flex-shrink-0
                      flex items-center justify-center text-xl">
        🎪
      </div>
      <div className="flex-1 min-w-0">
        <p className="font-semibold text-ink text-sm truncate">{evento.titulo}</p>
        <p className="text-xs text-ink-muted mt-0.5">
          📅 {formatDate(evento.fecha_inicio)} · 📍 {evento.municipio}
        </p>
      </div>
      <Badge estado={evento.estado} />
      <span className="text-primary text-lg ml-1">›</span>
    </button>
  );
}
```

---

## 8. EmpresaPanel — Panel Principal del Organizador

### Layout del panel

```
MÓVIL                              DESKTOP (lg+)
──────────────────────────────     ────────────────────────────────────────
┌──────────────────────────┐       ┌────────────────────────────────────┐
│ Header: nombre evento    │       │ Sidebar        │  Contenido         │
│ Estado + badge           │       │ (w-64)         │  principal         │
└──────────────────────────┘       │                │                    │
┌──────────────────────────┐       │ 📋 Datos       │  [Sección activa]  │
│ Tabs de navegación:      │       │ 🗓 Agenda      │                    │
│ [Datos][Agenda][Publicar]│       │ 🌐 Publicar    │                    │
│ [Chat IA]                │       │ 💬 Chat IA     │                    │
└──────────────────────────┘       └────────────────────────────────────┘
┌──────────────────────────┐
│  Sección activa          │
│  (cambia según tab)      │
└──────────────────────────┘
```

```jsx
// src/pages/empresa/EmpresaPanel.jsx

const TABS = [
  { id: 'datos',   icon: '📋', label: 'Datos del evento' },
  { id: 'agenda',  icon: '🗓', label: 'Agenda' },
  { id: 'publicar',icon: '🌐', label: 'Publicación' },
  { id: 'chat',    icon: '💬', label: 'Asistente IA' },
];

function EmpresaPanel() {
  const { eventoActivo, agenda, isLoading } = useEmpresa();
  const [tabActivo, setTabActivo] = useState('datos');
  const isDesktop = useIsDesktop();

  if (!eventoActivo) return <Redirect to="/empresa/inicio" />;

  return (
    <div className="min-h-screen bg-sand">

      {/* Header del panel — nombre del evento activo */}
      <div className="bg-white border-b border-gray-100 shadow-sm sticky top-16 z-30">
        <PageContainer className="py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center
                              justify-center text-white text-sm flex-shrink-0">
                🎪
              </div>
              <div className="min-w-0">
                <p className="font-semibold text-ink text-sm truncate">
                  {eventoActivo.titulo}
                </p>
                <p className="text-xs text-ink-muted">
                  Panel de gestión
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge estado={eventoActivo.estado} />
              <button
                onClick={() => navigate('/empresa/inicio')}
                className="text-xs text-ink-muted hover:text-primary px-2 py-1 
                           rounded-lg hover:bg-gray-50"
              >
                Cambiar evento
              </button>
            </div>
          </div>
        </PageContainer>
      </div>

      <PageContainer className="py-6">
        <div className="lg:flex lg:gap-6 lg:items-start">

          {/* Sidebar de navegación — visible solo en desktop */}
          <aside className="hidden lg:flex flex-col gap-1 w-56 flex-shrink-0
                            bg-white rounded-2xl p-3 shadow-card sticky top-36">
            {TABS.map(tab => (
              <SidebarTabButton
                key={tab.id}
                tab={tab}
                activo={tabActivo === tab.id}
                onClick={() => setTabActivo(tab.id)}
              />
            ))}
          </aside>

          {/* Contenido principal */}
          <div className="flex-1 min-w-0">

            {/* Tabs horizontales — solo en móvil/tablet */}
            <div className="lg:hidden flex gap-1 mb-5 overflow-x-auto
                            pb-1 scrollbar-none">
              {TABS.map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setTabActivo(tab.id)}
                  className={`
                    flex-shrink-0 flex items-center gap-1.5
                    px-3 py-2 rounded-xl text-sm font-medium
                    transition-colors whitespace-nowrap
                    ${tabActivo === tab.id
                      ? 'bg-primary text-white'
                      : 'bg-white text-ink hover:bg-gray-50'
                    }
                  `}
                >
                  <span>{tab.icon}</span>
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>

            {/* Secciones del panel */}
            {tabActivo === 'datos'    && <SeccionDatosEvento evento={eventoActivo} />}
            {tabActivo === 'agenda'   && <SeccionAgenda eventoId={eventoActivo.id} />}
            {tabActivo === 'publicar' && <SeccionPublicacion evento={eventoActivo} />}
            {tabActivo === 'chat'     && (
              <SeccionChatEmpresario eventoId={eventoActivo.id} titulo={eventoActivo.titulo} />
            )}
          </div>
        </div>
      </PageContainer>
    </div>
  );
}
```

### SeccionDatosEvento — Formulario de edición
```jsx
function SeccionDatosEvento({ evento }) {
  // Formulario pre-poblado con los datos actuales
  // Mismo EventoForm reutilizado, pero en modo edición
  // Al guardar: PUT /api/v1/empresa/panel/evento
  // Feedback con Toast de éxito
}
```

### SeccionAgenda — Gestión de actividades
```jsx
function SeccionAgenda({ eventoId }) {
  // Lista de AgendaItem con acciones editar/eliminar
  // Botón "Agregar actividad" → Modal (bottom-sheet en móvil)
  // Orden visual cronológico con AgendaTimeline
  // Los cambios se reflejan inmediatamente (optimistic update)
}
```

### SeccionPublicacion — Toggle de estado
```jsx
function SeccionPublicacion({ evento }) {
  const [estado, setEstado] = useState(evento.estado);

  return (
    <div className="bg-white rounded-2xl p-6 shadow-card">
      <h2 className="text-display text-xl font-bold text-ink mb-2">
        Visibilidad del evento
      </h2>
      <p className="text-ink-light text-sm mb-6">
        Controla si tu evento es visible para el público en la plataforma.
      </p>

      {/* Card de estado actual */}
      <div className={`
        flex items-center justify-between p-4 rounded-xl border-2 mb-5
        ${estado === 'publicado'
          ? 'border-primary-200 bg-primary-50'
          : 'border-gray-200 bg-gray-50'
        }
      `}>
        <div className="flex items-center gap-3">
          <div className={`w-10 h-10 rounded-full flex items-center justify-center text-xl
                          ${estado === 'publicado' ? 'bg-primary text-white' : 'bg-gray-200'}`}>
            {estado === 'publicado' ? '🌐' : '🔒'}
          </div>
          <div>
            <p className="font-semibold text-ink text-sm">
              {estado === 'publicado' ? 'Evento publicado' : 'Evento en borrador'}
            </p>
            <p className="text-xs text-ink-muted">
              {estado === 'publicado'
                ? 'Visible para todos los usuarios'
                : 'Solo tú puedes verlo'
              }
            </p>
          </div>
        </div>
        <Badge estado={estado} />
      </div>

      {/* Requisitos para publicar */}
      {estado !== 'publicado' && (
        <ChecklistPublicacion evento={evento} />
      )}

      {/* Botón principal */}
      <Button
        variant={estado === 'publicado' ? 'danger' : 'primary'}
        className="w-full"
        onClick={handleToggle}
      >
        {estado === 'publicado' ? '🔒 Despublicar evento' : '🌐 Publicar evento'}
      </Button>
    </div>
  );
}
```

### SeccionChatEmpresario — Chat IA del organizador
```jsx
function SeccionChatEmpresario({ eventoId, titulo }) {
  // Reutiliza ChatWindow con prop rolChat="empresario"
  // Header diferente: "🤖 Asistente de Gestión"
  // Mensaje de bienvenida: "Hola, soy tu asistente para gestionar [Evento].
  //   Puedo ayudarte con dudas sobre fechas, agenda, publicación y más."
  return (
    <div className="bg-white rounded-2xl shadow-card overflow-hidden">
      <ChatWindow
        eventoId={eventoId}
        eventoTitulo={titulo}
        rolChat="empresario"           // cambia el system prompt en el backend
        welcomeMessage={`Hola 👋 Soy tu asistente para gestionar **${titulo}**. Pregúntame sobre fechas, agenda, publicación o lo que necesites.`}
        headerColor="bg-golden"        // dorado para el empresario vs verde para el cliente
        panel                          // siempre en altura completa
      />
    </div>
  );
}
```

---

## 9. EventoDetailPage — Diseño con Paleta Temática

```jsx
// src/pages/EventoDetailPage.jsx

function EventoDetailPage() {
  const { id } = useParams();

  return (
    <div className="min-h-screen bg-sand">

      {/* Hero con gradiente oscuro sobre la imagen */}
      <div className="relative w-full overflow-hidden h-56 md:h-72 lg:h-80 bg-gray-200">
        <img
          src={evento?.imagen_url || '/placeholder-event.jpg'}
          alt={evento?.titulo}
          className="w-full h-full object-cover"
        />
        {/* Gradiente card-gradient para legibilidad del título */}
        <div className="absolute inset-0 bg-card-gradient" />
        <div className="absolute bottom-4 left-4 right-4">
          <Badge categoria={evento?.categoria} />
          <h1 className="text-display text-xl md:text-2xl font-bold text-white mt-2
                         drop-shadow-lg leading-tight">
            {evento?.titulo}
          </h1>
        </div>
      </div>

      <PageContainer className="py-6">
        <div className="lg:flex lg:gap-6 lg:items-start">

          {/* Columna principal */}
          <div className="flex-1 min-w-0 space-y-4">

            {/* Info chips — con colores de la paleta */}
            <div className="bg-white rounded-2xl p-5 shadow-card">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                <InfoChip icon="📅" label="Fecha"    value={formatDate(evento?.fecha_inicio)}
                          color="text-primary" />
                <InfoChip icon="🕐" label="Hora"     value={formatTime(evento?.hora_inicio)}
                          color="text-golden" />
                <InfoChip icon="📍" label="Lugar"    value={evento?.ubicacion}
                          color="text-sky" />
                <InfoChip icon="🏙️" label="Municipio" value={evento?.municipio}
                          color="text-earth" />
                {evento?.aforo && (
                  <InfoChip icon="👥" label="Aforo"  value={`${evento.aforo} personas`}
                            color="text-ink-light" />
                )}
              </div>
            </div>

            {/* Descripción */}
            <div className="bg-white rounded-2xl p-5 shadow-card">
              <h2 className="text-display text-lg font-bold text-ink mb-3">
                Sobre el evento
              </h2>
              <p className="text-ink-light text-sm leading-relaxed md:text-base">
                {evento?.descripcion}
              </p>
            </div>

            {/* Agenda con la paleta */}
            <div className="bg-white rounded-2xl p-5 shadow-card">
              <h2 className="text-display text-lg font-bold text-ink mb-4">
                Programación
              </h2>
              <AgendaTimeline items={agenda} accentColor="primary" />
            </div>

            {/* Chat inline — móvil */}
            <div className="block lg:hidden">
              <ChatWindow eventoId={id} eventoTitulo={evento?.titulo}
                          rolChat="cliente" />
            </div>
          </div>

          {/* Panel chat — desktop */}
          <div className="hidden lg:block w-96 flex-shrink-0 sticky top-20 self-start">
            <ChatWindow eventoId={id} eventoTitulo={evento?.titulo}
                        rolChat="cliente" panel
                        headerColor="bg-primary" />
          </div>
        </div>
      </PageContainer>

      {/* FAB chat — móvil */}
      <ChatFAB className="lg:hidden" color="bg-primary" />
    </div>
  );
}
```

---

## 10. Badge — Componente con Paleta Temática

```jsx
// src/components/ui/Badge.jsx

const CATEGORIA_CONFIG = {
  cultural:     { label: 'Cultural',      bg: 'bg-purple-600',  icon: '🎭' },
  deportivo:    { label: 'Deportivo',     bg: 'bg-blue-700',    icon: '⚽' },
  turistico:    { label: 'Turístico',     bg: 'bg-teal-600',    icon: '🌿' },
  gastronomico: { label: 'Gastronómico',  bg: 'bg-orange-600',  icon: '🍽️' },
  otro:         { label: 'Otro',          bg: 'bg-gray-600',    icon: '📌' },
};

const ESTADO_CONFIG = {
  publicado:  { label: 'Publicado',  bg: 'bg-primary',     dot: 'bg-green-300' },
  borrador:   { label: 'Borrador',   bg: 'bg-golden',      dot: 'bg-yellow-200' },
  cancelado:  { label: 'Cancelado',  bg: 'bg-red-600',     dot: '' },
};

function Badge({ categoria, estado, size = 'sm' }) {
  if (categoria) {
    const cfg = CATEGORIA_CONFIG[categoria] || CATEGORIA_CONFIG.otro;
    return (
      <span className={`badge-categoria ${cfg.bg} ${size === 'lg' ? 'text-sm px-3 py-1.5' : ''}`}>
        <span className="mr-1">{cfg.icon}</span>
        {cfg.label}
      </span>
    );
  }

  if (estado) {
    const cfg = ESTADO_CONFIG[estado] || ESTADO_CONFIG.borrador;
    return (
      <span className={`
        inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full
        text-xs font-semibold text-white ${cfg.bg}
      `}>
        {cfg.dot && <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot} animate-pulse`} />}
        {cfg.label}
      </span>
    );
  }

  return null;
}
```

---

## 11. EventCard — Con Paleta Temática

```jsx
// src/components/events/EventCard.jsx
function EventCard({ evento }) {
  return (
    <article className="
      bg-white rounded-2xl overflow-hidden
      border border-sand-dark
      shadow-card hover:shadow-card-hover
      transition-all duration-200 flex flex-col h-full
    ">
      {/* Imagen con gradiente superpuesto */}
      <div className="relative overflow-hidden flex-shrink-0">
        <img
          src={evento.imagen_url || '/placeholder-event.jpg'}
          alt={evento.titulo}
          loading="lazy"
          className="w-full object-cover h-44 md:h-48 lg:h-52"
        />
        {/* Capa de color según categoría con opacidad baja */}
        <div className={`
          absolute inset-0 opacity-20
          ${evento.categoria === 'cultural'     ? 'bg-purple-600' : ''}
          ${evento.categoria === 'deportivo'    ? 'bg-blue-700' : ''}
          ${evento.categoria === 'turistico'    ? 'bg-teal-600' : ''}
          ${evento.categoria === 'gastronomico' ? 'bg-orange-600' : ''}
        `} />
        {/* Badge en esquina superior */}
        <div className="absolute top-3 left-3">
          <Badge categoria={evento.categoria} />
        </div>
      </div>

      {/* Contenido */}
      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-display font-bold text-ink text-base lg:text-lg
                       line-clamp-2 leading-snug">
          {evento.titulo}
        </h3>
        <div className="mt-2 space-y-1">
          <p className="text-xs text-ink-muted flex items-center gap-1.5">
            <span className="text-golden">📅</span>
            {formatDate(evento.fecha_inicio)}
          </p>
          <p className="text-xs text-ink-muted flex items-center gap-1.5">
            <span className="text-primary">📍</span>
            <span className="truncate">{evento.municipio || evento.ubicacion}</span>
          </p>
        </div>
        <p className="text-sm text-ink-light mt-2 line-clamp-2 flex-1">
          {evento.descripcion}
        </p>
        <Link
          to={`/eventos/${evento.id}`}
          className="mt-4 block text-center btn-primary"
        >
          Ver detalle →
        </Link>
      </div>
    </article>
  );
}
```

---

## 12. ChatWindow — Diferenciado por Rol

```jsx
// src/components/chat/ChatWindow.jsx
// Props: eventoId, eventoTitulo, rolChat ("cliente"|"empresario"),
//        panel, welcomeMessage, headerColor

function ChatWindow({
  eventoId,
  eventoTitulo,
  rolChat = 'cliente',
  panel = false,
  welcomeMessage,
  headerColor = 'bg-primary',
}) {
  const { user } = useAuth();
  const { mensajes, isLoading, enviarMensaje } = useChat(eventoId, rolChat);

  const defaultWelcome = rolChat === 'cliente'
    ? `¡Hola! Soy el asistente de **${eventoTitulo}**. ¿En qué puedo ayudarte?`
    : `Hola 👋 Soy tu asistente de gestión para **${eventoTitulo}**. Pregúntame lo que necesites.`;

  if (!user) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-card border border-sand-dark text-center">
        <div className="text-4xl mb-3">🤖</div>
        <h3 className="font-bold text-ink mb-2">Asistente IA</h3>
        <p className="text-sm text-ink-light mb-4">
          Inicia sesión para chatear con el asistente del evento
        </p>
        <Link to="/login" className="btn-primary block text-center">
          Iniciar sesión
        </Link>
      </div>
    );
  }

  return (
    <div className={`
      bg-white rounded-2xl shadow-card overflow-hidden flex flex-col
      ${panel ? 'h-[calc(100vh-8rem)]' : 'h-[420px] md:h-[480px]'}
    `}>
      {/* Header — color según rol */}
      <div className={`${headerColor} text-white flex items-center gap-3 px-4 py-3 flex-shrink-0`}>
        <span className="text-xl">🤖</span>
        <div className="min-w-0">
          <p className="font-semibold text-sm">
            {rolChat === 'empresario' ? 'Asistente de Gestión' : 'Asistente'}
          </p>
          <p className="text-xs opacity-75 truncate">{eventoTitulo}</p>
        </div>
        <div className="ml-auto flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-white/60 animate-pulse" />
          <span className="text-xs opacity-75">En línea</span>
        </div>
      </div>

      {/* Mensajes */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-sand">
        <ChatMessage rol="assistant" contenido={welcomeMessage || defaultWelcome}
                     accentColor={rolChat === 'empresario' ? 'golden' : 'primary'} />
        {mensajes.map(m => (
          <ChatMessage key={m.id} {...m}
                       accentColor={rolChat === 'empresario' ? 'golden' : 'primary'} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={isLoading}
                 accentColor={rolChat === 'empresario' ? 'golden' : 'primary'} />
    </div>
  );
}
```

---

## 13. Navbar — Adaptado a Roles

```jsx
// src/components/layout/Navbar.jsx
// Muestra links diferentes según el rol del usuario autenticado

// Menú para CLIENTE (rol='usuario'):
//   Desktop: [Inicio] [Perfil] [Cerrar sesión]
//   Móvil:   Igual en drawer

// Menú para EMPRESARIO (rol='empresario'):
//   Desktop: [Mi Evento] → /empresa/panel  [Perfil] [Cerrar sesión]
//   Móvil:   Igual en drawer

// Sin sesión:
//   Desktop: [Explorar Eventos] [Ingresar] [Registrarse]
//   Móvil:   Igual en drawer

// El logo usa el gradiente hero-gradient como fondo del ícono
```

---

## 14. Homepage — Con Paleta Temática

```jsx
// src/pages/HomePage.jsx

// Sección Hero:
// Fondo: bg-hero-gradient (verde → dorado)
// Título con fuente display: "Descubre Casanare en Movimiento"
// Subtítulo: "Eventos culturales, deportivos y turísticos del departamento"
// Sin botón CTA — el grid de eventos está justo abajo

// Grid de eventos:
// Fondo de la página: bg-sand (#F9F5EE)
// Cards con shadow-card y hover:shadow-card-hover
// Skeleton con tonos de sand

// Sección de categorías (opcional, encima del grid):
// Filtros visuales tipo chips con el color de cada categoría
// Ej: [🎭 Cultural] [⚽ Deportivo] [🌿 Turístico] [🍽 Gastronómico]
```

---

## 15. Breakpoints y Checklist Responsive

| Breakpoint | px | Dispositivo típico |
|-----------|----|--------------------|
| sm (base) | 320px | iPhone SE, Galaxy A |
| md | 768px | iPad Mini |
| lg | 1024px | iPad Pro, laptop |
| xl | 1280px | Desktop |

### Checklist por vista

| Vista | 320px | 768px | 1024px |
|-------|-------|-------|--------|
| LoginPage — selector de rol | Grid 2 cols centrado | Ídem más grande | Tarjeta max-md centrada |
| EmpresaInicio | Botón crear full, lista cards | Ídem | Ídem con max-w |
| EmpresaPanel | Tabs horizontales scroll | Tabs inline | Sidebar + contenido |
| EventoDetailPage | Stack: img→info→agenda→chat | Stack | 2 cols: contenido + chat |
| HomePage | 1 col cards | 2 cols | 3 cols |
| ChatWindow | 420px altura inline | 480px inline | Panel sticky altura viewport |
| Badge categoría | Texto + icono | Ídem | Ídem |
