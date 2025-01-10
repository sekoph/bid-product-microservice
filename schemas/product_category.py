from pydantic import BaseModel
from datetime import datetime


class BaseProductCategory(BaseModel):
    name: str
    file_name: str


class CreateProductCategory(BaseProductCategory):
    pass

class ProductCategory(BaseProductCategory):
    id: int
    date_created: datetime

    class Config:
        from_attributes = True
        
