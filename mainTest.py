from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import List

app = FastAPI()

# ให้ Vue frontend เรียก backend ได้
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# โมเดลข้อมูลที่รับเข้า
class Stock(BaseModel):
    id: int
    createBy: str
    createByID: int
    createDate: date
    freshFoodRemain_1: int
    freshFoodOrder_1: int
    unitRemain_1: str
    unitOrder_1: str
    note_1:str
    freshFoodRemain_2: int
    freshFoodOrder_2: int
    unitRemain_2: str
    unitOrder_2: str
    note_2:str

class StockCreate(BaseModel):
    createBy: str
    createByID: int
    createDate: date
    freshFoodRemain_1: int
    freshFoodOrder_1: int
    unitRemain_1: str
    unitOrder_1: str
    note_1:str
    freshFoodRemain_2: int
    freshFoodOrder_2: int
    unitRemain_2: str
    unitOrder_2: str
    note_2:str

class Unit(BaseModel):
    name: str
    code: str

# ตัวอย่างฐานข้อมูลจำลอง (ใน memory)
stocks = [
    Stock(id=1, createBy="จ๋อย", createDate="2025-01-01", createByID=1,
          freshFoodRemain_1=1, freshFoodOrder_1=1, unitRemain_1="KG",
          unitOrder_1="KG",  note_1="",
          freshFoodRemain_2=1, freshFoodOrder_2=1, unitRemain_2="KG",
          unitOrder_2="KG",  note_2=""),
    Stock(id=2, createBy="บอส", createDate="2025-03-01", createByID=2,
          freshFoodRemain_1=5, freshFoodOrder_1=3, unitRemain_1="KG",
          unitOrder_1="KG", note_1="Test",
          freshFoodRemain_2=1, freshFoodOrder_2=1, unitRemain_2="KG",
          unitOrder_2="KG",  note_2="")
]

units = [
    Unit(name="กิโลกรัม", code="KG"),
    Unit(name="ถุง", code="BAG"),
    Unit(name="ลูก", code="L"),
    Unit(name="เส้น", code="LINE"),
]
id_counter = len(stocks)

# GET: รายชื่อผู้ใช้ทั้งหมด
@app.get("/stocks", response_model=List[Stock])
def get_stocks():
    return stocks

@app.get("/stocksUnit", response_model=List[Unit])
def get_units():
    return units

# GET: ผู้ใช้รายเดียว
@app.get("/stocks/{Stock_id}", response_model=Stock)
def get_Stock(Stock_id: int):
    for Stock in stocks:
        if Stock.id == Stock_id:
            return Stock
    raise HTTPException(status_code=404, detail="Stock not found")

# POST: สร้างผู้ใช้ใหม่
@app.post("/stocks", response_model=Stock)
def create_Stock(stock: StockCreate):
    global id_counter
    id_counter += 1
    new_stock = Stock(id=id_counter, **stock.dict())
    stocks.append(new_stock)
    return new_stock

# PUT: แก้ไขข้อมูล
@app.put("/stocks/{Stock_id}", response_model=Stock)
def update_Stock(Stock_id: int, updated_Stock: Stock):
    for idx, Stock in enumerate(stocks):
        if Stock.id == Stock_id:
            stocks[idx] = updated_Stock
            return updated_Stock
    raise HTTPException(status_code=404, detail="Stock not found")

# DELETE: ลบผู้ใช้
@app.delete("/stocks/{Stock_id}")
def delete_Stock(Stock_id: int):
    for idx, Stock in enumerate(stocks):
        if Stock.id == Stock_id:
            del stocks[idx]
            return {"message": "Stock deleted"}
    raise HTTPException(status_code=404, detail="Stock not found")
