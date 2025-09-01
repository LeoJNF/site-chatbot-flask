document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatBody = document.getElementById('chat-body');

    // Função para adicionar uma única mensagem na tela
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.innerHTML = `<p>${text.replace(/\n/g, '<br>')}</p>`; // Converte quebras de linha em <br>

        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        const now = new Date();
        timeDiv.textContent = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;

        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        chatBody.appendChild(messageDiv);

        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Função para enviar mensagem e receber respostas
    async function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user');
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: messageText })
            });

            const data = await response.json();

            // Itera sobre as respostas do bot e as exibe com um pequeno atraso
            for (let i = 0; i < data.responses.length; i++) {
                await new Promise(resolve => setTimeout(resolve, 500)); // Atraso de 500ms
                addMessage(data.responses[i], 'bot');
            }

        } catch (error) {
            console.error('Erro ao comunicar com o bot:', error);
            addMessage('Desculpe, estou com problemas. Tente novamente.', 'bot');
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Mensagem inicial do bot

    async function startConversation() {
         await new Promise(resolve => setTimeout(resolve, 500));
         addMessage("Olá! 👋 Seja bem-vindo(a) à Clínica Sorriso Aberto. Como posso ajudar hoje?", 'bot');
         await new Promise(resolve => setTimeout(resolve, 500));
         addMessage("1️⃣ Agendar consulta<br>2️⃣ Falar com um atendente", 'bot');
    }

    startConversation();
});