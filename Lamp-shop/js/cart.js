const API   = "http://localhost:8001";
const cart  = JSON.parse(localStorage.getItem("cart") || "[]");
const tbody = document.querySelector("#cart-table tbody");
let total   = 0;

(async () => {
  for (const {id, qty} of cart) {
    const p   = await fetch(`${API}/products/${id}`).then(r=>r.ok?r.json():null);
    if (!p) continue;                         // товар мог быть удалён админом
    const sum = p.price * qty;
    total    += sum;

    tbody.insertAdjacentHTML("beforeend",`
      <tr>
         <td><img class="thumb" src="${p.image_url}"> ${p.name}</td>
         <td>${qty}</td><td>${p.price} ₽</td><td>${sum} ₽</td>
      </tr>`);
  }
  document.getElementById("total").textContent = `Итого: ${total} ₽`;
})();
