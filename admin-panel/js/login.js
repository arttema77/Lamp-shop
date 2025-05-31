/* admin-panel/js/login.js
   авторизация + сохранение токена в localStorage                */

import { logout } from './auth.js';

const API_AUTH = 'http://localhost:8001/auth/login'; // product-service

// ───────────────── helpers ──────────────────
async function login(username, password) {
  const r = await fetch(API_AUTH, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body:   JSON.stringify({ username, password })
  });

  if (!r.ok) throw new Error('Неверный логин или пароль');
  return (await r.json()).access_token;          // {access_token, token_type}
}

// ───────────────── UI ────────────────────────
document.getElementById('login-form').onsubmit = async e => {
  e.preventDefault();
  const fd = new FormData(e.target);
  const u  = fd.get('username');
  const p  = fd.get('password');

  try {
    const token = await login(u, p);
    localStorage.setItem('token', token);
    location.href = 'dashboard.html';            // успех → в панель
  } catch (err) {
    alert(err.message);
    logout();                                    // на всякий случай чистим токен
  }
};
