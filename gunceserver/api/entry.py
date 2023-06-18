from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

import lib.security as sec
from core.deps import get_db
import models
from schemas import EntryBase, EntryCreate, EntryUpdate, EntryOut, EntryInDB, UserInDB
from lib.oauth2 import get_current_active_user


r = APIRouter(tags=["Entry"])


@r.get("/entries", response_model=List[EntryOut])
async def entry_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    return (
        db.query(models.Entry)
        .filter(models.Entry.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@r.post("/entries", response_model=EntryOut, status_code=status.HTTP_201_CREATED)
async def save_entry(
    entry: EntryCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    db_entry = models.Entry(
        user_id=current_user.id,
        date=entry.date,
        title=entry.title,
        title_key_tag=entry.title_key_tag,
        title_key_nonce=entry.title_key_nonce,
        content=entry.content,
        content_key_tag=entry.content_key_tag,
        content_key_nonce=entry.content_key_nonce,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@r.get("/entries/{entry_id}", response_model=EntryOut)
async def entry_detail(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()

    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if entry is None:
        raise HTTPException(status_code=404, detail="User not found")
    return entry


@r.put("/entries/{entry_id}", response_model=EntryOut)
async def entry_update(
    entry_id: UUID,
    entry_update: EntryUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()

    if not entry:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if entry.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    db.query(models.Entry).filter(models.Entry.id == entry_id).update(
        entry_update.dict(exclude_unset=True)
    )
    db.commit()

    entry.__dict__.update(entry_update.dict(exclude_unset=True))
    return entry


@r.delete("/entries/{user_id}")
async def entry_delete(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    db.query(models.Entry).filter(
        models.Entry.id == user_id, models.Entry.user_id == current
    ).delete()
    db.commit()
