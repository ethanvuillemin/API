from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    """
    Modèle de données pour les utilisateurs.

    Attributes:
    - `__tablename__`: Nom de la table dans la base de données.
    - `id`: Identifiant de l'utilisateur (clé primaire).
    - `username`: Nom d'utilisateur de l'utilisateur.
    - `email`: Adresse e-mail de l'utilisateur.
    - `hashed_password`: Mot de passe hashé de l'utilisateur.
    - `is_active`: Indicateur d'activation de l'utilisateur (par défaut : True).
    """
    __tablename__ = "utilisateurs"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
