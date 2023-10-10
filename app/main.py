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
  
db_posts = [{"id": 1, "title": "Best food in KFC", "content": "Burer, Chiken fry, Cocacola","published": True,"rating": 4.5},
             {"id": 2, "title": "Fruit that good for heart", "content": "bananas, oranges, grapes","published": True,"rating": 4.5}]

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI root directory"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"Data": posts}

@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts (title,content,published,rating) VALUES(%s,%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published,post.rating))
    new_crted_post = cursor.fetchone()
    connection.commit()

    return {"data": new_crted_post}

def find_post(id):
    for p in db_posts:
        if p['id'] == id:
            return p
        
@app.get("/posts/{id}")
def get_post(id: int, responce: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    fecth_post = cursor.fetchone()
    
    # post = find_post(int(id))
    if not fecth_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
        responce.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with {id} not found"}
    return {"text": fecth_post}

def find_index(id):
    for index, p in enumerate(db_posts):
        if p['id'] == id:
            return index

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID {id} dose not exist")
    db_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def patch_update(id: int, post: Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'ID {id} dose not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    db_posts[index] = post_dict
    return {'data': post_dict}
