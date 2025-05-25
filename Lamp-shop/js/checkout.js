/* js/checkout.js – оформление заказа */

const PRODUCT_API = "http://localhost:8001";
const ORDER_API   = "http://localhost:8002";

const rawCart = JSON.parse(localStorage.getItem("cart") || "[]");

// защита от пустой корзины
if (!rawCart.length) {
  alert("Корзина пуста");
  location.href = "index.html";
}

document.getElementById("form").addEventListener("submit", async e => {
  e.preventDefault();

  /* ------------------------------------------------------------------
     1. данные покупателя
  ------------------------------------------------------------------ */
  const client = Object.fromEntries(new FormData(e.target));

  /* ------------------------------------------------------------------
     2. формируем items = [{ product_id, quantity, price }]
        ─ запрашиваем цену у product-service, чтобы она была 100 % верной
  ------------------------------------------------------------------ */
  const items = await Promise.all(
    rawCart
      .filter(it => it.qty > 0)
      .map(async ({ id, qty }) => {
        const p = await fetch(`${PRODUCT_API}/products/${id}`).then(r => r.json());
        return {
          product_id: id,
          quantity  : Number(qty),
          price     : Number(p.price)           // ← гарантированно целое число
        };
      })
  );

  /* ------------------------------------------------------------------
     3. собираем тело заказа и отправляем POST /orders
  ------------------------------------------------------------------ */
  const body = {
    customer_name   : client.name,
    customer_phone  : client.phone,
    customer_address: client.address,
    items
  };

  try {
    const res = await fetch(`${ORDER_API}/orders`, {
      method : "POST",
      headers: { "Content-Type": "application/json" },
      body   : JSON.stringify(body)
    });

    if (!res.ok) throw new Error(await res.text());

    const { id } = await res.json();          // ← UUID заказа
    localStorage.removeItem("cart");          // корзина оформлена → чистим
    location.href = `success.html?order=${id}`;
  } catch (err) {
    console.error(err);
    alert("Не удалось оформить заказ. Попробуйте ещё раз.");
  }
});
