from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import Books
from schemas import Book

router = APIRouter()


@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(Books).all()
    return {"books": books}


@router.get("/books/{id}")
def say_hello(id: int, db: Session = Depends(get_db)):
    book = db.query(Books).filter(Books.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id {id} was not found.')
    return {"book": book}


@router.post('/books')
def create(book: Book, db: Session = Depends(get_db)):
    new_book = Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"book": new_book}


@router.delete('/books/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    deleted_book = db.query(Books).filter(Books.id == id)
    if deleted_book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deleted_book.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/books/{id}")
def update(id: int, book: Book, db: Session = Depends(get_db)):
    updated_query = db.query(Books).filter(Books.id == id)
    updated_book = updated_query.first()
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id: {id} does not exists.')
    updated_query.update(book.dict(), synchronize_session=False)
    db.commit()
    return {'data': updated_query.first()}