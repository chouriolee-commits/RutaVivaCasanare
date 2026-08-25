# FRONTEND — Tareas de Codificación

**Proyecto:** Casanare en Movimiento  
**Desarrollador:** Frontend  
**Versión:** 2.0 — Mobile-First Responsive

---

## Reglas generales

- Toda tarea se implementa **mobile-first**: primero funciona en 320px, luego se agregan clases `md:` y `lg:` para escalar.
- Cada tarea incluye una sub-sección **Checklist Responsive** que debe completarse antes de marcar la tarea como terminada.
- Para probar el responsive: usar DevTools → modo dispositivo → probar en iPhone SE (375px), iPad (768px) y Desktop (1280px).

---

## SPRINT 0 — Setup del Proyecto

### T-F01 🔴 — Inicializar proyecto Vite + React + Tailwind
**Estimado:** 1.5h | **Dependencias:** Ninguna

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install react-router-dom axios date-fns
npm install -D tailwindcss postcss autoprefixer \
  vitest @vitest/ui @vitejs/plugin-react \
  @testing-library/react @testing-library/user-event \
  @testing-library/jest-dom jsdom
npx tailwindcss init -p
```

Configurar `tailwind.config.js` completo (ver `design.md §1`):
- Breakpoints personalizados (sm=320px, md=768px, lg=1024px)
- Colores primary, secondary, neutral
- Keyframes para animaciones slide-up y fade-scale

Configurar `src/index.css` (ver `design.md §15`):
- Import fuente Inter desde Google Fonts
- `@tailwind base`, `components`, `utilities`
- Utilidades custom: `scrollbar-none`, `line-clamp-2`
- Reset táctil: `-webkit-tap-highlight-color: transparent`

Configurar `vite.config.js`:
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js'],
    coverage: { provider: 'v8', reporter: ['text', 'html'], thresholds: { lines: 70 } }
  },
});
```

**Criterios de aceptación:**
- [ ] `npm run dev` levanta sin errores en http://localhost:5173
- [ ] Tailwind funciona: agregar `className="bg-primary text-white p-4"` a un div y verificar
- [ ] `npm run test -- --run` corre el setup sin errores
- [ ] En DevTools, cambiar a iPhone SE (375px) no genera scroll horizontal

---

### T-F02 🔴 — Crear capa de servicios API y AuthContext
**Estimado:** 2h | **Dependencias:** T-F01

1. Crear `src/services/api.js` con instancia axios + interceptores de request y response (ver `design.md §3`)
2. Crear `src/context/AuthContext.jsx` (ver `design.md §2`)
3. Crear `src/hooks/useAuth.js`
4. Crear `src/hooks/useMediaQuery.js` con `useIsMobile`, `useIsTablet`, `useIsDesktop` (ver `design.md §11`)
5. Crear `src/services/authService.js`:
   - `login(email, password)` → POST /auth/login, guarda tokens en localStorage
   - `register(data)` → POST /auth/register
   - `logout()` → limpia localStorage

**Criterios de aceptación:**
- [ ] Login guarda `access_token` y `refresh_token` en localStorage
- [ ] Interceptor refresca token automáticamente al recibir 401
- [ ] `useAuth()` retorna `{ user, isLoading, login, logout, isEmpresario }`
- [ ] Al refrescar la página, la sesión se recupera si el token es válido
- [ ] `useIsMobile()` retorna `true` en viewport < 768px y `false` en mayor

---

### T-F03 🔴 — Componentes UI base + Layout base
**Estimado:** 3h | **Dependencias:** T-F01

#### Componentes UI (`src/components/ui/`)

**Button.jsx**
```jsx
// Props: variant (primary|secondary|ghost|danger), size (sm|md|lg), loading, disabled, className
// Tamaños: sm=py-1.5 px-3 text-sm | md=py-2 px-4 text-sm | lg=py-2.5 px-5 text-base
// Área táctil mínima: ≥ 44px height en todos los tamaños
// Con loading: muestra <Spinner size="xs" /> inline + texto opaco
```

**Input.jsx**
```jsx
// Props: label, error, helperText, icon, ...rest (pasa al <input>)
// Label siempre encima del input (nunca placeholder como label)
// Error: texto rojo + borde rojo en el input
// Área del input: py-2.5 mínimo para área táctil adecuada
// Clase: w-full por defecto
```

