from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserOut
from passlib.context import CryptContext


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #hash password
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/users/{id}', response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user
