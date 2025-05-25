# ---------------------------------------------------------------------------
# точка входа микросервиса.
# Поднимает FastAPI-приложение, подключает маршруты и инициализирует БД.
# Запускается командой: uvicorn app.main:app --host 0.0.0.0 --port 80
# ---------------------------------------------------------------------------

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from . import db, management as mgmt, schemas

db.init_db()
app = FastAPI(title="Product Service")


def get_session():
    with Session(db.engine) as session:
        yield session


@app.get("/products", response_model=list[schemas.ProductRead])
def list_products(session: Session = Depends(get_session)):
    return mgmt.get_products(session)


@app.get("/products/{pid}", response_model=schemas.ProductRead)
def get_product(pid, session: Session = Depends(get_session)):
    prod = mgmt.get_product(session, pid)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod


@app.post(
    "/products", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED
)
def add_product(
    data: schemas.ProductCreate, session: Session = Depends(get_session)
):
    return mgmt.create_product(session, data)


@app.put("/products/{pid}", response_model=schemas.ProductRead)
def edit_product(
    pid, data: schemas.ProductCreate, session: Session = Depends(get_session)
):
    prod = mgmt.update_product(session, pid, data)
    if not prod:
        raise HTTPException(404, "Product not found")
    return prod


@app.delete("/products/{pid}", status_code=204)
def remove_product(pid, session: Session = Depends(get_session)):
    if not mgmt.delete_product(session, pid):
        raise HTTPException(404, "Product not found")
