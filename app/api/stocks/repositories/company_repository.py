from services.db.models.company import Company


class CompanyRepository:
    def __init__(self, session, test=False):

        self.session = session
        self.test = test

    def get_by_id(self, company_id: int):

        return self.session.query(Company).filter_by(id=company_id).first()

    def get_by_symbol(self, symbol: str):
        symbol = symbol.strip().upper()
        return self.session.query(Company).filter_by(symbol=symbol).first()

    def get_all(self):
        return self.session.query(Company).filter().all()

    def create(self, symbol: str, nasdaq_stock_data):

        company_info = nasdaq_stock_data.extract_company_info()
        company_obj = Company(**company_info)
        self.session.add(company_obj)
        self.session.commit()
        return company_obj

    def get_or_create(self, symbol: str, nasdaq_stock_data):
        symbol = symbol.strip().upper()
        company = self.get_by_symbol(symbol)
        if not company:
            company = self.create(symbol, nasdaq_stock_data)
        return company
