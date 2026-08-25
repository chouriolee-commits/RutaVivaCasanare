# FRONTEND — Diseño Técnico Detallado + Sistema Responsive

**Proyecto:** Casanare en Movimiento  
**Tecnología:** React 18 + JavaScript + Vite + Tailwind CSS  
**Versión:** 2.0 — Mobile-First

---

## 1. Sistema de Breakpoints

La estrategia es **mobile-first**: los estilos base aplican a móvil y se escalan hacia arriba con modificadores de Tailwind.

```
xs  →  < 320px   (móviles pequeños — edge case)
sm  →  320px      Base móvil — DISEÑO PRIMARIO
md  →  768px      Tablet
lg  →  1024px     Laptop
xl  →  1280px     Desktop
2xl →  1536px     Desktop grande
```

Configuración en `tailwind.config.js`:
```javascript
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
        primary:   { DEFAULT: '#16A34A', light: '#22C55E', dark: '#15803D' },
        secondary: { DEFAULT: '#D97706', light: '#F59E0B', dark: '#B45309' },
        neutral:   { DEFAULT: '#374151', light: '#6B7280', dark: '#111827' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      spacing: {
        'safe-bottom': 'env(safe-area-inset-bottom)', // iOS notch
      },
      maxWidth: {
        'content': '1280px',
      },
    },
  },
  plugins: [],
}
```

---

## 2. Estructura de Carpetas

```
frontend/
├── public/
│   ├── placeholder-event.jpg
│   └── icons/                     # PWA icons (192x192, 512x512)
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── index.css                  # @tailwind + fuentes + variables CSS
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useEventos.js
│   │   ├── useChat.js
│   │   └── useMediaQuery.js       # Hook para detectar breakpoint activo
│   │
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── eventosService.js
│   │   ├── agendaService.js
│   │   └── iaService.js
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.jsx         # Con menú hamburguesa en móvil
│   │   │   ├── MobileMenu.jsx     # Drawer lateral para móvil
│   │   │   ├── Footer.jsx
│   │   │   ├── PageContainer.jsx  # Wrapper con max-width y padding lateral
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── EmpresarioRoute.jsx
│   │   ├── ui/
│   │   │   ├── Button.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Textarea.jsx
│   │   │   ├── Select.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Modal.jsx          # Full-screen en móvil, centrado en desktop
│   │   │   ├── Drawer.jsx         # Slide-in desde abajo en móvil
│   │   │   ├── Spinner.jsx
│   │   │   ├── SkeletonCard.jsx
│   │   │   ├── EmptyState.jsx
│   │   │   └── Toast.jsx          # Notificaciones de éxito/error
│   │   ├── events/
│   │   │   ├── EventCard.jsx
│   │   │   ├── EventFilters.jsx   # Colapsable en móvil
│   │   │   └── AgendaTimeline.jsx
│   │   └── chat/
│   │       ├── ChatWindow.jsx     # Panel fijo en desktop, drawer en móvil
│   │       ├── ChatFAB.jsx        # Botón flotante para abrir chat en móvil
│   │       ├── ChatMessage.jsx
│   │       └── ChatInput.jsx
│   │
│   ├── pages/
│   │   ├── HomePage.jsx
│   │   ├── EventoDetailPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── PerfilPage.jsx
│   │   └── dashboard/
│   │       ├── DashboardPage.jsx
│   │       ├── EventoFormPage.jsx
│   │       └── AgendaPage.jsx
│   │
│   └── utils/
│       ├── formatDate.js
│       ├── constants.js
│       └── validators.js
│
├── .env
├── .env.example
├── vite.config.js
├── tailwind.config.js
└── package.json
```

---

## 3. Layout Base — PageContainer

Componente wrapper que aplica el ancho máximo y padding lateral consistente en toda la app.

```jsx
// src/components/layout/PageContainer.jsx

function PageContainer({ children, className = '' }) {
  return (
    <div className={`
      w-full max-w-content mx-auto
      px-4          /* 16px en móvil */
      sm:px-4
      md:px-6       /* 24px en tablet */
      lg:px-8       /* 32px en desktop */
      ${className}
    `}>
      {children}
    </div>
  );
}
```

---

## 4. Navbar — Diseño Responsive

### Comportamiento por breakpoint

| Breakpoint | Comportamiento |
|------------|---------------|
| Móvil (< md) | Logo izquierda + botón hamburguesa derecha. Links ocultos. |
| Tablet (md) | Logo + links principales inline. Menú usuario con dropdown. |
| Desktop (lg+) | Logo + todos los links + botones login/registro o menú usuario. |

