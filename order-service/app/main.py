# order-service/app/main.py
# ────────────────────────────────────────────────────────────────
# Запуск: uvicorn app.main:app --host 0.0.0.0 --port 80
# ────────────────────────────────────────────────────────────────
from typing import Literal
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from . import db, schemas
from . import management as mgmt          # ← импорт под тем же alias’ом, что в коде

# ───────── Init DB ──────────────────────────────────────────────
db.init_db()
# ────────────────────────────────────────────────────────────────

app = FastAPI(title="Order Service", version="1.0")

# ───────── CORS ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",   # витрина
        "http://localhost:8003",   # админ-панель
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
# ────────────────────────────────────────────────────────────────

def get_session():
    with Session(db.engine) as session:
        yield session

# ───────── Endpoints ───────────────────────────────────────────

# создать заказ (витрина)
@app.post("/orders", response_model=schemas.OrderRead,
          status_code=status.HTTP_201_CREATED, tags=["orders"])
def create(order: schemas.OrderCreate, session: Session = Depends(get_session)):
    return mgmt.create_order(session, order)

# получить все заказы (админ)
@app.get("/orders", response_model=list[schemas.OrderRead], tags=["orders"])
def read_all(session: Session = Depends(get_session)):
    return mgmt.list_orders(session)

# получить один заказ
@app.get("/orders/{oid}", response_model=schemas.OrderRead, tags=["orders"])
def read_one(oid: str, session: Session = Depends(get_session)):
    ord_ = mgmt.get_order(session, oid)
    if not ord_:
        raise HTTPException(404, "Order not found")
    return ord_

# сменить статус (быстрое действие из выпадашки)
@app.patch("/orders/{oid}/status", response_model=schemas.OrderRead, tags=["orders"])
def change_status(
    oid: str,
    status: Literal["new", "paid", "shipped", "done"],
    session: Session = Depends(get_session),
):
    ord_ = mgmt.update_status(session, oid, status)
    if not ord_:
        raise HTTPException(404, "Order not found")
    return ord_

# гибкое PATCH-редактирование (карандаш)
@app.patch("/orders/{oid}", response_model=schemas.OrderRead, tags=["orders"])
def patch_order(
    oid: str,
    data: schemas.OrderUpdate,
    session: Session = Depends(get_session),
):
    ord_ = mgmt.patch_order(session, oid, data)
    if not ord_:
        raise HTTPException(404, "Order not found")
    return ord_
# ────────────────────────────────────────────────────────────────
