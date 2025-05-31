# product-service/app/seed.py
from sqlmodel import Session
from .models import Product, User
from passlib.context import CryptContext
from uuid import uuid4

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fill(engine):
    with Session(engine) as s:
        if not s.query(User).first():                 # ещё нет данных?
            s.add(User(username="admin",
                       password=pwd_ctx.hash("admin123")))

            for i in range(1, 21):
                s.add(Product(
                    id=uuid4(), name=f"Лампочка {i}",
                    description="Классная лампа",
                    price=950 + i*50, quantity=50,
                    image_url="http://localhost:8000/assets/img/lamp.png"))
            s.commit()
