from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
import psycopg2, psycopg2.extras
import time 
from typing import Optional, List
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        connection = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '197300',cursor_factory=psycopg2.extras.RealDictCursor)
        cursor = connection.cursor()
        print("Succesfully connected to the Database")
        break

    except Exception as error:

        print("Truble Connecting to the Database")
        print(error)
        time.sleep(3)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI root directory"}

