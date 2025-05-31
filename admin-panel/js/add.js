// admin-panel/js/add.js
import { authHeader, logout } from "./auth.js";

const API = "http://localhost:8001/products";

document.getElementById("frm").onsubmit = async e => {
  e.preventDefault();

  const data = Object.fromEntries(new FormData(e.target));
  data.price    = +data.price;
  data.quantity = +data.quantity;

  const r = await fetch(API, {
    method : "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeader()
    },
    body: JSON.stringify(data)
  });

  if (r.status === 401) return logout();

  if (!r.ok) {
    alert("Ошибка сохранения (проверьте поля / JWT)");
    return;
  }
  alert("Добавлено!");
  location.href = "dashboard.html";
};