```jsx
// src/components/layout/Navbar.jsx

function Navbar() {
  const { user, logout, isEmpresario } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="
      sticky top-0 z-50
      bg-white border-b border-gray-100
      shadow-sm
    ">
      <PageContainer>
        <nav className="flex items-center justify-between h-16">

          {/* Logo — siempre visible */}
          <Link to="/" className="flex items-center gap-2 flex-shrink-0">
            <span className="text-2xl">🌿</span>
            <span className="
              font-bold text-primary
              text-base      /* 16px móvil */
              md:text-lg     /* 18px tablet+ */
            ">
              Casanare en Movimiento
            </span>
          </Link>

          {/* Links — solo visible en md+ */}
          <div className="hidden md:flex items-center gap-6">
            <Link to="/" className="text-sm font-medium text-neutral hover:text-primary transition-colors">
              Inicio
            </Link>
            {user && isEmpresario() && (
              <Link to="/dashboard" className="text-sm font-medium text-neutral hover:text-primary transition-colors">
                Dashboard
              </Link>
            )}
          </div>

          {/* Acciones — visible en md+ */}
          <div className="hidden md:flex items-center gap-3">
            {!user ? (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm">Ingresar</Button>
                </Link>
                <Link to="/register">
                  <Button variant="primary" size="sm">Registrarse</Button>
                </Link>
              </>
            ) : (
              <div className="flex items-center gap-3">
                <Link to="/perfil" className="text-sm text-neutral hover:text-primary">
                  👤 {user.nombre?.split(' ')[0]}
                </Link>
                <Button variant="ghost" size="sm" onClick={logout}>
                  Salir
                </Button>
              </div>
            )}
          </div>

          {/* Botón hamburguesa — solo visible en móvil */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            onClick={() => setMenuOpen(true)}
            aria-label="Abrir menú"
            aria-expanded={menuOpen}
          >
            {/* Icono hamburguesa */}
            <div className="w-6 flex flex-col gap-1.5">
              <span className="block h-0.5 bg-neutral-dark rounded" />
              <span className="block h-0.5 bg-neutral-dark rounded" />
              <span className="block h-0.5 bg-neutral-dark rounded" />
            </div>
          </button>
        </nav>
      </PageContainer>

      {/* Drawer de menú móvil */}
      <MobileMenu
        isOpen={menuOpen}
        onClose={() => setMenuOpen(false)}
        user={user}
        isEmpresario={isEmpresario}
        logout={logout}
      />
    </header>
  );
}
```

### MobileMenu — Drawer lateral

```jsx
// src/components/layout/MobileMenu.jsx

function MobileMenu({ isOpen, onClose, user, isEmpresario, logout }) {
  // Bloquear scroll del body cuando el menú está abierto
  useEffect(() => {
    document.body.style.overflow = isOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  return (
    <>
      {/* Overlay oscuro */}
      <div
        className={`
          fixed inset-0 z-40 bg-black transition-opacity duration-300
          ${isOpen ? 'opacity-50' : 'opacity-0 pointer-events-none'}
        `}
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Panel del menú — slide desde la derecha */}
      <div className={`
        fixed top-0 right-0 z-50
        h-full w-72 bg-white shadow-xl
        transform transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : 'translate-x-full'}
      `}
        role="dialog"
        aria-modal="true"
        aria-label="Menú de navegación"
      >
        {/* Header del drawer */}
        <div className="flex items-center justify-between p-4 border-b border-gray-100">
          <span className="font-bold text-primary">Menú</span>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100"
            aria-label="Cerrar menú"
          >
            ✕
          </button>
        </div>

        {/* Links de navegación */}
        <nav className="p-4 flex flex-col gap-1">
          <MobileNavLink to="/" onClick={onClose}>🏠 Inicio</MobileNavLink>

          {user ? (
            <>
              <MobileNavLink to="/perfil" onClick={onClose}>👤 Mi Perfil</MobileNavLink>
              {isEmpresario() && (
                <MobileNavLink to="/dashboard" onClick={onClose}>📊 Dashboard</MobileNavLink>
              )}
              <hr className="my-3 border-gray-100" />
              <button
                onClick={() => { logout(); onClose(); }}
                className="text-left w-full px-3 py-2.5 rounded-lg text-red-600 hover:bg-red-50 transition-colors text-sm font-medium"
              >
                🚪 Cerrar Sesión
              </button>
            </>
          ) : (
            <>
              <hr className="my-3 border-gray-100" />
              <MobileNavLink to="/login" onClick={onClose} highlight>
                Ingresar
              </MobileNavLink>
              <MobileNavLink to="/register" onClick={onClose} primary>
                Registrarse
              </MobileNavLink>
            </>
          )}
        </nav>
      </div>
    </>
  );
}

// Componente auxiliar para los links del menú móvil
function MobileNavLink({ to, onClick, children, primary = false }) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className={`
        block px-3 py-2.5 rounded-lg text-sm font-medium transition-colors
        ${primary
          ? 'bg-primary text-white text-center'
          : 'text-neutral hover:bg-gray-50'
        }
      `}
    >
      {children}
    </Link>
  );
}
```

---

## 5. HomePage — Diseño Responsive

### Layout general

```
MÓVIL                    TABLET                   DESKTOP
─────────────────────    ─────────────────────    ─────────────────────
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│   HERO (stack)    │    │   HERO (stack)    │    │   HERO (stack)    │
│  título, subtít.  │    │  título, subtít.  │    │  título, subtít.  │
└───────────────────┘    └───────────────────┘    └───────────────────┘
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│  FILTROS (stack)  │    │ FILTROS (3 cols)  │    │ FILTROS (4 cols)  │
│  [buscar]         │    │[buscar][cat][mun] │    │[buscar][cat][mun] │
└───────────────────┘    └───────────────────┘    └───────────────────┘
┌───────────────────┐    ┌────────┐ ┌────────┐    ┌────┐ ┌────┐ ┌────┐
│   EventCard       │    │ Card  │ │ Card  │    │Card│ │Card│ │Card│
├───────────────────┤    └────────┘ └────────┘    └────┘ └────┘ └────┘
│   EventCard       │    ┌────────┐ ┌────────┐    ┌────┐ ┌────┐ ┌────┐
├───────────────────┤    │ Card  │ │ Card  │    │Card│ │Card│ │Card│
│   EventCard       │    └────────┘ └────────┘    └────┘ └────┘ └────┘
└───────────────────┘
```

