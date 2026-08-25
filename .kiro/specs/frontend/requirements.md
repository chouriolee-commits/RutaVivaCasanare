# FRONTEND — Requerimientos Funcionales y Técnicos

**Proyecto:** Casanare en Movimiento  
**Tecnología:** React 18 + JavaScript (ES2022) + Vite + Tailwind CSS  
**Responsable:** Desarrollador Frontend  
**Versión:** 2.0 — Mobile-First Responsive

---

## 1. Alcance del Frontend

Aplicación web SPA (Single Page Application) construida con React 18 y Vite que:
- Presenta eventos del departamento de Casanare al público general
- Permite a organizadores gestionar sus eventos desde un dashboard
- Integra un chat con asistente IA contextual por evento
- Es completamente **responsive y mobile-first**: diseñada primero para móvil (320px) y escalada hacia tablet y desktop

---

## 2. Páginas y Vistas

### Públicas (sin autenticación)
| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/` | `HomePage` | Listado de eventos con filtros responsive |
| `/eventos/:id` | `EventoDetailPage` | Detalle + agenda + chat IA adaptado al breakpoint |
| `/login` | `LoginPage` | Formulario centrado con tarjeta |
| `/register` | `RegisterPage` | Formulario centrado con tarjeta |

### Protegidas — Usuario autenticado
| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/perfil` | `PerfilPage` | Ver y editar perfil |