**Textarea.jsx**
```jsx
// Props: label, error, rows (default 3), ...rest
// Mismo estilo visual que Input
// resize-y habilitado, resize-x deshabilitado
```

**Select.jsx**
```jsx
// Props: label, error, options [{value, label}], placeholder, value, onChange, className
// Usa <select> nativo (accesible y funciona bien en móvil con el picker nativo)
// Mismo estilo visual que Input
```

**Badge.jsx**
```jsx
// Props: categoria | estado
// Colores por categoría:
//   cultural     → bg-purple-100 text-purple-700
//   deportivo    → bg-blue-100 text-blue-700
//   turistico    → bg-cyan-100 text-cyan-700
//   gastronomico → bg-orange-100 text-orange-700
//   otro         → bg-gray-100 text-gray-600
// Colores por estado:
//   publicado    → bg-green-100 text-green-700
//   borrador     → bg-yellow-100 text-yellow-700
//   cancelado    → bg-red-100 text-red-700
// Texto siempre en mayúsculas con text-xs font-semibold
```

**Spinner.jsx**
```jsx
// Props: size (xs=16px | sm=20px | md=24px | lg=32px), color (default=primary | white)
// Implementar con border-4 border-primary/30 border-t-primary animate-spin
```

**SkeletonCard.jsx**
```jsx
// Placeholder de EventCard: mismas dimensiones pero con fondo animate-pulse
// Imagen: h-44 md:h-48 lg:h-52 bg-gray-200
// Líneas de texto: h-4 bg-gray-200 rounded con anchos variables
```

**EmptyState.jsx**
```jsx
// Props: icon (emoji), title, description, action (nodo React opcional)
// Centrado, máximo ancho 320px, iconos grandes (text-5xl)
```

**Toast.jsx**
```jsx
// Props: message, type (success|error|info), duration (default 3500ms)
// Posición: fixed top-4 right-4 en desktop, fixed bottom-20 left-4 right-4 en móvil
// Ancho: w-auto en desktop, w-full en móvil
// Aparece con animación slide-up, desaparece automáticamente
```

**Modal.jsx** (ver `design.md §10`):
- En móvil (< md): **bottom sheet** que sube desde abajo con `rounded-t-2xl`
- En desktop (md+): modal centrado con `rounded-2xl` y overlay oscuro
- Handle visual en la parte superior para indicar que se puede cerrar
- Bloquea scroll del body mientras está abierto
- Cierra con click en overlay o tecla ESC

#### Componente de Layout (`src/components/layout/`)

**PageContainer.jsx** (ver `design.md §3`):
```jsx
// Aplica: w-full max-w-content mx-auto px-4 md:px-6 lg:px-8
// Prop className para extensión
```

**Criterios de aceptación generales:**
- [ ] Todos los inputs tienen `label` asociado con `htmlFor` / `id`
- [ ] El modal es bottom sheet en 375px y centrado en 1024px (verificar en DevTools)
- [ ] Botones tienen min-height 44px en todos los tamaños
- [ ] El Toast aparece en la parte inferior en móvil y arriba-derecha en desktop
- [ ] Ningún componente genera scroll horizontal en 320px

---

### T-F04 🔴 — Navbar responsive + MobileMenu
**Estimado:** 2.5h | **Dependencias:** T-F02, T-F03

Implementar `src/components/layout/Navbar.jsx` (ver `design.md §4`):
- Logo siempre visible
- En **md+**: links y botones de auth inline en la barra
- En **< md**: solo logo + botón hamburguesa (3 líneas)
- Sticky en la parte superior (`sticky top-0 z-50`)

Implementar `src/components/layout/MobileMenu.jsx` (ver `design.md §4`):
- Drawer que desliza desde la **derecha** con `translate-x-full` → `translate-x-0`
- Overlay oscuro semi-transparente detrás del drawer
- Bloquea `body.overflow` mientras está abierto
- Muestra links según estado de autenticación y rol
- Cierra con click en overlay, botón ✕ o al navegar

**Checklist Responsive:**
- [ ] En 375px: solo se ve el logo y el botón hamburguesa
- [ ] Al abrir el menú en móvil, el overlay oscurece el fondo correctamente
- [ ] El drawer ocupa 288px de ancho (w-72) y no sale de la pantalla
- [ ] En 768px: desaparece el hamburguesa, aparecen los links inline
- [ ] En 1280px: se ven todos los links y botones sin overflow
- [ ] El foco del teclado queda atrapado dentro del menú abierto (accesibilidad)
- [ ] Navegación a otra ruta cierra automáticamente el menú

