from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

# Настройка базы данных
DATABASE_URL = "postgresql://username:password@localhost/dbname"  # Замените на ваши данные
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель данных
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Создание FastAPI приложения
app = FastAPI()

# Pydantic модель для валидации данных
class AuthorCreate(BaseModel):
    name: str

class AuthorRead(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Получение сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD операции

@app.post("/authors/", response_model=AuthorRead)
def create_author(author: AuthorCreate, db: Session = next(get_db())):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@app.get("/authors/{author_id}", response_model=AuthorRead)
def read_author(author_id: int, db: Session = next(get_db())):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.get("/authors/", response_model=list[AuthorRead])
def read_authors(skip: int = 0, limit: int = 10, db: Session = next(get_db())):
    authors = db.query(Author).offset(skip).limit(limit).all()
    return authors

@app.put("/authors/{author_id}", response_model=AuthorRead)
def update_author(author_id: int, author: AuthorCreate, db: Session = next(get_db())):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db_author.name = author.name
    db.commit()
    db.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = next(get_db())):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(db_author)
    db.commit()
    return {"detail": "Author deleted"}