### EventFilters — Comportamiento responsive

```jsx
// src/components/events/EventFilters.jsx

function EventFilters({ filtros, onChange }) {
  const [filtersOpen, setFiltersOpen] = useState(false);

  return (
    <div className="mb-6">
      {/* Barra superior: búsqueda siempre visible + toggle de filtros en móvil */}
      <div className="flex gap-3 items-center">
        <Input
          placeholder="Buscar eventos..."
          value={filtros.busqueda}
          onChange={(e) => onChange({ ...filtros, busqueda: e.target.value })}
          className="flex-1"
          icon="🔍"
        />
        {/* Botón "Filtros" solo en móvil */}
        <button
          className="md:hidden flex items-center gap-1.5 px-3 py-2 border border-gray-200 rounded-lg text-sm text-neutral bg-white"
          onClick={() => setFiltersOpen(!filtersOpen)}
          aria-expanded={filtersOpen}
        >
          🎚 Filtros
          {(filtros.categoria || filtros.municipio) && (
            <span className="ml-1 w-2 h-2 rounded-full bg-primary inline-block" />
          )}
        </button>
      </div>

      {/* Filtros adicionales:
          - Móvil: se despliegan debajo al hacer clic en el botón
          - md+: siempre visibles en fila */}
      <div className={`
        mt-3 gap-3
        md:flex md:items-center
        ${filtersOpen ? 'flex flex-col' : 'hidden'}
      `}>
        <Select
          value={filtros.categoria}
          onChange={(val) => onChange({ ...filtros, categoria: val })}
          placeholder="Todas las categorías"
          options={CATEGORIAS}
          className="w-full md:w-48"
        />
        <Select
          value={filtros.municipio}
          onChange={(val) => onChange({ ...filtros, municipio: val })}
          placeholder="Todos los municipios"
          options={MUNICIPIOS}
          className="w-full md:w-48"
        />
        {(filtros.categoria || filtros.municipio || filtros.busqueda) && (
          <button
            className="text-sm text-red-500 hover:text-red-700 px-2 py-1"
            onClick={() => onChange({ busqueda: '', categoria: '', municipio: '' })}
          >
            ✕ Limpiar filtros
          </button>
        )}
      </div>
    </div>
  );
}
```

### Grid de EventCards

```jsx
// En HomePage.jsx — el grid se adapta a cada breakpoint
<div className="
  grid gap-4
  grid-cols-1           /* 1 columna en móvil */
  md:grid-cols-2        /* 2 columnas en tablet */
  lg:grid-cols-3        /* 3 columnas en desktop */
  xl:grid-cols-3        /* 3 columnas en desktop grande */
">
  {eventos.map(evento => <EventCard key={evento.id} evento={evento} />)}
</div>
```

### EventCard — Diseño responsive

```jsx
// src/components/events/EventCard.jsx

function EventCard({ evento }) {
  return (
    <article className="
      bg-white rounded-xl overflow-hidden
      border border-gray-100
      shadow-sm hover:shadow-md
      transition-all duration-200
      flex flex-col              /* columna en móvil */
      md:flex-col               /* columna en tablet+ también */
      h-full                    /* altura completa para grid uniforme */
    ">
      {/* Imagen */}
      <div className="relative overflow-hidden">
        <img
          src={evento.imagen_url || '/placeholder-event.jpg'}
          alt={evento.titulo}
          className="
            w-full object-cover
            h-44          /* altura fija móvil */
            md:h-48       /* altura fija tablet */
            lg:h-52       /* altura fija desktop */
          "
          loading="lazy"
        />
        {/* Badge de categoría superpuesto en la imagen */}
        <div className="absolute top-3 left-3">
          <Badge categoria={evento.categoria} />
        </div>
      </div>

      {/* Contenido */}
      <div className="p-4 flex flex-col flex-1">
        <h3 className="
          font-bold text-neutral-dark leading-snug
          text-base       /* 16px móvil */
          lg:text-lg      /* 18px desktop */
          line-clamp-2
        ">
          {evento.titulo}
        </h3>

        <div className="mt-2 flex flex-col gap-1">
          <p className="text-xs text-neutral-light flex items-center gap-1">
            📅 <span>{formatDate(evento.fecha_inicio)}</span>
          </p>
          <p className="text-xs text-neutral-light flex items-center gap-1">
            📍 <span className="truncate">{evento.municipio || evento.ubicacion}</span>
          </p>
        </div>

        <p className="mt-2 text-sm text-neutral line-clamp-2 flex-1">
          {evento.descripcion}
        </p>

        {/* CTA — siempre al final de la card */}
        <Link
          to={`/eventos/${evento.id}`}
          className="
            mt-4 block text-center
            bg-primary hover:bg-primary-dark
            text-white font-medium rounded-lg
            py-2 text-sm
            transition-colors duration-150
          "
        >
          Ver detalle
        </Link>
      </div>
    </article>
  );
}
```

---

## 6. EventoDetailPage — Diseño Responsive

### Layout por breakpoint

