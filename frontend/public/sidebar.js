const sideMenu = document.getElementById("side-menu");
const sidebar = document.getElementById("sidebar-id");

sideMenu.addEventListener("click", () => {
  sidebar.classList.toggle("hidden");
});
