from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from environs import Env
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session

env = Env()
env.read_env()

DATABASE_PSSWRD = env.str("DATABASE_PASSWORD")

"""
    Cours:
    Pour lancer serveur : uvicorn main:app
    avec reload (pas besoin de restart serveur à chaque modif): uvicorn main:app --reload

    A chaque changement il faut restart le serveur

    Attention dans le pathing, s'il est le même, par ex get("/") ou get("/posts"), cela renverra la premier référence au path
"""
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # permets de mettre le default à -> TRUE
    # rating: Optional[int] = None # cette ligne est optionale grace à "Option[int]"
# La class permet d'avoir une struct sur les requetes générées, les requetes doivent suivrent cette struct ou -> error 

while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password=DATABASE_PSSWRD, cursor_factory=RealDictCursor)
    # cursor_factory=Realdictcursor -> returns dict format
        cursor = conn.cursor()
    #cursor va permettre d'utiliser des cmd SQL
        print("Database connection was successfull !")
        break
    except Exception as e:
        print("Connection to Database failed")
        print("Error:", e)
        time.sleep(2)
    
my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/") # "@" decorator, "get" fonction http, "/" donne le path ex: tu peux avoir "/login" ou "/posts/vote"
def root():
    return {f"message": "Welcome to my API ! Please take your shoes off..."}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "successfull"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # prends Body, sous forme de dict puis le stock dans payLoad
    # print(post)
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 10000000)
    # my_posts.append(post_dict)

    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))

    # NE PAS FAIRE cursor.execute(f"INSERT INTO posts (...), VALUES({post.title},...)") car lorsqu'un user rentre un titre, il pourrait potentiellement rentrer
    # une cmd SQL par ex: title = INSERT INTO posts ...., c'est un protection

    new_post = cursor.fetchone()

    conn.commit() #permet d'enregistrer les changes

    return {"data": new_post}



# @app.get("/posts/latest") # attention cas "/posts/latest", pour une requete /posts/latest, cela va prendre en compte "/posts/{id}" car il ne sait pas que "id" ne peut pas être un str 
# def get_latest_post(): # THATS WHY ORDER MATTERS
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int): #Attention au type de "id", il se peut que l'id soit un str (même si c'est 2, ca peut être "2") donc caster avec (int(id))
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) #l'id doit être un str ici /// Autre problm -> "," après "id" permets de régler certaines probl (pas d'explications)
    test_post = cursor.fetchone()
    print(test_post)
    # post = find_post(id) 
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f"post with id: {id} was not found")
    ### Autre manière :
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
        
    return{"post_detail": test_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # index = find_index_post(id)

    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    # my_posts.pop(index)

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    # index = find_index_post(id)

    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"message": updated_post}