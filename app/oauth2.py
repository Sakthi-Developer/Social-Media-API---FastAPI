from jose import JWTError, jwt
from datetime import datetime, timedelta
SCERET_KEY = "93b2c67de665c6c7d7d1c09e605038290cfbefb5f107e9904fd3a060e2871b5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 15

def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": exp})
    
    enc_jwt = jwt.encode(to_encode, SCERET_KEY, algorithm=ALGORITHM)
    return enc_jwt