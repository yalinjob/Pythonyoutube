from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
from sqlalchemy.orm import Session

from random import randrange
import psycopg2
from app import models, schemas ,utils
 
from sqlalchemy.sql.functions import mode
from psycopg2.extras import RealDictCursor
import time
from app.database import Base, engine , get_db
from app.routers  import post, user ,auth


app = FastAPI()

Base.metadata.create_all(bind=engine)


      
while True:
  try: 
    conn = psycopg2.connect(host= 'localhost' , database='fastapi', user='postgres',password= 'HarTavor7!',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("DB is conneetction ")
    break
  except Exception as error :
     print ("Connetcion to DB Faild ")
     print ("Error", error)
     time.sleep(2)

my_posts =[{"title":"title of post1", "content": "content of post1", "id":1}, {"title":"titleof post2", "content": "content of post2", "id":2}]

    
def find_post(id): 
    for p in my_posts:
       if p['id'] == id:
           return p 


def find_index_post(id):
  for i , p in enumerate(my_posts):
    if p['id'] == id:
           return i 


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return{"message" :"hello World"}
