from typing import Optional, List
from datetime import datetime
import strawberry

@strawberry.type
class ProductTypes:
    id: int
    product_name: str
    description: str
    location: str
    disposal_price: float
    # is_closed: bool
    # product_category_id: int
    date_created: datetime
    owner_id: int
    
