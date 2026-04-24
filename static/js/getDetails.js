document.addEventListener('DOMContentLoaded', () => {
    const productDetails = document.querySelector('.productDetails');
    const quantityInput = document.getElementById("productCount");
    
    // Obtener ID de la URL (?id=X)
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    
    if (productId) {
        getDetails(parseInt(productId));
    } else if (productDetails && productDetails.dataset.productId) {
        getDetails(parseInt(productDetails.dataset.productId));
    }

    // Controladores de cantidad
    const minusBtn = document.getElementById("minus");
    const plusBtn = document.getElementById("plus");

    if (minusBtn && quantityInput) {
        minusBtn.addEventListener("click", () => {
            let value = parseInt(quantityInput.value) || 1;
            if (value > 1) quantityInput.value = value - 1;
        });
    }

    if (plusBtn && quantityInput) {
        plusBtn.addEventListener("click", () => {
            let value = parseInt(quantityInput.value) || 1;
            if (value < 999) quantityInput.value = value + 1;
        });
    }
});

async function getDetails(id) {
    try {
        const response = await fetch('static/json/products.json');
        const products = await response.json();
        const product = products.find(p => p.id === id);
        
        if (!product) throw new Error('Producto no encontrado');
        
        displayDetails(product);
    } catch (error) {
        console.error('Error:', error);
        document.querySelector('.productDetails').innerHTML = '<p>Error al cargar detalles del producto.</p>';
    }
}

function displayDetails(product) {
    // Actualizar elementos del DOM
    let imagePath = product.images.length > 0 ? product.images[0] : 'static/images/no-image.png';
    if (!imagePath.startsWith('static/')) imagePath = 'static/' + imagePath;
    
    document.getElementById("product_image").src = imagePath;
    document.querySelector(".category_name").textContent = product.category;
    document.querySelector(".product_name").textContent = product.name;
    document.querySelector(".product_price").textContent = product.price;
    document.querySelector(".product_des").textContent = product.description;

    // Configurar botón de añadir al carrito
    const btnAdd = document.getElementById("btn_add");
    const quantityInput = document.getElementById("productCount");
    
    if (btnAdd) {
        // Clonamos el botón para eliminar listeners previos si los hubiera
        const newBtn = btnAdd.cloneNode(true);
        btnAdd.parentNode.replaceChild(newBtn, btnAdd);
        
        newBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const qty = parseInt(quantityInput.value) || 1;
            addToCart(product.id, qty); // Función global de cart.js
            showToast();
        });
    }
}

function showToast() {
    const toastOverlay = document.getElementById("toast-overlay");
    if (!toastOverlay) return;
    
    toastOverlay.classList.add("show");
    
    // Animación Lottie
    const checkIconContainer = document.getElementById('checkIcon');
    if (checkIconContainer && window.lottie) {
        checkIconContainer.innerHTML = '';
        lottie.loadAnimation({
            container: checkIconContainer,
            renderer: 'svg',
            loop: false,
            autoplay: true,
            path: '/static/json/Animation check.json' // Asegúrate de que este archivo exista en static/json
        });
    }

    setTimeout(() => {
        toastOverlay.classList.remove("show");
        // Abrir carrito lateral
        const cartSection = document.querySelector('.cart-section');
        if (cartSection) {
            cartSection.classList.add('active');
            if (typeof renderSideCart === 'function') renderSideCart();
        }
    }, 2000);
}