```
MÓVIL                         DESKTOP (lg+)
──────────────────────────    ──────────────────────────────────────
┌──────────────────────────┐  ┌──────────────────────────────────┐
│  Imagen hero (16:9)      │  │  Imagen hero (21:9)              │
└──────────────────────────┘  └──────────────────────────────────┘
┌──────────────────────────┐  ┌────────────────┐ ┌──────────────┐
│  Título + badges          │  │                │ │  CHAT PANEL  │
│  Fecha / hora / lugar     │  │  Info evento   │ │  (sticky)    │
│  Aforo                    │  │  Descripción   │ │              │
│  Descripción              │  │  Agenda        │ │  Fijo en     │
│  Agenda                   │  │                │ │  el costado  │
│                           │  │                │ │  derecho     │
│  [Chat flotante FAB] 💬   │  └────────────────┘ └──────────────┘
└──────────────────────────┘
```

```jsx
// src/pages/EventoDetailPage.jsx

function EventoDetailPage() {
  const { id } = useParams();
  const [evento, setEvento] = useState(null);
  const [agenda, setAgenda] = useState([]);
  const [chatOpen, setChatOpen] = useState(false);   // solo móvil
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Imagen hero */}
      <div className="w-full overflow-hidden bg-gray-200">
        <img
          src={evento?.imagen_url || '/placeholder-event.jpg'}
          alt={evento?.titulo}
          className="
            w-full object-cover
            h-56          /* 224px móvil */
            md:h-72       /* 288px tablet */
            lg:h-80       /* 320px desktop */
          "
        />
      </div>

      <PageContainer className="py-6">
        {/* Layout de dos columnas en desktop */}
        <div className="
          flex flex-col gap-6
          lg:flex-row
          lg:items-start
        ">

          {/* Columna principal — izquierda en desktop */}
          <div className="flex-1 min-w-0">

            {/* Encabezado del evento */}
            <div className="bg-white rounded-xl p-5 shadow-sm">
              <div className="flex flex-wrap gap-2 mb-3">
                <Badge categoria={evento?.categoria} />
                <StatusBadge estado={evento?.estado} />
              </div>

              <h1 className="
                font-bold text-neutral-dark
                text-xl        /* móvil */
                md:text-2xl    /* tablet */
                lg:text-3xl    /* desktop */
              ">
                {evento?.titulo}
              </h1>

              {/* Info rápida: fecha, lugar, aforo */}
              <div className="
                mt-4 grid gap-3
                grid-cols-1         /* stack en móvil */
                sm:grid-cols-2      /* 2 cols en sm */
                lg:grid-cols-3      /* 3 cols en desktop */
              ">
                <InfoChip icon="📅" label="Fecha" value={formatDate(evento?.fecha_inicio)} />
                <InfoChip icon="🕐" label="Hora" value={formatTime(evento?.hora_inicio)} />
                <InfoChip icon="📍" label="Lugar" value={evento?.ubicacion} />
                <InfoChip icon="🏙️" label="Municipio" value={evento?.municipio} />
                {evento?.aforo && (
                  <InfoChip icon="👥" label="Aforo" value={`${evento.aforo} personas`} />
                )}
              </div>
            </div>

            {/* Descripción */}
            <div className="bg-white rounded-xl p-5 shadow-sm mt-4">
              <h2 className="font-bold text-lg text-neutral-dark mb-3">Sobre el evento</h2>
              <p className="text-neutral text-sm leading-relaxed md:text-base">
                {evento?.descripcion}
              </p>
            </div>

            {/* Agenda */}
            <div className="bg-white rounded-xl p-5 shadow-sm mt-4">
              <h2 className="font-bold text-lg text-neutral-dark mb-4">Programación</h2>
              {agenda.length > 0
                ? <AgendaTimeline items={agenda} />
                : <p className="text-neutral-light text-sm">Programación próximamente.</p>
              }
            </div>

            {/* Chat en móvil/tablet — se muestra inline debajo de la agenda
                en desktop se muestra en el panel lateral */}
            <div className="block lg:hidden mt-4">
              <ChatSection eventoId={id} eventoTitulo={evento?.titulo} />
            </div>
          </div>

          {/* Panel lateral del chat — solo visible en desktop (lg+) */}
          <div className="
            hidden lg:block
            w-full lg:w-96 xl:w-[420px]
            flex-shrink-0
            sticky top-20          /* queda fijo al hacer scroll */
            self-start
            max-h-[calc(100vh-6rem)]
          ">
            <ChatSection eventoId={id} eventoTitulo={evento?.titulo} panel />
          </div>
        </div>
      </PageContainer>

      {/* Botón flotante del chat — solo en móvil/tablet cuando el chat inline está fuera de vista */}
      {user && (
        <ChatFAB
          onClick={() => setChatOpen(true)}
          className="lg:hidden"
        />
      )}
    </div>
  );
}
```

---

## 7. Chat IA — Diseño Responsive

### ChatFAB — Botón flotante (solo móvil)

```jsx
// src/components/chat/ChatFAB.jsx
function ChatFAB({ onClick, className = '' }) {
  return (
    <button
      onClick={onClick}
      aria-label="Abrir asistente IA"
      className={`
        fixed bottom-6 right-4
        z-30
        bg-primary hover:bg-primary-dark
        text-white
        w-14 h-14 rounded-full
        shadow-lg hover:shadow-xl
        flex items-center justify-center
        text-2xl
        transition-all duration-200
        active:scale-95
        pb-safe-bottom          /* seguro para iPhone con notch */
        ${className}
      `}
    >
      💬
    </button>
  );
}
```

### ChatWindow — Panel fijo desktop / Drawer móvil

