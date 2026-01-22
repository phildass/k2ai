require('dotenv').config();
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Root route - Testing page
app.get('/', (req, res) => {
  res.send('Testing page for K2 AI');
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
