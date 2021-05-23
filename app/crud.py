from sqlalchemy.orm import Session

from . import models, schemas


def get_journal(db: Session, journal_id: int):
    return db.query(models.Journal).filter(models.Journal.id == journal_id).first()


def get_journals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Journal).offset(skip).limit(limit).all()


def create_journal(db: Session, journal: schemas.JournalCreate):
    db_journal = models.Journal()
    if journal.date != -1:
        db_journal.id = journal.date
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_journal_item(db: Session, item: schemas.ItemCreate, journal_id: int):
    db_item = models.Item(**item.dict(), owner_id=journal_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
