from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

"""
    EXPLICATION "DEPENDS" : "Depends" is a powerful feature of the FastAPI web framework that allows you to define dependencies for your API endpoints. 
    A dependency is a piece of code that needs to be executed before the main function of the endpoint can run.
"""

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
#va faire une requete sur la table user, va chercher la première occurence du "username" dans la table User
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    # return token

    return {"access_token": access_token, "token_type": "bearer"}