from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import chat

app = FastAPI()

class Query(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(query: Query):
    response = chat(query.message)
    return {"response": response}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Skysecure AI Agent</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  
  body {
    background: #0a0a0f;
    color: #e0e0e0;
    font-family: 'Segoe UI', sans-serif;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    padding: 20px 32px;
    background: #0d0d18;
    border-bottom: 1px solid #1e1e3a;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .logo {
    width: 10px;
    height: 10px;
    background: #4f6ef7;
    border-radius: 50%;
    box-shadow: 0 0 10px #4f6ef7;
  }

  header h1 {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 1px;
  }

  .status {
    margin-left: auto;
    font-size: 12px;
    color: #4f6ef7;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .status::before {
    content: '';
    width: 7px;
    height: 7px;
    background: #4f6ef7;
    border-radius: 50%;
    animation: pulse 1.5s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  #chat-box {
    flex: 1;
    overflow-y: auto;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    scrollbar-width: thin;
    scrollbar-color: #1e1e3a transparent;
  }

  .message {
    max-width: 75%;
    padding: 14px 18px;
    border-radius: 12px;
    font-size: 14px;
    line-height: 1.7;
    animation: fadeIn 0.3s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .user {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    align-self: flex-end;
    color: #c0c0e0;
  }

  .agent {
    background: #0d1117;
    border: 1px solid #1e1e3a;
    align-self: flex-start;
    color: #e0e0ff;
  }

  .agent .label {
    font-size: 11px;
    color: #4f6ef7;
    margin-bottom: 6px;
    letter-spacing: 1px;
    font-weight: 600;
  }

  .typing {
    display: flex;
    gap: 5px;
    align-items: center;
    padding: 14px 18px;
    background: #0d1117;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    align-self: flex-start;
    width: fit-content;
  }

  .typing span {
    width: 7px;
    height: 7px;
    background: #4f6ef7;
    border-radius: 50%;
    animation: bounce 1s infinite;
  }

  .typing span:nth-child(2) { animation-delay: 0.15s; }
  .typing span:nth-child(3) { animation-delay: 0.3s; }

  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
  }

  .input-area {
    padding: 20px 32px;
    background: #0d0d18;
    border-top: 1px solid #1e1e3a;
    display: flex;
    gap: 12px;
    align-items: center;
  }

  input {
    flex: 1;
    background: #12121f;
    border: 1px solid #2a2a4a;
    color: #e0e0e0;
    padding: 14px 18px;
    border-radius: 10px;
    font-size: 14px;
    outline: none;
    transition: border 0.2s;
  }

  input:focus { border-color: #4f6ef7; }
  input::placeholder { color: #444466; }

  button {
    background: #4f6ef7;
    color: white;
    border: none;
    padding: 14px 24px;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    letter-spacing: 0.5px;
  }

  button:hover { background: #3a58e0; }
  button:disabled { background: #2a2a4a; cursor: not-allowed; }
</style>
</head>
<body>

<header>
  <div class="logo"></div>
  <h1>SKYSECURE AI AGENT</h1>
  <div class="status">ONLINE</div>
</header>

<div id="chat-box">
  <div class="message agent">
    <div class="label">AGENT</div>
    Hello. I'm Skysecure's AI Agent. How can I assist you today?
  </div>
</div>

<div class="input-area">
  <input type="text" id="user-input" placeholder="Type your query..." />
  <button id="send-btn" onclick="sendMessage()">Send</button>
</div>

<script>
  const chatBox = document.getElementById('chat-box');
  const input = document.getElementById('user-input');
  const btn = document.getElementById('send-btn');

  input.addEventListener('keydown', e => {
    if (e.key === 'Enter') sendMessage();
  });

  function appendMessage(role, text) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    if (role === 'agent') {
      div.innerHTML = `<div class="label">AGENT</div>${text}`;
    } else {
      div.textContent = text;
    }
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function showTyping() {
    const div = document.createElement('div');
    div.className = 'typing';
    div.id = 'typing';
    div.innerHTML = '<span></span><span></span><span></span>';
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function removeTyping() {
    const t = document.getElementById('typing');
    if (t) t.remove();
  }

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage('user', message);
    input.value = '';
    btn.disabled = true;
    showTyping();

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await res.json();
      removeTyping();
      appendMessage('agent', data.response);
    } catch {
      removeTyping();
      appendMessage('agent', 'Error occurred. Please try again.');
    }

    btn.disabled = false;
    input.focus();
  }
</script>
</body>
</html>
"""