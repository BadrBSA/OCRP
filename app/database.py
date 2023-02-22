from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env
from app.config import settings

env = Env()
env.read_env()

def get_db(): # Fonction qui crée une connexion avec notre database
    #A mettre dans chaque requete qui ouvrira la session et la fermera 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' 
# template : 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # permet d'établir une connexion avec la postgres database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # créer une session qui permet de communiquer avec la database

Base = declarative_base() # tous les models qui permettent de créer des tables vont être extended from Base