---

### T-F05 🔴 — Páginas de Auth (Login y Registro)
**Estimado:** 2h | **Dependencias:** T-F02, T-F03

Crear `src/pages/LoginPage.jsx` con `AuthPageLayout`:
- Tarjeta blanca centrada: `max-w-sm` en móvil, `max-w-md` en desktop
- Campos: email, password
- Validación: email válido con regex, password no vacío
- En éxito: redirige a `/dashboard` si empresario, a `/` si usuario
- En error 401: "Credenciales incorrectas"

Crear `src/pages/RegisterPage.jsx` con `AuthPageLayout`:
- Campos: nombre, email, password, confirmar password
- Validación en tiempo real: passwords coinciden, password ≥ 8 chars
- En éxito: login automático → redirige a `/`

Crear `src/components/layout/AuthPageLayout.jsx` (ver `design.md §12`):
- Centra el contenido vertical y horizontalmente en pantalla completa
- Tarjeta con padding responsivo: `p-6 md:p-8`

**Checklist Responsive:**
- [ ] En 375px: la tarjeta ocupa casi todo el ancho con padding lateral de 16px
- [ ] En 768px: la tarjeta queda centrada con ancho máximo visible
- [ ] Campos de formulario con ancho 100% de la tarjeta
- [ ] Botón de submit con ancho 100%

---

### T-F06 🟡 — Rutas protegidas
**Estimado:** 1h | **Dependencias:** T-F02

Crear `src/components/layout/ProtectedRoute.jsx`:
- Sin sesión → redirige a `/login`
- Con sesión → renderiza `<Outlet />`

Crear `src/components/layout/EmpresarioRoute.jsx`:
- Sin sesión → redirige a `/login`
- Con sesión pero sin rol empresario → redirige a `/perfil`
- Con rol empresario → renderiza `<Outlet />`

Crear `src/App.jsx` con toda la estructura de rutas (ver `design.md §5`):
- Envuelto en `<AuthProvider>` y `<BrowserRouter>`
- Incluye `<Navbar />` arriba y `<Footer />` abajo
- Todas las rutas definidas incluyendo `*` → `NotFoundPage`

**Criterios de aceptación:**
- [ ] `/dashboard` sin sesión → redirige a `/login`
- [ ] `/dashboard` con rol usuario → redirige a `/perfil`
- [ ] `/dashboard` con rol empresario → renderiza la página

---

## SPRINT 2 — Vista Pública de Eventos

### T-F07 🔴 — Servicios y hook de eventos
**Estimado:** 1.5h | **Dependencias:** T-F02

Crear `src/services/eventosService.js`:
- `getEventos(filtros, page)` → GET /eventos
- `getEventoById(id)` → GET /eventos/:id
- `getAgendaEvento(id)` → GET /eventos/:id/agenda

Crear `src/hooks/useEventos.js`:
```javascript
// Retorna: { eventos, isLoading, error, pagination, loadMore }
// Refetch automático al cambiar filtros (useEffect con debounce de 300ms en búsqueda de texto)
// Acumula páginas en el array para el "Cargar más"
```

**Criterios de aceptación:**
- [ ] Cambio de filtros dispara nuevo fetch (reemplaza la lista)
- [ ] "Cargar más" agrega items al final sin reemplazar los anteriores
- [ ] Errores de red son capturados y expuestos en el estado `error`

---

### T-F08 🔴 — EventFilters — Responsive
**Estimado:** 2h | **Dependencias:** T-F07

Crear `src/components/events/EventFilters.jsx` (ver `design.md §5`):

**Comportamiento móvil (< md):**
- Fila con: `[🔍 Input de búsqueda flex-1] [🎚 Filtros button]`
- Al presionar "Filtros": se despliegan los selects en columna debajo
- El botón muestra un indicador visual (punto verde) si hay filtros activos
- Botón "✕ Limpiar filtros" visible cuando hay filtros aplicados

**Comportamiento tablet/desktop (md+):**
- Fila única con: `[🔍 Búsqueda flex-1] [Categoría w-48] [Municipio w-48] [Limpiar]`
- Siempre visible, sin toggle

