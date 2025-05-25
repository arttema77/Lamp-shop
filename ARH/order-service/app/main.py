# ---------------------------------------------------------------------------
# точка входа микросервиса.
# Поднимает FastAPI-приложение, подключает маршруты и инициализирует БД.
# Запускается командой: uvicorn app.main:app --host 0.0.0.0 --port 80
# ---------------------------------------------------------------------------

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from . import db, management as mgmt, schemas

db.init_db()
app = FastAPI(title="Order Service")


def get_session():
    with Session(db.engine) as s:
        yield s


@app.post("/orders", response_model=schemas.OrderRead, status_code=201)
def new_order(order: schemas.OrderCreate, session: Session = Depends(get_session)):
    return mgmt.create_order(session, order)


@app.get("/orders/{oid}", response_model=schemas.OrderRead)
def get_order(oid, session: Session = Depends(get_session)):
    ord_ = mgmt.get_order(session, oid)
    if not ord_:
        raise HTTPException(404, "Order not found")
    return ord_


@app.get("/orders", response_model=list[schemas.OrderRead])
def all_orders(session: Session = Depends(get_session)):
    return mgmt.list_orders(session)


@app.patch("/orders/{oid}", response_model=schemas.OrderRead)
def set_status(
    oid, status: str, session: Session = Depends(get_session)
):
    ord_ = mgmt.update_status(session, oid, status)
    if not ord_:
        raise HTTPException(404, "Order not found")
    return ord_
