# Know U — E-commerce de Moda con Inteligencia Artificial

Know U es una plataforma de e-commerce de vanguardia que fusiona la moda urbana con la inteligencia artificial generativa. No es solo una tienda; es un estudio creativo donde los usuarios pueden diseñar sus propias prendas mediante un chatbot IA, publicarlas en una galería comunitaria y realizar compras con un flujo de e-commerce profesional.

## 🚀 Características Principales

### 🎨 Estudio de Creación IA
- **Chatbot Integrado**: Interfaz interactiva para describir y generar diseños únicos mediante IA.
- **Mockups en Tiempo Real**: Visualización instantánea de los diseños aplicados a prendas.
- **Armario Privado**: Guarda tus creaciones antes de decidir comprarlas o publicarlas.

### 🛒 Experiencia E-commerce Profesional
- **Catálogo Dinámico**: Navegación por categorías (Hombre, Mujer, Accesorios) con un diseño minimalista "Antigravity".
- **Carrito y Checkout**: Sistema completo de gestión de artículos, cálculo de totales y procesamiento de pedidos.
- **Seguimiento de Pedidos**: Historial detallado de compras para usuarios finales.

### 👥 Comunidad y Marketplace
- **Galería Pública**: Explora, dale "Like" y comenta los diseños creados por la comunidad.
- **Perfiles de Creador**: Portafolios públicos para mostrar el talento individual.

### 🛡️ Panel Administrativo Robusto
- **Gestión Integral**: CRUD de productos, moderación de la comunidad y control de pedidos.
- **Seguridad Avanzada**: Protección CSRF, Rate Limiting y políticas de seguridad de contenido (CSP).

---

## 🛠️ Stack Tecnológico

- **Backend**: Python con [Flask](https://flask.palletsprojects.com/) (Arquitectura Modular de Blueprints).
- **Base de Datos**: SQLite con [SQLAlchemy](https://www.sqlalchemy.org/).
- **Frontend**: HTML5, Vanilla CSS, JavaScript (ES6+).
- **Seguridad**: Flask-WTF, Flask-Login, Flask-Limiter.
- **UI/UX**: Estética minimalista, iconos de IonIcons y micro-animaciones Lottie.

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue el patrón **Application Factory** y está organizado de forma modular para garantizar la escalabilidad:

```text
KnowU_Project/
├── app.py              # Punto de entrada y Fábrica de la Aplicación
├── extensions.py       # Inicialización de extensiones (DB, Login, etc.)
├── models.py           # Modelos de datos (User, Product, Order, etc.)
├── routes/             # Blueprints de la lógica de negocio
│   ├── admin.py        # Rutas administrativas
│   ├── api.py          # Endpoints JSON y Carrito
│   ├── auth.py         # Autenticación y Registro
│   ├── main.py         # Vistas públicas y catálogo
│   └── user.py         # Gestión de perfil y configuración
├── templates/          # Plantillas Jinja2
└── static/             # Assets (CSS, JS, Imágenes)
```

---

## 🚦 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd KnowU_Project
```

### 2. Crear un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf flask-limiter flask-migrate
```

### 4. Inicializar la base de datos y ejecutar
```bash
python app.py
```
> La aplicación creará automáticamente un usuario administrador predeterminado: `admin@knowu.com` / `admin123`.

---

## 📋 Requerimientos Implementados (Hasta la fecha)

A continuación se detallan los requerimientos completados según el backlog del proyecto:

### ✅ Epic 1: Generación de Diseños (Chatbot IA)
- [x] **US 1.1**: Interfaz de chat integrada para entrada de prompts.
- [x] **US 1.2**: Generación de mockups de previsualización.
- [x] **US 1.4**: Funcionalidad de guardar en el Armario.

### ✅ Epic 3: Proceso de Compra
- [x] **US 3.1**: Selección de detalles del producto (Tallas, Colores).
- [x] **US 3.3**: Flujo de Carrito y Checkout completo.

### ✅ Epic 4: Panel de Usuario y Gestión
- [x] **US 4.1**: Historial de pedidos y diseños guardados.
- [x] **US 4.2**: Panel administrativo para gestión de productos y órdenes.

### ✅ Epic 5: Seguridad y Refactorización
- [x] **Modularización**: Transición de monolito a Blueprints.
- [x] **Seguridad**: Implementación de headers de seguridad, Limiter de peticiones y CSRF.
