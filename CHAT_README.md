# Simple HTML+JS Chat Interface

A simple, elegant HTML+JS chat interface for the K2 Communications AI Chatbot FastAPI backend.

## Features

- 🎨 **Modern & Elegant Design** - Clean UI with gradient background
- 💬 **Real-time Chat** - Send messages and receive responses from the AI
- ⌨️ **Enter Key Support** - Press Enter to send messages
- 📱 **Responsive** - Works on different screen sizes
- 🔄 **Auto-scroll** - Automatically scrolls to the latest message
- ⏳ **Loading Indicator** - Shows animated dots while waiting for response
- ⚠️ **Error Handling** - Graceful error messages if the server is unavailable
- 🎭 **Distinct Styling** - User and bot messages clearly differentiated

## Files

- `chat.html` - Main HTML file with embedded CSS
- `script.js` - JavaScript for API communication and chat functionality

## Usage

### Quick Start

1. Make sure the FastAPI backend is running at `http://localhost:8000`:
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. Open `chat.html` directly in your browser, or serve it via HTTP:
   ```bash
   # Option 1: Open directly
   open chat.html  # macOS
   xdg-open chat.html  # Linux
   start chat.html  # Windows

   # Option 2: Serve via HTTP (recommended)
   python -m http.server 8080
   ```

3. If using HTTP server, navigate to: `http://localhost:8080/chat.html`

### Configuration

The API endpoint can be changed in `script.js`:

```javascript
const API_URL = 'http://localhost:8000/api/chat/';
```

Update this URL if your backend is running on a different host or port.

## Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- FastAPI backend running at `http://localhost:8000` (or configured URL)

## Styling

The interface uses:
- Purple gradient theme matching K2 Communications branding
- User messages: Right-aligned with purple gradient background
- Bot messages: Left-aligned with white background
- Smooth animations for message appearance
- Custom scrollbar styling

## API Integration

The chat interface communicates with the FastAPI backend using:

**Endpoint:** `POST http://localhost:8000/api/chat/`

**Request:**
```json
{
  "message": "Your message here",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "message": "AI response",
  "conversation_id": "conversation-id",
  "suggestions": ["suggestion1", "suggestion2"],
  "metadata": {}
}
```

## No Dependencies

This is a pure HTML+CSS+JS implementation with no external dependencies or frameworks. Everything needed is included in the two files.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Any modern browser with ES6 support

## Screenshots

![Chat Interface](https://github.com/user-attachments/assets/68e1dcca-714b-4c9c-9e8a-888210ada9dc)

## License

Part of the K2 Communications AI Chatbot project.
