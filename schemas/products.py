from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseProduct(BaseModel):
    product_name: str
    description: str
    location: str
    is_closed: Optional[bool]
    file_name: str
    disposal_price: float
    owner_id: int


    
class CreateProduct(BaseProduct):
    pass

class UpdateProductStatus(BaseModel):
    is_closed: Optional[bool]

class Product(BaseProduct):
    id: int
    date_created: datetime
    product_category_id: int
    
    class Config:
        from_attributes = True