const input = document.getElementById('input');
const messages = document.getElementById('messages');

function addMessage(text, sender) {
  const msg = document.createElement('div');
  msg.className = sender;
  msg.textContent = `${sender === 'user' ? 'You' : 'Bot'}: ${text}`;
  messages.appendChild(msg);
}

async function sendMessage() {
  const userText = input.value;
  if (!userText) return;
  addMessage(userText, 'user');
  input.value = '';

  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userText })
  });
  const data = await response.json();
  addMessage(data.reply, 'bot');
}