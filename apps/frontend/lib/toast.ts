import { isBrowser } from './safe';

export const toast = (msg: string, duration = 3000) => {
  if (!isBrowser()) return;
  const div = document.createElement('div');
  div.textContent = msg;
  div.className = 'fixed top-2 right-2 z-50 rounded bg-gray-800 px-2 py-1 text-sm text-white shadow';
  document.body.appendChild(div);
  setTimeout(() => div.remove(), duration);
};

export default toast;
