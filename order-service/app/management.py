# ---------------------------------------------------------------------------
# функции «слой бизнес-логики»: создать / получить / обновить
# / удалить сущность. Отделяем чистый доступ к БД от роутов,
# чтобы логику было удобно тестировать и переиспользовать.
# ---------------------------------------------------------------------------

from sqlmodel import Session, select
from .models import Order, OrderItem
from .schemas import OrderCreate


def create_order(db: Session, dto: OrderCreate) -> Order:
    order = Order(
        customer_name=dto.customer_name,
        customer_phone=dto.customer_phone,
        customer_address=dto.customer_address,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    items = [
        OrderItem(
            order_id=order.id,
            product_id=i.product_id,
            quantity=i.quantity,
            price=i.price,
        )
        for i in dto.items
    ]
    db.add_all(items)
    db.commit()
    order.items = items
    return order


def get_order(db: Session, oid):
    return db.get(Order, oid)


def list_orders(db: Session):
    return db.exec(select(Order)).all()


def update_status(db: Session, oid, status: str):
    ord_ = db.get(Order, oid)
    if not ord_:
        return None
    ord_.status = status
    db.commit()
    return ord_
