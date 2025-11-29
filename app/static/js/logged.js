document.getElementById("btn_logout").addEventListener("click", async function (e) {
  e.preventDefault();

  const response = await fetch("users/api/logout/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  });

  if (response.ok) {
      closeLoginModal();
      location.reload();
  }
});
