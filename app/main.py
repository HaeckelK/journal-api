from typing import List

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
    return crud.create_journal(db=db, journal=journal)


@app.get("/journals/", response_model=List[schemas.Journal])
def read_journals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    journals = crud.get_journals(db, skip=skip, limit=limit)
    return journals


@app.get("/journals/{journal_id}", response_model=schemas.Journal)
def read_journal(journal_id: int, db: Session = Depends(get_db)):
    db_journal = crud.get_journal(db, journal_id=journal_id)
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    return db_journal


@app.post("/journals/{journal_id}/items/", response_model=schemas.Item)
def create_item_for_journal(
    journal_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_journal_item(db=db, item=item, journal_id=journal_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
