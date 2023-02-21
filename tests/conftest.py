from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

"""
pytest -v -s -x tests\test_users.py --disable-warnings

Permet de lancer les tests
-v rajouter des détails
-s affiche les print()
-x s'arrête lorsqu'un test ne passe pas
--disable-warnings enlever les warnings

"""

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test' 
# template : 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # permet d'établir une connexion

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # créer une session


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):

    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "badr_2@gmail.com","password": "1234"}
    res =client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user=res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {"email": "badr@gmail.com","password": "1234"}
    res =client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user=res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user,test_user2, session):
    posts_data = [{
        "title": "first title",
        "content" : "first content",
        "owner_id" : test_user['id']
    }, {
        "title": "second title",
        "content" : "second content",
        "owner_id" : test_user['id']
    }, {
        "title": "third title",
        "content" : "third content",
        "owner_id" : test_user['id']
    },
    {
        "title": "USER 2",
        "content" : "CONTENT USER2 ",
        "owner_id" : test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    #### REVIENS A FAIRE : ###
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="second title", content="second content", owner_id=test_user['id']),
    #                 models.Post(title="third title", content="third content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts