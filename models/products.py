from sqlalchemy import DateTime, Column, String, Integer, Boolean, ForeignKey,func, Float
from sqlalchemy.orm import relationship
from config.db import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key = True, nullable= False)
    product_name = Column (String, index = True, nullable= False)
    description = Column(String, index = True, nullable= False)
    location = Column(String, index = True, nullable= False)
    disposal_price = Column(Float, index = True, nullable= False)
    is_closed = Column(Boolean, default = False)
    file_name = Column(String, index = True, nullable= False)
    product_category_id = Column(Integer, ForeignKey("product_category.id", ondelete="CASCADE"), nullable= False)
    date_created = Column(DateTime, default = func.now())
    owner_id = Column(Integer, nullable=False)
    
    # relationship
    product_category =  relationship("ProductCategory", back_populates = "products")