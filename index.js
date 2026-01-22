require('dotenv').config();
const express = require('express');
const path = require('path');

const app = express();  // <-- THIS must come before any app.get or app.use

const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Root route - Serve Assistant UI
app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>K2 AI Assistant</title>
    </head>
    <body>
      <h1>K2 AI Assistant</h1>
      <div>
        <input id="prompt" type="text" placeholder="Ask a question..." style="width:300px">
        <button onclick="sendMessage()">Send</button>
        <pre id="response" style="background:#eee; padding:1em;"></pre>
      </div>
      <script>
        async function sendMessage() {
          const prompt = document.getElementById('prompt').value;
          document.getElementById('response').innerText = 'Loading...';
          const res = await fetch('/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
          });
          const data = await res.json();
          document.getElementById('response').innerText = data.response || data.error || 'No response';
        }
      </script>
    </body>
    </html>
  `);
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    env: {
      hasOpenAIKey: !!process.env.OPENAI_API_KEY,
      port: PORT
    }
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`K2 AI Server running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
  
  // Check for OpenAI API key
  if (!process.env.OPENAI_API_KEY) {
    console.warn('⚠️  WARNING: OPENAI_API_KEY is not set in environment variables');
    console.warn('   Set OPENAI_API_KEY in your .env file or Render dashboard');
  } else {
    console.log('✓ OPENAI_API_KEY is configured');
  }
});
