from fastapi import FastAPI
import models
from database import engine, get_db
from routers import books, user



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()

app.include_router(books.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


