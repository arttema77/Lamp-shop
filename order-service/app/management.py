# order-service/app/management.py
# ---------------------------------------------------------------------------
# слой бизнес-логики для сущности Order
# ---------------------------------------------------------------------------
from typing import Sequence
from sqlmodel import Session, select          # 🆕  <-- ЭТИХ строк не хватало

from . import models, schemas

Order       = models.Order
OrderItem   = models.OrderItem
OrderCreate = schemas.OrderCreate
OrderUpdate = schemas.OrderUpdate            # чтобы mypy / IDE «видели» тип

# ───────────────────── создание ──────────────────────────────────────────
def create_order(db: Session, dto: OrderCreate) -> Order:
    order = Order(
        customer_name   = dto.customer_name,
        customer_phone  = dto.customer_phone,
        customer_address= dto.customer_address,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # товары заказа
    items: Sequence[OrderItem] = [
        OrderItem(
            order_id   = order.id,
            product_id = i.product_id,
            quantity   = i.quantity,
            price      = i.price,
        )
        for i in dto.items
    ]
    db.add_all(items)
    db.commit()
    order.items = list(items)
    return order

# ───────────────────── чтение ────────────────────────────────────────────
def get_order(db: Session, oid: str) -> Order | None:
    return db.get(Order, oid)

def list_orders(db: Session) -> list[Order]:
    return db.exec(select(Order)).all()

# ───────────────────── частичное обновление ──────────────────────────────
def update_status(db: Session, oid: str, status: str) -> Order | None:
    ord_ = db.get(Order, oid)
    if not ord_:
        return None
    ord_.status = status
    db.commit()
    return ord_

def patch_order(db: Session, order_id: str, upd: OrderUpdate) -> Order | None:
    ord_ = db.get(Order, order_id)
    if not ord_:
        return None

    # только переданные поля
    data = upd.model_dump(exclude_unset=True)
    if "items" in data:
        ord_.items = [
            OrderItem(**i.model_dump(exclude_unset=True)) for i in upd.items
        ]

    for k, v in data.items():
        if k != "items":
            setattr(ord_, k, v)

    db.add(ord_)
    db.commit()
    db.refresh(ord_)
    return ord_
