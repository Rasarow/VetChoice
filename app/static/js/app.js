document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-autofocus]').forEach((element) => element.focus());
  document.querySelectorAll('.js-searchable-select').forEach((select) => {
    select.setAttribute('title', 'Open the list and type letters to jump to matching breeds.');
  });
});
