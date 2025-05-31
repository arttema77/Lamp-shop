# product-service/app/schemas.py
# Pydantic-схемы: обеспечивают валидацию входящих / исходящих JSON-данных,
# не зависят от ORM-моделей SQLModel.

import uuid
from pydantic import BaseModel, Field

# ---------- Product ----------
class ProductBase(BaseModel):
    name        : str
    description : str | None = None
    price       : int = Field(gt=0)
    quantity    : int = Field(ge=0)
    image_url   : str | None = None

class ProductCreate(ProductBase):
    """Тело POST /products"""
    pass

class ProductRead(ProductBase):
    """Ответ на GET-запросы"""
    id: uuid.UUID

# ---------- Аутентификация ----------
class Token(BaseModel):
    access_token: str
    token_type  : str = "bearer"

class TokenData(BaseModel):
    username: str | None = None          # содержимое payload’a JWT

class LoginForm(BaseModel):
    username: str
    password: str
    
class LoginRequest(BaseModel):
    username: str
    password: str
