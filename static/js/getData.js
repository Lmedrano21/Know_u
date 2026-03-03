const productsContainer = document.querySelector('.products .content');
const productCount = document.getElementById('productCount');

// Función principal para obtener productos
async function getProducts() {
    try {
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error('Error en la red');
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error al cargar productos:', error);
        if(productsContainer) productsContainer.innerHTML = '<p>Error cargando productos. Intenta de nuevo.</p>';
    }
}

// Renderizar productos en el DOM
function displayProducts(products) {
    if (!productsContainer) return;

    productsContainer.innerHTML = '';
    
    if (productCount) {
        productCount.textContent = `${products.length} Productos`;
    }

    products.forEach(product => {
        // Aseguramos que la ruta de la imagen sea absoluta desde la raíz
        // La API devuelve "static/images/...", le agregamos "/" al inicio
        const imagePath = product.images.length > 0 ? `/${product.images[0]}` : '/static/images/no-image.png';
        
        const productHTML = `
            <div class="product-card">
                <div class="card-banner">
                    <img src="${imagePath}" alt="${product.name}" class="image-contain" width="300" height="300">
                    ${product.isTrending ? '<span class="card-badge">Tendencia</span>' : ''}
                    <div class="card-actions">
                        <button class="action-btn" aria-label="add to cart" onclick="addToCart(${product.id})">
                            <ion-icon name="cart-outline"></ion-icon>
                        </button>
                        <button class="action-btn" aria-label="view details" onclick="window.location.href='/product/${product.id}'">
                            <ion-icon name="eye-outline"></ion-icon>
                        </button>
                    </div>
                </div>
                <div class="card-content">
                    <h3 class="card-title">
                        <a href="/product/${product.id}">${product.name}</a>
                    </h3>
                    <data class="card-price" value="${product.price}">${product.price}</data>
                </div>
            </div>
        `;
        productsContainer.innerHTML += productHTML;
    });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', getProducts);
