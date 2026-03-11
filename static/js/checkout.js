document.addEventListener('DOMContentLoaded', () => {
    // Obtener el ID de la orden de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('orderId');

    if (orderId) {
        getOrderDetails(orderId);
    } else {
        // Si no hay ID, redirigir al inicio
        window.location.href = '/';
    }

    // Cargar animación
    const iconContainer = document.getElementById('checkoutIcon');
    if (iconContainer && window.lottie) {
        lottie.loadAnimation({
            container: iconContainer,
            renderer: 'svg',
            loop: false,
            autoplay: true,
            path: '/static/json/Animation check.json' // Asegúrate de tener este archivo o usa uno genérico
        });
    }
});

async function getOrderDetails(id) {
    try {
        const response = await fetch(`/api/orders/${id}`);
        
        if (!response.ok) {
            throw new Error('No se pudo cargar la orden');
        }

        const order = await response.json();

        // Actualizar el DOM con datos reales de la BD
        document.getElementById('id_order').textContent = `#${order.id}`;
        document.getElementById('total_price').textContent = `$${order.total_price}`;
        document.getElementById('order_date').textContent = order.date;

    } catch (error) {
        console.error('Error:', error);
        alert('Error al cargar los detalles de tu pedido.');
    }
}

function backHome() {
    window.location.href = '/';
}