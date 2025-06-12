from sqlalchemy.orm import Session
import models, schemas
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
def create_stock(db: Session, stock_data: schemas.StockCreate):

    dateStr = stock_data.create_date.isoformat()
    date = datetime.fromisoformat(dateStr)
    dateFormat = date.isoformat()

    stock = models.Stock(
        create_date=dateFormat,
        create_by=stock_data.create_by,
        create_by_id=stock_data.create_by_id,
        notes=stock_data.notes,
        status='created'
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)

    for p in stock_data.products:
        product = models.Product(
            stock_id=stock.id,
            name=p.name,
            category=p.category,
            remain=p.remain,
            remain_unit=p.remain_unit,
            order=p.order,
            order_unit=p.order_unit,
            note=p.note
        )
        db.add(product)

    db.commit()
    db.refresh(stock)
    return stock

def broadcast_line(db: Session, stock_id: int, message, channel_access_token):

    stock = db.query(models.Stock).filter(models.Stock.id == stock_id).first()
    if not stock:
        return None
    stock.status = 'broadcasts'
    db.commit()
    db.refresh(stock)

    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {channel_access_token}'
    }
    group_id = os.getenv("GROUP_ID")
    payload = {
        'to': group_id,
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

def get_stocks(db: Session):
    return db.query(models.Stock).order_by(models.Stock.create_date).all()

def get_stock_by_id(db: Session, stock_id: int):
    return db.query(models.Stock).filter(models.Stock.id == stock_id).first()

def create_master_product(db: Session, product: schemas.MasterProductCreate):
    db_product = models.MasterProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
def get_master_products(db: Session):
    return db.query(models.MasterProduct).order_by(models.MasterProduct.id).all()

def get_master_product_status(db: Session, status: str):
    return db.query(models.MasterProduct).filter(models.MasterProduct.visible_item == status).order_by(models.MasterProduct.id).all()

def update_master_product(db: Session, product_id: int, product_data: schemas.MasterProductUpdate):
    db_product = db.query(models.MasterProduct).filter(models.MasterProduct.id == product_id).first()
    if db_product:
        for key, value in product_data.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_master_product(db: Session, product_id: int):
    db_product = db.query(models.MasterProduct).filter(models.MasterProduct.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product