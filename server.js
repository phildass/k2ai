const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Replace this function with OpenAI or other AI API integration
async function getAIResponse(message) {
  // Simple canned response for demo. Replace with OpenAI if you have API key.
  if (message.toLowerCase().includes('services')) {
    return "We offer PR consultancy, crisis management, digital marketing, and content development. How can I help?";
  }
  return "I'm the K2 Communications AI assistant. Ask me about our PR services!";
}

app.post('/api/chat', async (req, res) => {
  const userMessage = req.body.message;
  const aiReply = await getAIResponse(userMessage);
  res.json({ reply: aiReply });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));