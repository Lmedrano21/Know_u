// Inicializar carrito desde localStorage
let cart = JSON.parse(localStorage.getItem('knowu_cart')) || [];

// Actualizar contador del carrito en el header (elemento en base.html)
function updateCartCounter() {
    const counter = document.getElementById('cart-counter');
    if (counter) {
        const totalItems = cart.reduce((acc, item) => acc + item.quantity, 0);
        counter.textContent = totalItems;
    }
}

// Añadir al carrito
function addToCart(productId) {
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ id: productId, quantity: 1, type: 'regular' });
    }
    
    localStorage.setItem('knowu_cart', JSON.stringify(cart));
    updateCartCounter();
    
    // Si el carrito lateral está abierto, actualizarlo
    const cartSection = document.querySelector('.cart-section');
    if (cartSection && cartSection.classList.contains('active')) {
        renderSideCart();
    }
    
    // Feedback visual (opcional)
    alert("Producto añadido al carrito");
}

// Añadir diseño personalizado IA al carrito
function addCustomDesignToCart(designId, promptText, imageUrl, basePrice) {
    // Generamos un ID virtual único para el carrito basado en el timestamp o designId
    const virtualId = 'custom_' + (designId || Date.now());
    
    // Lo guardamos con un type 'custom'
    cart.push({
        id: virtualId,
        type: 'custom',
        designId: designId,
        name: 'Diseño IA: ' + promptText.substring(0, 20) + '...',
        prompt: promptText,
        price: basePrice,
        image_url: imageUrl,
        quantity: 1
    });
    
    localStorage.setItem('knowu_cart', JSON.stringify(cart));
    updateCartCounter();
    
    alert("Diseño IA añadido al carrito");
}

// Renderizar carrito lateral (Side Cart)
async function renderSideCart() {
    const cartContainer = document.querySelector('.cart-section .cart_products');
    const totalElement = document.getElementById('total_price');
    
    if (!cartContainer) return;
    
    cartContainer.innerHTML = '';
    let totalPrice = 0;
    
    if (cart.length === 0) {
        cartContainer.innerHTML = '<p class="empty-cart">Tu carrito está vacío</p>';
        if(totalElement) totalElement.textContent = '$0.00';
        return;
    }

    try {
        // Obtenemos todos los productos para cruzar datos
        // (En producción idealmente usarías un endpoint que reciba IDs específicos)
        const response = await fetch('/api/products');
        const allProducts = await response.json();
        
        cart.forEach(item => {
            if (item.type === 'custom') {
                // Renderizado para ítem personalizado IA
                const priceNumber = parseFloat(item.price);
                totalPrice += priceNumber * item.quantity;
                
                cartContainer.innerHTML += `
                    <div class="cart-item">
                        <img src="${item.image_url}" alt="Diseño IA">
                        <div class="item-details">
                            <h4>${item.name}</h4>
                            <p>$${priceNumber.toFixed(2)} x ${item.quantity}</p>
                            <div class="qty-control">
                                <button onclick="updateQuantity('${item.id}', -1)">-</button>
                                <span>${item.quantity}</span>
                                <button onclick="updateQuantity('${item.id}', 1)">+</button>
                            </div>
                        </div>
                        <ion-icon name="trash-outline" class="remove-item" onclick="removeFromCart('${item.id}')"></ion-icon>
                    </div>
                `;
            } else {
                // Renderizado para producto normal
                const product = allProducts.find(p => p.id === item.id);
                if (product) {
                    const priceNumber = parseFloat(product.price.replace(/[^0-9.-]+/g,""));
                    totalPrice += priceNumber * item.quantity;
                    
                    const imagePath = product.images.length > 0 ? `/${product.images[0]}` : '/static/images/no-image.png';

                    cartContainer.innerHTML += `
                        <div class="cart-item">
                            <img src="${imagePath}" alt="${product.name}">
                            <div class="item-details">
                                <h4>${product.name}</h4>
                                <p>${product.price} x ${item.quantity}</p>
                                <div class="qty-control">
                                    <button onclick="updateQuantity(${item.id}, -1)">-</button>
                                    <span>${item.quantity}</span>
                                    <button onclick="updateQuantity(${item.id}, 1)">+</button>
                                </div>
                            </div>
                            <ion-icon name="trash-outline" class="remove-item" onclick="removeFromCart(${item.id})"></ion-icon>
                        </div>
                    `;
                }
            }
        });
        
        if(totalElement) totalElement.textContent = `$${totalPrice.toFixed(2)}`;
        
    } catch (error) {
        console.error('Error cargando carrito:', error);
    }
}