**Criterios de aceptación:**
- [ ] En 375px: solo se ve la búsqueda y el botón Filtros
- [ ] Al abrir filtros en móvil, los selects aparecen debajo sin romper el layout
- [ ] En 768px: todos los filtros inline en una sola fila
- [ ] Limpiar filtros resetea todos los valores y oculta el botón "Limpiar"

---

### T-F09 🔴 — HomePage
**Estimado:** 3h | **Dependencias:** T-F07, T-F08

Crear `src/pages/HomePage.jsx`:

**Sección Hero:**
```jsx
<section className="bg-gradient-to-br from-primary/10 to-secondary/5 py-10 md:py-16">
  <PageContainer className="text-center">
    <h1 className="text-2xl md:text-4xl font-bold text-neutral-dark">
      Eventos en Casanare
    </h1>
    <p className="mt-3 text-neutral text-sm md:text-base max-w-xl mx-auto">
      Descubre toda la agenda cultural, deportiva y turística del departamento
    </p>
  </PageContainer>
</section>
```

**Grid de eventos:**
```jsx
<div className="
  grid gap-4
  grid-cols-1
  md:grid-cols-2
  lg:grid-cols-3
">
```

**SkeletonCard** durante carga: mostrar 6 skeletons en el mismo grid

**EmptyState** si no hay resultados con el ícono 🎭 y mensaje sugeriendo limpiar filtros

**Checklist Responsive:**
- [ ] En 375px: 1 columna, tarjetas ocupan el ancho completo
- [ ] En 768px: 2 columnas sin overflow
- [ ] En 1280px: 3 columnas con espacio entre tarjetas
- [ ] El hero se ve bien en todos los breakpoints
- [ ] No hay scroll horizontal en ningún tamaño

---

### T-F10 🔴 — EventCard — Responsive
**Estimado:** 1.5h | **Dependencias:** T-F03

Crear `src/components/events/EventCard.jsx` (ver `design.md §5`):
- Imagen con `loading="lazy"` y alt descriptivo
- Altura de imagen adaptada: `h-44 md:h-48 lg:h-52`
- Badge de categoría superpuesto en esquina de la imagen
- Información compacta: título (clamp 2 líneas), fecha, municipio (truncated), descripción (clamp 2 líneas)
- Botón "Ver detalle" siempre al fondo de la card (`flex-1` en el contenido para empujar el botón)

**Checklist Responsive:**
- [ ] En 375px: la card ocupa el ancho completo, imagen de 176px de alto
- [ ] El título nunca desborda la card (line-clamp-2 funciona)
- [ ] El botón "Ver detalle" siempre está al fondo, independiente de la longitud del contenido
- [ ] La imagen muestra el placeholder si `imagen_url` es null

---

### T-F11 🔴 — EventoDetailPage — Responsive
**Estimado:** 4h | **Dependencias:** T-F07

Crear `src/pages/EventoDetailPage.jsx` (ver `design.md §6`):

**Layout:**
- Imagen hero: `h-56 md:h-72 lg:h-80` — siempre ancho completo
- Contenido con `<PageContainer>`:
  - **< lg**: stack vertical completo — info, descripción, agenda, chat inline
  - **lg+**: `flex flex-row gap-6` — columna izquierda (`flex-1`) + panel chat derecho (`w-96 sticky top-20`)

