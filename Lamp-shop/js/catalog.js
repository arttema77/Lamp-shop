const products = [...Array(20)].map((_, i) => ({
  id: i + 1,
  name: `Лампочка ${i + 1}`,
  price: 1000 + 50 * i,
  img: "assets/img/lamp.png"
}));

const grid = document.getElementById("products-grid");
const cart = JSON.parse(localStorage.getItem("cart") || "[]");

products.forEach(p => {
  const qty = cart.find(i => i.id === p.id)?.qty || 0;

grid.insertAdjacentHTML("beforeend", `
  <div class="card" id="card-${p.id}">
    <a class="card-link" href="product.html?id=${p.id}">
      <img src="${p.img}" alt="">
      <h3>${p.name}</h3>
      <p>${p.price} ₽</p>
    </a>

    <div class="ctrl-row">
      <button onclick="changeQty(${p.id}, -1)">–</button>
      <span id="q-${p.id}">${qty}</span>
      <button onclick="changeQty(${p.id}, 1)">+</button>
    </div>
  </div>
`);
});

function add(id) {
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const item = cart.find(i => i.id === id);
  if (item) {
    item.qty++;
  } else {
    cart.push({ id, qty: 1 });
  }
  localStorage.setItem("cart", JSON.stringify(cart));

  // обновляем цифру в карточке
  document.getElementById(`q-${id}`).textContent =
    cart.find(i => i.id === id).qty;

  // обновляем счётчик в шапке
  updateHeader();
}

function updateHeader() {
  const n = JSON.parse(localStorage.getItem("cart") || "[]")
              .reduce((s, i) => s + i.qty, 0);
  document.getElementById("cart-count").textContent = n;
}
updateHeader();

function changeQty(id, delta) {
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const idx = cart.findIndex(i => i.id === id);

  if (idx >= 0) {
    cart[idx].qty += delta;
    if (cart[idx].qty <= 0) {
      cart.splice(idx, 1);
    }
  } else if (delta > 0) {
    cart.push({ id, qty: 1 });
  }

  localStorage.setItem("cart", JSON.stringify(cart));
  document.getElementById(`q-${id}`).textContent =
    cart.find(i => i.id === id)?.qty || 0;

  updateHeader();
}