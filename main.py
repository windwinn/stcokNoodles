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

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI app"}
@app.post("/stocks/", response_model=schemas.StockOut)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

@app.get("/stocks/line/{category}/{stock_id}", response_model=schemas.StockOut)
def broadcast_line(stock_id: int, category: str, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_id(db, stock_id=stock_id, category=category)
    create_date = stock.create_date.strftime("%d-%m-%Y %H:%M:%S")
    message_lines = [f"📦 สรุปจำนวนสต๊อกที่สั่งเพิ่มวันที่ {create_date}\n"]
    fresh_items = [p for p in stock.products if p.category == 'FF' and p.order > 0]
    vege_items = [p for p in stock.products if p.category == 'VT' and p.order > 0]

    if fresh_items:

        type1 = [p for p in stock.products if p.type == 1 and p.order > 0]
        type2 = [p for p in stock.products if p.type == 2 and p.order > 0]

        message_lines.append("🥩 ของสด#1\n")
        for p in type1:
            note_text = f"❗{p.note}" if p.note else ""
            message_lines.append(f"- {p.name} : {p.order} {p.order_unit} {note_text}")

        message_lines.append("\n")
        message_lines.append("🥩 ของสด#2\n")
        for p in type2:
            note_text = f"❗{p.note}" if p.note else ""
            message_lines.append(f"- {p.name} : {p.order} {p.order_unit} {note_text}")


    if vege_items:
        message_lines.append("🥬 ผัก\n")
        for p in vege_items:
            note_text = f"❗{p.note}" if p.note else ""
            message_lines.append(f"- {p.name} : {p.order} {p.order_unit} {note_text}")

    if stock.notes:
        message_lines.append("\n📝 เพิ่มเติม\n")
        message_lines.append(f"- {stock.notes}")

    message = "\n".join(message_lines)
    token = os.getenv("TOKEN")
    crud.broadcast_line(db, stock_id, message, token)
    return stock

@app.get("/stocks/{category}", response_model=list[schemas.StockOut])
def read_stocks(category: str, db: Session = Depends(get_db)):
    return crud.get_stocks(db, category=category)

@app.get("/units", response_model=list[schemas.UnitOut])
def read_units(db: Session = Depends(get_db)):
    return crud.get_all_units(db)

@app.post("/units", response_model=schemas.UnitOut)
def add_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    return crud.create_unit(db, unit)
@app.put("/units/{product_id}", response_model=schemas.UnitOut)
def update(product_id: int, product: schemas.UnitUpdate, db: Session = Depends(get_db)):
    return crud.update_master_unit(db, product_id, product)

@app.get("/stocks/{category}/{stock_id}", response_model=schemas.StockOut)
def get_stock(stock_id: int, category: str, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_id(db, stock_id=stock_id, category=category)
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