from fastapi import FastAPI
import psycopg2, psycopg2.extras
from . import models
from .database import engine
from .routers import posts, users, auth, vote
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)     
app.include_router(vote.router)
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI root directory"}
