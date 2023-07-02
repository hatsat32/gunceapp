from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.deps import get_db
from core.exceptions import NOT_FOUND_EXCEPTION, UNAUTHORIZED_EXCEPTION
import models
from schemas import EntryCreate, EntryUpdate, EntryOut, UserInDB
from lib.oauth2 import get_current_active_user


r = APIRouter(
    prefix="/api",
    tags=["Entry"],
    dependencies=[Depends(get_current_active_user)],
)


@r.get(
    "/entries",
    response_model=List[EntryOut],
    status_code=status.HTTP_200_OK,
)
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


@r.post(
    "/entries",
    response_model=EntryOut,
    status_code=status.HTTP_201_CREATED,
)
async def entry_create(
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


@r.get(
    "/entries/{entry_id}",
    response_model=EntryOut,
    status_code=status.HTTP_200_OK,
)
async def entry_detail(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()

    if entry.user_id != current_user.id:
        raise UNAUTHORIZED_EXCEPTION

    if entry is None:
        raise NOT_FOUND_EXCEPTION
    return entry


@r.put(
    "/entries/{entry_id}",
    response_model=EntryOut,
    status_code=status.HTTP_200_OK,
)
async def entry_update(
    entry_id: UUID,
    entry_update: EntryUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()

    if not entry:
        raise NOT_FOUND_EXCEPTION

    if entry.user_id != current_user.id:
        raise UNAUTHORIZED_EXCEPTION

    db.query(models.Entry).filter(models.Entry.id == entry_id).update(
        entry_update.dict(exclude_unset=True)
    )
    db.commit()

    entry.__dict__.update(entry_update.dict(exclude_unset=True))
    return entry


@r.delete(
    "/entries/{entry_id}",
    status_code=status.HTTP_200_OK,
)
def entry_delete(
    entry_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    db.query(models.Entry).filter(
        models.Entry.id == entry_id, models.Entry.user_id == current_user.id
    ).delete()
    db.commit()
