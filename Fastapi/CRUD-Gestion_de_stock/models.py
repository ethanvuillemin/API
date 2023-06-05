from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    """
    Modèle pour l'utilisateur.
    """
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
class InventaireBar(Base):
    __tablename__="inventaire_bar" 
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(TIMESTAMP)
    name = Column(String, unique=True, index=True)
    alcohol_type = Column(String, index=True)
    alcohol_sub_category = Column(String, index=True)
    content = Column(Float,index=True)
    
    
class InventaireStock(Base):
    __tablename__="inventaire_stock" 
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(TIMESTAMP)
    name = Column(String, unique=True, index=True)
    alcohol_type = Column(String, index=True)
    alcohol_sub_category = Column(String, index=True)
    content = Column(Integer,index=True)