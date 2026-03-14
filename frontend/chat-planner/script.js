const chatWindow = document.getElementById('chatWindow');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

function addMessage(content, role = 'assistant') {
  const div = document.createElement('div');
  div.className = `message message--${role}`;
  div.textContent = content;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(userPrompt) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_prompt: userPrompt }),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  const payload = await response.json();
  return payload.data ?? 'Không nhận được phản hồi từ hệ thống.';
}

addMessage('Xin chào! Mình là Chat Planner. Bạn muốn đi Quy Nhơn mấy ngày và ngân sách bao nhiêu?');

chatForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const userPrompt = messageInput.value.trim();
  if (!userPrompt) return;

  addMessage(userPrompt, 'user');
  messageInput.value = '';
  sendBtn.disabled = true;

  try {
    addMessage('Đang xử lý yêu cầu của bạn...');
    const loadingMessage = chatWindow.lastElementChild;
    const answer = await sendMessage(userPrompt);
    loadingMessage.textContent = answer;
  } catch (error) {
    addMessage(`Có lỗi khi gọi backend: ${error.message}`);
  } finally {
    sendBtn.disabled = false;
    messageInput.focus();
  }
});
