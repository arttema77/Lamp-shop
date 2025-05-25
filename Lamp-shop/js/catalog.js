// js/catalog.js
const API  = "http://localhost:8001";
const grid = document.getElementById("products-grid");
const cart = JSON.parse(localStorage.getItem("cart") || "[]");

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
  const total = cart.reduce((s, i) => s + i.qty, 0);
  document.getElementById("cart-count").textContent = total;
}
saveCart();

// изменение количества
function setQty(id, delta, span) {
  let row = cart.find(i => i.id === id);
  if (!row && delta > 0) {
    row = { id, qty: 0 };
    cart.push(row);
  }
  if (!row) return;

  row.qty = Math.max(0, row.qty + delta);
  if (row.qty === 0) cart.splice(cart.indexOf(row), 1);

  span.textContent = row.qty;
  saveCart();
}

(async () => {
  const products = await fetch(`${API}/products`).then(r => r.json());

  products.forEach(p => {
    const inCart = cart.find(i => i.id === p.id);
    const qty    = inCart ? inCart.qty : 0;

    const card   = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <a href="product.html?id=${p.id}">
        <img src="${p.image_url || 'assets/img/lamp.png'}" alt="${p.name}">
      </a>

      <h3><a href="product.html?id=${p.id}">${p.name}</a></h3>
      <p class="price">${p.price} ₽</p>

      <div class="ctrl">
        <button class="minus">-</button>
        <span class="qty">${qty}</span>
        <button class="plus">+</button>
      </div>
    `;

    const span = card.querySelector(".qty");
    card.querySelector(".minus").onclick = () => setQty(p.id, -1, span);
    card.querySelector(".plus").onclick  = () => setQty(p.id, +1, span);

    grid.append(card);
  });
})();
