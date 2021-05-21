from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class JournalBase(BaseModel):
    pass


class JournalCreate(JournalBase):
    pass


class Journal(JournalBase):
    id: int
    items: List[Item] = []

    class Config:
        orm_mode = True
