const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const minimizeBtn = document.getElementById('minimizeBtn');
const chatBubble = document.querySelector('.chat-bubble');

minimizeBtn.addEventListener('click', () => {
    chatBubble.classList.toggle('minimized');
    minimizeBtn.textContent = chatBubble.classList.contains('minimized') ? '+' : '−';
});

function addMessage(message, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const messageP = document.createElement('p');
    messageP.textContent = message;
    
    messageDiv.appendChild(messageP);
    chatMessages.appendChild(messageDiv);
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
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
    }, 1000);
}

function sendMessage() {
    const message = chatInput.value.trim();
    
    if (message) {
        addMessage(message, true);
        chatInput.value = '';
        botResponse(message);
    }
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

chatInput.focus();