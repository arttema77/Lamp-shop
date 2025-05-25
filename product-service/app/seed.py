from sqlmodel import Session
from .db import engine
from .models import Product

DATA = [
    {
        "name": f"Лампочка {i}",
        "description": "Классная лампа",
        "price": 1000 + 50 * (i - 1),
        "quantity": 50,
        "image_url": "http://localhost:8000/assets/img/lamp.png",
    }
    for i in range(1, 21)
]

with Session(engine) as s:
    if s.query(Product).count() == 0:
        s.add_all(Product(**p) for p in DATA)
        s.commit()
        print("🚀 20 products inserted")
