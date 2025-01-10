from sqlalchemy import Column, Integer, String,DateTime, func
from sqlalchemy.orm import relationship
from config.db import Base

class ProductCategory(Base):
    __tablename__ = 'product_category'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    file_name = Column(String, index = True, nullable= False)
    date_created = Column(DateTime, default=func.now())
    
    #relationship
    products = relationship('Product', back_populates='product_category')