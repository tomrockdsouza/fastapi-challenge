from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import Numeric, DateTime

Base = declarative_base()


class Orders(Base):
    __tablename__ = 'orders'
    id = Column(String(length=256), primary_key=True)
    user_id = Column(String(length=256), nullable=False)
    product_code = Column(String(length=256), nullable=False)
    customer_fullname = Column(String(length=256), nullable=True)
    product_name = Column(String(length=256), nullable=True)
    total_amount = Column(Numeric(precision=15, scale=2), nullable=True)
    created_at = Column(DateTime, nullable=False)
