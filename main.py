from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='books', user='postgres',
#                                 password='@DJzdD3qu2^gd+*f53$Ts', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful.')
#         break
#     except ConnectionError as error:
#         print('Connecting to database failes', error)
#         time.sleep(2)


class Book(BaseModel):
    title: str
    author: str
    review: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Books).all()
    return {"books": books}


@app.get("/books/{id}")
def say_hello(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id {id} was not found.')
    return {"book": book}


@app.post('/books')
def create(book: Book, db: Session = Depends(get_db)):
    new_book = models.Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"book": new_book}


@app.delete('/books/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    deleted_book = db.query(models.Books).filter(models.Books.id == id)
    if deleted_book.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    deleted_book.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/books/{id}")
def update(id: int, book: Book, db: Session = Depends(get_db)):
    updated_query = db.query(models.Books).filter(models.Books.id == id)
    updated_book = updated_query.first()
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id: {id} does not exists.')
    updated_query.update(book.dict(), synchronize_session=False)
    db.commit()
    return {'data': updated_query.first()}