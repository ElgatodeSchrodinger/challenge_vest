from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

float_characters = '1234567890.'

@dataclass
class StockDataDTO:
    lastSalePrice: str
    netChange: str
    percentageChange: str
    deltaIndicator: str
    lastTradeTimestamp: str
    isRealTime: bool

    def extract_current_info(self):

        currency_symbol, price = self._decompose_price(self.lastSalePrice)
        return {
            'currency_symbol': currency_symbol,
            'price': price,
        }
    
    @staticmethod
    def _decompose_price(str_price):

        str_price = str_price.strip().replace(' ', '')
        n = len(str_price)
        i = 0
        for chrt in str_price[::-1]:
            if chrt in float_characters:
                i+=1
        limit = n - i
        return str_price[:limit], str_price[limit:]


@dataclass
class StockHistoryDTO:
    """
    Declarar campos de stock
    """
    symbol: Optional[str]
    companyName: str
    stockType: str
    exchange: str
    isNasdaqListed: bool
    isNasdaq100: bool
    isHeld: bool
    primaryData: StockDataDTO
    secondaryData: Any
    marketStatus: str
    assetClass: str
    tradingHeld: Any
    complianceStatus: Any

    def __post_init__(self):
        pass
    
    def extract_company_info(self):

        return {
            'name': self.companyName,
            'symbol': self.symbol,
        }
    
    def extract_stock_info(self):
        stock_data = StockDataDTO(**self.primaryData)
        return stock_data.extract_current_info()