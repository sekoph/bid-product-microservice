from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pathlib import Path
import aiofiles
from sqlalchemy.orm import Session
from config.db import SessionLocal
from crud.product_category import create_product_category, get_product_category
from schemas.product_category import CreateProductCategory, ProductCategory



# define database dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
categotyTypeRouter = APIRouter()

UploadDirectory = Path("/home/sekoph/projects/online_bidding_fastapi-v2/uploads/category_image")
# Create the directory if it doesn't exist
UploadDirectory.mkdir(exist_ok=True)

@categotyTypeRouter.post('/api/create_product_category/', response_model=ProductCategory)
async def create_product_category_route(name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    file_name = await upload_image(file)
    product_category = CreateProductCategory(name=name, file_name=file_name)
    return create_product_category(db, product_category)


async def upload_image(file: UploadFile):
    file_name = UploadDirectory / file.filename
    
    # Use asynchronous file operations
    async with aiofiles.open(file_name, "wb") as buffer:
        while content := await file.read(1024):  # Read in chunks
            await buffer.write(content)
    
    return str(file_name)


@categotyTypeRouter.get('/api/product_category', response_model=list[ProductCategory])
def get_product_category_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_product_category(db, skip, limit)

