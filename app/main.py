from fastapi import FastAPI
from environs import Env
import models
from database import engine
import routers.post, routers.user , routers.auth, routers.vote



env = Env()
env.read_env()


"""
    Cours:
    Pour lancer serveur : uvicorn main:app
    avec reload (pas besoin de restart serveur à chaque modif): uvicorn main:app --reload

    A chaque changement il faut restart le serveur

    Attention dans le pathing, s'il est le même, par ex get("/") ou get("/posts"), cela renverra la premier référence au path
"""

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routers.post.router)
app.include_router(routers.user.router)    
app.include_router(routers.auth.router)
app.include_router(routers.vote.router)

@app.get("/") # "@" decorator, "get" fonction http, "/" donne le path ex: tu peux avoir "/login" ou "/posts/vote"
def root():
    return {f"message": "Welcome to my API ! Please take your shoes off..."}



