from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(tags=['Authentication'])

@router.post('/auth')
def auth(UserCerdentials: schemas.UserAuth ,db: Session = Depends(get_db)):
    User = db.query(models.User).filter(models.User.email == UserCerdentials.email).first()

    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with {UserCerdentials.email} is not found.")

    if not utils.verify(UserCerdentials.password, User.password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"Invalid Password")
    
    # Create Token
    #return TOken

    return{"token": "Token"}