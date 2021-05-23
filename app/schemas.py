from typing import List, Optional
import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True


class JournalBase(BaseModel):
    pass


class JournalCreate(JournalBase):
    date: Optional[int] = -1


class Journal(JournalBase):
    id: int
    items: List[Item] = []
    created_at: datetime.datetime
    modified_at: datetime.datetime

    class Config:
        orm_mode = True
