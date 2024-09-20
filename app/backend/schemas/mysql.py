from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class OrderModel(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)