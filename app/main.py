from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
import sqlalchemy
from typing import Optional
from random import randrange
import psycopg2, psycopg2.extras
import time 
from typing import Optional, List
from . import models, schemas
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

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

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI root directory"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts",response_model=list[schemas.post])
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@app.post("/createposts",status_code=status.HTTP_201_CREATED,response_model= schemas.post)
def create_posts(post:schemas.CreatePost, db: Session =Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published,rating) VALUES(%s,%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published,post.rating))
    # new_crted_post = cursor.fetchone()
    # connection.commit()
    #new_posts = models.Post(title = post.title, content = post.content, published = post.published)
   
    new_posts = models.Post(**post.dict())   # **post.dict() Automaticaly unpack the values from the dictionary
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts

@app.get("/posts/{id}", response_model=schemas.post)
def get_post(id: int, responce: Response, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #fecth_post = cursor.fetchone()
   
    fecth_post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = find_post(int(id))
    if not fecth_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
    return fecth_post

@app.delete("/posts/{id}", response_model=schemas.post)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s """,((id),))
    # connection.commit()
    
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if delete_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID {id} dose not exist")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=schemas.post)
def patch_update(id: int, post:schemas.UpdatePost, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)),)
    # updated_posts = cursor.fetchone()
    # connection.commit()
    
    update_query = db.query(models.Post).where(models.Post.id == id)
    update_post = update_query.first()

    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
    
    update_query.update(post.dict(),synchronize_session=False) # type: ignore
    db.commit()
    
    return update_query.first()

@app.post('/users', status_code= status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user.dict())
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user