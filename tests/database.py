"""
    IS USELESS NOW BECAUSE OF THE CONFTEST.PY
"""


# from fastapi.testclient import TestClient
# from app.main import app
# import pytest

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from environs import Env
# from app.config import settings
# from app.database import get_db, Base

# """
# pytest -v -s -x tests\test_users.py --disable-warnings

# Permet de lancer les tests
# -v rajouter des détails
# -s affiche les print()
# -x s'arrête lorsqu'un test ne passe pas
# --disable-warnings enlever les warnings

# """


# env = Env()
# env.read_env()


# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture
# def client(session):

#     def override_get_db():

#         try:
#             yield session
#         finally:
#             session.close()
#     app.dependency_overrides[get_db] = override_get_db

#     yield TestClient(app)


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test' 
# # template : 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

# engine = create_engine(SQLALCHEMY_DATABASE_URL) # permet d'établir une connexion

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # créer une session
