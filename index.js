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
