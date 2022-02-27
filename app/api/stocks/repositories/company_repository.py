from services.db.models.company import Company
from api.stocks.dtos.stock import StockHistoryDTO
from services.nasdaq import NASDAQService

class SQLAlchemyCompanyRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test
        self.nasdaq_service = NASDAQService()

    def get_company_by_symbol(self, symbol: str):

        company = self.session.query(Company).filter_by(symbol=symbol).first()
        return company

    def create(self, symbol: str):
        nasdaq_stock_data = self.nasdaq_service.get_stock_by_symbol(symbol)
        company_info = StockHistoryDTO(**nasdaq_stock_data).extract_company_info()
        company_obj = Company(**company_info)
        self.session.add(company_obj)
        self.session.commit()
        return company_obj

    def get_or_create_company(self, symbol: str):
        company = self.get_company_by_symbol(symbol)
        if not company:
            company = self.create(symbol)
        return company
        