```jsx
// src/components/chat/ChatWindow.jsx

function ChatWindow({ eventoId, eventoTitulo, panel = false }) {
  const { user } = useAuth();
  const { mensajes, isLoading, enviarMensaje } = useChat(eventoId);
  const [input, setInput] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [mensajes]);

  if (!user) {
    return (
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 text-center">
        <div className="text-4xl mb-3">🤖</div>
        <h3 className="font-bold text-neutral-dark mb-2">Asistente IA</h3>
        <p className="text-sm text-neutral mb-4">
          ¿Tienes dudas sobre este evento? Nuestro asistente puede ayudarte.
        </p>
        <Link to="/login" className="
          block bg-primary text-white text-sm font-medium
          py-2.5 px-5 rounded-lg text-center
          hover:bg-primary-dark transition-colors
        ">
          Iniciar sesión para chatear
        </Link>
      </div>
    );
  }

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    await enviarMensaje(input.trim());
    setInput('');
  };

  return (
    <div className={`
      bg-white rounded-xl shadow-sm border border-gray-100
      flex flex-col overflow-hidden
      ${panel
        ? 'h-[calc(100vh-7rem)]'   /* altura fija en panel desktop */
        : 'h-[420px] md:h-[500px]' /* altura fija en móvil/inline */
      }
    `}>
      {/* Header del chat */}
      <div className="
        flex items-center gap-3 px-4 py-3
        bg-primary text-white
        flex-shrink-0
      ">
        <span className="text-xl">🤖</span>
        <div className="min-w-0">
          <p className="font-medium text-sm">Asistente</p>
          <p className="text-xs opacity-80 truncate">{eventoTitulo}</p>
        </div>
        <div className="ml-auto flex items-center gap-1">
          <span className="w-2 h-2 rounded-full bg-green-300 animate-pulse" />
          <span className="text-xs opacity-80">En línea</span>
        </div>
      </div>

      {/* Área de mensajes — scrolleable */}
      <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-3">
        {/* Mensaje de bienvenida */}
        <ChatMessage
          rol="assistant"
          contenido={`¡Hola! Soy el asistente de **${eventoTitulo}**. ¿En qué puedo ayudarte?`}
        />
        {mensajes.map(m => <ChatMessage key={m.id} {...m} />)}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input — fijo al fondo */}
      <ChatInput
        value={input}
        onChange={setInput}
        onSend={handleSend}
        disabled={isLoading}
      />
    </div>
  );
}
```

### ChatInput — Responsive

```jsx
// src/components/chat/ChatInput.jsx

function ChatInput({ value, onChange, onSend, disabled }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="
      flex-shrink-0
      flex items-end gap-2
      px-3 py-3
      border-t border-gray-100
      bg-white
    ">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Escribe tu pregunta..."
        disabled={disabled}
        rows={1}
        className="
          flex-1 resize-none
          border border-gray-200 rounded-xl
          px-3 py-2
          text-sm text-neutral-dark
          placeholder:text-neutral-light
          focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary
          disabled:opacity-50 disabled:bg-gray-50
          max-h-28 overflow-y-auto
        "
        aria-label="Escribe tu pregunta al asistente"
      />
      <button
        onClick={onSend}
        disabled={disabled || !value.trim()}
        aria-label="Enviar mensaje"
        className="
          flex-shrink-0
          w-9 h-9 rounded-full
          bg-primary hover:bg-primary-dark
          disabled:opacity-40 disabled:cursor-not-allowed
          text-white flex items-center justify-center
          transition-colors duration-150
          active:scale-95
        "
      >
        {disabled ? <Spinner size="xs" color="white" /> : '➤'}
      </button>
    </div>
  );
}
```

### ChatMessage — Burbujas

```jsx
// src/components/chat/ChatMessage.jsx

function ChatMessage({ rol, contenido }) {
  const isUser = rol === 'user';

  return (
    <div className={`flex items-end gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`
        flex-shrink-0 w-7 h-7 rounded-full
        flex items-center justify-center text-sm
        ${isUser ? 'bg-primary/10' : 'bg-secondary/10'}
      `}>
        {isUser ? '👤' : '🤖'}
      </div>

      {/* Burbuja */}
      <div className={`
        max-w-[80%] md:max-w-[75%]
        px-3.5 py-2.5 rounded-2xl
        text-sm leading-relaxed
        ${isUser
          ? 'bg-primary text-white rounded-br-sm'
          : 'bg-gray-100 text-neutral-dark rounded-bl-sm'
        }
      `}>
        {contenido}
      </div>
    </div>
  );
}

// Indicador de escritura (3 puntos animados)
function TypingIndicator() {
  return (
    <div className="flex items-end gap-2">
      <div className="w-7 h-7 rounded-full bg-secondary/10 flex items-center justify-center text-sm flex-shrink-0">
        🤖
      </div>
      <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1 items-center">
        {[0, 1, 2].map(i => (
          <span
            key={i}
            className="w-2 h-2 rounded-full bg-neutral-light animate-bounce"
            style={{ animationDelay: `${i * 150}ms` }}
          />
        ))}
      </div>
    </div>
  );
}
```

---

## 8. Dashboard — Diseño Responsive

### Tabla → Cards en móvil

En móvil, la tabla de eventos se convierte en cards apiladas para ser legible en pantalla pequeña.

```jsx
// src/pages/dashboard/DashboardPage.jsx

