from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models.product_category import ProductCategory
from schemas.product_category import CreateProductCategory



def create_product_category(db: Session, product_category: CreateProductCategory):
    try:
        new_product_category = ProductCategory(**product_category.model_dump())
        db.add(new_product_category)
        db.commit()
        db.refresh(new_product_category)
        return new_product_category
    except IntegrityError:
        db.rollback()
        return False
    
    
def get_product_category(db: Session, skip: int, limit: int):
    return db.query(ProductCategory).offset(skip).limit(limit).all()

