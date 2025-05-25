# ---------------------------------------------------------------------------
# функции «слой бизнес-логики»: создать / получить / обновить
# / удалить сущность. Отделяем чистый доступ к БД от роутов,
# чтобы логику было удобно тестировать и переиспользовать.
# ---------------------------------------------------------------------------

from sqlmodel import Session, select
from .models import Product


# ---------- READ ----------
def get_products(db: Session) -> list[Product]:
    return db.exec(select(Product)).all()


def get_product(db: Session, pid):
    return db.get(Product, pid)


# ---------- CREATE ----------
def create_product(db: Session, dto) -> Product:
    prod = Product(**dto.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod


# ---------- UPDATE ----------
def update_product(db: Session, pid, dto):
    prod = db.get(Product, pid)
    if not prod:
        return None
    for key, value in dto.model_dump(exclude_unset=True).items():
        setattr(prod, key, value)
    db.commit()
    db.refresh(prod)
    return prod


# ---------- DELETE ----------
def delete_product(db: Session, pid) -> bool:
    prod = db.get(Product, pid)
    if not prod:
        return False
    db.delete(prod)
    db.commit()
    return True
