from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

import lib.security as sec
from core.deps import get_db
import models
from schemas import UserCreate, UserOut, UserInDB
from lib.oauth2 import get_current_active_user


r = APIRouter(tags=["User"])


@r.get("/users", response_model=List[UserOut])
async def users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.User).offset(skip).limit(limit).all()


@r.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def save_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email)
    db_user.set_password(user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@r.get("/users/me", response_model=UserOut)
async def me(current_user: UserInDB = Depends(get_current_active_user)):
    return current_user


# @r.post("/users/me", response_model=UserOut)
# async def me_update(
#     user: UserUpdate,
#     current_user: UserInDB = Depends(get_current_active_user),
#     db: Session = Depends(get_db),
# ):
#     db.query(models.User).filter(models.User.id == current_user.id).update(
#         user.dict(exclude_unset=True)
#     )
#     db.commit()
#     current_user.copy(update=user.dict(exclude_unset=True))
#     return current_user


@r.post("/users/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def me_change_password(
    password,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db.query(models.User).filter(models.User.username == current_user.username).update(
        {"hashed_password": sec.get_password_hash(password=password)}
    )
    db.commit()


@r.get("/users/{user_id}", response_model=UserOut)
async def user_detail(user_id: UUID, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@r.delete("/users/{user_id}")
async def user_delete(user_id: UUID, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()


# @r.put("/users/{user_id}", response_model=UserOut)
# async def user_update(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)):
#     u = db.query(models.User).filter(models.User.id == user_id).first()
#     if not u:
#         raise HTTPException(status.HTTP_404_NOT_FOUND)

#     db.query(models.User).filter(models.User.id == user_id).update(
#         user.dict(exclude_unset=True)
#     )
#     db.commit()

#     u.__dict__.update(user.dict(exclude_unset=True))
#     return u


@r.post("/users/{user_id}/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def user_change_password(
    user_id: UUID,
    password: str = Body(...),
    password_repeat: str = Body(...),
    db: Session = Depends(get_db),
):
    if password != password_repeat:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Password does'nt match!"
        )

    db.query(models.User).filter(models.User.id == user_id).update(
        {"hashed_password": sec.get_password_hash(password=password)}
    )
    db.commit()
