from sqlalchemy import Column, Integer, String, DateTime, ForeignKey ,Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    create_by = Column(String)
    create_by_id = Column(Integer)
    notes = Column(String)
    status = Column(String)
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

class MasterProduct(Base):
    __tablename__ = "master_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    category = Column(String)
    remain = Column(String)
    remain_unit = Column(String)
    order = Column(String)
    order_unit = Column(String)
    note = Column(String, default="")
    visible_item = Column(Boolean, default=True)