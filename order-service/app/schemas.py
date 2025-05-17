# ---------------------------------------------------------------------------
# Pydantic-схемы для валидации входных / выходных данных API.
# Эти объекты не сохраняются в БД напрямую, а лишь гарантируют,
# что JSON-payload соответствует ожидаемой структуре.
# ---------------------------------------------------------------------------

import uuid
from pydantic import BaseModel, Field
from datetime import datetime


class OrderItemIn(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(gt=0)
    price: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str
    items: list[OrderItemIn]


class OrderItemOut(OrderItemIn):
    id: uuid.UUID


class OrderRead(BaseModel):
    id: uuid.UUID
    customer_name: str
    customer_phone: str
    customer_address: str
    status: str
    created_at: datetime
    items: list[OrderItemOut]
