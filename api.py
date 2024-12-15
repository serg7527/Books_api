from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

@app.post("/authors/")
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
      db_author = Author(author.dict())
      db.add(db_author)
      db.commit()
      db.refresh(db_author)
      return db_author

@app.get("/authors/")
def get_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
      authors = db.query(Author).offset(skip).limit(limit).all()
      return authors

  # Другие эндпоинты аналогично...