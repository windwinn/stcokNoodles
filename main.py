# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from dotenv import load_dotenv
import os

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://stocknoodles.pages.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

units = [
    schemas.Units(name="กิโลกรัม", code="KG"),
    schemas.Units(name="ถุง", code="BAG"),
    schemas.Units(name="ลูก", code="L"),
    schemas.Units(name="เส้น", code="LINE"),
    schemas.Units(name="ชุด", code="MEAL"),
    schemas.Units(name="วัน", code="DAY"),
    schemas.Units(name="หัว", code="DAY"),
    schemas.Units(name="มัด", code="DAY"),
]
@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI app"}
@app.post("/stocks/", response_model=schemas.StockOut)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

@app.get("/stocks/line/{stock_id}", response_model=schemas.StockOut)
def broadcast_line(stock_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_id(db, stock_id=stock_id)
    message_lines = [f"📦 สรุปจำนวนสต๊อกที่สั่งเพิ่มวันที่ {stock.create_date}\n"]
    message_lines.append(f"🥩 ของสด \n")
    for p in stock.products:
        message_lines.append(f"- {p.name} : {p.order} {p.order_unit} {p.note}")
        if p.name == 'กากหมู':
            message_lines.append(f"\n")
            message_lines.append(f"🥬 ผัก \n")
    message = "\n".join(message_lines)
    token = os.getenv("TOKEN")
    crud.broadcast_line(message, token)
    return stock

@app.get("/stocks/", response_model=list[schemas.StockOut])
def read_stocks(db: Session = Depends(get_db)):
    return crud.get_stocks(db)

@app.get("/stocksUnit", response_model=list[schemas.Units])
def read_stocks():
    return units

@app.get("/stocks/{stock_id}", response_model=schemas.StockOut)
def get_stock(stock_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_id(db, stock_id=stock_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock
