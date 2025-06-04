from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    create_by = Column(String)
    create_by_id = Column(Integer)

    products = relationship("Product", back_populates="stock")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    name = Column(String)
    category = Column(String)
    remain = Column(Integer)
    remain_unit = Column(String)
    order = Column(Integer)
    order_unit = Column(String)
    note = Column(String)

    stock = relationship("Stock", back_populates="products")
