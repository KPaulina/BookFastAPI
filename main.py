from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
import models
import schemas
from database import engine, get_db
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()


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
def create(book: schemas.Book, db: Session = Depends(get_db)):
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
def update(id: int, book: schemas.Book, db: Session = Depends(get_db)):
    updated_query = db.query(models.Books).filter(models.Books.id == id)
    updated_book = updated_query.first()
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'book with id: {id} does not exists.')
    updated_query.update(book.dict(), synchronize_session=False)
    db.commit()
    return {'data': updated_query.first()}


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user
