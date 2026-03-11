document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input-field');
    const sendBtn = document.getElementById('send-btn');
    const chatContainer = document.getElementById('chat-container');

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