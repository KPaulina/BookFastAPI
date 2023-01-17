from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
import oauth2
from database import get_db
from models import Books
from schemas import Book

book_router = APIRouter(
    prefix='/books',
    tags=['Books']
)


@book_router.get("/")
def get_books(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    books = db.query(Books).all()
    return {"books": books}


@book_router.get("/{id}")
def say_hello(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(Books).filter(Books.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id {id} was not found.')
    return {"book": book}


@book_router.post('/')
def create(book: Book, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    new_book = Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"book": new_book}


@book_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_book = db.query(Books).filter(Books.id == id)
    if deleted_book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deleted_book.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@book_router.put("/{id}")
def update(id: int, book: Book, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    updated_query = db.query(Books).filter(Books.id == id)
    updated_book = updated_query.first()
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id: {id} does not exists.')
    updated_query.update(book.dict(), synchronize_session=False)
    db.commit()
    return {'data': updated_query.first()}
