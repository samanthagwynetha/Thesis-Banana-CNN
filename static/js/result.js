const mobileMenuButton = document.getElementById("mobile-menu-button");
const mobileMenu = document.getElementById("mobile-menu");

// Mobile menu toggle
mobileMenuButton.addEventListener("click", () => {
  mobileMenu.classList.toggle("hidden");
});
