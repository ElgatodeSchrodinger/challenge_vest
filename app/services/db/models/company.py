from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from services.db import Base
from services.db.models.share_transaction import ShareTransaction
from services.db.models.stock_history import StockHistory


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    symbol = Column(String, unique=True, index=True)

    share_transactions = relationship(
        ShareTransaction, back_populates="company"
    )
    stock_histories = relationship(StockHistory, back_populates="company")
