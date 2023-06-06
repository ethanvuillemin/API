from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
import os
import crud
import models
import schemas
from database import SessionLocal, engine
import datetime

# Vérifier si le dossier Raport existe, sinon le créer
if not os.path.exists('Rapport'):
    os.makedirs('Rapport')

# Crée toutes les tables définies dans les modèles dans la base de données
models.Base.metadata.create_all(bind=engine)

# Crée une instance FastAPI
app = FastAPI()

# Configuration pour servir des fichiers statiques (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuration des templates Jinja2
templates = Jinja2Templates(directory="templates")

# Affiche le formulaire de création d'utilisateur   
@app.get("/")
def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

 
###############################################################
### Routes pour la création et l'affichage des utilisateurs ###
###############################################################

# Crée un nouvel utilisateur   
@app.post("/users/")
def create_user(username: str, email: str, password: str, db: Session = Depends(crud.get_db)):
    """
    Crée un nouvel utilisateur avec les informations fournies.

    Args:
        username (str): Nom d'utilisateur.
        email (str): Adresse e-mail de l'utilisateur.
        password (str): Mot de passe de l'utilisateur.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        schemas.User: Utilisateur créé.
    """
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, username=username, email=email, hashed_password=password)
 
# Affiche le formulaire de création d'utilisateur   
@app.get("/users/create")
def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

################################################################
### Routes pour la création et l'affichage du contenu de bar ### 
################################################################
 
# Crée un nouveau contenu de bar
@app.post("/bar/")   
def create_bar_variable(name: str, content: int, alcohol_type: str, alcohol_sub_category: str, db: Session = Depends(crud.get_db)):
    """
    Crée un nouveau contenu de bar avec les informations fournies. 

    Args:
        name (str): Nom du contenu de bar.
        content (float): Contenu du bar.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        schemas.InventaireBar: Contenu de bar créé.
    """
    return crud.create_bar(db=db, name=name, content=content, alcohol_type=alcohol_type, alcohol_sub_category=alcohol_sub_category)

# Met à jour une variable de contenu de bar 
@app.put("/bar/{name}", response_model=schemas.InventaireBar)
def update_bar_variable(name: str, content: float, db: Session = Depends(crud.get_db)):
    """
    Endpoint pour mettre à jour une variable du bar.

    Args:
        name (str): Nom de la variable.
        content (float): Nouvelle valeur de la variable.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        schemas.InventaireBar: Variable de bar mise à jour.
    """
    return crud.update_bar(name, content, db)

# Supprime une variable de contenu de bar
@app.delete("/bar/{name}")
def delete_bar_variable(name: str, db: Session = Depends(crud.get_db)):
    """
    Supprime une variable de contenu de bar.

    Args:
        name (str): Nom de la variable à supprimer.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        dict: Message de succès.
    """
    deleted_variable = crud.delete_bar_variable(db=db, name=name)
    if not deleted_variable:
        raise HTTPException(status_code=404, detail="Variable introuvable")

    return {"message": "Variable supprimée avec succès"}

# Affiche le contenu de bar
@app.get("/bar/", response_model=List[schemas.InventaireBar])
def display_bar(request: Request, db: Session = Depends(crud.get_db)):
    """
    Affiche tous les contenus de bar.

    Args:
        request (Request): Requête HTTP.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        templates.TemplateResponse: Réponse HTML contenant la liste des contenus de bar.
    """
    bar = crud.get_bar(db=db)
    return templates.TemplateResponse("read_all_bar.html", {"request": request, "bars": bar})

 
# Extraction des données sous forme de fichier Excel
@app.get("/bar/rapport_exel/")
def export_to_excel(request: Request, db: Session = Depends(crud.get_db)):
    """
    Exporte les données du bar vers un fichier Excel.

    Args:
        request (Request): Requête HTTP.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        FileResponse: Réponse HTTP avec le fichier Excel téléchargeable.
    """
    bar = crud.get_bar(db=db)
    
    # Extraire les données de chaque objet Inventairebar
    data = []
    for item in bar:
        data.append({
            "nom": item.name,
            "Contenu en unite": item.content,
            "Type": item.alcohol_type,
            "Sous-catégorie": item.alcohol_sub_category 
        })
    
    # Créer un DataFrame à partir des données extraites
    df = pd.DataFrame(data)
    
    # Obtenir la date du jour au format dd-mm-aaaa
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    
    # Enregistrer le DataFrame dans un fichier Excel avec le nom du fichier contenant la date  
    file_name = f'Rapport/Inventaire_Bar_{current_date}.xlsx'
    df.to_excel(file_name, index=False)
    
    # Retourner le fichier Excel en tant que réponse HTTP
    return FileResponse(file_name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)


