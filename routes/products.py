from sqlalchemy.orm import Session
from starlette.requests import Request
import requests
from config.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException,File, UploadFile
import shutil
from pathlib import Path
import os
import aiofiles


from crud.products import Create_Product, Get_Products,update_product_status,get_Product_By_Id, get_close_products
from schemas.products import CreateProduct, Product,UpdateProductStatus
from services.requests import fetch_data



from datetime import datetime, timedelta

import time
import threading

productsRouter = APIRouter()

# define dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

UploadDirectory = Path("/home/sekoph/projects/online_bidding_fastapi-v2/uploads/product_image")
# Create the directory if it doesn't exist
UploadDirectory.mkdir(exist_ok=True)


# @productsRouter.get("/api/home")  # Root path
# def home():
#     return {"message": "Products Service Running"}


#get all products
@productsRouter.get('/api/products', response_model = list[Product])
async def get_products(limit: int = 100, skip: int = 0 , db: Session = Depends(get_db)):
    return Get_Products(db, limit = limit, skip = skip)


# create new products
@productsRouter.post('/api/products/add', response_model = Product)
async def create_product(token: str, product_name: str, description: str, location: str, disposal_price: float, product_category_id : int, file: UploadFile = File(...), db : Session = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_name = await upload_image(file)
    
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
    }
    
    
    owner = await fetch_data(f'api/user/me',service_name="user-service", method='get', headers=headers)
    
    new_product = CreateProduct(product_name = product_name, description = description, location = location, is_closed = False, file_name = file_name, disposal_price = disposal_price, owner_id = owner['id'])

    return Create_Product(db = db, product = new_product, product_category_id = product_category_id)


async def upload_image(file: UploadFile = File(...)):
    file_name = UploadDirectory / file.filename
    
    # Use asynchronous file operations
    async with aiofiles.open(file_name, "wb") as buffer:
        while content := await file.read(1024):  # Read in chunks
            await buffer.write(content)
    
    return str(file_name)

@productsRouter.get('/api/products/{product_id}', response_model=Product)
async def get_product_by_id(product_id: int, db:Session = Depends(get_db)):
    return get_Product_By_Id(db,product_id)



@productsRouter.put("/api/products/update_status/{product_id}", response_model=Product)
async def update_product_status_route(product_id: int, is_closed: bool, db: Session = Depends(get_db)):
    update = UpdateProductStatus(is_closed)
    return update_product_status(db, product_id, update)

# @productsRouter.put("/api/products/close/{product_id}", response_model=Product)
# async def update_product_status_route(product_id: int, db: Session = Depends(get_db)):
#     update = UpdateProductStatus(is_closed=True)
#     return update_product_status(db, product_id, update)




# @productsRouter.put("/api/products/update/{product_id}", response_model=Product)
# async def update_product_status_route(
#     product_id: int,
#     product: UpdateProductStatus,
#     db: Session = Depends(get_db)
# ):
#     product_to_update = update_product_status(db, product_id, product)
#     if product_to_update is None:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     if product_to_update.is_closed:  # Assuming you have an is_closed field
#         Product.model_validate(product_to_update)
#         asyncio.create_task(count_down_and_save_win(product_id, db, seconds=60))
#     return Product.model_validate(product_to_update)


# def get_highest_bid(product_id: int, db: Session):
#     return db.query(Bid).filter(Bid.product_id == product_id).order_by(Bid.amount.desc()).first()

# def close_bids(db: Session):
#     # Find products that are open for bidding and have exceeded the bidding period
#     products_to_close = db.query(Product).filter(
#         Product.is_closed == False,
#         Product.bid_end_time <= datetime.utcnow()
#     ).all()

#     for product in products_to_close:
#         highest_bid = get_highest_bid(product.id, db)
#         if highest_bid:
#             new_win = Wins(product_id=product.id, amount=highest_bid.amount, bid_id=highest_bid.id)
#             db.add(new_win)
#             product.is_closed = True  # Mark product as closed
#             db.commit()
#             db.refresh(new_win)
#             print(f"Product {product.id} closed with highest bid: {highest_bid.amount}")

# # Schedule the function to run periodically
# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(close_bids, 'interval', minutes=1, args=[get_db()])
#     scheduler.start()


# @productsRouter.get('/api/wins', response_model=list[Wins])
# def get_wins(limit:int = 100,skip:int=0,db:Session = Depends(get_db),current_user: User = Depends(security.auth.get_current_active_user)):
#     return Get_Wins(db=db,limit=limit,skip=skip)

# import asyncio

# def get_highest_bid(product_id: int, db: Session):
#     return db.query(Bid).filter(Bid.product_id == product_id).order_by(Bid.amount.desc()).first()

# async def save_win(product_id: int, db: Session):
#     highest_bid = get_highest_bid(product_id, db)
#     if highest_bid:
#         new_win = Wins(product_id=product_id, amount=highest_bid.amount, bid_id=highest_bid.id)
#         db.add(new_win)
#         db.commit()
#         db.refresh(new_win)
#         # Mark product as closed
#         product = db.query(Product).filter(Product.id == product_id).first()
#         if product:
#             product.is_closed = True
#             db.commit()
#         return new_win
#     return None

# async def count_down_and_save_win(product_id: int, db: Session, seconds: int):
#     await asyncio.sleep(seconds)
#     await save_win(product_id, db)

# @productsRouter.put("/api/products/update/{product_id}", response_model=Product)
# def update_product_status_route(product_id: int, product: UpdateProductStatus, db: Session = Depends(get_db),current_user: User = Depends(security.auth.get_current_active_user)):
#     product_to_update = update_product_status(db, product_id, product)
#     if product_to_update is None:
#         raise HTTPException(status_code=404, detail="Product not found")
    
#     product_is_closed = get_close_products(db,product_id)
#     if product_is_closed:
#         Product.from_orm(product_to_update)
#         count_down(product_id,seconds=60)
#     return Product.from_orm(product_to_update)