# Listado de Vistas (Pages) Faltantes para "Know U"

Basado en el Product Backlog y considerando que es una plataforma de E-commerce + Comunidad con IA, aquí está el detalle de las vistas (archivos HTML/Rutas) que debemos construir:

## 1. Vistas Públicas (Core E-commerce & Comunidad)
* **Página de Inicio (Landing Page):** 
  * Bienvenida, explicación del concepto "Diseña con IA".
  * Carrusel con los diseños *trend* de la comunidad.
* **Marketplace / Feed Principal (`/shop`):**
  * Grilla infinita o paginada con todos los diseños públicos de los creadores.
  * Filtros por estilo, popularidad y fecha de publicación.
* **Perfil Público del Creador (`/creator/<username>`):**
  * El "escaparate" o portafolio de un usuario específico.
  * Foto de perfil, biografía y grilla con sus prendas a la venta.
* **Detalle del Producto (`/product/<id>`):**
  * Vista donde se elige: Tipo de prenda base (ej. Suéter, Camiseta), Color y Talla.
  * Botón para dar "Me gusta" y sección de comentarios.
  * Precio dinámico (Base + Regalías del creador).

## 2. Vistas de Generación de IA (El "Estudio")
* **Estudio de Creación IA (`/create`):**
  * La vista más importante y compleja.
  * **Layout sugerido:** Dividida en dos columnas.
    * *Izquierda/Inferior:* Interfaz de Chatbot para hablar con la IA y pedir el diseño.
    * *Derecha/Centro:* Lienzo o *Mockup* en tiempo real proyectado sobre una prenda en 3D o 2D interactivo.
  * Opciones para: "Guardar en el armario" o "Publicar para la venta".

## 3. Vistas de Transacción (Flujo de Compra)
* **Carrito de Compras (`/cart`):**
  * Resumen de prendas personalizadas añadidas.
  * Coste de envío estimado.
* **Checkout (`/checkout`):**
  * Formulario de dirección de envío.
  * Pasarela de pagos (integración con Stripe, PayPal, etc.).
* **Confirmación de Orden (`/order/success`):**
  * Resumen del pedido y número de seguimiento del proceso de confección/impresión.

## 4. Vistas de Gestión Privada (El Dashboard del Usuario)
* **Mi Armario Privado (`/dashboard/wardrobe`):**
  * Diseños generados con IA que el usuario guardó pero no ha comprado ni publicado.
* **Mis Pedidos (`/dashboard/orders`):**
  * Historial de compras físicas con barra de estado (Generado -> En Producción -> Enviado).
* **Panel de Creador/Ventas (`/dashboard/analytics`):**
  * Gráficas de diseños vendidos a terceros.
  * Saldo acumulado (Regalías ganadas) y botón para "Retirar Fondos".
* **Ajustes de Cuenta (`/settings`):**
  * Cambiar datos personales, foto de perfil, contraseña y preferencias.

## 5. Vistas Administrativas (Moderación)
* **Panel de Control (Admin):**
  * Lista de diseños reportados por la comunidad.
  * Moderación de contenido NSFW / Copyright detectado automáticamente por la IA.
