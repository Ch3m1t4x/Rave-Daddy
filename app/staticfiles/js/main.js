// Ojos que siguen el ratón
(function () {
  const head = document.getElementById('botHead');
  const left = document.getElementById('pupilLeft');
  const right = document.getElementById('pupilRight');

  // límites del movimiento del pupil dentro del ojo
  const maxOffset = 10; // px desde el centro

  function movePupils(e) {
    const rect = head.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    const dx = e.clientX - cx;
    const dy = e.clientY - cy;

    // normalizamos
    const angle = Math.atan2(dy, dx);
    const dist = Math.min(Math.hypot(dx, dy) / 80, 1); // suavizado
    const ox = Math.cos(angle) * maxOffset * dist;
    const oy = Math.sin(angle) * maxOffset * dist;

    left.style.transform = `translate(${ox}px, ${oy}px)`;
    right.style.transform = `translate(${ox}px, ${oy}px)`;
  }

  window.addEventListener('mousemove', movePupils, { passive: true });
})();

const input = document.getElementById("chatInput");
const sendBtn = document.getElementById("chatSend");
const chatBox = document.getElementById("chatMessages");

// Add user message
function addUserMessage(text) {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble", "user");
  bubble.textContent = text;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// Add bot message
function addBotMessage(text) {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble", "bot");
  bubble.textContent = text;
  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function handleSend() {
  const msg = input.value.trim();
  if (!msg) return;

  addUserMessage(msg);
  input.value = "";

  // Llamada real al backend
  const res = await fetch("/chatbot/send/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg }),
  });

  addBotMessage("Daddy está pensando...");

  const data = await res.json();
  addBotMessage(data.response);
}

sendBtn.addEventListener("click", handleSend);
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") handleSend();
});
