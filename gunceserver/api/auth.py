from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from lib.oauth2 import (
    get_current_active_user,
    authenticate_user,
    create_access_token,
    oauth2_scheme,
)
from schemas.token import Token
from schemas.auth import LoginForm
from schemas.user import UserOut, UserInDB, UserCreate
from core.deps import get_db
import models


r = APIRouter(prefix="/api", tags=["Auth"])


@r.post(
    "/auth/register",
    response_model=UserOut,
    summary="Register new account",
    response_description="Register new account",
)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> dict:
    """
    Register new account
    """
    db_user = models.User(
        username=user.username,
        serverkey=user.serverkey,
        masterkey=user.masterkey,
        nonce=user.nonce,
        tag=user.tag,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@r.post("/auth/login", response_model=Token)
async def login(
    form_data: LoginForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    user = authenticate_user(db, form_data.username, form_data.serverkey)
    access_token = create_access_token(
        username=user.username, role=user.role, is_active=user.is_active
    )
    return {"access_token": access_token, "token_type": "bearer"}


# -------------------------------------------------------------------


@r.get(
    "/auth/token",
    response_model=Token,
    summary="Get auth token.",
    response_description="Get token and token type.",
)
async def auth(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Get auth token and token type.
    """
    return {"access_token": token, "token_type": "bearer"}


@r.get(
    "/auth/check",
    dependencies=[Depends(get_current_active_user)],
    summary="Check auth status",
    response_description="Check uath status",
)
async def check():
    """
    If token is still walid, reutn True, False otherwise.
    """
    return {"check": True}


@r.get(
    "/auth/me",
    response_model=UserOut,
    summary="Get logged in user information.",
    response_description="Logged in user.",
)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Get logged in user information.
    """
    return current_user


@r.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict:
    print(form_data, form_data.username, form_data.password)
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(
        username=user.username, role=user.role, is_active=user.is_active
    )
    return {"access_token": access_token, "token_type": "bearer"}
