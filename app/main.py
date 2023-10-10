from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2, psycopg2.extras
import time 

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

class Post(BaseModel):
    title: str
    content: str
    published: bool
    rating: float

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI root directory"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"Data": posts}

@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published,rating) VALUES(%s,%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published,post.rating))
    new_crted_post = cursor.fetchone()
    connection.commit()

    return {"data": new_crted_post}

@app.get("/posts/{id}")
def get_post(id: int, responce: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    fecth_post = cursor.fetchone()
    
    # post = find_post(int(id))
    if not fecth_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
    return {"text": fecth_post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s """,((id),))
    connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID {id} dose not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def patch_update(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s, rating=%s  WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, post.rating, str(id)),)
    updated_posts = cursor.fetchone()
    connection.commit()
    if not updated_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
    return {'data': updated_posts}
