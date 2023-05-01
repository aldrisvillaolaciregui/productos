from pydantic import BaseModel
from datetime import date
from typing import Optional



class categoryBasemodel(BaseModel):
    name_category: str
    
    

class productBasemodel(BaseModel):
    cod_product: int
    id_category: str
    nameProdcut: str 
    description: str
    price_purchase: float
    price_sale:float
    stock:int
    
    
class ventaBasemodel(BaseModel):
    cod_product:int
    quantity:int
   
class usernameBasemodel(BaseModel):
    username: str
    password: str
   
    
    