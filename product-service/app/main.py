# product-service/app/main.py
# ─────────────────────────────────────────────────────────────────────────────
# Запуск:  uvicorn app.main:app --host 0.0.0.0 --port 80
# ─────────────────────────────────────────────────────────────────────────────

import uuid
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from . import db, schemas
from .auth       import router as auth_router, current_user          # JWT
from .management import (                                           # CRUD-helpers
    get_products, get_product, create_product,
    update_product, delete_product,
)

# ───────── FASTAPI-приложение ────────────────────────────────────────────────
app = FastAPI(title="Product Service", version="1.0")

# CORS для витрины и админ-панели
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",   # storefront
        "http://localhost:8003",   # admin panel
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────── Инициализация БД при старте контейнера ────────────────────────────
@app.on_event("startup")
def on_startup() -> None:
    db.init_db()          # создаём таблицы
    import app.seed       # наполняем демо-данными / admin:admin123


# ───────── Dependency для сессии ─────────────────────────────────────────────
def get_session():
    with Session(db.engine) as session:
        yield session


# ───────── Роуты ─────────────────────────────────────────────────────────────
# 1) аутентификация
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# 2) продукты
@app.get("/products", response_model=list[schemas.ProductRead], tags=["products"])
def list_products(session: Session = Depends(get_session)):
    """Получить все товары (публично)."""
    return get_products(session)


@app.get("/products/{pid}", response_model=schemas.ProductRead, tags=["products"])
def read_product(pid: uuid.UUID, session: Session = Depends(get_session)):
    """Получить товар по ID (публично)."""
    prod = get_product(session, pid)
    if not prod:
        raise HTTPException(404, "Product not found")
    return prod


@app.post(
    "/products",
    response_model=schemas.ProductRead,
    status_code=status.HTTP_201_CREATED,
    tags=["products"],
)
def create_product_endpoint(
    data: schemas.ProductCreate,
    session: Session = Depends(get_session),
    _=Depends(current_user),          # 🔐 требуется JWT
):
    """Создать товар (admin)."""
    return create_product(session, data)


@app.put("/products/{pid}", response_model=schemas.ProductRead, tags=["products"])
def update_product_endpoint(
    pid: uuid.UUID,
    data: schemas.ProductCreate,
    session: Session = Depends(get_session),
    _=Depends(current_user),          # 🔐
):
    """Изменить товар (admin)."""
    prod = update_product(session, pid, data)
    if not prod:
        raise HTTPException(404, "Product not found")
    return prod


@app.delete("/products/{pid}", status_code=204, tags=["products"])
def delete_product_endpoint(
    pid: uuid.UUID,
    session: Session = Depends(get_session),
    _=Depends(current_user),          # 🔐
):
    """Удалить товар (admin)."""
    if not delete_product(session, pid):
        raise HTTPException(404, "Product not found")
