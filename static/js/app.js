document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const toggle = document.querySelector("[data-toggle-sidebar]");

  if (toggle && sidebar) {
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("is-open");
    });
  }

  document.querySelectorAll("[data-auto-dismiss]").forEach((node) => {
    setTimeout(() => node.remove(), 4000);
  });

  document.querySelectorAll("[data-pw-toggle]").forEach((btn) => {
    const wrap = btn.closest(".password-wrap");
    const input = wrap && wrap.querySelector("input");
    if (!input) return;
    btn.addEventListener("click", () => {
      const isHidden = input.type === "password";
      input.type = isHidden ? "text" : "password";
      btn.textContent = isHidden ? "\uD83D\uDE48" : "\uD83D\uDC41";
    });
  });
});
