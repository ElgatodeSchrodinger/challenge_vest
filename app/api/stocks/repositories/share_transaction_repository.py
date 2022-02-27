from fastapi.encoders import jsonable_encoder
import pprint

from api.stocks.schemas.models import TransactionSchemaInput
from services.db.models.share_transaction import ShareTransaction
from api.stocks.repositories import SQLAlchemyCompanyRepository
from api.stocks.dtos.stock import StockHistoryDTO
from services.nasdaq import NASDAQService

class ShareTransactionRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test
        self.company_repository = SQLAlchemyCompanyRepository(session)
        self.nasdaq_service = NASDAQService()

    def create(self, transaction: TransactionSchemaInput):
        print("----------")
        print("======")
        print(transaction)
        print("----------")
        transaction_data = self._fill_related_fields(transaction)
        share_transaction_obj = ShareTransaction(**transaction_data)
        self.session.add(share_transaction_obj)
        self.session.commit()
        return share_transaction_obj
    
    def _fill_related_fields(self, transaction: TransactionSchemaInput):
        transaction_in_data = jsonable_encoder(transaction)
        symbol = transaction_in_data.pop("symbol")
        nasdaq_stock_data = self.nasdaq_service.get_stock_by_symbol(symbol)
        # print(type(nasdaq_stock_data))
        company = self.company_repository.get_or_create_company(symbol)
        stock_info = StockHistoryDTO(**nasdaq_stock_data).extract_stock_info()
        stock_info.update(
            {
                'company_id': company.id,
            }
        )
        print("----------")
        print(transaction_in_data)
        print(stock_info)
        print("----------")
        transaction_in_data.update(stock_info)
        return transaction_in_data