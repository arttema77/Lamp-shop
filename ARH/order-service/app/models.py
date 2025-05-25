# ---------------------------------------------------------------------------
# ORM-модели SQLModel <-> таблицы Postgres.
# Здесь описываем структуру данных, которая реально хранится в базе
# (Product, Order, OrderItem и др.).
# ---------------------------------------------------------------------------

import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Order(SQLModel, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    customer_name: str
    customer_phone: str
    customer_address: str
    status: str = "new"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    order_id: uuid.UUID = Field(foreign_key="order.id")
    product_id: uuid.UUID
    quantity: int
    price: int

    order: Order | None = Relationship(back_populates="items")