### Protegidas — Solo Empresario
| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/dashboard` | `DashboardPage` | Cards en móvil / tabla en desktop |
| `/dashboard/eventos/nuevo` | `EventoFormPage` | Formulario 1 col móvil / 2 cols desktop |
| `/dashboard/eventos/:id/editar` | `EventoFormPage` | Ídem con campos pre-poblados |
| `/dashboard/eventos/:id/agenda` | `AgendaPage` | Lista de actividades con acciones |

---

## 3. Requerimientos Funcionales

### RF-F01 — Autenticación
- RF-F01.1: Formulario de registro con validación en tiempo real (email, password ≥ 8 chars, nombre)
- RF-F01.2: Formulario de login con manejo de error de credenciales
- RF-F01.3: Tokens JWT en `localStorage` (access + refresh)
- RF-F01.4: Refresh automático del access_token (interceptor axios al recibir 401)
- RF-F01.5: Logout limpia tokens y redirige a `/`
- RF-F01.6: Rutas protegidas redirigen a `/login` si no hay sesión activa
- RF-F01.7: En móvil el formulario ocupa todo el ancho disponible dentro de una tarjeta centrada

### RF-F02 — Homepage de Eventos
- RF-F02.1: Mostrar tarjetas de eventos publicados: imagen, título, fecha, municipio, categoría
- RF-F02.2: Filtro por categoría con tabs o select
- RF-F02.3: Filtro por municipio con select
- RF-F02.4: Búsqueda de texto en tiempo real por título
- RF-F02.5: Paginación con botón "Cargar más"
- RF-F02.6: Skeleton loader mientras se obtienen los datos
- RF-F02.7: Estado vacío cuando no hay resultados
- RF-F02.8: Los filtros secundarios (categoría, municipio) se ocultan detrás de un botón "Filtros" en móvil y se muestran inline en tablet+
- RF-F02.9: El grid se adapta: 1 columna en móvil, 2 en tablet, 3 en desktop

### RF-F03 — Detalle de Evento
- RF-F03.1: Imagen hero del evento (ratio 16:9 en móvil, más ancho en desktop)
- RF-F03.2: Info completa: título, descripción, fecha, hora, ubicación, municipio, aforo, categoría
- RF-F03.3: Agenda en formato timeline vertical con hora, título, ponente y descripción expandible
- RF-F03.4: En **móvil/tablet**: chat IA inline debajo de la agenda
- RF-F03.5: En **desktop (lg+)**: chat IA en panel lateral sticky de 400px a la derecha del contenido
- RF-F03.6: En **móvil**: botón flotante (FAB) 💬 para abrir el chat como drawer desde abajo cuando el usuario hace scroll y el chat queda fuera de vista
- RF-F03.7: Sin sesión: mostrar CTA de login en lugar del chat

### RF-F04 — Chat con Asistente IA
- RF-F04.1: Área de mensajes scrolleable con burbujas: usuario a la derecha, asistente a la izquierda
- RF-F04.2: Textarea de entrada multi-línea con botón enviar y soporte de Enter (Shift+Enter para salto de línea)
- RF-F04.3: Indicador de escritura animado (3 puntos) mientras el asistente procesa
- RF-F04.4: Historial persistido en API, cargado al montar el componente
- RF-F04.5: Mensaje de bienvenida fijo al inicio del chat
- RF-F04.6: En móvil, altura del chat limitada a 420px con scroll interno
- RF-F04.7: En desktop (panel), altura que ocupe el viewport disponible con scroll interno
- RF-F04.8: Auto-scroll al último mensaje tras cada respuesta

### RF-F05 — Dashboard del Empresario
- RF-F05.1: En **móvil**: lista de cards con información compacta y botones de acción horizontales
- RF-F05.2: En **tablet/desktop**: tabla con columnas: Evento, Categoría (oculta en tablet), Fecha, Estado, Acciones
- RF-F05.3: Tabs de filtro con scroll horizontal en móvil: Todos / Publicados / Borradores / Cancelados
- RF-F05.4: Botón "Crear Evento" alineado a la derecha en tablet+, ancho completo en móvil
- RF-F05.5: Acciones por evento: Editar, Agenda, Publicar/Despublicar, Eliminar
- RF-F05.6: Modal de confirmación (bottom sheet en móvil, centrado en desktop) antes de eliminar
- RF-F05.7: Badge de estado con colores: verde=publicado, amarillo=borrador, rojo=cancelado

### RF-F06 — Formulario de Evento
- RF-F06.1: En **móvil**: todos los campos en una sola columna
- RF-F06.2: En **desktop (md+)**: grid de 2 columnas para campos cortos (fechas, horas, municipio, aforo); campos largos (título, descripción, ubicación) en ancho completo
- RF-F06.3: En modo edición los campos vienen pre-poblados
- RF-F06.4: Botones "Guardar borrador" y "Guardar y publicar": en móvil apilados, en tablet+ en fila
- RF-F06.5: Validación inline: error visible debajo de cada campo
- RF-F06.6: Toast de confirmación de éxito o error tras guardar

### RF-F07 — Gestión de Agenda
- RF-F07.1: Lista de actividades ordenadas por hora con botones editar/eliminar por item
- RF-F07.2: Formulario de nueva actividad en Modal (bottom sheet en móvil)
- RF-F07.3: Campos del formulario: hora inicio, hora fin, título actividad, ponente, descripción
- RF-F07.4: Confirmación antes de eliminar (modal de confirmación)
- RF-F07.5: Validación: hora fin > hora inicio

---

## 4. Requerimientos No Funcionales

| ID | Descripción |
|----|-------------|
| RNF-F01 | Carga inicial ≤ 3 segundos en conexión 3G simulada |
| RNF-F02 | **Responsive obligatorio en:** 320px, 375px, 768px, 1024px, 1280px |
| RNF-F03 | Accesibilidad WCAG 2.1 AA: contraste mínimo 4.5:1, todos los inputs con `label`, navegación por teclado, roles ARIA en drawer y modales |
| RNF-F04 | Touch-friendly: todos los elementos interactivos ≥ 44x44px de área táctil |
| RNF-F05 | Formularios con validación cliente antes de llamar al API |
| RNF-F06 | Sin scroll horizontal en ningún breakpoint |
| RNF-F07 | Imágenes con `loading="lazy"` y atributo `alt` descriptivo |
| RNF-F08 | El FAB del chat no tapa contenido esencial en móvil (posición fija con padding) |
| RNF-F09 | Menú móvil bloquea el scroll del body mientras está abierto |
| RNF-F10 | Modales y drawers cierran con clic en overlay o tecla ESC |

---

## 5. Componentes Nuevos por Responsive

Además de los componentes base, el diseño responsive requiere estos componentes adicionales:

| Componente | Motivo |
|-----------|--------|
| `PageContainer` | Wrapper con max-width y padding lateral consistente en toda la app |
| `MobileMenu` | Drawer lateral para navegación en móvil |
| `ChatFAB` | Botón flotante para abrir chat en móvil cuando está fuera de vista |
| `Drawer` | Panel deslizable desde abajo (bottom sheet) para modales en móvil |
| `EventoMobileCard` | Vista compacta del evento en dashboard para pantallas pequeñas |
| `Toast` | Notificaciones flotantes de éxito/error |
| `useMediaQuery` | Hook para detectar breakpoint activo y renderizar condicionalmente |

---

## 6. Dependencias npm

```json
{
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.23.1",
    "axios": "^1.7.2",
    "date-fns": "^3.6.0"
  },
  "devDependencies": {
    "vite": "^5.2.0",
    "@vitejs/plugin-react": "^4.3.0",
    "vitest": "^1.6.0",
    "@vitest/ui": "^1.6.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/user-event": "^14.5.2",
    "@testing-library/jest-dom": "^6.4.5",
    "jsdom": "^24.1.0",
    "tailwindcss": "^3.4.4",
    "postcss": "^8.4.38",
    "autoprefixer": "^10.4.19"
  }
}
```

> No se usan librerías de componentes UI externas (Material UI, Ant Design, etc.) para mantener el bundle ligero y control total sobre el diseño responsive.

---

## 7. Variables de Entorno

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=Casanare en Movimiento
```

---

## 8. Breakpoints de Referencia

| Nombre | Valor | Dispositivos objetivo |
|--------|-------|-----------------------|
| `sm` (base) | 320px | Móviles pequeños (iPhone SE, Galaxy A) |
| `md` | 768px | Tablets (iPad mini, tablets Android) |
| `lg` | 1024px | Laptops, iPad Pro landscape |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Monitores grandes |

La filosofía es **mobile-first**: escribir el CSS base para 320px y agregar clases `md:`, `lg:`, `xl:` para pantallas mayores. Nunca hacer lo contrario.
