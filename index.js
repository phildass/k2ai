require('dotenv').config();
const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 10000;
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

// Proxy /api/admin to FastAPI backend
app.use('/api/admin', createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    logLevel: 'debug'
}));

// Proxy /api/chat to FastAPI backend
app.use('/api/chat', createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    logLevel: 'debug'
}));

// Proxy /api/health to FastAPI backend
app.use('/api/health', createProxyMiddleware({
    target: PYTHON_BACKEND_URL,
    changeOrigin: true,
    pathRewrite: { '^/api/health': '/health' },
    logLevel: 'debug'
}));

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Special route to serve admin.html at /admin
app.get('/admin', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'admin.html'));
});

// Optional catch-all for frontend SPA
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`K2 AI Server running on port ${PORT}`);
    console.log(`Proxying /api/* -> Python backend at ${PYTHON_BACKEND_URL}`);
});