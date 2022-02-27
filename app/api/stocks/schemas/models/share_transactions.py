from pydantic import BaseModel
from api.stocks.schemas.enums import TransactionType
from datetime import datetime

class TransactionSchemaBase(BaseModel):
    qty: str
    symbol: str
    transaction_type: TransactionType

class TransactionSchema(BaseModel):
    qty: str
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