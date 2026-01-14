// API Configuration
const API_URL = 'http://localhost:8000/api/chat/';

// State management
let conversationId = null;
let isLoading = false;

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Add welcome message
    addBotMessage('Hello! I\'m the K2 Communications AI assistant. How can I help you today?');
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Focus input
    messageInput.focus();
});

// Send message function
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || isLoading) {
        return;
    }
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    messageInput.value = '';
    
    // Show loading indicator
    showLoading();
    
    // Disable input while loading
    setLoading(true);
    
    try {
        // Prepare request payload
        const payload = {
            message: message
        };
        
        // Add conversation_id if exists
        if (conversationId) {
            payload.conversation_id = conversationId;
        }
        
        // Make API call
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Store conversation ID
        conversationId = data.conversation_id;
        
        // Hide loading indicator
        hideLoading();
        
        // Add bot response to chat
        addBotMessage(data.message);
        
    } catch (error) {
        console.error('Error sending message:', error);
        hideLoading();
        showError('Failed to send message. Please make sure the server is running at ' + API_URL);
    } finally {
        setLoading(false);
        messageInput.focus();
    }
}

// Add user message to chat
function addUserMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = message;
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

// Add bot message to chat
function addBotMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = message;
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    scrollToBottom();
}

// Show loading indicator
function showLoading() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message bot';
    loadingDiv.id = 'loadingIndicator';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble loading';
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'loading-dot';
        bubble.appendChild(dot);
    }
    
    loadingDiv.appendChild(bubble);
    chatMessages.appendChild(loadingDiv);
    
    scrollToBottom();
}

// Hide loading indicator
function hideLoading() {
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.remove();
    }
}

// Show error message
function showError(message) {
    // Remove any existing error
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    chatMessages.appendChild(errorDiv);
    scrollToBottom();
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Set loading state
function setLoading(loading) {
    isLoading = loading;
    sendButton.disabled = loading;
    messageInput.disabled = loading;
    
    if (loading) {
        sendButton.textContent = 'Sending...';
    } else {
        sendButton.textContent = 'Send';
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
