from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

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
    return {"Data": db_posts}

@app.post("/createposts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,999999) 
    db_posts.append(post_dict)
    return {"data": post_dict}

def find_post(id):
    for p in db_posts:
        if p['id'] == id:
            return p
        
@app.get("/posts/{id}")
def get_post(id: int, responce: Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} not found")
        #responce.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with {id} not found"}
    return {"text": post}

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
