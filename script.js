// Constantes de configuration
const MAX_MESSAGE_LENGTH = 500;
const MAX_MESSAGE_HISTORY = 100;
const BOT_RESPONSE_DELAY = 1000;
const THROTTLE_DELAY = 300;
const FOCUS_RESTORE_DELAY = 500;

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
        setTimeout(() => chatInput.focus(), FOCUS_RESTORE_DELAY);
    }
});

/**
 * Ajoute un message à l'interface de chat
 * @param {string} message - Le contenu du message
 * @param {boolean} isUser - Indique si le message vient de l'utilisateur
 */
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

/**
 * Limite l'historique des messages en supprimant les plus anciens
 * pour maintenir la performance et éviter les problèmes de mémoire
 */
function limitMessageHistory() {
    const messages = chatMessages.querySelectorAll('.message');
    if (messages.length >= MAX_MESSAGE_HISTORY) {
        const messagesToRemove = messages.length - MAX_MESSAGE_HISTORY + 1;
        for (let i = 0; i < messagesToRemove; i++) {
            messages[i].remove();
        }
    }
}

/**
 * Génère une réponse automatique du bot
 * @param {string} userMessage - Le message de l'utilisateur (non utilisé actuellement)
 */
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

/**
 * Envoie un message utilisateur et déclenche une réponse du bot
 * Inclut la validation et le throttling
 */
function sendMessage() {
    const message = chatInput.value.trim();
    
    // Validation en premier
    if (!message) return;
    
    if (message.length > MAX_MESSAGE_LENGTH) {
        alert(`Le message ne peut pas dépasser ${MAX_MESSAGE_LENGTH} caractères.`);
        return;
    }
    
    // Vérifier le throttling après validation
    const currentTime = Date.now();
    if (currentTime - lastSendTime < THROTTLE_DELAY) {
        return;
    }
    
    // Traiter le message
    lastSendTime = currentTime;
    addMessage(message, true);
    chatInput.value = '';
    botResponse(message);
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

chatInput.focus();