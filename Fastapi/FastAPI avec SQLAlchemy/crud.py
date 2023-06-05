from sqlalchemy.orm import Session
import models, schemas
from jose import JWTError, jwt
from database import SessionLocal
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

SECRET_KEY = "7cd08eb826a57a352154e28841d77b2b9117d3ab6d8140c4f0e916558cf9453e"  # !!! .env !!!
ALGORITHM = "HS256"  # !!! .env !!!

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Dependency
def get_db():
    """
    Fonction de dépendance pour obtenir une session de base de données.
    La session est fermée automatiquement après utilisation.

    Returns:
    - `db`: Session de base de données.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: Session, user_id: int):
    """
    Récupère un utilisateur à partir de l'ID d'utilisateur.

    Arguments:
    - `db`: Session de base de données.
    - `user_id`: ID de l'utilisateur à récupérer.

    Returns:
    - Utilisateur correspondant à l'ID donné.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """
    Récupère un utilisateur à partir du nom d'utilisateur.

    Arguments:
    - `db`: Session de base de données.
    - `username`: Nom d'utilisateur de l'utilisateur à récupérer.

    Returns:
    - Utilisateur correspondant au nom d'utilisateur donné.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """
    Récupère un utilisateur à partir de l'adresse e-mail.

    Arguments:
    - `db`: Session de base de données.
    - `email`: Adresse e-mail de l'utilisateur à récupérer.

    Returns:
    - Utilisateur correspondant à l'adresse e-mail donnée.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère une liste d'utilisateurs.

    Arguments:
    - `db`: Session de base de données.
    - `skip`: Nombre d'utilisateurs à sauter (par défaut : 0).
    - `limit`: Nombre maximal d'utilisateurs à récupérer (par défaut : 100).

    Returns:
    - Liste des utilisateurs récupérés.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, username: str, email: str, hashed_password: str):
    """
    Crée un nouvel utilisateur.

    Arguments:
    - `db`: Session de base de données.
    - `username`: Nom d'utilisateur du nouvel utilisateur.
    - `email`: Adresse e-mail du nouvel utilisateur.
    - `hashed_password`: Mot de passe hashé du nouvel utilisateur.

    Returns:
    - Nouvel utilisateur créé.
    """
    db_user = models.User(username=username, email=email, hashed_password=get_password_hash(hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_password_hash(password):
    """
    Hash du mot de passe.

    Arguments:
    - `password`: Mot de passe à hasher.

    Returns:
    - Hash du mot de passe.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Vérifie si le mot de passe en clair correspond au mot de passe hashé.

    Arguments:
    - `plain_password`: Mot de passe en clair.
    - `hashed_password`: Mot de passe hashé à vérifier.

    Returns:
    - Booléen indiquant si le mot de passe correspond ou non.
    """
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    """
    Authentifie l'utilisateur en vérifiant les informations d'identification.

    Arguments:
    - `db`: Session de base de données.
    - `username`: Nom d'utilisateur ou adresse e-mail de l'utilisateur.
    - `password`: Mot de passe de l'utilisateur.

    Returns:
    - L'utilisateur authentifié ou False si les informations d'identification sont incorrectes.
    """
    email = get_user_by_email(db, username)
    if not email:
        email = get_user_by_username(db, username)

    if not email:
        return False

    if not verify_password(password, email.hashed_password):
        return False

    return email


def create_access_token(data: dict, expires_delta: timedelta or None = None):
    """
    Crée un jeton d'accès JWT.

    Arguments:
    - `data`: Données à encoder dans le jeton.
    - `expires_delta`: Délai d'expiration du jeton (par défaut : 1440 minutes).

    Returns:
    - Jeton d'accès JWT.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth_2_scheme)):
    """
    Fonction de dépendance pour obtenir l'utilisateur actuel à partir du jeton JWT présent dans la requête.

    Arguments:
    - `db`: Session de base de données (injectée automatiquement).
    - `token`: Jeton JWT d'accès (injecté automatiquement).

    Returns:
    - Utilisateur actuel.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    user = get_user_by_email(db, username)
    if user is None:
        user = get_user_by_username(db, username)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user


async def get_current_active_user(user: schemas.User = Depends(get_current_user)):
    """
    Fonction de dépendance pour obtenir l'utilisateur actuel actif.

    Arguments:
    - `user`: Utilisateur actuel (injecté automatiquement).

    Returns:
    - Utilisateur actuel actif.
    """
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return user
