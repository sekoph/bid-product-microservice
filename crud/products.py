from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.products import Product
from schemas.products import CreateProduct, UpdateProductStatus
from schemas.products import BaseProduct as pd
from sqlalchemy import and_ , update
import requests


# create new product
def Create_Product(db: Session , product: CreateProduct, product_category_id:int):
    try:
        new_product = Product(**product.model_dump(), product_category_id = product_category_id)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except IntegrityError:
        db.rollback()
        return False
    # product_name = product.product_name, description = product.description, location = product.location, is_closed = product.is_closed,
    
def Get_Products(db: Session, limit:int, skip: int):
    return db.query(Product).offset(skip).limit(limit).all()


def update_product_status(db: Session, product_id: int, product: UpdateProductStatus):
    product_to_update = db.query(Product).filter(Product.id == product_id).first()
    if product_to_update:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(product_to_update, key, value)
        db.commit()
        db.refresh(product_to_update)
    return product_to_update

    
def get_Product_By_Id(db:Session,product_id):
    return db.query(Product).filter(Product.id == product_id).first()


def get_close_products(db:Session,product_id:int):
    return db.query(Product).filter(and_(Product.id == product_id,Product.is_closed == True))


async def get_won_products(product_id:int):
    headers2 = {
    'Content-Type': 'application/json'
    }
    response = requests.get(f'http://localhost:8003/api/bid/product/{product_id}', headers=headers2)
    if response.status_code == 200:
        return response.json()
    return None

