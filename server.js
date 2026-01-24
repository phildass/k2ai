const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
app.use(cors());
app.use(express.json());

// Serve static files from public directory
app.use(express.static('public'));

// Proxy API requests to Python FastAPI backend
// Change this URL to your Python backend URL when deployed
const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || 'http://localhost:8000';

app.use('/api', createProxyMiddleware({
  target: PYTHON_BACKEND_URL,
  changeOrigin: true,
  onProxyReq: (proxyReq, req, res) => {
    console.log(`[Proxy] ${req.method} ${req.path} -> ${PYTHON_BACKEND_URL}${req.path}`);
  },
  onError: (err, req, res) => {
    console.error('[Proxy Error]:', err.message);
    res.status(500).json({ 
      error: 'Backend connection error',
      message: 'Unable to connect to AI backend. Please ensure the Python server is running.'
    });
  }
}));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✓ Frontend server running on port ${PORT}`);
  console.log(`✓ Proxying API requests to: ${PYTHON_BACKEND_URL}`);
  console.log(`✓ Visit: http://localhost:${PORT}`);
  console.log(`✓ Admin Panel: http://localhost:${PORT}/admin.html`);
});
