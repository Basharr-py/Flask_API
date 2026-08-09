// success-modal.js
// Controls the success modal overlay. No JSON used.
// Usage:
// - Call showSuccessModal() to open the modal.
// - The modal auto-closes after AUTO_CLOSE_MS (set to 4500 ms).
// - You can disable auto-close by setting AUTO_CLOSE_MS = 0.
// - The "Go to Login" button retains its href behavior.

(function () {
  var AUTO_CLOSE_MS = 4500; // set to 0 to disable auto-close
  var modal = document.getElementById('successModal');

  if (!modal) {
    // nothing to do if modal not present
    return;
  }

  var autoCloseTimer = null;
  var previouslyFocused = null;

  function openModal() {
    previouslyFocused = document.activeElement;
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    // focus first focusable inside modal (button)
    var btn = modal.querySelector('button, [tabindex]:not([tabindex="-1"])');
    if (btn && typeof btn.focus === 'function') btn.focus();

    if (AUTO_CLOSE_MS > 0) {
      clearAutoClose();
      autoCloseTimer = setTimeout(closeModal, AUTO_CLOSE_MS);
    }
  }

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    clearAutoClose();
    // restore focus
    if (previouslyFocused && typeof previouslyFocused.focus === 'function') {
      previouslyFocused.focus();
    }
  }

  function clearAutoClose() {
    if (autoCloseTimer) {
      clearTimeout(autoCloseTimer);
      autoCloseTimer = null;
    }
  }

  // Close when clicking backdrop (modal overlay) but not when clicking modal-content
  modal.addEventListener('click', function (e) {
    var content = modal.querySelector('.modal-content');
    if (!content) return;
    if (!content.contains(e.target)) {
      closeModal();
    }
  });

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      // only act if modal is open
      if (modal.classList.contains('open')) {
        closeModal();
      }
    }
  });

  // Expose functions globally for server-side to trigger or for other scripts
  window.showSuccessModal = openModal;
  window.closeSuccessModal = closeModal;

  // Auto-open if a data attribute is present on the modal element:
  // e.g., <div id="successModal" data-open="true" ...>
  if (modal.getAttribute('data-open') === 'true') {
    // wait for DOM ready if not yet
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { openModal(); });
    } else {
      openModal();
    }
  }

  // Optional: allow programmatic open when form submission redirects to this page:
  // In your Flask template, if registration succeeded, add the attribute:
  // <div id="successModal" data-open="true" ...>
  // OR call showSuccessModal() from inline script after page load.

})();