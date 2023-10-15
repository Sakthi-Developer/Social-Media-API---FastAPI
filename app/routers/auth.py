from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(tags=['Authentication'])

@router.post('/auth',status_code= status.HTTP_200_OK)
def auth(UserCerdentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
    User = db.query(models.User).filter(models.User.email == UserCerdentials.username).first()

    if not User:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with {UserCerdentials.username} is not found.")

    if not utils.verify(UserCerdentials.password, User.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Invalid Password")
    
    # Create Token
    access_token = oauth2.create_access_token(data= {"User_id": User.id, "Username":User.email})
    #return TOken

    return{"token": "Token"}