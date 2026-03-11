document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input-field');
    const sendBtn = document.getElementById('send-btn');
    const chatContainer = document.getElementById('chat-container');
    const togglePanelBtn = document.getElementById('toggle-panel-btn');
    const floatingPanel = document.getElementById('floating-panel');
    const demoBtn = document.getElementById('demo-techwear-btn');

    // Manejo del panel flotante
    if(togglePanelBtn && floatingPanel) {
        togglePanelBtn.addEventListener('click', () => {
            floatingPanel.classList.toggle('hidden');
        });
    }

    // Cargar demo inicial
    if (demoBtn) {
        demoBtn.addEventListener('click', () => {
            chatContainer.innerHTML = '';
            
            const demoHTML = `
                <div class="message user-msg">
                    <p>Quiero una chaqueta techwear para invierno. Negra, con paneles reflectantes plateados y muchos bolsillos útiles. ¿Puedes hacer un boceto?</p>
                </div>

                <div class="message ai-msg">
                    <div class="ai-header">
                        <span class="u-icon-small">U</span>
                        <strong>KNOW U AI</strong>
                    </div>
                    <p>¡Entendido, Elena! He generado una propuesta inicial. ¿Qué te parece?</p>
                </div>

                <div class="result-row">
                    <div class="product-image-container">
                        <img src="/static/images/man/jacket-with-hood-in-stone_02.webp" alt="Chaqueta Techwear" class="product-img" loading="lazy" style="width: 200px; object-fit: cover;">
                        <button class="icon-btn top-right"><i class="fa-solid fa-expand"></i></button>
                        <button class="icon-btn bottom-left"><i class="fa-solid fa-pen"></i></button>
                    </div>
                    <div class="action-buttons">
                        <button class="btn-primary"><i class="fa-solid fa-bag-shopping"></i> AÑADIR AL CARRITO</button>
                        <button class="btn-secondary"><i class="fa-solid fa-share-from-square"></i> COMPARTIR EN PERFIL</button>
                    </div>
                </div>

                <div class="message collab-msg">
                    <div class="collab-header">ADRIÁN</div>
                    <p>¡Me encanta! ¿Podemos añadir una capucha desmontable y hacer el logo reflectante?</p>
                </div>

                <div class="result-row right-align">
                    <div class="message ai-msg small-msg">
                        <p>Hecho. Aquí tienes la versión 2 con la capucha desmontable y el logo reflectante en el pecho.</p>
                    </div>
                    <div class="product-image-container small-img">
                        <img src="/static/images/man/jacket-with-hood-in-stone_04.webp" alt="Chaqueta Techwear V2" class="product-img" loading="lazy" style="width: 150px; object-fit: cover;">
                    </div>
                </div>
            `;
            
            chatContainer.innerHTML = demoHTML;
            scrollToBottom();
        });
    }

    // Función principal para enviar el mensaje
    const sendMessage = () => {
        const text = chatInput.value.trim();
        
        if (text !== '') {
            // 1. Crear el mensaje del usuario
            const userMsgDiv = document.createElement('div');
            userMsgDiv.classList.add('message', 'user-msg');
            userMsgDiv.innerHTML = `<p>${text}</p>`;
            
            // 2. Añadirlo al contenedor de chat
            chatContainer.appendChild(userMsgDiv);
            
            // 3. Limpiar el input
            chatInput.value = '';
            
            // 4. Bajar el scroll para ver el mensaje nuevo
            scrollToBottom();

            // 5. Simular la respuesta de la IA (Know U AI)
            simulateAIResponse();
        }
    };

    const simulateAIResponse = () => {
        // Indicador de "escribiendo" (opcional, le da realismo)
        setTimeout(() => {
            const aiMsgDiv = document.createElement('div');
            aiMsgDiv.classList.add('message', 'ai-msg');
            aiMsgDiv.innerHTML = `
                <div class="ai-header">
                    <span class="u-icon-small">U</span>
                    <strong>KNOW U AI</strong>
                </div>
                <p>¡Anotado! Estoy procesando tu solicitud para actualizar el diseño de la chaqueta. Dame un segundo...</p>
            `;
            chatContainer.appendChild(aiMsgDiv);
            scrollToBottom();
        }, 800); // Responde en 0.8 segundos
    };

    const scrollToBottom = () => {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: 'smooth'
        });
    };

    // Escuchar el clic en el botón con el logo "U"
    sendBtn.addEventListener('click', sendMessage);

    // Escuchar la tecla "Enter" en el teclado
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // Evita que se recargue la página si estuviera en un form
            sendMessage();
        }
    });
});