function DashboardPage() {
  const { eventos, isLoading } = useMisEventos();
  const isMobile = useMediaQuery('(max-width: 767px)');

  return (
    <div className="min-h-screen bg-gray-50">
      <PageContainer className="py-6">

        {/* Header */}
        <div className="
          flex items-center justify-between mb-6
          flex-col gap-3       /* stack en móvil */
          sm:flex-row          /* fila en sm+ */
        ">
          <h1 className="text-xl md:text-2xl font-bold text-neutral-dark self-start">
            📊 Mis Eventos
          </h1>
          <Link to="/dashboard/eventos/nuevo">
            <Button variant="primary" className="w-full sm:w-auto">
              + Crear Evento
            </Button>
          </Link>
        </div>

        {/* Tabs de filtro */}
        <div className="
          flex gap-1 mb-4
          overflow-x-auto
          pb-1 scrollbar-none    /* scroll horizontal en móvil */
        ">
          {['Todos', 'Publicados', 'Borradores', 'Cancelados'].map(tab => (
            <TabButton key={tab} label={tab} />
          ))}
        </div>

        {/* Modo tabla — solo en md+ */}
        {!isMobile ? (
          <div className="bg-white rounded-xl shadow-sm overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50 border-b border-gray-100">
                  <tr>
                    <th className="text-left px-4 py-3 font-semibold text-neutral">Evento</th>
                    <th className="text-left px-4 py-3 font-semibold text-neutral hidden lg:table-cell">Categoría</th>
                    <th className="text-left px-4 py-3 font-semibold text-neutral">Fecha</th>
                    <th className="text-left px-4 py-3 font-semibold text-neutral">Estado</th>
                    <th className="text-right px-4 py-3 font-semibold text-neutral">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50">
                  {eventos.map(evento => (
                    <EventoTableRow key={evento.id} evento={evento} />
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          /* Modo cards — solo en móvil */
          <div className="flex flex-col gap-3">
            {eventos.map(evento => (
              <EventoMobileCard key={evento.id} evento={evento} />
            ))}
          </div>
        )}
      </PageContainer>
    </div>
  );
}
```

### EventoMobileCard — Vista de evento en móvil para el Dashboard

```jsx
function EventoMobileCard({ evento, onEditar, onPublicar, onEliminar, onAgenda }) {
  const [actionsOpen, setActionsOpen] = useState(false);

  return (
    <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
      {/* Encabezado */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-neutral-dark text-sm line-clamp-1">
            {evento.titulo}
          </h3>
          <p className="text-xs text-neutral-light mt-0.5">
            📅 {formatDate(evento.fecha_inicio)} · 📍 {evento.municipio}
          </p>
        </div>
        <Badge estado={evento.estado} />
      </div>

      {/* Acciones rápidas — siempre visibles en fila */}
      <div className="flex gap-2 mt-3 pt-3 border-t border-gray-50">
        <button
          onClick={() => onEditar(evento.id)}
          className="flex-1 flex items-center justify-center gap-1 text-xs py-1.5 rounded-lg border border-gray-200 text-neutral hover:bg-gray-50"
        >
          ✏️ Editar
        </button>
        <button
          onClick={() => onAgenda(evento.id)}
          className="flex-1 flex items-center justify-center gap-1 text-xs py-1.5 rounded-lg border border-gray-200 text-neutral hover:bg-gray-50"
        >
          📋 Agenda
        </button>
        <button
          onClick={() => onPublicar(evento.id, evento.estado)}
          className={`flex-1 flex items-center justify-center gap-1 text-xs py-1.5 rounded-lg border
            ${evento.estado === 'publicado'
              ? 'border-orange-200 text-orange-600 hover:bg-orange-50'
              : 'border-primary/30 text-primary hover:bg-primary/5'
            }`}
        >
          {evento.estado === 'publicado' ? '🔒 Ocultar' : '🌐 Publicar'}
        </button>
        <button
          onClick={() => onEliminar(evento.id)}
          className="w-9 flex items-center justify-center text-xs py-1.5 rounded-lg border border-red-100 text-red-500 hover:bg-red-50"
          aria-label="Eliminar evento"
        >
          🗑️
        </button>
      </div>
    </div>
  );
}
```

---

## 9. Formulario de Evento — Diseño Responsive

```jsx
// src/pages/dashboard/EventoFormPage.jsx — Estructura del layout

function EventoFormPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <PageContainer className="py-6">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <button onClick={() => navigate(-1)} className="text-neutral hover:text-primary p-1">
            ← Volver
          </button>
          <h1 className="text-xl font-bold text-neutral-dark">
            {isEditing ? 'Editar Evento' : 'Crear Evento'}
          </h1>
        </div>

        {/* Formulario en tarjeta */}
        <div className="bg-white rounded-xl shadow-sm p-5 md:p-8">
          <form onSubmit={handleSubmit} noValidate>

            {/* Grid de campos — 1 col móvil, 2 cols desktop */}
            <div className="
              grid gap-4
              grid-cols-1
              md:grid-cols-2
            ">
              {/* Título — ancho completo siempre */}
              <div className="md:col-span-2">
                <Input label="Título del evento *" name="titulo" error={errors.titulo} />
              </div>

              {/* Descripción — ancho completo siempre */}
              <div className="md:col-span-2">
                <Textarea label="Descripción *" name="descripcion" rows={4} error={errors.descripcion} />
              </div>

              {/* Categoría y municipio — 1 col cada uno en md */}
              <Select label="Categoría *" name="categoria" options={CATEGORIAS} error={errors.categoria} />
              <Input label="Municipio" name="municipio" />

              {/* Fechas — siempre en fila en md */}
              <Input label="Fecha de inicio *" type="date" name="fecha_inicio" error={errors.fecha_inicio} />
              <Input label="Fecha de fin" type="date" name="fecha_fin" />

              {/* Horas */}
              <Input label="Hora de inicio" type="time" name="hora_inicio" />
              <Input label="Hora de fin" type="time" name="hora_fin" />

              {/* Ubicación — ancho completo */}
              <div className="md:col-span-2">
                <Input label="Ubicación *" name="ubicacion" placeholder="Ej: Plaza Central, Yopal" error={errors.ubicacion} />
              </div>

              {/* Aforo e imagen URL */}
              <Input label="Aforo" type="number" name="aforo" placeholder="Capacidad máxima" />
              <Input label="URL de imagen" name="imagen_url" placeholder="https://..." />
            </div>

            {/* Botones de acción */}
            <div className="
              flex gap-3 mt-8
              flex-col          /* stack en móvil */
              sm:flex-row-reverse  /* fila invertida en sm+ */
            ">
              <Button
                type="submit"
                variant="primary"
                loading={isSaving === 'publicar'}
                onClick={() => setSaveMode('publicar')}
                className="w-full sm:w-auto"
              >
                Guardar y publicar
              </Button>
              <Button
                type="submit"
                variant="secondary"
                loading={isSaving === 'borrador'}
                onClick={() => setSaveMode('borrador')}
                className="w-full sm:w-auto"
              >
                Guardar borrador
              </Button>
              <Button
                type="button"
                variant="ghost"
                onClick={() => navigate(-1)}
                className="w-full sm:w-auto"
              >
                Cancelar
              </Button>
            </div>
          </form>
        </div>
      </PageContainer>
    </div>
  );
}
```

---

## 10. Modal — Responsive (full-screen en móvil)

```jsx
// src/components/ui/Modal.jsx

function Modal({ isOpen, onClose, title, children, size = 'md' }) {
  useEffect(() => {
    if (isOpen) document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = ''; };
  }, [isOpen]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm:  'max-w-sm',
    md:  'max-w-md',
    lg:  'max-w-lg',
    xl:  'max-w-xl',
  };

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Panel del modal */}
      <div className={`
        relative bg-white z-10 w-full shadow-xl
        /* Móvil: ocupa toda la pantalla desde abajo (sheet) */
        rounded-t-2xl
        /* sm+: centrado con bordes redondeados */
        sm:rounded-2xl sm:${sizeClasses[size]}
        /* Animación */
        animate-slide-up sm:animate-fade-scale
      `}>
        {/* Header */}
        <div className="flex items-center justify-between px-5 pt-5 pb-4 border-b border-gray-100">
          {/* Handle para swipe en móvil */}
          <div className="absolute top-3 left-1/2 -translate-x-1/2 w-10 h-1 rounded-full bg-gray-200 sm:hidden" />
          <h2 id="modal-title" className="font-bold text-neutral-dark mt-2 sm:mt-0">{title}</h2>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg hover:bg-gray-100 text-neutral-light text-lg"
            aria-label="Cerrar"
          >
            ✕
          </button>
        </div>

        {/* Contenido */}
        <div className="p-5 overflow-y-auto max-h-[75vh] sm:max-h-[70vh]">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
}
```

---

## 11. Hook useMediaQuery

```javascript
// src/hooks/useMediaQuery.js

