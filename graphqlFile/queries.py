from typing import List
import strawberry
from fastapi import Depends
from sqlalchemy.orm import Session
from .types import ProductTypes
from models.products import Product
from crud.products import get_won_products

@strawberry.type
class Query:
    @strawberry.field
    def open_products(self, info) -> List[ProductTypes]:
        db:Session = info.context['db']
        products = db.query(Product).filter(Product.is_closed == False).all()
        return [
            ProductTypes(
                id = product.id,
                product_name = product.product_name,
                description = product.description,
                location = product.location,
                disposal_price = product.disposal_price,
                date_created = product.date_created,
                owner_id = product.owner_id
                )
                for product in products]
    
    @strawberry.field
    async def closed_products(self,info) -> List[ProductTypes]:
        db: Session = info.context["db"]
        products = db.query(Product).filter(Product.is_closed == True).all()
        
        products_with_bids = []
        for product in products:
            bid = await get_won_products(product.id)
            if bid:
                products_with_bids.append(
                        ProductTypes(
                            id = product.id,
                            product_name = product.product_name,
                            description = product.description,
                            location = product.location,
                            disposal_price = product.disposal_price,
                            date_created = product.date_created,
                            owner_id = product.owner_id,
                        )
                    )
        return products_with_bids
    
    @strawberry.field
    async def awaiting_auctions(self, info) -> List[ProductTypes]:
        db: Session = info.context["db"]
        products = db.query(Product).filter(Product.is_closed == True).all()
        
        products_without_bids = []
        
        for product in products:
            bid = await get_won_products(product.id)
            if bid is None:
                products_without_bids.append(
                    ProductTypes(
                        id = product.id,
                        product_name = product.product_name,
                        description = product.description,
                        location = product.location,
                        disposal_price = product.disposal_price,
                        date_created = product.date_created,
                        owner_id = product.owner_id,
                    )
                )
                
        return products_without_bids