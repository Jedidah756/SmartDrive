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
});
