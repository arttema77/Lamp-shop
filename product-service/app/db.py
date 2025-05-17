# ---------------------------------------------------------------------------
# инициализация соединения с Postgres и создание таблиц.
# Функция init_db() вызывается при старте контейнера, создавая таблицы,
# если их ещё нет.
# ---------------------------------------------------------------------------

import os
from sqlmodel import create_engine, SQLModel

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:lamp@localhost:5432/products",
)

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    from .models import Product  # noqa
    SQLModel.metadata.create_all(engine)
