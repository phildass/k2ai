require('dotenv').config();
const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

// Error handlers for debugging
process.on('uncaughtException', function (err) {
  console.error('Uncaught Exception:', err);
});
process.on('unhandledRejection', function (err) {
  console.error('Unhandled Rejection:', err);
});

const app = express();
const PORT = process.env.PORT || 3000;

// --- Proxy POST/any requests to /api/chat to FastAPI backend ---
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';
app.use(
  '/api/chat',
  createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    pathRewrite: { '^/api/chat': '/chat' },
    logLevel: 'debug'
  })
);

// --- Serve static frontend files such as HTML, CSS ---
app.use(express.static(path.join(__dirname, 'public')));

// --- Health check endpoint ---
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

// --- Fallback: serve index.html for all other GETs ---
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// --- Start server ---
app.listen(PORT, '0.0.0.0', () => {
  console.log(`K2 AI Server running on port ${PORT}`);
  if (!process.env.OPENAI_API_KEY) {
    console.warn('⚠️  WARNING: OPENAI_API_KEY is not set in environment variables');
  } else {
    console.log('✓ OPENAI_API_KEY is configured');
  }
  console.log(`Proxying /api/chat ↔ ${PYTHON_BACKEND_URL}/chat`);
});