from fastapi.encoders import jsonable_encoder
from api.stocks.schemas.enums import TransactionType
from api.stocks.schemas.models import TransactionSchemaInput
from services.db.models.share_transaction import ShareTransaction
from api.stocks.repositories import SQLAlchemyCompanyRepository


class ShareTransactionRepository():

    def __init__(self, session, test=False):

        self.session = session
        self.test = test
        self.company_repository = SQLAlchemyCompanyRepository(session)

    def create(
            self, 
            transaction: TransactionSchemaInput, 
            nasdaq_stock_data):
        transaction_data = self._fill_related_fields(transaction, nasdaq_stock_data)
        share_transaction_obj = ShareTransaction(**transaction_data)
        self.session.add(share_transaction_obj)
        self.session.commit()
        return share_transaction_obj

    def _fill_related_fields(
            self,
            transaction: TransactionSchemaInput,
            nasdaq_stock_data):

        transaction_in_data = jsonable_encoder(transaction)
        symbol = transaction_in_data.pop("symbol")
        company = self.company_repository.get_or_create_company(
            symbol, nasdaq_stock_data)
        stock_info = nasdaq_stock_data.extract_stock_info()
        stock_info.update(
            {
                'company_id': company.id,
            }
        )
        transaction_in_data.update(stock_info)
        return transaction_in_data

    def get_all_share_transactions(self):
        return (
            self.session
            .query(ShareTransaction)
            .all()
        )

    def get_share_transactions_by_company(self, company_id):

        return (
            self.session
            .query(ShareTransaction)
            .filter_by(company_id=company_id)
            .all()
        )

    @staticmethod
    def factor_transaction_type(type: str):
        print(type)
        if type == TransactionType.buy:
            return 1
        elif type == TransactionType.sell:
            return -1

    @staticmethod
    def compute_margen_percentage(current_value, initial_value):
        if not initial_value:
            return "0%"
        diff_amount = current_value - initial_value
        diff_percentual = round((diff_amount / initial_value) * 100, 2)
        sign = '+' if diff_percentual > 0 else ''
        return sign + str(abs(diff_percentual)) + "%"

    def get_margen_value_indicators(self, company_id, stock_dto):
        transactions = self.get_share_transactions_by_company(company_id)
        stock_current_info = stock_dto.extract_stock_info()
        currency_symbol = transactions[0].currency_symbol \
            if transactions else ''
        held_shares = sum(
            [
                transaction.qty *
                self.factor_transaction_type(transaction.transaction_type)
                for transaction in transactions
            ]
        )
        total_value = sum(
            [
                transaction.qty * transaction.price *
                self.factor_transaction_type(transaction.transaction_type)
                for transaction in transactions
            ]
        )
        current_value = stock_current_info.get('price') * held_shares

        return {
            "margen_percentage": self.compute_margen_percentage(
                current_value, total_value),
            "held_shares": held_shares,
            "total_value_shares": currency_symbol + str(round(total_value, 2))
        }
