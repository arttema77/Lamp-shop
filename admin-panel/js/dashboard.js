// admin-panel/js/dashboard.js
import { authHeader, logout } from "./auth.js";

const API_PROD  = "http://localhost:8001/products";
const API_ORDER = "http://localhost:8002/orders";

const pBody = document.querySelector("#tbl-products tbody");
const oBody = document.querySelector("#tbl-orders  tbody");

/* ───────────────────── ТОВАРЫ ───────────────────── */
async function loadProducts() {
  const r = await fetch(API_PROD, { headers: authHeader() });
  if (r.status === 401) return logout();
  const list = await r.json();
  pBody.innerHTML = "";
  list.forEach(p => {
    pBody.insertAdjacentHTML("beforeend", `
      <tr data-id="${p.id}">
        <td>${p.id.slice(0,6)}…</td>
        <td>${p.name}</td>
        <td>${p.price}</td>
        <td>${p.quantity}</td>
        <td>
          <button class="edit">✏️</button>
          <button class="del" >🗑️</button>
        </td>
      </tr>`);
  });
}

/* удалить */
pBody.onclick = async e => {
  if (!e.target.classList.contains("del")) return;
  const id = e.target.closest("tr").dataset.id;
  if (!confirm("Удалить товар?")) return;
  await fetch(`${API_PROD}/${id}`, { method:"DELETE", headers: authHeader() });
  loadProducts();
};

/* редактировать (минимально: изменить количество) */
pBody.onclick = async e => {
  const tr = e.target.closest("tr[data-id]");
  if (!tr) return;
  const id = tr.dataset.id;

  /* — удалить — */
  if (e.target.classList.contains("del")) {
    if (!confirm("Удалить товар?")) return;
    await fetch(`${API_PROD}/${id}`, {
      method : "DELETE",
      headers: authHeader()
    });
    return loadProducts();
  }

  /* — редактировать — */
  if (e.target.classList.contains("edit")) {
  const tr   = e.target.closest("tr");
  const id   = tr.dataset.id;

  const curr = {
    name     : tr.children[1].textContent,
    price    : tr.children[2].textContent,
    quantity : tr.children[3].textContent
  };

  const name  = prompt("Название товара:",  curr.name);
  if (name === null) return;
  const price = prompt("Цена:",              curr.price);
  if (price === null) return;
  const qty   = prompt("Количество:",        curr.quantity);
  if (qty === null) return;

  const res = await fetch(`${API_PROD}/${id}`, {
    method : "PUT",
    headers: { "Content-Type":"application/json", ...authHeader() },
    body   : JSON.stringify({
      name     : name.trim(),
      price    : +price,
      quantity : +qty
    })
  });

  if (!res.ok) alert("Ошибка сохранения");
 else         loadProducts();
  }
};

/* ───────────────────── ЗАКАЗЫ ───────────────────── */
async function loadOrders() {
  const r = await fetch(API_ORDER, { headers: authHeader() });
  if (r.status === 401) return logout();
  const list = await r.json();

  oBody.innerHTML = "";
  list.forEach(o => {
    const total = o.items.reduce((s,i)=>s+i.price*i.quantity,0);

    oBody.insertAdjacentHTML("beforeend", `
      <tr data-id="${o.id}">
        <td>${o.id.slice(0,6)}…</td>
        <td class="cust">${o.customer_name}</td>
        <td>
          <select class="status">
            ${["new","paid","shipped","done"].map(s=>
               `<option value="${s}" ${s===o.status?"selected":""}>${s}</option>`).join("")}
          </select>
        </td>
        <td>${total}</td>
        <td>
          <button class="edit">✏️</button>
          <button class="del" >🗑️</button>
        </td>
      </tr>`);
  });
}

/* --- смена статуса (select) --- */
oBody.addEventListener("change", async e => {
  if (!e.target.classList.contains("status")) return;

  const id     = e.target.closest("tr").dataset.id;
  const status = e.target.value;                  // new | paid | shipped | done

  const res = await fetch(`${API_ORDER}/${id}`, {
    method : "PATCH",
    headers: { "Content-Type":"application/json", ...authHeader() },
    body   : JSON.stringify({ status })
  });

  if (!res.ok) {
    alert("Не удалось сменить статус");
    return loadOrders();                          // откатить селект, если упало
  }
});

/* --- удалить заказ --- */
oBody.addEventListener("click", async e => {
  if (!e.target.classList.contains("del")) return;
  const id = e.target.closest("tr").dataset.id;
  if (!confirm("Удалить заказ полностью?")) return;

  const res = await fetch(`${API_ORDER}/${id}`, {           // <-- DELETE /orders/{id}
    method :"DELETE",
    headers: authHeader()
  });
  if (!res.ok) return alert("Не удалось удалить заказ");
  loadOrders();
});

/* --- редактировать заказ (имя покупателя) --- */
oBody.addEventListener("click", async e => {
  if (!e.target.classList.contains("edit")) return;
  const tr  = e.target.closest("tr");
  const id  = tr.dataset.id;
  const now = tr.querySelector(".cust").textContent.trim();

  const name = prompt("Новое имя покупателя:", now);
  if (name === null || name === now) return;

  const ok = await fetch(`${API_ORDER}/${id}`, {           // PATCH /orders/{id}
    method :"PATCH",
    headers:{ "Content-Type":"application/json", ...authHeader() },
    body   : JSON.stringify({ customer_name:name })
  }).then(r=>r.ok);

  if (!ok) return alert("Ошибка сохранения");
  loadOrders();
});

/* -------------------------- init -------------------------- */
document.getElementById("logout").onclick = logout;
document.getElementById("btn-add").onclick = () => location.href = "add.html";

loadProducts();
loadOrders();
setInterval(loadOrders, 10_000);
