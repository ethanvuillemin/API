# FastAPI avec SQLAlchemy

Ce projet est un exemple de configuration d'une application FastAPI avec l'utilisation de SQLAlchemy pour la gestion de la base de données. (Il est également compatible avec la génération de la documentation automatique avec Sphinx Autodoc).

## Structure des fichiers

- `main.py`: Fichier principal de l'application FastAPI.
- `database.py`: Configuration de la base de données SQLAlchemy.
- `crud.py`: Opérations CRUD (Create, Read, Update, Delete) pour la gestion des utilisateurs.
- `models.py`: Définition des modèles de données SQLAlchemy.
- `schemas.py`: Définition des schémas Pydantic pour la validation des données.
- `README.md`: Ce fichier.

## Fonctionnalités principales

- Création et gestion des utilisateurs :
    - Création d'un nouvel utilisateur avec un nom d'utilisateur, une adresse e-mail et un mot de passe.
    - Vérification de l'existence d'un utilisateur avec une adresse e-mail ou un nom d'utilisateur.
- Authentification et génération de jetons d'accès :
    - Connexion avec un nom d'utilisateur et un mot de passe.
    - Génération d'un jeton d'accès pour l'utilisateur connecté.
- Protection des routes avec des dépendances :
    - Vérification de l'authenticité du jeton d'accès pour accéder à certaines routes.


## Configuration

Avant d'exécuter l'application, assurez-vous de configurer correctement les paramètres suivants :

- `SQLALCHEMY_DATABASE_URL`: URL de la base de données PostgreSQL.
- `SECRET_KEY`: Clé secrète pour la génération des jetons d'accès.
- `ALGORITHM`: Algorithme utilisé pour la génération des jetons d'accès.

## Installation et exécution
1. Assurez-vous d'avoir Python 3.7+ installé.
2. Clonez ce dépôt sur votre machine.
3. Créez un environnement virtuel et activez-le.
4. Installez les dépendances à l'aide de la commande pip install -r requirements.txt.
5. Assurez-vous que la base de données est configurée correctement.
6. Exécutez l'application avec la commande uvicorn main:app --reload.
7. Accédez à http://localhost:8000/docs dans votre navigateur pour consulter la documentation générée automatiquement.

---


### Base de données

Le projet utilise une base de données PostgreSQL par défaut. Cependant, il est possible de configurer une autre base de données en modifiant l'URL de connexion dans le fichier **`database.py`**. Voici comment configurer différents types de bases de données :

#### PostgreSQL
Pour utiliser PostgreSQL, modifiez l'URL de connexion `SQLALCHEMY_DATABASE_URL` dans le fichier `database.py` :

```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/database"
```

#### MYSQL
Pour utiliser MySQL, modifiez l'URL de connexion SQLALCHEMY_DATABASE_URL dans le fichier database.py :
```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://user:password@host:port/database"
```

#### SQLite
Pour utiliser SQLite, modifiez l'URL de connexion SQLALCHEMY_DATABASE_URL dans le fichier database.py :
```python
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
```
Cela utilisera un fichier de base de données SQLite nommé database.db dans le répertoire courant.


