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
    const dist = Math.min(Math.hypot(dx, dy) / 80, 1);
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

  const res = await fetch("/chatbot/send/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg }),
  });

  const data = await res.json();
  addBotMessage(data.response);
}

sendBtn.addEventListener("click", handleSend);
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") handleSend();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function openLoginModal() {
  document.getElementById("login-modal").classList.remove("hidden");
}

function closeLoginModal() {
  document.getElementById("login-modal").classList.add("hidden");
}

document.getElementById("login-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const response = await fetch("users/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  });

  const data = await response.json();

  if (data.success) {
      closeLoginModal();
      location.reload();
  } else {
      document.getElementById("login-error").classList.remove("hidden");
  }
});


function openRegister() {
    document.getElementById("login-view").classList.add("hidden");
    document.getElementById("register-view").classList.remove("hidden");
}

function openLogin() {
    document.getElementById("register-view").classList.add("hidden");
    document.getElementById("login-view").classList.remove("hidden");
}

document.getElementById("register-form").addEventListener("submit", async function(e){
    e.preventDefault();

    const username = document.getElementById("reg-username").value;
    const email = document.getElementById("reg-email").value;
    const password = document.getElementById("reg-password").value;

    const response = await fetch("/users/api/register/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })
    });

    const data = await response.json();

    if (data.success) {
        closeLoginModal();
        location.reload();
    } else {
        document.getElementById("register-error").innerText = data.error || "Error desconocido";
        document.getElementById("register-error").classList.remove("hidden");
    }
});