import { useState, useEffect } from 'react';

export function useMediaQuery(query) {
  const [matches, setMatches] = useState(
    () => window.matchMedia(query).matches
  );

  useEffect(() => {
    const mq = window.matchMedia(query);
    const handler = (e) => setMatches(e.matches);
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [query]);

  return matches;
}

// Helpers pre-definidos
export const useIsMobile  = () => useMediaQuery('(max-width: 767px)');
export const useIsTablet  = () => useMediaQuery('(min-width: 768px) and (max-width: 1023px)');
export const useIsDesktop = () => useMediaQuery('(min-width: 1024px)');
```

---

## 12. Páginas de Auth — Responsive (Login y Registro)

```jsx
// Patrón compartido para LoginPage y RegisterPage

function AuthPageLayout({ title, subtitle, children }) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-10">
      <div className="
        w-full bg-white rounded-2xl shadow-sm border border-gray-100
        p-6          /* 24px móvil */
        md:p-8       /* 32px tablet+ */
        max-w-sm     /* ancho máximo del formulario */
        md:max-w-md
      ">
        {/* Logo */}
        <div className="text-center mb-6">
          <span className="text-4xl">🌿</span>
          <h1 className="text-xl font-bold text-neutral-dark mt-2">{title}</h1>
          <p className="text-sm text-neutral-light mt-1">{subtitle}</p>
        </div>

        {children}
      </div>
    </div>
  );
}
```

---

## 13. AgendaTimeline — Responsive

```jsx
// src/components/events/AgendaTimeline.jsx

