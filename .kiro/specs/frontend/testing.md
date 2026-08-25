# FRONTEND — Guía de Testing

**Proyecto:** Casanare en Movimiento  
**Framework:** Vitest + React Testing Library  
**Versión:** 1.0

---

## 1. Stack de Testing

| Herramienta | Uso |
|-------------|-----|
| `vitest` | Runner de tests (compatible con Vite) |
| `@testing-library/react` | Render y queries de componentes React |
| `@testing-library/user-event` | Simular interacciones del usuario |
| `@testing-library/jest-dom` | Matchers DOM (toBeInTheDocument, etc.) |
| `jsdom` | Entorno DOM para Node.js |
| `vi.mock()` | Mock de módulos (axios, react-router) |

---

## 2. Configuración

### vite.config.js
```javascript
export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
      thresholds: { lines: 70, functions: 70 }
    }
  }
});
```

### src/test/setup.js
```javascript
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock de localStorage
Object.defineProperty(window, 'localStorage', {
  value: {
    getItem: vi.fn(),
    setItem: vi.fn(),
    removeItem: vi.fn(),
    clear: vi.fn(),
  }
});
```

---

## 3. Patrón de Tests por Componente

```jsx
// Ejemplo: src/components/events/EventCard.test.jsx

import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import EventCard from './EventCard';

const mockEvento = {
  id: 1,
  titulo: 'Festival Llanero 2026',
  descripcion: 'Gran festival de música llanera',
  categoria: 'cultural',
  fecha_inicio: '2026-09-15',
  municipio: 'Yopal',
  imagen_url: null,
};

const renderWithRouter = (component) =>
  render(<BrowserRouter>{component}</BrowserRouter>);

describe('EventCard', () => {
  it('muestra el título del evento', () => {
    renderWithRouter(<EventCard evento={mockEvento} />);
    expect(screen.getByText('Festival Llanero 2026')).toBeInTheDocument();
  });

  it('muestra el municipio', () => {
    renderWithRouter(<EventCard evento={mockEvento} />);
    expect(screen.getByText(/Yopal/)).toBeInTheDocument();
  });

  it('muestra imagen placeholder si no hay imagen', () => {
    renderWithRouter(<EventCard evento={mockEvento} />);
    const img = screen.getByRole('img');
    expect(img).toHaveAttribute('src', '/placeholder-event.jpg');
  });

  it('tiene link al detalle del evento', () => {
    renderWithRouter(<EventCard evento={mockEvento} />);
    const link = screen.getByRole('link', { name: /ver detalle/i });
    expect(link).toHaveAttribute('href', '/eventos/1');
  });
});
```

---

## 4. Mock del AuthContext

```jsx
// src/test/mocks/authContext.jsx

import { AuthContext } from '../../context/AuthContext';

export function MockAuthProvider({ children, user = null, isEmpresario = false }) {
  return (
    <AuthContext.Provider value={{
      user,
      isLoading: false,
      login: vi.fn(),
      logout: vi.fn(),
      isEmpresario: () => isEmpresario
    }}>
      {children}
    </AuthContext.Provider>
  );
}

// Uso en tests:
// render(<MockAuthProvider user={mockUser} isEmpresario><Navbar /></MockAuthProvider>)
```

---

## 5. Mock de Axios

```javascript
// src/test/mocks/api.js

import { vi } from 'vitest';

// Mock del módulo completo
vi.mock('../../services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
    patch: vi.fn(),
    interceptors: {
      request: { use: vi.fn() },
      response: { use: vi.fn() },
    }
  }
}));
```

---

## 6. Tests de Páginas con Llamadas API

```jsx
// src/pages/LoginPage.test.jsx

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import LoginPage from './LoginPage';
import { MockAuthProvider } from '../test/mocks/authContext';

// Mock del hook de auth
const mockLogin = vi.fn();
vi.mock('../hooks/useAuth', () => ({
  useAuth: () => ({
    login: mockLogin,
    user: null
  })
}));

describe('LoginPage', () => {
  const renderPage = () => render(
    <BrowserRouter>
      <MockAuthProvider>
        <LoginPage />
      </MockAuthProvider>
    </BrowserRouter>
  );

  it('renderiza el formulario de login', () => {
    renderPage();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ingresar/i })).toBeInTheDocument();
  });

  it('muestra error si el email es inválido', async () => {
    renderPage();
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/email/i), 'noesunemail');
    await user.click(screen.getByRole('button', { name: /ingresar/i }));
    expect(await screen.findByText(/email inválido/i)).toBeInTheDocument();
  });

  it('llama a login con credenciales correctas', async () => {
    mockLogin.mockResolvedValueOnce({ rol: 'usuario' });
    renderPage();
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/email/i), 'test@test.com');
    await user.type(screen.getByLabelText(/contraseña/i), 'password123');
    await user.click(screen.getByRole('button', { name: /ingresar/i }));
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('test@test.com', 'password123');
    });
  });

  it('muestra error cuando login falla', async () => {
    mockLogin.mockRejectedValueOnce({ response: { status: 401 } });
    renderPage();
    const user = userEvent.setup();
    await user.type(screen.getByLabelText(/email/i), 'bad@test.com');
    await user.type(screen.getByLabelText(/contraseña/i), 'wrongpass');
    await user.click(screen.getByRole('button', { name: /ingresar/i }));
    expect(await screen.findByText(/credenciales incorrectas/i)).toBeInTheDocument();
  });
});
```

---

## 7. Comandos de Ejecución

```bash
# Correr todos los tests (modo CI, sin watch)
npm run test -- --run

# Correr en modo watch (desarrollo)
npm run test

# Con reporte de cobertura
npm run test -- --run --coverage

# Correr un archivo específico
npm run test -- src/pages/LoginPage.test.jsx --run

# Ver UI interactiva de tests
npm run test -- --ui
```

---

## 8. Checklist de Calidad Frontend

Antes de marcar una tarea completada:
- [ ] El componente renderiza sin errores en el navegador
- [ ] Responsive verificado en 320px, 768px y 1280px (DevTools)
- [ ] Tests del componente pasan en verde
- [ ] Formularios con tab-order correcto y labels accesibles
- [ ] Estados de carga y error cubiertos visualmente
- [ ] Sin `console.error` en la consola del navegador
