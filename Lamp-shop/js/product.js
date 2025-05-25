
// ──────────────────────────────────────────────────────────────
// Карточка товара: загрузка данных, счётчик и синхронизация корзины
// API      : GET http://localhost:8001/products/:id
// localStorage key: "cart"  →  [{ id: "<uuid>", qty: <number> }, … ]
// ──────────────────────────────────────────────────────────────
const API = "http://localhost:8001";
const id  = new URLSearchParams(location.search).get("id");   // id товара из query-строки

// ссылки на элементы ✨
const $name  = document.getElementById("p-name");
const $price = document.getElementById("p-price");
const $img   = document.getElementById("p-img");
const $desc  = document.getElementById("p-desc");
const $qty   = document.getElementById("p-qty");

// ─── начальное количество: берём из корзины, иначе 1 ───────────
const cart   = JSON.parse(localStorage.getItem("cart") || "[]");
const found  = cart.find(i => i.id === id);
let   qty    = found ? found.qty : 1;
$qty.textContent = qty;                                      // сразу выводим

// ─── загружаем данные товара с бэкенда ────────────────────────
(async () => {
  try {
    const p = await fetch(`${API}/products/${id}`).then(r => r.json());

    $name.textContent   = p.name        ?? `Товар ${id}`;
    $price.textContent  = (p.price ?? 0) + " ₽";
    $img.src            = p.image_url   || "assets/img/lamp.png";
    $img.alt            = p.name        ?? "Фото товара";
    $desc.textContent   = p.description || "Описание отсутствует";
  } catch (err) {
    console.error("Не удалось загрузить товар:", err);
    $name.textContent = "Ошибка загрузки";
  }
})();

// ─── кнопки «-» и «+» ──────────────────────────────────────────
document.getElementById("btn-minus").onclick = () => changeQty(-1);
document.getElementById("btn-plus").onclick  = () => changeQty(+1);

function changeQty(delta) {
  qty = Math.max(0, qty + delta);       // не даём уйти в минус
  $qty.textContent = qty;
  syncCart();
}

// ─── синхронизация localStorage ───────────────────────────────
function syncCart() {
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const idx  = cart.findIndex(i => i.id === id);

  if (qty === 0) {
    if (idx !== -1) cart.splice(idx, 1);        // удаляем позицию
  } else {
    idx !== -1 ? (cart[idx].qty = qty)          // обновляем количество
               : cart.push({ id, qty });        // или добавляем новую
  }

  localStorage.setItem("cart", JSON.stringify(cart));
}
