# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    create_date = stock.create_date.strftime("%d-%m-%Y %H:%M:%S")
    message_lines = [f"📦 สรุปจำนวนสต๊อกที่สั่งเพิ่มวันที่ {create_date}\n"]
    message_lines.append(f"🥩 ของสด \n")
    for p in stock.products:
        if p.order > 0:
            note_text = f"❗{p.note}" if p.note else ""
            message_lines.append(f"- {p.name} : {p.order} {p.order_unit} {note_text}")
            if p.name == 'กากหมู':
                message_lines.append(f"\n")
                message_lines.append(f"🥬 ผัก \n")

    notes_text = f"{stock.notes}" if stock.notes else ""
    if notes_text != "":
        message_lines.append(f"\n")
        message_lines.append(f"📝 เพิ่มเติม \n")
        message_lines.append(f"- {notes_text}")

    message = "\n".join(message_lines)
    token = os.getenv("TOKEN")
    crud.broadcast_line(db, stock_id, message, token)
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

@app.get("/master-products-all/", response_model=list[schemas.MasterProductOut])
def read_master_all(db: Session = Depends(get_db)):
    return crud.get_master_products(db)

@app.post("/master-products/", response_model=schemas.MasterProductOut)
def create(product: schemas.MasterProductCreate, db: Session = Depends(get_db)):
    return crud.create_master_product(db, product)

@app.get("/master-products/", response_model=list[schemas.MasterProductBase])
def read_master(db: Session = Depends(get_db)):
    product = crud.get_master_product_status(db, True)
    if product is None:
        raise HTTPException(status_code=404, detail="Not found")
    return product

@app.put("/master-products/{product_id}", response_model=schemas.MasterProductOut)
def update(product_id: int, product: schemas.MasterProductUpdate, db: Session = Depends(get_db)):
    return crud.update_master_product(db, product_id, product)

@app.delete("/master-products/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_master_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "Deleted"}