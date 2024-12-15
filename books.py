@app.post("/borrows/")
def create_borrow(borrow: BorrowCreate, db: Session = Depends(get_db)):
      book = db.query(Book).filter(Book.id == borrow.book_id).first()
      if book.available_copies <= 0:
          raise HTTPException(status_code=400, detail="Книга недоступна для выдачи.")
      # Уменьшение количества доступных экземпляров
      book.available_copies -= 1
      db.commit()
      return "Книга выдана."