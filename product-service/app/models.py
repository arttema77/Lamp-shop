# product-service/app/models.py
import uuid
from uuid import uuid4
from sqlmodel import SQLModel, Field, create_engine, Session as _Session
from passlib.context import CryptContext

# ---------- конфигурация ----------
DATABASE_URL = "postgresql+psycopg2://postgres:lamp@db:5432/postgres"
pwd_ctx      = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- таблицы ----------
class User(SQLModel, table=True):
    __tablename__ = "users"
    id       : str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    username : str = Field(index=True, unique=True)
    password : str                                 # уже захэшированная строка


class Product(SQLModel, table=True):
    id          : uuid.UUID | None = Field(default_factory=uuid.uuid4,
                                           primary_key=True, index=True)
    name        : str
    description : str | None = None
    price       : int = 0
    quantity    : int = 0
    image_url   : str | None = None

# ---------- инициализация БД ----------
engine  = create_engine(DATABASE_URL, echo=False)
Session = lambda: _Session(engine)                 # «короткая» фабрика

def init_db() -> None:
    """Создать таблицы и посадить пользователя admin/admin123 при первом старте"""
    SQLModel.metadata.create_all(engine)
    with Session() as db:
        if not db.query(User).first():
            db.add(User(username="admin",
                        password=pwd_ctx.hash("admin123")))
            db.commit()
