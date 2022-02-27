from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from services.db import Base


class StockHistory(Base):
    __tablename__ = "stock_history"

    id = Column(Integer, primary_key=True, index=True)
    currency_symbol = Column(String, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    price = Column(Float, index=True)
    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="stock_histories")