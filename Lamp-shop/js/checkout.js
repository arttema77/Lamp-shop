// обработка формы оформления заказа
document.getElementById("form").onsubmit = e => {
  e.preventDefault();

  // генерируем случайный 5‑значный номер заказа
  const orderId = Math.floor(Math.random() * 90000 + 10000);

  // сохраняем, чтобы success.html мог его показать
  localStorage.setItem("lastOrderId", orderId);

  // корзина выполнена → очищаем
  localStorage.removeItem("cart");

  // переходим на страницу «Спасибо»
  location.href = "success.html";
};
