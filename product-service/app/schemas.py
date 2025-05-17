# ---------------------------------------------------------------------------
# Pydantic-схемы для валидации входных / выходных данных API.
# Эти объекты не сохраняются в БД напрямую, а лишь гарантируют,
# что JSON-payload соответствует ожидаемой структуре.
# ---------------------------------------------------------------------------

import uuid
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: int = Field(gt=0)
    quantity: int = Field(ge=0)
    image_url: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: uuid.UUID
