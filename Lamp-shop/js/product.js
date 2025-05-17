const id=1; // пока всегда «первая лампочка»
const product={id,name:`Лампочка ${id}`,price:1200,descr:"Классная лампа",img:"assets/img/lamp.png"};

document.getElementById("title").textContent=product.name;
document.getElementById("photo").src=product.img;
document.getElementById("price").textContent=`${product.price} ₽`;
document.getElementById("descr").textContent=product.descr;

document.getElementById("add-btn").onclick=()=>{  
  const cart=JSON.parse(localStorage.getItem("cart")||"[]");
  const idx=cart.findIndex(i=>i.id===product.id);
  idx>=0?cart[idx].qty++:cart.push({id:product.id,qty:1});
  localStorage.setItem("cart",JSON.stringify(cart));
  alert("Добавлено!");
};
