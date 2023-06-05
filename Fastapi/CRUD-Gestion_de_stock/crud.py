from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models, schemas, database

# Crée un objet CryptContext pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

# Fonction pour obtenir une instance de la base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally: 
        db.close()

################################################################
####################### Fonction USERS #########################
################################################################

def get_all_users(db: Session):
    """
    Obtient tous les utilisateurs de la base de données.
    Args:
        db (Session): Instance de la base de données.
    Returns:
        List[models.User]: Liste des utilisateurs.
    """
    return db.query(models.User).offset(0).limit(100).all()

def get_user_by_email(db: Session, email: str):
    """
    Obtient un utilisateur en fonction de son adresse e-mail.
    Args:
        db (Session): Instance de la base de données.
        email (str): Adresse e-mail de l'utilisateur.
    Returns:
        models.User: Utilisateur correspondant à l'adresse e-mail donnée.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_password_hash(password):
    """
    Retourne le hachage d'un mot de passe.
    Args:
        password (str): Mot de passe à hacher.
    Returns:
        str: Le hachage du mot de passe.
    """
    return pwd_context.hash(password)

def create_user(db: Session, username: str, email: str, hashed_password: str):
    """
    Crée un nouvel utilisateur.
    Args:
        db (Session): Instance de la base de données.
        username (str): Nom d'utilisateur du nouvel utilisateur.
        email (str): Adresse e-mail du nouvel utilisateur.
        hashed_password (str): Mot de passe haché du nouvel utilisateur.
    Returns:
        models.User: L'utilisateur créé.
    """
    db_user = models.User(username=username, email=email, hashed_password=get_password_hash(hashed_password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

################################################################
######################### Fonction BAR #########################
################################################################

def get_bar(db: Session):
    """
    Obtient tous les éléments du bar de la base de données.
    Args:
        db (Session): Instance de la base de données.
    Returns:
        List[models.InventaireBar]: Liste des éléments du bar.
    """
    return db.query(models.InventaireBar).offset(0).limit(100).all()

def create_bar(db: Session, name: str, content: float, alcohol_type: str, alcohol_sub_category: str):
    """
    Crée un nouvel élément du bar.
    Args:
        db (Session): Instance de la base de données.
        name (str): Nom de l'élément.
        content (float): Contenu de l'élément.
        alcohol_type (str): Type d'alcool de l'élément.
        alcohol_sub_category (str): Sous-catégorie d'alcool de l'élément.
    Returns:
        models.InventaireBar: L'élément du bar créé.
    """
    db_stock = models.InventaireBar(name=name, content=content, alcohol_type=alcohol_type, alcohol_sub_category=alcohol_sub_category)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def update_bar(name: str, content: float, db: Session):
    """
    Met à jour une variable du bar.

    Args:
        name (str): Nom de la variable.
        content (float): Nouvelle valeur de la variable.
        db (Session): Session de base de données.

    Returns:
        schemas.Inventairebar: Variable de bar mise à jour.
    """
    bar = get_bar(db=db)

    variable = next((var for var in bar if var.name == name), None)
    if not variable:
        return {"Error":"bad query"}

    variable.content = content
    db.commit()
    db.refresh(variable)
    return variable

def delete_bar_variable(db: Session, name: str):
    """
    Supprime un élément du bar en fonction de son nom.
    Args:
        db (Session): Instance de la base de données.
        name (str): Nom de l'élément à supprimer.
    Returns:
        bool: True si l'élément a été supprimé avec succès, False sinon.
    """
    variable = db.query(models.InventaireBar).filter(models.InventaireBar.name == name).first()
    if variable:
        db.delete(variable)
        db.commit()
        return True
    else:
        return False

################################################################
####################### Fonction STOCK #########################
################################################################

def get_stock(db: Session):
    """
    Obtient tous les éléments du stock de la base de données.
    Args:
        db (Session): Instance de la base de données.
    Returns:
        List[models.InventaireStock]: Liste des éléments du stock.
    """
    return db.query(models.InventaireStock).offset(0).limit(100).all()

def create_stock(db: Session, name: str, content: float, alcohol_type: str, alcohol_sub_category: str):
    """
    Crée un nouvel élément du stock.
    Args:
        db (Session): Instance de la base de données.
        name (str): Nom de l'élément.
        content (float): Contenu de l'élément.
        alcohol_type (str): Type d'alcool de l'élément.
        alcohol_sub_category (str): Sous-catégorie d'alcool de l'élément.
    Returns:
        models.InventaireStock: L'élément du stock créé.
    """
    db_stock = models.InventaireStock(name=name, content=content, alcohol_type=alcohol_type, alcohol_sub_category=alcohol_sub_category)
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def update_stock(name: str, content: float, db: Session):
    """
    Met à jour une variable du stock.

    Args:
        name (str): Nom de la variable.
        content (float): Nouvelle valeur de la variable.
        db (Session): Session de base de données.

    Returns:
        schemas.Inventairestock: Variable de stock mise à jour.
    """
    stock = get_stock(db=db)

    variable = next((var for var in stock if var.name == name), None)
    if not variable:
        return {"Error":"bad query"}

    variable.content = content
    db.commit()
    db.refresh(variable)
    return variable
    

def delete_stock_variable(db: Session, name: str):
    """
    Supprime un élément du stock en fonction de son nom.
    Args:
        db (Session): Instance de la base de données.
        name (str): Nom de l'élément à supprimer.
    Returns:
        bool: True si l'élément a été supprimé avec succès, False sinon.
    """
    variable = db.query(models.InventaireStock).filter(models.InventaireStock.name == name).first()
    if variable:
        db.delete(variable)
        db.commit()
        return True
    else:
        return False
