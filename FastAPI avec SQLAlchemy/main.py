from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, Form
from sqlalchemy.orm import Session
import os
from datetime import datetime, timedelta
import crud, models, schemas
from database import SessionLocal, engine
from crud import *
from schemas import *

# Creation des Tables du fichier models
models.Base.metadata.create_all(bind=engine)

######################## A mettre dans un fichier .env #############################
SECRET_KEY = "7cd08eb826a57a352154e28841d77b2b9117d3ab6d8140c4f0e916558cf9453e"    #
ALGORITHM = "HS256"                                                                #
ACCESS_TOKEN_EXPIRE_MINUTES = 1440                                                 #
####################################################################################

app = FastAPI()

@app.post('/login', response_model=Token)
async def create_token_with_username_or_email(db: Session = Depends(get_db), from_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint pour créer un jeton d'accès en utilisant un nom d'utilisateur ou un e-mail.

    Arguments:
    - `db`: Session de la base de données (injectée automatiquement).
    - `from_data`: Formulaire de requête OAuth2PasswordRequestForm (injecté automatiquement).
    """
    user = authenticate_user(db, from_data.username, from_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": from_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(username: str, email: str, hashed_password: str, db: Session = Depends(get_db)):
    """
    Endpoint pour créer un nouvel utilisateur.

    Arguments:
    - `username`: Nom d'utilisateur.
    - `email`: Adresse e-mail de l'utilisateur.
    - `hashed_password`: Mot de passe hashé de l'utilisateur.
    - `db`: Session de la base de données (injectée automatiquement).
    """
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, username=username, email=email, hashed_password=hashed_password)

@app.get("/user/me/", response_model=schemas.User)
async def about_me(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint pour récupérer les informations sur l'utilisateur actuel.

    Arguments:
    - `current_user`: Utilisateur actuel (injecté automatiquement).

    Returns:
    - `current_user`: Utilisateur actuel.
    """
    return current_user