**Sección info del evento:**
- Grid de chips `InfoChip`: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3`
- Cada chip: icono + label + valor

**AgendaTimeline** (ver `design.md §13`):
- Timeline vertical con dot circular, línea conectora y contenido a la derecha
- Descripción expandible con `<details>/<summary>` nativo

**Chat:**
- En **< lg**: `<ChatSection>` como componente inline debajo de la agenda
- En **lg+**: `<ChatSection panel>` en el sidebar derecho (`sticky top-20 self-start`)
- `<ChatFAB>` visible solo en `< lg` y solo si el usuario está autenticado

**Checklist Responsive:**
- [ ] En 375px: todo en columna, imagen de 224px, chat al final de la página
- [ ] En 768px: igual al móvil pero con más espacio horizontal
- [ ] En 1280px: dos columnas, chat sticky visible a la derecha
- [ ] El FAB no tapa el contenido importante en móvil (posicionado abajo-derecha)
- [ ] Al hacer scroll, el panel del chat sigue visible en desktop
- [ ] Los chips de info se reorganizan según el breakpoint (1→2→3 columnas)

---

## SPRINT 4 — Chat IA

### T-F12 🔴 — Hook y servicio de chat IA
**Estimado:** 2h | **Dependencias:** T-F02

Crear `src/services/iaService.js`:
- `enviarMensaje(eventoId, mensaje)` → POST /ia/chat
- `getHistorial(eventoId)` → GET /ia/conversacion/:eventoId

Crear `src/hooks/useChat.js`:
- Carga historial al montar (si el usuario está autenticado)
- `enviarMensaje(texto)`: actualización optimista (el mensaje del usuario aparece inmediatamente), luego llama la API y agrega la respuesta
- Estado `isLoading` para mostrar el indicador de escritura

**Criterios de aceptación:**
- [ ] El mensaje del usuario aparece instantáneamente, sin esperar la respuesta
- [ ] Error en API muestra mensaje de error en el chat (no rompe el layout)
- [ ] Historial previo se carga al abrir el chat

---

### T-F13 🔴 — Componentes de chat — Responsive
**Estimado:** 3h | **Dependencias:** T-F12

**ChatWindow.jsx** (ver `design.md §7`):
- Prop `panel` para ajustar la altura: `h-[calc(100vh-7rem)]` (panel) vs `h-[420px] md:h-[500px]` (inline)
- Header verde con nombre del asistente y nombre del evento (truncado)
- Área de mensajes con `overflow-y-auto`
- Auto-scroll al último mensaje
- Sin sesión: muestra CTA de login centrado

**ChatMessage.jsx** (ver `design.md §7`):
- Usuario: burbuja verde, alineada a la derecha, `max-w-[80%]`
- Asistente: burbuja gris, alineada a la izquierda, `max-w-[80%]`
- Avatar circular de 28px para cada rol

**ChatInput.jsx** (ver `design.md §7`):
- `<textarea>` que crece automáticamente (max-h-28 con overflow)
- Botón enviar circular de 36px
- Enter envía, Shift+Enter inserta salto de línea
- Todo el área tiene mínimo 44px de altura

**ChatFAB.jsx** (ver `design.md §7`):
- Botón circular verde, `fixed bottom-6 right-4 z-30`
- Solo renderizado en `< lg` (clase `lg:hidden`)
- Emoji 💬, tamaño 56px

**TypingIndicator** (3 puntos animados):
- Tres dots con `animate-bounce` y `animationDelay` escalonado

**Checklist Responsive:**
- [ ] En 375px: ChatWindow inline tiene 420px de altura, scroll interno funciona
- [ ] En 375px: ChatFAB visible en esquina inferior derecha sin tapar el input de mensajes
- [ ] En 1280px: ChatFAB no se renderiza, panel lateral sticky visible
- [ ] Burbujas tienen max-width 80% y no desbordan la pantalla en 320px
- [ ] El textarea crece al escribir varias líneas pero no supera max-h-28
- [ ] Burbuja de asistente y usuario tienen avatar visible

---

## SPRINT 3 — Dashboard Empresario

### T-F14 🔴 — Servicios CRUD del empresario
**Estimado:** 1.5h | **Dependencias:** T-F02

Actualizar `eventosService.js` con:
- `getMisEventos(filtros)` → GET /mis-eventos
- `crearEvento(data)` → POST /eventos
- `actualizarEvento(id, data)` → PUT /eventos/:id
- `eliminarEvento(id)` → DELETE /eventos/:id
- `togglePublicar(id)` → PATCH /eventos/:id/publicar

Crear `src/services/agendaService.js`:
- `getAgenda(eventoId)` → GET /eventos/:id/agenda
- `crearItem(eventoId, data)` → POST /eventos/:id/agenda
- `actualizarItem(itemId, data)` → PUT /agenda/:id
- `eliminarItem(itemId)` → DELETE /agenda/:id

---

### T-F15 🔴 — DashboardPage — Responsive
**Estimado:** 4h | **Dependencias:** T-F14, T-F03

Crear `src/pages/dashboard/DashboardPage.jsx` (ver `design.md §8`):

**Header:**
- `flex-col gap-3` en móvil → `flex-row justify-between` en `sm+`
- Botón "Crear Evento": `w-full` en móvil, `w-auto` en `sm+`

**Tabs de estado:**
- `flex gap-1 overflow-x-auto pb-1 scrollbar-none` — permite scroll horizontal en móvil sin scrollbar visible
- Tabs: Todos / Publicados / Borradores / Cancelados

**Vista condicional basada en breakpoint:**
```jsx
const isMobile = useIsMobile(); // hook del proyecto

