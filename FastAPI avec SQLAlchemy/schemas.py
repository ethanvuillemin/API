from pydantic import BaseModel

class Token(BaseModel):
    """
    Modèle de données pour le jeton d'accès.

    Attributes:
    - `access_token`: Jeton d'accès.
    - `token_type`: Type de jeton.
    - `username`: Nom d'utilisateur (peut être None).
    """
    access_token: str
    token_type: str
    username: str or None = None
    
class User(BaseModel):
    """
    Modèle de données pour les utilisateurs.

    Attributes:
    - `username`: Nom d'utilisateur (peut être None).
    - `email`: Adresse e-mail (peut être None).
    - `hashed_password`: Mot de passe hashé.
    - `is_active`: Indicateur d'activation de l'utilisateur (peut être None).
    """
    username: str or None = None
    email: str or None = None
    hashed_password: str
    is_active: bool or None = None
    
    class Config:
        orm_mode = True
