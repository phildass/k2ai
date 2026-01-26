require('dotenv').config();
const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 10000;
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

// Proxy /api/chat to FastAPI /api/chat/
app.use('/api/chat', createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    logLevel: 'debug'
}));

// Proxy /api/health to FastAPI /health
app.use('/api/health', createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    pathRewrite: { '^/api/health': '/health' },
    logLevel: 'debug'
}));

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'public')));

// Fallback to index.html for any other GET requests
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`K2 AI Server running on port ${PORT}`);
    console.log(`Proxying /api/* -> Python backend at ${PYTHON_BACKEND_URL}`);
});