##################################################################
### Routes pour la création et l'affichage du contenu du stock ###
##################################################################

# Ajoute une nouvelle référence au stock 
@app.post("/stock/") 
def create_stock_variable(name: str, content: int, alcohol_type: str, alcohol_sub_category: str, db: Session = Depends(crud.get_db)):
    """
    Ajoute une nouvelle référence au stock.

    Args:
        name (str): Nom de la référence.
        content (int): Contenu de la référence.
        alcohol_type (str): Type d'alcool de la référence.
        alcohol_sub_category (str): Sous-catégorie d'alcool de la référence.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        schemas.InventaireStock: Référence ajoutée au stock.
    """
    return crud.create_stock(db=db, name=name, content=content, alcohol_type=alcohol_type, alcohol_sub_category=alcohol_sub_category)

@app.put("/stock/{name}", response_model=schemas.InventaireStock)
def update_stock_variable(name: str, content: float, db: Session = Depends(crud.get_db)):
    """
    Endpoint pour mettre à jour une variable du bar.

    Args:
        name (str): Nom de la variable.
        content (float): Nouvelle valeur de la variable.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        schemas.InventaireBar: Variable de bar mise à jour.
    """
    return crud.update_stock(name, content, db)

# Supprime une variable dans le stock 
@app.delete("/stock/{name}")
def delete_stock_variable(name: str, db: Session = Depends(crud.get_db)):
    """
    Supprime une variable du stock.

    Args:
        name (str): Nom de la variable à supprimer.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        dict: Message de succès.
    """
    deleted_variable = crud.delete_stock_variable(db=db, name=name)
    if not deleted_variable:
        raise HTTPException(status_code=404, detail="Variable introuvable")  

    return {"message": "Variable supprimée avec succès"}


# Affiche le contenu du stock dans une page html
@app.get("/stock/", response_model=List[schemas.InventaireStock])
def display_stock(request: Request, db: Session = Depends(crud.get_db)):
    """
    Affiche le contenu du stock.

    Args:
        request (Request): Requête HTTP.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        templates.TemplateResponse: Réponse HTML contenant la liste du contenu du stock.
    """
    stock = crud.get_stock(db=db)
    return templates.TemplateResponse("read_all_stock.html", {"request": request, "stocks": stock})


# Extraction des données sous forme de fichier Excel
@app.get("/stock/rapport_exel/")
def export_to_excel(request: Request, db: Session = Depends(crud.get_db)):
    """
    Exporte les données du stock vers un fichier Excel.

    Args:
        request (Request): Requête HTTP.
        db (Session, optional): Session de base de données. Defaults to Depends(crud.get_db).

    Returns:
        FileResponse: Réponse HTTP avec le fichier Excel téléchargeable.
    """
    stock = crud.get_stock(db=db)
    
    # Extraire les données de chaque objet InventaireStock
    data = []
    for item in stock:
        data.append({
            "Nom": item.name,
            "Contenu": item.content,
            "Type": item.alcohol_type,
            "Sous-catégorie": item.alcohol_sub_category
        })
    
    # Créer un DataFrame à partir des données extraites
    df = pd.DataFrame(data)
    
    # Obtenir la date du jour au format dd-mm-aaaa
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    
    # Enregistrer le DataFrame dans un fichier Excel avec le nom du fichier contenant la date
    file_name = f'Rapport/Inventaire_Stock_{current_date}.xlsx'
    df.to_excel(file_name, index=False)
    
    # Retourner le fichier Excel en tant que réponse HTTP
    return FileResponse(file_name, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=file_name)




