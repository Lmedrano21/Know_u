# Product Backlog: Know U (Tienda de Ropa con Diseños IA)

Este documento detalla los requerimientos ágiles (Epics y User Stories) para construir la plataforma "Know U", donde los usuarios pueden crear diseños con IA, comprarlos o venderlos a terceros.

## Epic 1: Generación de Diseños (Chatbot IA)
*El núcleo creativo donde los usuarios diseñan su propia ropa.*

* **US 1.1:** Como usuario, quiero interactuar con un chatbot integrado para describir mediante texto el diseño que deseo para mi ropa.
* **US 1.2:** Como usuario, quiero que la IA me genere imágenes de previsualización (mockups) de la prenda en tiempo real.
* **US 1.3:** Como usuario, quiero poder pedirle al chatbot iteraciones y correcciones sobre el diseño anterior hasta estar satisfecho.
* **US 1.4:** Como usuario, quiero guardar el diseño finalizado en mi "Armario Privado" para decidir más tarde si lo compro.

## Epic 2: Marketplace y Comunidad (Publicación de Diseños)
*El ecosistema donde los diseños se vuelven productos públicos.*

* **US 2.1:** Como creador, quiero tener la opción de publicar mis diseños guardados en el "Catálogo Público" de la tienda.
* **US 2.2:** Como creador, quiero definir si mi diseño público será gratuito (solo cobran la fabricación) o si tendrá una comisión/regalía a mi favor por cada compra.
* **US 2.3:** Como comprador, quiero poder explorar un feed con los diseños más populares, recientes y recomendados publicados por otros usuarios.
* **US 2.4:** Como comprador, quiero dar "Me gusta" o dejar comentarios en los diseños públicos de otras personas.
* **US 2.5:** Como creador, quiero tener un "Perfil Público" que funcione como mi propio portafolio de tienda, donde se vean mis prendas listadas y mis seguidores.

## Epic 3: Proceso de Compra (Checkout de Prendas Personalizadas)
*Adaptación del flujo de E-commerce tradicional a productos custom*

* **US 3.1:** Como comprador, al elegir mi propio diseño o el de un tercero, quiero poder seleccionar el tipo de prenda (camiseta, sudadera, etc.), el color de la tela y mi talla.
* **US 3.2:** Como comprador, quiero ver el precio dinámico actualizado según el tipo de prenda, los costos de impresión y las regalías del creador.
* **US 3.3:** Como comprador, quiero añadir la prenda personalizada al carrito de compras y proceder al pago.
* **US 3.4:** Como usuario, quiero recibir seguimiento de mi pedido sabiendo en qué etapa está (Generado, En producción/Impresión, Enviado).

## Epic 4: Panel de Usuario y Gestión
*Administración de la cuenta y los ingresos.*

* **US 4.1:** Como usuario, quiero ver mi historial completo tanto de pedidos físicos que he comprado, como de diseños que he generado y guardado.
* **US 4.2:** Como creador con diseños a la venta, quiero un panel (Dashboard) para ver cuántas ventas han tenido mis creaciones.
* **US 4.3:** Como creador, quiero gestionar el retiro o uso de mi saldo acumulado por la venta de mis diseños.

## Epic 5: Moderación y Calidad
*Garantizar que el uso de la plataforma sea seguro.*

* **US 5.1:** Como administrador, quiero que exista un filtro automático en la IA que impida la generación de contenido ofensivo o sujeto a derechos de autor restrictivos (NSFW/Copyright blocks).
* **US 5.2:** Como usuario, quiero poder reportar diseños públicos de terceros si considero que infringen normas o roban contenido.
