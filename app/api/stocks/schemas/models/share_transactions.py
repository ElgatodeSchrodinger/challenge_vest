from pydantic import BaseModel
from api.stocks.schemas.enums import TransactionType
from datetime import datetime


class TransactionSchemaBase(BaseModel):
    qty: int
    symbol: str
    transaction_type: TransactionType


class TransactionSchema(BaseModel):
    qty: int
    transaction_type: TransactionType


class TransactionSchemaInput(TransactionSchemaBase):
    pass


class ShareTransactionSchema(TransactionSchema):
    id: int
    currency_symbol: str
    date: datetime
    price: float
    company_id: int

    class Config:
        orm_mode = True
