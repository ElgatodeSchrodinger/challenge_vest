from typing import List

from pydantic import BaseModel
from .share_transactions import ShareTransactionSchema


class CompanyBase(BaseModel):
    name: str
    symbol: str


class Company(CompanyBase):
    id: int
    share_transactions: List[ShareTransactionSchema] = []

    class Config:
        orm_mode = True