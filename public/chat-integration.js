const widget = document.getElementById('k2Widget');
const chatWindow = document.getElementById('chatWindow');
const closeBtn = document.getElementById('closeBtn');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

const API_BASE = window.location.origin;
let conversationId = null;

// Toggle chat window
widget.addEventListener('click', () => {
  chatWindow.classList.toggle('active');
  if (chatWindow.classList.contains('active')) {
    userInput.focus();
  }
});

// Close chat window
closeBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  chatWindow.classList.remove('active');
});

// Send message to backend
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // Disable input while processing
  sendBtn.disabled = true;
  userInput.disabled = true;

  // Add user message
  const userMsg = document.createElement('div');
  userMsg.className = 'message user-msg';
  userMsg.textContent = message;
  chatMessages.appendChild(userMsg);

  // Clear input
  userInput.value = '';

  // Show typing indicator
  const typingIndicator = document.createElement('div');
  typingIndicator.className = 'message typing-indicator';
  typingIndicator.textContent = 'K2 Assistant is typing...';
  chatMessages.appendChild(typingIndicator);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    // Call backend API
    const response = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: message,
        conversation_id: conversationId,
        language: 'en'
      })
    });

    const data = await response.json();
    
    // Store conversation ID
    if (data.conversation_id) {
      conversationId = data.conversation_id;
    }

    // Remove typing indicator
    typingIndicator.remove();

    // Add assistant response
    const assistantMsg = document.createElement('div');
    assistantMsg.className = 'message assistant-msg';
    assistantMsg.innerHTML = data.message.replace(/\n/g, '<br>');
    chatMessages.appendChild(assistantMsg);

  } catch (error) {
    console.error('Error sending message:', error);
    
    // Remove typing indicator
    typingIndicator.remove();

    // Show error message
    const errorMsg = document.createElement('div');
    errorMsg.className = 'message assistant-msg';
    errorMsg.textContent = 'Sorry, I encountered an error. Please try again.';
    chatMessages.appendChild(errorMsg);
  }

  // Re-enable input
  sendBtn.disabled = false;
  userInput.disabled = false;
  userInput.focus();
  
  // Scroll to bottom
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !sendBtn.disabled) {
    sendMessage();
  }
});

// Close chat when clicking outside
document.addEventListener('click', (e) => {
  if (!chatWindow.contains(e.target) && !widget.contains(e.target)) {
    chatWindow.classList.remove('active');
  }
});
