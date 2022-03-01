from fastapi.encoders import jsonable_encoder
from api.stocks.repositories import (
    SQLAlchemyCompanyRepository,
    ShareTransactionRepository
)
from api.stocks.dtos.stock import (
    StockNasdaqDTO,
)
from api.stocks.schemas.models.stock_history import StockHistoryInput
from services.db.models.stock_history import StockHistory
from sqlalchemy import func
from datetime import date




class StockHistoryRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test
        self.company_repository = SQLAlchemyCompanyRepository(session)
        self.transaction_repository = ShareTransactionRepository(session)

    def create(self, stock_history: StockHistoryInput, symbol: str):
        history_in_data = jsonable_encoder(stock_history)
        company = self.company_repository.get_company_by_symbol(symbol)
        history_in_data.update(
            {
                'company_id': company.id,
            }
        )
        stock_history_obj = StockHistory(**history_in_data)
        self.session.add(stock_history_obj)
        self.session.commit()
        self.session.refresh(stock_history_obj)
        return stock_history_obj

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

    def get_all_by_company(self, company_id: int):

        return (
            self.session
            .query(StockHistory)
            .filter_by(company_id=company_id)
            .all()
        )

    def get_current_day_indicators(self, company_id):

        today_stock_histories = self.get_today_stock_history(company_id=company_id)
        today_prices = [stock_history.price for stock_history in today_stock_histories]
        currency_symbol = today_stock_histories[0].currency_symbol if today_stock_histories else ''
        return  {
            'lowest': currency_symbol + str(today_prices and min(today_prices) or 0),
            'highest': currency_symbol + str(today_prices and max(today_prices) or 0),
            'average': currency_symbol + str(today_prices and round(sum(today_prices)/len(today_prices), 2) or 0),
        }
