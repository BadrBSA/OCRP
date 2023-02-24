from fastapi import FastAPI
from environs import Env
from app.database import engine
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from . import models


env = Env()
env.read_env()


"""
    Cours:
    Pour lancer serveur : uvicorn main:app
    avec reload (pas besoin de restart serveur à chaque modif): uvicorn main:app --reload or / uvicorn app.main:app --reload

    A chaque changement il faut restart le serveur

    Attention dans le pathing, s'il est le même, par ex get("/") ou get("/posts"), cela renverra la premier référence au path
"""

models.Base.metadata.create_all(bind=engine) #NO LONGER NEED IT SINCE WE'VE GOT ALEMBIC

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)    
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") # "@" decorator, "get" fonction http, "/" donne le path ex: tu peux avoir "/login" ou "/posts/vote"
def root():
    return {f"message": "Welcome to my API ! Please take your shoes off..."}



