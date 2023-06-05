from typing import List, Union, Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str 
    email: str
    hashed_password: str    
    class Config:
        orm_mode = True
        
class InventaireBar(BaseModel):
    name :str
    alcohol_type :str
    alcohol_sub_category :str or None = None
    content : float or None = None
    class Config:
        orm_mode = True
        
class InventaireStock(BaseModel):
    __tablename__="inventaire_stock" 
    
    name :str
    alcohol_type :str
    alcohol_sub_category :str or None = None
    content :int
    class Config:
        orm_mode = True