return isMobile
  ? <EventosMobileCards eventos={eventos} onAccion={...} />
  : <EventosTable eventos={eventos} onAccion={...} />;
```

**EventosMobileCards (< md):**
- `EventoMobileCard` por cada evento (ver `design.md §8`)
- Botones de acción en fila horizontal dentro de cada card
- Botón eliminar con icono 🗑️ sin texto (solo icono para ahorrar espacio)

**EventosTable (md+):**
- `overflow-x-auto` para scroll horizontal si la pantalla es justa
- Columna "Categoría" con `hidden lg:table-cell` (no visible en tablet)
- Acciones: iconos con tooltip en tablet, iconos + texto en desktop

**Checklist Responsive:**
- [ ] En 375px: cards apiladas, botones de acción horizontales en cada card
- [ ] En 768px: tabla visible con columnas Evento, Fecha, Estado, Acciones
- [ ] En 1024px: tabla añade la columna Categoría
- [ ] Tabs con scroll horizontal en 375px sin scrollbar visible
- [ ] Botón "Crear Evento" ocupa todo el ancho en 375px

---

### T-F16 🔴 — EventoFormPage — Responsive
**Estimado:** 3h | **Dependencias:** T-F14, T-F03

Crear `src/pages/dashboard/EventoFormPage.jsx` (ver `design.md §9`):

**Grid del formulario:**
```jsx
<div className="grid gap-4 grid-cols-1 md:grid-cols-2">
  {/* Ancho completo siempre */}
  <div className="md:col-span-2"><Input label="Título *" /></div>
  <div className="md:col-span-2"><Textarea label="Descripción *" rows={4} /></div>

  {/* Medio ancho en md+ */}
  <Select label="Categoría *" />
  <Input label="Municipio" />
  <Input label="Fecha inicio *" type="date" />
  <Input label="Fecha fin" type="date" />
  <Input label="Hora inicio" type="time" />
  <Input label="Hora fin" type="time" />

  {/* Ancho completo */}
  <div className="md:col-span-2"><Input label="Ubicación *" /></div>

  <Input label="Aforo" type="number" />
  <Input label="URL imagen" />
</div>
```

**Botones de acción:**
```jsx
<div className="flex gap-3 mt-8 flex-col sm:flex-row-reverse">
  <Button className="w-full sm:w-auto">Guardar y publicar</Button>
  <Button className="w-full sm:w-auto">Guardar borrador</Button>
  <Button className="w-full sm:w-auto">Cancelar</Button>
