from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import database as database
import models as models
import utils as utils
import schemas as schemas

auth_router = APIRouter(tags=['Authentication'])


@auth_router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Ceredentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    return {"token": 'example_token'}
