from fastapi import FastAPI, Depends ,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, Base
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue dev server
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

@app.post("/stocks/", response_model=schemas.StockOut)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

@app.get("/stocks/line/{stock_id}", response_model=schemas.StockOut)
def broadcast_line(stock_id: int, db: Session = Depends(get_db)):
    stock = crud.get_stock_by_id(db, stock_id=stock_id)
    message_lines = []
    message_lines.append(f"📦 สรุปจำนวนสต๊อกที่สั่งเพิ่มวันที่ {stock.create_date}\n")

    for p in stock.products:
        message_lines.append(f"- {p.name}: {p.order} {p.order_unit}")

    message = "\n".join(message_lines)
    token = 'PCQYVri8Sj3x7ut1sdEiGNUbXfI4/2kEQ7i+w+ggGJ5A+cCe/t4rySQvBxux8E/yQIoMDisMykSeLG/R17B7QUIkGBzs3yciD+vRzM642T43IcXC+12GzMT0AjE6ZV1h0Yv8VU0ALCvVn/N/5S8xhAdB04t89/1O/w1cDnyilFU='
    status = crud.broadcast_line(message,token)
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