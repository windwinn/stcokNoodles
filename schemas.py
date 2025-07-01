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
    notes: Optional[str] = ""
    category: str
    products: List[ProductCreate]

class StockOut(BaseModel):
    id: int
    create_date: datetime
    create_by: str
    create_by_id: int
    notes: Optional[str] = ""
    category: str
    status: str
    products: List[ProductOut]

    class Config:
        orm_mode = True

class Units(BaseModel):
    code: str
    name: str

class MasterProductBase(BaseModel):
    name: str
    category: str
    remain: Optional[str] = None
    order: Optional[str] = None
    remain_unit: str
    order_unit: str
    note: Optional[str] = ""
    visible_item: Optional[bool] = True
    class Config:
        orm_mode = True
class MasterProductCreate(MasterProductBase):
    pass

class MasterProductUpdate(MasterProductBase):
    pass

class MasterProductOut(MasterProductBase):
    id: int

    class Config:
        orm_mode = True