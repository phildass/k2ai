// Error handlers for debugging
process.on('uncaughtException', function (err) {
  console.error('Uncaught Exception:', err);
});
process.on('unhandledRejection', function (err) {
  console.error('Unhandled Rejection:', err);
});

console.log("Starting index.js...");

require('dotenv').config();
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// === Serve everything (HTML, CSS, assets, k2logo.png, etc) from the /public folder ===
app.use(express.static('public'));

// Chat API endpoint
app.post('/ask', (req, res) => {
  res.json({ response: "This is a placeholder response from K2 AI. Backend integration needed!" });
});

// Admin API endpoint
app.get('/admin', (req, res) => {
  res.send(`
    <h2>K2 AI Assistant Admin Panel</h2>
    <p>This page is under construction. Admin tools for managing custom Q/A will appear here.</p>
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
  if (!process.env.OPENAI_API_KEY) {
    console.warn('⚠️  WARNING: OPENAI_API_KEY is not set in environment variables');
    console.warn('   Set OPENAI_API_KEY in your .env file or Render dashboard');
  } else {
    console.log('✓ OPENAI_API_KEY is configured');
  }
});
