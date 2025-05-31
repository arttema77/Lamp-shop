/* admin-panel/js/auth.js
   хранит/выдаёт JWT-токен и помогает выйти из панели            */

const KEY = 'token';

// вернуть токен как заголовки для fetch
function authHeader() {
  const t = localStorage.getItem(KEY);
  return t ? { Authorization: `Bearer ${t}` } : {};
}

// выйти
function logout() {
  localStorage.removeItem(KEY);
  location.href = 'login.html';
}

export { authHeader, logout };
