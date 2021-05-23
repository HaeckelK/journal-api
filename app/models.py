from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class TimestampMixin(object):
    created_at = Column(DateTime, default=func.now())
    modified_at = Column(DateTime, default=func.now())
    source = Column(String)


class Journal(TimestampMixin, Base):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, index=True)

    items = relationship("Item", back_populates="owner")


class Item(TimestampMixin, Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("journals.id"))

    owner = relationship("Journal", back_populates="items")
