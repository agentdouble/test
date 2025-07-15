// Constantes de configuration
const MAX_MESSAGE_LENGTH = 500;
const MAX_MESSAGE_HISTORY = 100;
const BOT_RESPONSE_DELAY = 1000;
const THROTTLE_DELAY = 300;

// Éléments DOM
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const minimizeBtn = document.getElementById('minimizeBtn');
const chatBubble = document.querySelector('.chat-bubble');

// Variables pour le throttling
let lastSendTime = 0;

minimizeBtn.addEventListener('click', () => {
    chatBubble.classList.toggle('minimized');
    minimizeBtn.textContent = chatBubble.classList.contains('minimized') ? '+' : '−';
    
    // Restaurer le focus sur l'input après maximisation
    if (!chatBubble.classList.contains('minimized')) {
        setTimeout(() => chatInput.focus(), 300);
    }
});

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const messageP = document.createElement('p');
    messageP.textContent = message;
    
    messageDiv.appendChild(messageP);
    chatMessages.appendChild(messageDiv);
    
    // Limiter l'historique des messages
    limitMessageHistory();
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function limitMessageHistory() {
    const messages = chatMessages.querySelectorAll('.message');
    if (messages.length > MAX_MESSAGE_HISTORY) {
        const messagesToRemove = messages.length - MAX_MESSAGE_HISTORY;
        for (let i = 0; i < messagesToRemove; i++) {
            messages[i].remove();
        }
    }
}

function botResponse(userMessage) {
    const responses = [
        "C'est intéressant, dites-m'en plus.",
        "Je comprends votre point de vue.",
        "Pouvez-vous préciser votre question ?",
        "Merci pour votre message !",
        "Je suis là pour vous aider.",
        "C'est une excellente question.",
        "Laissez-moi réfléchir à cela...",
        "D'accord, je vois ce que vous voulez dire."
    ];
    
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    
    setTimeout(() => {
        addMessage(randomResponse, false);
    }, BOT_RESPONSE_DELAY);
}

function sendMessage() {
    // Vérifier le throttling
    const currentTime = Date.now();
    if (currentTime - lastSendTime < THROTTLE_DELAY) {
        return;
    }
    
    const message = chatInput.value.trim();
    
    // Validation de la longueur du message
    if (message && message.length <= MAX_MESSAGE_LENGTH) {
        lastSendTime = currentTime;
        addMessage(message, true);
        chatInput.value = '';
        botResponse(message);
    } else if (message.length > MAX_MESSAGE_LENGTH) {
        alert(`Le message ne peut pas dépasser ${MAX_MESSAGE_LENGTH} caractères.`);
    }
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

chatInput.focus();