</div>
```

**Checklist Responsive:**
- [ ] En 375px: todos los campos en 1 columna, botones apilados de arriba abajo
- [ ] En 768px: campos cortos en 2 columnas, botones en fila (Publicar | Borrador | Cancelar)
- [ ] La tarjeta del formulario tiene padding `p-5 md:p-8`
- [ ] Los campos `date` y `time` abren el picker nativo del OS en móvil

---

### T-F17 🟡 — AgendaPage — Responsive
**Estimado:** 2.5h | **Dependencias:** T-F14, T-F03

Crear `src/pages/dashboard/AgendaPage.jsx`:

**Header:**
- Botón "← Volver" + título "Agenda — [Nombre Evento]" + botón "Agregar actividad"
- En móvil: título truncado con `truncate`, botón Agregar con solo icono `+` en pantallas muy pequeñas

**Lista de items:**
- Cada item: hora, título, ponente y botones ✏️ / 🗑️
- En móvil: botones de acción como iconos a la derecha
- En desktop: botones con icono + texto

**Modal de formulario:**
- Usar el componente `Modal` (bottom sheet en móvil, centrado en desktop)
- Campos: hora inicio, hora fin, título, ponente (opcional), descripción (optional)
- Grid de horas en fila: `grid grid-cols-2 gap-3`

**Checklist Responsive:**
- [ ] En 375px: modal aparece como bottom sheet (sube desde abajo)
- [ ] En 1024px: modal aparece centrado
- [ ] La lista de items es legible en 375px sin overflow

---

## SPRINT 5 — Testing

### T-F18 🔴 — Setup de tests
**Estimado:** 1h | **Dependencias:** T-F01

Crear `src/test/setup.js`:
```javascript
import '@testing-library/jest-dom';
import { vi } from 'vitest';
Object.defineProperty(window, 'localStorage', {
  value: { getItem: vi.fn(), setItem: vi.fn(), removeItem: vi.fn(), clear: vi.fn() }
});
// Mock matchMedia para tests con useMediaQuery
Object.defineProperty(window, 'matchMedia', {
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  }))
});
```

**Criterios de aceptación:**
- [ ] `npm run test -- --run` corre sin errores de configuración
- [ ] `matchMedia` mock previene errores en tests de componentes que usan `useMediaQuery`

---

### T-F19 🔴 — Tests responsive de componentes clave
**Estimado:** 3.5h | **Dependencias:** T-F18

| Componente | Tests requeridos |
|-----------|-----------------|
| `Navbar` | Renderiza hamburguesa en viewport < 768px; renderiza links en viewport ≥ 768px |
| `MobileMenu` | Abre y cierra correctamente; muestra links según autenticación |
| `EventFilters` | En móvil: botón Filtros visible, selects ocultos; al hacer clic: selects se muestran |
| `EventCard` | Renderiza todos los datos; placeholder si sin imagen; link correcto |
| `HomePage` | Muestra skeletons durante carga; muestra EmptyState sin resultados; grid renderizado |
| `EventoDetailPage` | Panel lateral no renderizado en viewport móvil; FAB visible en móvil |
| `ChatWindow` | CTA si no autenticado; burbujas alineadas correctamente; input envía con Enter |
| `DashboardPage` | Cards en móvil; tabla en desktop; tabs con scroll horizontal |
| `Modal` | Clase `rounded-t-2xl` en móvil; clase `rounded-2xl` en desktop |
| `LoginPage` | Formulario renderiza; validación funciona; submit llama a login |

**Patrón para simular breakpoints en tests:**
```javascript
// Al inicio del test, mockear matchMedia para simular móvil
beforeEach(() => {
  window.matchMedia = vi.fn().mockImplementation(query => ({
    matches: query.includes('max-width: 767px'), // simula móvil
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  }));
});
```

**Criterios de aceptación:**
- [ ] Todos los tests pasan en verde
- [ ] Ningún test hace llamadas HTTP reales
- [ ] Los tests de viewport simulan correctamente el breakpoint con el mock de `matchMedia`
- [ ] Cobertura de los componentes listados ≥ 70%

---

## SPRINT 6 — Preparación Final

### T-F20 🟡 — Footer + PerfilPage + NotFoundPage
**Estimado:** 2h | **Dependencias:** T-F03

**Footer** (ver `design.md §14`):
- Grid: 1 columna en móvil, 3 columnas en `md+`
- Línea inferior con copyright: stack en móvil, fila en `md+`

**PerfilPage:**
- Formulario de edición de nombre y teléfono
- Sección para cambiar rol a empresario con descripción + botón
- Mismo layout de tarjeta que los formularios de auth

**NotFoundPage:**
- EmptyState centrado con ícono 🗺️
- Botón "Volver al inicio"

---

### T-F21 🟡 — Checklist de calidad responsive final
**Estimado:** 1h | **Dependencias:** Todos los sprints anteriores

Verificar **cada vista** en estas dimensiones usando DevTools:

| Dispositivo | Resolución | Verificar |
|-------------|-----------|-----------|
| iPhone SE | 375 × 667 | Sin scroll horizontal, FAB visible, menú hamburguesa |
| iPhone 14 Pro | 393 × 852 | Sin scroll horizontal, layout correcto |
| iPad Mini | 768 × 1024 | Grids 2 cols, tabla dashboard, filtros inline |
| iPad Pro | 1024 × 1366 | Chat panel lateral, 3 cols grid, tabla completa |
| Desktop | 1280 × 800 | Layout completo, sin elementos cortados |

**Accesibilidad:**
- [ ] Todos los inputs tienen `label` asociado
- [ ] Botones sin texto tienen `aria-label`
- [ ] Drawer y modales tienen `role="dialog"` y `aria-modal="true"`
- [ ] Contraste de texto principal ≥ 4.5:1 (verde #16A34A sobre blanco ✓)
- [ ] Tab-order lógico en todos los formularios
- [ ] No hay elementos con `tabIndex > 0`
