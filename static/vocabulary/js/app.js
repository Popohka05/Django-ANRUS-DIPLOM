document.addEventListener('DOMContentLoaded', () => {
  const button = document.querySelector('[data-menu-button]');
  const menu = document.querySelector('[data-menu]');
  if (button && menu) {
    button.addEventListener('click', () => menu.classList.toggle('is-open'));
  }

  const modeTabs = document.querySelectorAll('[data-mode-tab]');
  const modeCards = document.querySelectorAll('[data-mode-card]');
  modeTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const mode = tab.dataset.modeTab;
      modeTabs.forEach((item) => item.classList.toggle('is-active', item === tab));
      modeCards.forEach((card) => {
        card.classList.toggle('is-active', card.dataset.modeCard === mode);
      });
    });
  });

  document.querySelectorAll('[data-deck]').forEach((deck) => {
    const cards = Array.from(deck.querySelectorAll('[data-deck-card]'));
    const prev = deck.querySelector('[data-deck-prev]');
    const next = deck.querySelector('[data-deck-next]');
    const current = deck.querySelector('[data-deck-current]');
    const progress = deck.querySelector('[data-deck-progress]');
    let index = 0;

    const showCard = (nextIndex) => {
      index = Math.max(0, Math.min(cards.length - 1, nextIndex));
      cards.forEach((card, cardIndex) => card.classList.toggle('is-active', cardIndex === index));
      if (current) current.textContent = String(index + 1);
      if (progress) progress.style.width = `${((index + 1) / cards.length) * 100}%`;
      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index === cards.length - 1;
    };

    prev?.addEventListener('click', () => showCard(index - 1));
    next?.addEventListener('click', () => showCard(index + 1));
    showCard(0);
  });
});
