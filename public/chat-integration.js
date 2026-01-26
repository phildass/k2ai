const widget = document.getElementById('k2Widget');
const chatWindow = document.getElementById('chatWindow');
const closeBtn = document.getElementById('closeBtn');
const sendBtn = document.getElementById('sendBtn');
const userInput = document.getElementById('userInput');
const chatMessages = document.getElementById('chatMessages');

const API_URL = 'http://localhost:8000/chat';  // Direct to Python
let conversationId = null;

widget.addEventListener('click', () => {
  chatWindow.classList.toggle('active');
  if (chatWindow.classList.contains('active')) {
    userInput.focus();
  }
});

closeBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  chatWindow.classList.remove('active');
});

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  sendBtn.disabled = true;
  userInput.disabled = true;

  const userMsg = document.createElement('div');
  userMsg.className = 'message user-msg';
  userMsg.textContent = message;
  chatMessages.appendChild(userMsg);
  userInput.value = '';

  const typingIndicator = document.createElement('div');
  typingIndicator.className = 'message typing-indicator';
  typingIndicator.textContent = 'K2 Assistant is typing...';
  chatMessages.appendChild(typingIndicator);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message,
        conversation_id: conversationId,
        language: 'en'
      })
    });

    typingIndicator.remove();

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const data = await response.json();
    if (data.conversation_id) conversationId = data.conversation_id;

    const assistantMsg = document.createElement('div');
    assistantMsg.className = 'message assistant-msg';
    assistantMsg.textContent = data.message || 'Sorry, I encountered an error.';
    chatMessages.appendChild(assistantMsg);

    if (data.suggestions && data.suggestions.length > 0) {
      const suggestionsDiv = document.createElement('div');
      suggestionsDiv.className = 'suggestions';
      data.suggestions.forEach(suggestion => {
        const btn = document.createElement('button');
        btn.className = 'suggestion-btn';
        btn.textContent = suggestion;
        btn.onclick = () => { userInput.value = suggestion; sendMessage(); };
        suggestionsDiv.appendChild(btn);
      });
      chatMessages.appendChild(suggestionsDiv);
    }
  } catch (error) {
    console.error('Error:', error);
    if (typingIndicator.parentNode) typingIndicator.remove();
    const errorMsg = document.createElement('div');
    errorMsg.className = 'message assistant-msg';
    errorMsg.textContent = 'Sorry, I encountered an error. Please try again.';
    chatMessages.appendChild(errorMsg);
  } finally {
    sendBtn.disabled = false;
    userInput.disabled = false;
    userInput.focus();
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});
