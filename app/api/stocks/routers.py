from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.stocks.schemas import StocksInformationResponseModel
from api.stocks.schemas.models import TransactionSchemaInput, ShareTransactionSchema
from api.stocks.repositories import (
    ShareTransactionRepository,
    StockHistoryRepository,
    SQLAlchemyCompanyRepository
)
from api.stocks.dtos.stock import StockHistoryDTO, StockNasdaqDTO
from services.db import get_db
from services.nasdaq import NASDAQService

stock = APIRouter()


@stock.get('/status')
def healthcheck():
    return {'message': 'Hola'}


@stock.post('/transfers', response_model=ShareTransactionSchema)
def transfer_stocks(transaction: TransactionSchemaInput, db: Session = Depends(get_db)):

    symbol = transaction.symbol
    share_transaction_repository = ShareTransactionRepository(db)
    nasdaq_stock_data = NASDAQService().get_stock_by_symbol(symbol)
    nasdaq_stock_dto = StockHistoryDTO(**nasdaq_stock_data)
    transaction_obj = share_transaction_repository.create(transaction, nasdaq_stock_dto)
    return transaction_obj


@stock.get('/mystocks', response_model=StocksInformationResponseModel)
def holding_stocks_information(db: Session = Depends(get_db)):
    share_transaction_repository = ShareTransactionRepository(db)
    stock_history_repository = StockHistoryRepository(db)
    company_repository = SQLAlchemyCompanyRepository(db)
    all_transactions = share_transaction_repository.get_all_share_transactions()
    unique_companies_ids = list(set([transaction.company.id for transaction in all_transactions]))
    stocks_info = []
    for company_id in unique_companies_ids:
        company = company_repository.get_company_by_id(company_id=company_id)
        stock_dto = StockNasdaqDTO(company.symbol).get_current_info_nasdaq()
        stock_info = {}
        stock_info['name'] = company.name
        stock_info['symbol'] = company.symbol
        stock_info['indicators_data'] = share_transaction_repository.get_margen_value_indicators(company_id, stock_dto)
        stock_info['current_day_prices'] = stock_history_repository.get_current_day_indicators(company_id)
        stocks_info.append(stock_info)

    return {
        'stocks': stocks_info
    }
