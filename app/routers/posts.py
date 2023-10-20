from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas,oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

@router.get("/post",response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/post/{id}", response_model=schemas.Post)
def get_post(id: int, responce: Response, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #fecth_post = cursor.fetchone()
   
    fecth_post = db.query(models.Post).filter(models.Post.id == id).first()
    # post = find_post(int(id))
    if not fecth_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
    return fecth_post

@router.delete("/delete/{id}", response_model=schemas.Post)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s """,((id),))
    # connection.commit()
    
    delete_query = db.query(models.Post).filter(models.Post.id == id)
    post = delete_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"ID {id} dose not exist")
    
    if post.id != current_user.id:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Not Authorized to perfom request action")
    

    delete_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/update/{id}',response_model=schemas.UpdatePost)
def patch_update(id: int, post:schemas.UpdatePost, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)),)
    # updated_posts = cursor.fetchone()
    # connection.commit()
    
    update_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = update_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with {id} not found")
    update_query.update(post.dict(),synchronize_session=False) # type: ignore
    db.commit()
    
    return update_query.first()
