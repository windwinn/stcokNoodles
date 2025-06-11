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
        notes=stock_data.notes
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

def broadcast_line(message, channel_access_token):

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
    return db.query(models.Stock).all()

def get_stock_by_id(db: Session, stock_id: int):
    return db.query(models.Stock).filter(models.Stock.id == stock_id).first()
