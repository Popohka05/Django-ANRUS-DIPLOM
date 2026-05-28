document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('[data-menu-button]');
  const menu = document.querySelector('[data-menu]');
  if (button && menu) {
    button.addEventListener('click', () => menu.classList.toggle('is-open'));
  }
});
