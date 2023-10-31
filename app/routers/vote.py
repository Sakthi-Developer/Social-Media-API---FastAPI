from fastapi import HTTPException, FastAPI, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas,database, oauth2, models
router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} does not found")
    
    vote_qurey = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,
                                                        models.Votes.user_id == current_user.id) # type: ignore
    found_vote = vote_qurey.first()
    
    if(vote.dir == 1):

        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail= f"User {current_user.id} has already voted on post {vote.post_id}") # type: ignore
        
        new_vote = models.Votes(post_id=vote.post_id, user_id= current_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        return {"message": "Succesfully voted"}
   
    else:

        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        vote_qurey.delete(synchronize_session=False)
        db.commit()

        return {"message": "Succesfully deleted vote"}
    