function AgendaTimeline({ items }) {
  return (
    <ol className="relative">
      {items.map((item, index) => (
        <li key={item.id} className="
          flex gap-4 pb-6
          last:pb-0
        ">
          {/* Línea vertical + dot */}
          <div className="flex flex-col items-center flex-shrink-0">
            <div className="w-3 h-3 rounded-full bg-primary mt-1 ring-4 ring-primary/10 flex-shrink-0" />
            {index < items.length - 1 && (
              <div className="w-0.5 bg-gray-200 flex-1 mt-1" />
            )}
          </div>

          {/* Contenido del item */}
          <div className="flex-1 min-w-0 pb-2">
            {/* Hora */}
            <p className="text-xs font-mono font-semibold text-primary mb-1">
              {item.hora_inicio}
              {item.hora_fin && ` — ${item.hora_fin}`}
            </p>

            {/* Título */}
            <h4 className="
              font-semibold text-neutral-dark
              text-sm md:text-base
            ">
              {item.titulo_actividad}
            </h4>

            {/* Ponente */}
            {item.ponente && (
              <p className="text-xs text-neutral-light mt-0.5 flex items-center gap-1">
                🎤 {item.ponente}
              </p>
            )}

            {/* Descripción expandible */}
            {item.descripcion && (
              <details className="mt-1">
                <summary className="text-xs text-primary cursor-pointer hover:underline select-none">
                  Ver detalle
                </summary>
                <p className="text-sm text-neutral mt-1 leading-relaxed">
                  {item.descripcion}
                </p>
              </details>
            )}
          </div>
        </li>
      ))}
    </ol>
  );
}
```

---

## 14. Footer — Responsive

```jsx
// src/components/layout/Footer.jsx

function Footer() {
  return (
    <footer className="bg-neutral-dark text-white mt-16">
      <PageContainer className="py-8 md:py-10">
        <div className="
          grid gap-8
          grid-cols-1
          md:grid-cols-3
        ">
          {/* Marca */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-2xl">🌿</span>
              <span className="font-bold text-lg">Casanare en Movimiento</span>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
              La plataforma oficial de eventos culturales, deportivos y turísticos del departamento de Casanare.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold mb-3 text-sm uppercase tracking-wide text-gray-300">
              Navegación
            </h3>
            <ul className="flex flex-col gap-2 text-sm text-gray-400">
              <li><Link to="/" className="hover:text-white transition-colors">Inicio</Link></li>
              <li><Link to="/login" className="hover:text-white transition-colors">Ingresar</Link></li>
              <li><Link to="/register" className="hover:text-white transition-colors">Registrarse</Link></li>
            </ul>
          </div>

          {/* Hackathon */}
          <div>
            <h3 className="font-semibold mb-3 text-sm uppercase tracking-wide text-gray-300">
              Proyecto
            </h3>
            <p className="text-sm text-gray-400">
              Desarrollado en el Simulacro de Hackathon 02<br />
              Casanare — 2026
            </p>
          </div>
        </div>

        {/* Línea inferior */}
        <div className="
          mt-8 pt-6 border-t border-gray-700
          flex flex-col gap-2 items-center text-center
          md:flex-row md:justify-between
        ">
          <p className="text-xs text-gray-500">
            © 2026 Casanare en Movimiento. Todos los derechos reservados.
          </p>
          <p className="text-xs text-gray-500">
            Hecho con ❤️ en Casanare, Colombia
          </p>
        </div>
      </PageContainer>
    </footer>
  );
}
```

---

## 15. Paleta de Colores y Sistema de Diseño

```javascript
// tailwind.config.js — configuración completa
module.exports = {
  theme: {
    extend: {
      colors: {
        primary:   { DEFAULT: '#16A34A', light: '#22C55E', dark: '#15803D' },
        secondary: { DEFAULT: '#D97706', light: '#F59E0B', dark: '#B45309' },
        neutral:   { DEFAULT: '#374151', light: '#9CA3AF', dark: '#111827' },
      },
      keyframes: {
        'slide-up': {
          '0%':   { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        'fade-scale': {
          '0%':   { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
        bounce: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%':       { transform: 'translateY(-4px)' },
        },
      },
      animation: {
        'slide-up':   'slide-up 0.3s ease-out',
        'fade-scale': 'fade-scale 0.2s ease-out',
      },
    },
  },
}
```

### Variables CSS globales (`src/index.css`)

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  html { font-family: 'Inter', system-ui, sans-serif; }
  * { -webkit-tap-highlight-color: transparent; } /* quitar highlight táctil en iOS */
}

@layer utilities {
  .scrollbar-none::-webkit-scrollbar { display: none; }
  .scrollbar-none { -ms-overflow-style: none; scrollbar-width: none; }
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
}
```

---

## 16. Checklist Responsive por Vista

| Vista | 320px ✓ | 768px ✓ | 1024px ✓ |
|-------|---------|---------|----------|
| Navbar | Hamburguesa + drawer | Links inline | Links inline + acciones |
| HomePage | 1 col cards | 2 cols cards | 3 cols cards |
| EventFilters | Búsqueda + toggle | 3 cols inline | 4 cols inline |
| EventoDetail | Stack completo | Stack completo | 2 cols (info + chat) |
| AgendaTimeline | Timeline vertical | Timeline vertical | Timeline vertical |
| ChatWindow | Inline o drawer | Inline | Panel lateral sticky |
| DashboardPage | Cards apiladas | Tabla completa | Tabla completa |
| EventoFormPage | 1 col, botones stack | 2 cols, botones fila | 2 cols, botones fila |
| Modal | Bottom sheet | Centrado | Centrado |
| LoginPage | Card full-width | Card max-sm | Card max-md |
| Footer | Stack 1 col | 3 cols | 3 cols |
