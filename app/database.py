from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env
from app.config import settings

env = Env()
env.read_env()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
DATABASE_PSSWRD = env.str("DATABASE_PASSWORD")

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' # template : 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # permet d'établir une connexion

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # créer une session

Base = declarative_base()