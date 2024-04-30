
from typing import List

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session

from .. import models, schemas ,oauth2
from ..database import get_db

router = APIRouter(
    
     prefix="/posts" ,
     tags=['Posts']

)


@router.get("/" , response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db) , user_id : int = Depends(oauth2.get_current_user)):

    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()

    posts =db.query(models.Post).all()
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post :schemas.PostCreate, db:Session= Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):

    #cursor.execute(""" INSERT INTO posts (title ,content , published) VALUES(%s,%s,%s) RETURNING * """ , (post.title, post.content, post.published))

    #new_post = cursor.fetchone()
    #conn.commit()
    print(user_id)
    new_post= models.Post(owner_id=user_id.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}" ,response_model=schemas.Post)
def get_post(id: int , db:Session=Depends(get_db) , user_id : int = Depends(oauth2.get_current_user)):
  #cursor.execute(""" SELECT * from posts WHERE id =%s """ ,(str(id)))
 # test_post=cursor.fetchone()
  #print (test_post)
  #post = find_post(id)

  post= db.query(models.Post).filter(models.Post.id==id).first()
  print(post)

  if not post :

       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id {id} was nont found ')
       # response.status_code = status.HTTP_404_NOT_FOUND
       # return {"message ": f"post with id:{id} was not found "}
  return post 


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int, db:Session = Depends(get_db)):


    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """ , (str (id),))
   # delete_post= cursor.fetchone()
   # conn.commit()


   post= db.guery (models.Post).filter(models.Post.id==id)
   if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id } does not exist")

   if post.owner_id != oauth2.get_current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    

   post.delete(synchronize_session=False)
   db.commit()

@router.put("/{id}" )
def update_post(id:int ,update_post:schemas.PostCreate, db:Session = Depends(get_db)):

  #cursor.execute(""" UPDATE posts SET title = %s , content = %s , published = %s WHERE id =%s RETUENING *""", (post.title , post.content, post.published , str (id)))
  #updated_post= cursor.fetchone()
  #conn.commit()

  post_query = db.query(models.Post).filter(models.Post.id==id)
  post=post_query.first()


  if post ==None:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id } does not exist")
  

  post_query.update({'title':'Hey this is my update title', 'content':'this is my update content'},synchronize_session=False)
  db.commit()
  return post_query.first()
