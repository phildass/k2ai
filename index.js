console.log("Starting index.js..."); // <--- ADD THIS AS FIRST LINE!
require('dotenv').config();
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>K2 AI Assistant</title>
      <style>
        body { font-family: Arial, sans-serif; }
        .k2-btn {
          position: fixed;
          right: 2vw;
          bottom: 2vw;
          width: 64px;
          height: 64px;
          border-radius: 50%;
          background: #73c7fa;
          box-shadow: 0 4px 16px #0002;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          font-size: 2rem;
          z-index: 10000;
          transition: box-shadow 0.2s;
        }
        .k2-btn:hover::after {
          content: 'I am the K2 AI Assistant, how may I help you?';
          position: absolute;
          right: 110%;
          bottom: 16px;
          background: #fff;
          color: #222;
          padding: 6px 16px;
          border-radius: 10px;
          box-shadow: 0 2px 6px #0003;
          white-space: nowrap;
          font-size: 1rem;
          pointer-events: none;
        }
        #k2-chatbox {
          display: none;
          position: fixed;
          right: 2vw;
          bottom: 90px;
          width: 360px;
          height: 480px;
          background: #e3f3ff;
          border-radius: 18px;
          box-shadow: 0 8px 32px #0002;
          padding: 16px;
          z-index: 10000;
          flex-direction: column;
        }
        #k2-chatbox.active {
          display: flex;
        }
        #k2-messages {
          flex: 1;
          overflow-y: auto;
          border-radius: 10px;
          background: #fff;
          margin-bottom: 10px;
          padding: 10px;
          font-size: 1rem;
        }
        #k2-chat-input {
          display: flex;
        }
        #k2-chat-input input {
          flex: 1;
          border: 1px solid #c5e6fa;
          border-radius: 6px;
          padding: 8px;
          margin-right: 6px;
        }
        #k2-chat-input button {
          background: #73c7fa;
          border: none;
          color: #fff;
          font-weight: bold;
          border-radius: 6px;
          padding: 8px 12px;
          cursor: pointer;
        }
      </style>
    </head>
    <body>
      <div class="k2-btn" id="k2-asst-btn" title="I am the K2 AI Assistant, how may I help you?">🤖</div>
      <div id="k2-chatbox">
        <div style="font-weight:bold; margin-bottom: 6px;">K2 AI Assistant</div>
        <div id="k2-messages"></div>
        <form id="k2-chat-input" autocomplete="off">
          <input type="text" id="k2-prompt" placeholder="Ask a question..." autofocus>
          <button type="submit">Send</button>
        </form>
      </div>
      <script>
        // Widget button events
        const k2Btn = document.getElementById('k2-asst-btn');
        const k2Box = document.getElementById('k2-chatbox');
        k2Btn.onclick = () => k2Box.classList.toggle('active');
        document.addEventListener('click', (e) => {
          if (!k2Box.contains(e.target) && !k2Btn.contains(e.target)) {
            k2Box.classList.remove('active');
          }
        });

        // Chat logic
        const form = document.getElementById('k2-chat-input');
        const prompt = document.getElementById('k2-prompt');
        const messages = document.getElementById('k2-messages');
        form.onsubmit = async (e) => {
          e.preventDefault();
          if (!prompt.value.trim()) return;
          const myMsg = prompt.value;
          addMsg('You', myMsg);
          prompt.value = '';
          addMsg('K2', '...');
          try {
            const res = await fetch('/ask', {
              method: 'POST',
              headers: {'Content-Type':'application/json'},
              body: JSON.stringify({prompt: myMsg})
            });
            const data = await res.json();
            messages.lastChild.innerText = 'K2: ' + (data.response || data.error || "No answer");
          } catch {
            messages.lastChild.innerText = 'K2: (Error, could not connect)';
          }
        };
        function addMsg(sender, txt) {
          const el = document.createElement('div');
          el.innerText = sender + ": " + txt;
          messages.appendChild(el);
          messages.scrollTop = messages.scrollHeight;
         }
      </script>
    </body>
    </html>
  `);  // <--- Closing the template string and res.send
});     // <--- Closing the app.get('/', ... )

// [PASTE THE ADDITIONAL ENDPOINTS AND APP.LISTEN CODE HERE]
