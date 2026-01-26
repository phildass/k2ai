// server.js or index.js
const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 10000;

// --- CORS & JSON body ---
app.use(cors());
app.use(express.json());

// --- Proxy /api/chat to FastAPI backend ---
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

app.use(
  '/api/chat',
  createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    pathRewrite: { '^/api/chat': '/chat' },
    onProxyReq: (proxyReq, req, res) => {
      // Make sure Content-Type and body is forwarded for POST
      if (
        req.body &&
        Object.keys(req.body).length &&
        req.method === 'POST'
      ) {
        const bodyData = JSON.stringify(req.body);
        proxyReq.setHeader('Content-Type', 'application/json');
        proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
        proxyReq.write(bodyData);
        proxyReq.end();
      }
    },
  })
);

// --- Serve static frontend files (customize if needed) ---
app.use(express.static(path.join(__dirname, 'public')));

// Fallback: serve index.html for frontend routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// --- Start server ---
app.listen(PORT, () => {
  console.log(`K2 AI Server running on port ${PORT}`);
  console.log(`Proxying /api/chat => ${PYTHON_BACKEND_URL}/chat`);
});