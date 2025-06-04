from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    category: str
    remain: int
    remain_unit: str
    order: int
    order_unit: str
    note: Optional[str] = ""

class ProductOut(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class StockCreate(BaseModel):
    create_date: datetime
    create_by: str
    create_by_id: int
    products: List[ProductCreate]

class StockOut(BaseModel):
    id: int
    create_date: datetime
    create_by: str
    create_by_id: int
    products: List[ProductOut]

    class Config:
        orm_mode = True

class Units(BaseModel):
    code: str
    name: str

