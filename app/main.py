from typing import List
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/journals/", response_model=schemas.Journal)
def create_journal(journal: schemas.JournalCreate, db: Session = Depends(get_db)):
    if journal.date != -1 and len(str(journal.date)) != 8:
        raise HTTPException(status_code=400, detail="date must be in yyyymmdd format")

    if journal.date == -1:
        journal.date = datetime.today().strftime('%Y%m%d')

    db_journal = crud.get_journal(db, journal_id=journal.date)
    if db_journal:
        raise HTTPException(status_code=400, detail=f"Journal with date {journal.date} already registered")

    return crud.create_journal(db=db, journal=journal)


@app.get("/journals/", response_model=List[schemas.Journal])
def read_journals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    journals = crud.get_journals(db, skip=skip, limit=limit)
    return journals


@app.get("/journals/{journal_id}", response_model=schemas.Journal)
def read_journal(journal_id: int, db: Session = Depends(get_db)):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail=f"Journal with id {journal_id} not found")
    return db_journal


@app.delete("/journals/{journal_id}", response_model=schemas.Journal)
def delete_journal(journal_id: int, db: Session = Depends(get_db)):
    db_journal = crud.delete_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail=f"Journal with id {journal_id} not found")
    return db_journal


@app.post("/journals/{journal_id}/items/", response_model=schemas.Item)
def create_item_for_journal(
    journal_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if not db_journal:
        raise HTTPException(status_code=400, detail=f"Journal with id {journal_id} not registered")
    return crud.create_journal_item(db=db, item=item, journal_id=journal_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return db_item
