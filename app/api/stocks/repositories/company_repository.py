from services.db.models.company import Company
from api.stocks.dtos.stock import StockHistoryDTO

class SQLAlchemyCompanyRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test

    def get_company_by_id(self, company_id: int):

        company = self.session.query(Company).filter_by(id=company_id).first()
        return company

    def get_company_by_symbol(self, symbol: str):

        company = self.session.query(Company).filter_by(symbol=symbol).first()
        return company

    def create(self, symbol: str, nasdaq_stock_data):
        
        company_info = nasdaq_stock_data.extract_company_info()
        company_obj = Company(**company_info)
        self.session.add(company_obj)
        self.session.commit()
        return company_obj

    def get_or_create_company(self, symbol: str, nasdaq_stock_data):
        symbol = symbol.strip().upper()
        company = self.get_company_by_symbol(symbol)
        if not company:
            company = self.create(symbol, nasdaq_stock_data)
        return company
        
