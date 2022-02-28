from api.stocks.repositories import (
    SQLAlchemyCompanyRepository,
    ShareTransactionRepository
)
from api.stocks.dtos.stock import (
    StockHistoryDTO, 
    StockNasdaqDTO,
)
from services.db.models.stock_history import StockHistory
from sqlalchemy import func
from datetime import date




class StockHistoryRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test
        self.company_repository = SQLAlchemyCompanyRepository(session)
        self.transaction_repository = ShareTransactionRepository(session)

    def get_today_stock_history(self, company_id: int = None, symbol: str = None):
        company = None
        if not company_id and symbol:
            company = self.company_repository.get_company_by_symbol(symbol)
        elif company_id:
            company = self.company_repository.get_company_by_id(company_id)

        return (
            self.session
            .query(StockHistory)
            .filter_by(company_id=company.id)
            .filter(func.date(StockHistory.date) == date.today())
            .all()
        )

    def get_current_day_indicators(self, company_id):

        # nasdaq_stock_dto = StockNasdaqDTO(company.symbol).get_current_info_nasdaq()
        today_stock_histories = self.get_today_stock_history(company_id=company_id)
        today_prices = [stock_history.price for stock_history in today_stock_histories]
        currency_symbol = today_stock_histories[0].currency_symbol if today_stock_histories else ''
        result =  {
            'lowest': currency_symbol + str(today_prices and min(today_prices) or 0),
            'highest': currency_symbol + str(today_prices and max(today_prices) or 0),
            'average': currency_symbol + str(today_prices and sum(today_prices)/len(today_prices) or 0),
        }
        print(result)
        return result

