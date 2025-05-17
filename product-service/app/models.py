# ---------------------------------------------------------------------------
# ORM-модели SQLModel <-> таблицы Postgres.
# Здесь описываем структуру данных, которая реально хранится в базе
# (Product, Order, OrderItem и др.).
# ---------------------------------------------------------------------------

import uuid
from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True
    )
    name: str
    description: str | None = None
    price: int = 0
    quantity: int = 0
    image_url: str | None = None
