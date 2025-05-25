const tbody = document.querySelector("#cart-table tbody");
const cart = JSON.parse(localStorage.getItem("cart") || "[]");
let total = 0;

cart.forEach(item => {
  const id = item.id;
  const name = `Лампочка ${id}`;
  const img = `assets/img/lamp.png`;
  const price = 1000 + 50 * (id - 1);  // пример
  const sum = price * item.qty;
  total += sum;

  tbody.insertAdjacentHTML("beforeend", `
    <tr>
      <td>
        <img src="${img}" class="thumb" alt="" />
        ${name}
      </td>
      <td>${item.qty}</td>
      <td>${price} ₽</td>
      <td>${sum} ₽</td>
    </tr>`);
});

document.getElementById("total").textContent = `Итого: ${total} ₽`;
