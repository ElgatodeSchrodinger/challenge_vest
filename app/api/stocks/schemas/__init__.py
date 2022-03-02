from typing import List, Optional
from pydantic import BaseModel
from .models import CompanyBase
from datetime import datetime


class IndicatorDataSchema(BaseModel):
    margen_percentage: str
    held_shares: int
    total_value_shares: str


class CurrentPricesSchema(BaseModel):
    lowest: str
    highest: str
    average: str


class StockInformationResponseModel(CompanyBase):
    indicators_data: IndicatorDataSchema
    current_day_prices: CurrentPricesSchema


class StocksInformationResponseModel(BaseModel):
    stocks: List[StockInformationResponseModel]


##########


class HistoryResponseModel(BaseModel):
    price: str
    date: datetime


class StockHistoryResponseModel(CompanyBase):
    # range_type: str
    records: List[HistoryResponseModel]
