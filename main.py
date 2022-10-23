from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='books', user='postgres',
                                password='@DJzdD3qu2^gd+*f53$Ts', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful.')
        break
    except ConnectionError as error:
        print('Connecting to database failes', error)
        time.sleep(2)


class Book(BaseModel):
    title: str
    author: str
    review: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/books")
def get_books():
    cursor.execute("""SELECT * FROM books""")
    books = cursor.fetchall()
    return {"books": books}


@app.get("/books/{id}")
def say_hello(id: int):
    cursor.execute("""SELECT * FROM books WHERE id = %s""", (str(id)))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id {id} was not found.')
    return {"book": book}


@app.post('/books')
def create(book: Book):
    cursor.execute("""INSERT INTO books (title, author, review, published) VALUES (%s, %s, %s, %s) RETURNING *""",
                   (book.title, book.author, book.review, book.published))
    new_book = cursor.fetchall()
    conn.commit()
    return {"book": new_book}


@app.delete('/books/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    cursor.execute("""DELETE FROM books WHERE id = %s RETURNING *""", (str(id),))
    deleted_book = cursor.fetchone()
    conn.commit()
    if deleted_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/books/{id}")
def update(id: int, book: Book):
    cursor.execute("""UPDATE books SET title = %s, author = %s, review = %s WHERE id = %s RETURNING *""",
                   (book.title, book.author, book.review, str(id)))

    updated_book = cursor.fetchone()
    conn.commit()
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id: {id} does not exists.')
    return {'data': updated_book}
