

from pydantic import BaseModel
from api.stocks.schemas.enums import TransactionType
from datetime import datetime


class StockHistoryBase(BaseModel):
    price: float
    currency_symbol: str


class StockHistoryTotal(StockHistoryBase):
    pass


class StockHistory(StockHistoryTotal):
    id: int
    company_id: int

    class Config:
        orm_mode = True