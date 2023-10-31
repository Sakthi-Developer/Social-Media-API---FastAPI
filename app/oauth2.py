from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = settings.access_token_expire_minutes 

def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": exp})
    
    enc_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return enc_jwt

def verify_access_token(token: str, credentail_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        id: str = str(payload.get("User_id"))

        if id is None:
            raise credentail_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentail_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Fucked up credentails",
                                         headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentail_exception=credential_exception) # type: ignore
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user

