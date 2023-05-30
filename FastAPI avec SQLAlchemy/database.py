from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de données PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/database"

# Création du moteur de base de données SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création d'une classe de session pour la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création de la classe de base pour la déclaration des modèles SQLAlchemy
Base = declarative_base()