// Renderizar página completa de carrito (cartPage.html)
async function renderCartPage() {
    const cartPageContainer = document.querySelector('.cart_page .cart_products');
    const subtotalEl = document.getElementById('Subtotal');
    const totalOrderEl = document.getElementById('total_order');
    const cartCountsEl = document.getElementById('cart_counts');
    
    if (!cartPageContainer) return;
    
    cartPageContainer.innerHTML = '';
    let subtotal = 0;
    const shipping = 70.00; // Valor fijo
    
    if (cart.length === 0) {
        cartPageContainer.innerHTML = '<p>No hay productos en tu bolsa.</p>';
        if(subtotalEl) subtotalEl.textContent = '$0.00';
        if(totalOrderEl) totalOrderEl.textContent = '$0.00';
        if(cartCountsEl) cartCountsEl.textContent = '(0)';
        return;
    }

    try {
        const response = await fetch('/api/products');
        const allProducts = await response.json();
        
        cart.forEach(item => {
            if (item.type === 'custom') {
                const priceNumber = parseFloat(item.price);
                const itemTotal = priceNumber * item.quantity;
                subtotal += itemTotal;
                
                cartPageContainer.innerHTML += `
                    <div class="cart_card">
                        <div class="card_img">
                            <img src="${item.image_url}" alt="Diseño IA">
                        </div>
                        <div class="card_details">
                            <h3>${item.name}</h3>
                            <p title="${item.prompt}">Diseño Personalizado</p>
                            <div class="price_control">
                                <span class="price">$${priceNumber.toFixed(2)}</span>
                                <div class="counts">
                                    <button onclick="updateQuantity('${item.id}', -1)">-</button>
                                    <span>${item.quantity}</span>
                                    <button onclick="updateQuantity('${item.id}', 1)">+</button>
                                </div>
                            </div>
                            <p class="item-total">Total: $${itemTotal.toFixed(2)}</p>
                        </div>
                        <div class="remove">
                             <ion-icon name="close-outline" onclick="removeFromCart('${item.id}')"></ion-icon>
                        </div>
                    </div>
                `;
            } else {
                const product = allProducts.find(p => p.id === item.id);
                if (product) {
                    const priceNumber = parseFloat(product.price.replace(/[^0-9.-]+/g,""));
                    const itemTotal = priceNumber * item.quantity;
                    subtotal += itemTotal;
                    
                    const imagePath = product.images.length > 0 ? `/${product.images[0]}` : '/static/images/no-image.png';

                    cartPageContainer.innerHTML += `
                        <div class="cart_card">
                            <div class="card_img">
                                <img src="${imagePath}" alt="${product.name}">
                            </div>
                            <div class="card_details">
                                <h3>${product.name}</h3>
                                <p>Categoría: ${product.category}</p>
                                <div class="price_control">
                                    <span class="price">${product.price}</span>
                                    <div class="counts">
                                        <button onclick="updateQuantity(${item.id}, -1)">-</button>
                                        <span>${item.quantity}</span>
                                        <button onclick="updateQuantity(${item.id}, 1)">+</button>
                                    </div>
                                </div>
                                <p class="item-total">Total: $${itemTotal.toFixed(2)}</p>
                            </div>
                            <div class="remove">
                                 <ion-icon name="close-outline" onclick="removeFromCart(${item.id})"></ion-icon>
                            </div>
                        </div>
                    `;
                }
            }
        });
        
        if(subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
        if(totalOrderEl) totalOrderEl.textContent = `$${(subtotal + shipping).toFixed(2)}`;
        if(cartCountsEl) cartCountsEl.textContent = `(${cart.reduce((a,b)=>a+b.quantity,0)})`;
        
    } catch (error) {
        console.error('Error cargando página de carrito:', error);
    }
}

// Funciones de control
function updateQuantity(productId, change) {
    const itemIndex = cart.findIndex(item => item.id === productId);
    if (itemIndex > -1) {
        cart[itemIndex].quantity += change;
        if (cart[itemIndex].quantity <= 0) {
            cart.splice(itemIndex, 1);
        }
        localStorage.setItem('knowu_cart', JSON.stringify(cart));
        updateCartCounter();
        renderSideCart();
        renderCartPage();
    }
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('knowu_cart', JSON.stringify(cart));
    updateCartCounter();
    renderSideCart();
    renderCartPage();
}

function viewCart() {
    window.location.href = '/cart';
}

async function checkOut() {
    if (cart.length === 0) {
        alert("Tu carrito está vacío");
        return;
    }

    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]') ? document.querySelector('meta[name="csrf-token"]').getAttribute('content') : '';
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ items: cart })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // Limpiar carrito y redirigir
            localStorage.removeItem('knowu_cart');
            cart = [];
            window.location.href = `/checkout?orderId=${result.order_id}`;
        } else {
            // Si falla (ej: no logueado), redirigir a login o mostrar error
            if (response.status === 401) {
                window.location.href = '/login';
            } else {
                alert('Error al procesar el pedido: ' + (result.message || 'Intente nuevamente'));
            }
        }
    } catch (error) {
        console.error('Error en checkout:', error);
        alert('Hubo un problema de conexión.');
    }
}

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    updateCartCounter();
    
    // Lógica para abrir/cerrar carrito lateral
    const cartIcon = document.querySelector('.icon-cart');
    const closeCartBtn = document.getElementById('closeCart');
    const cartSection = document.querySelector('.cart-section');
    
    if(cartIcon && cartSection) {
        cartIcon.addEventListener('click', (e) => {
            e.preventDefault();
            cartSection.classList.add('active');
            renderSideCart();
        });
    }
    
    if(closeCartBtn && cartSection) {
        closeCartBtn.addEventListener('click', () => {
            cartSection.classList.remove('active');
        });
    }
    
    // Si estamos en la página de carrito, cargarla
    if (document.querySelector('.cart_page')) {
        renderCartPage();
    }
});
