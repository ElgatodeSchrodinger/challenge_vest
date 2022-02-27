from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.services.db import Base
# from schemas import TypeAction


class ShareTransaction(Base):
    __tablename__ = "share_transaction"

    id = Column(Integer, primary_key=True, index=True)
    qty = Column(Integer, index=True)
    currency_symbol = Column(String, index=True)
    price = Column(Float, index=True)
    transaction_type = Column(Enum(TypeAction))
    date = Column(DateTime(timezone=True), server_default=func.now())

    company_id = Column(Integer, ForeignKey("company.id"))

    company = relationship("Company", back_populates="share_transactions")