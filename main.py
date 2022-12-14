from fastapi import FastAPI
import models
from database import engine, get_db
from routers.books import book_router
from routers.user import user_router
from routers.auth import auth_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db()

app.include_router(user_router)
app.include_router(book_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Hello World"}


