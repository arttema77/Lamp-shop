# product-service/app/auth.py
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session as _Session

from .models import User, Session
from .schemas import LoginRequest, Token

SECRET_KEY = "CHANGE_ME"
ALGORITHM   = "HS256"
ACCESS_TTL  = timedelta(hours=2)

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2   = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + ACCESS_TTL
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest,
          session: Annotated[_Session, Depends(Session)]):
    user = session.query(User).filter_by(username=payload.username).first()
    if not user or not pwd_ctx.verify(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")

    access = create_access_token({"sub": user.id})
    return {"access_token": access, "token_type": "bearer"}


async def current_user(token: Annotated[str, Depends(oauth2)]) -> User:
    cred_exc = HTTPException(
        status_code=401,
        detail="invalid creds",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        if uid is None:
            raise cred_exc
    except JWTError:
        raise cred_exc

    with Session() as db:
        user = db.get(User, uid)
        if not user:
            raise cred_exc
        return user
