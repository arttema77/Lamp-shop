# product-service/app/db.py
import uuid
from sqlmodel import SQLModel, create_engine

# ------------------- engine & session -------------------
DATABASE_URL = "postgresql+psycopg2://postgres:lamp@db:5432/postgres"
engine = create_engine(DATABASE_URL, echo=False)

# ------------------- init & seed ------------------------
def init_db() -> None:
    # 1) создаём структуру
    SQLModel.metadata.create_all(engine)

    # 2) наполняем начальными данными
    from . import seed
    seed.fill(engine)                     # >>> вставка 20 лампочек и admin
