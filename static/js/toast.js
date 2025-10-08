function showToast(title, message, type = 'info', duration = 2500) {
  const toast = document.getElementById('toast-component');
  const tTitle = document.getElementById('toast-title');
  const tMsg = document.getElementById('toast-message');
  const tIcon = document.getElementById('toast-icon');

  if (!toast) return;

  // reset style
  toast.classList.remove('border-green-500','bg-green-50',
                         'border-red-500','bg-red-50',
                         'border-blue-500','bg-blue-50');

  if (type === 'success') {
    toast.classList.add('border-green-500','bg-green-50');
    tIcon.textContent = '✅';
  } else if (type === 'error') {
    toast.classList.add('border-red-500','bg-red-50');
    tIcon.textContent = '⚠️';
  } else {
    toast.classList.add('border-blue-500','bg-blue-50');
    tIcon.textContent = '🔔';
  }

  tTitle.textContent = title || '';
  tMsg.textContent = message || '';

  toast.classList.remove('opacity-0','translate-y-10');
  toast.classList.add('opacity-100','translate-y-0');

  clearTimeout(window.__toastTimer);
  window.__toastTimer = setTimeout(()=>{
    toast.classList.remove('opacity-100','translate-y-0');
    toast.classList.add('opacity-0','translate-y-10');
  }, duration);
}
