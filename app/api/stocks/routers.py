from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.stocks.schemas import StocksInformationResponseModel
from api.stocks.schemas.models import (
    TransactionSchemaInput,
    ShareTransactionSchema,
    StockHistoryInput,
)
from api.stocks.repositories import (
    ShareTransactionRepository,
    StockHistoryRepository,
    CompanyRepository,
)
from api.stocks.dtos.stock import StockNasdaqDTO
from exceptions import ClientException
from services import nasdaq
from services.db import get_db
from services.nasdaq import NASDAQService
from fastapi_utils.tasks import repeat_every
import logging

_logger = logging.getLogger(__name__)
stock = APIRouter()

nasdaq_service = StockNasdaqDTO()


@stock.get("/status")
def healthcheck():
    return {"message": "Hola"}


@stock.post("/transfers", response_model=ShareTransactionSchema)
async def transfer_stocks(
    transaction: TransactionSchemaInput, db: Session = Depends(get_db)
):
    try:
        nasdaq_stock_dto = nasdaq_service.get_current_info_nasdaq(
            transaction.symbol
        )
    except ClientException as e:
        _logger.error(str(e))
        message = "[Unsuccessful Transaction] Symbol not found"
        raise HTTPException(status_code=404, detail=message)

    share_transaction_repository = ShareTransactionRepository(db)
    transaction_obj = share_transaction_repository.create(
        transaction, nasdaq_stock_dto
    )
    if transaction_obj:
        return transaction_obj
    else:
        message = "[Unsuccessful Transaction] No enough shares"
        raise HTTPException(status_code=422, detail=message)


@stock.get("/mystocks", response_model=StocksInformationResponseModel)
async def holding_stocks_information(db: Session = Depends(get_db)):
    share_transaction_repository = ShareTransactionRepository(db)
    stock_history_repository = StockHistoryRepository(db)
    company_repository = CompanyRepository(db)
    all_transactions = share_transaction_repository.get_all_share_transactions()
    unique_companies_ids = company_repository.get_all()
    stocks_info = []
    for company in unique_companies_ids:
        stock_dto = nasdaq_service.get_current_info_nasdaq(company.symbol)
        stock_info = {}
        stock_info["name"] = company.name
        stock_info["symbol"] = company.symbol
        stock_info[
            "indicators_data"
        ] = share_transaction_repository.get_margen_value_indicators(
            company.id, stock_dto
        )
        stock_info[
            "current_day_prices"
        ] = stock_history_repository.get_current_day_indicators(company.id)
        stocks_info.append(stock_info)

    return {"stocks": stocks_info}


@stock.get("/stockhistory/{symbol}")
async def information_stock_history(symbol: str, db: Session = Depends(get_db)):
    company_repository = CompanyRepository(db)
    stock_history_repository = StockHistoryRepository(db)
    company = company_repository.get_by_symbol(symbol)
    if not company:
        message = "[No tracking] Company Not Found"
        raise HTTPException(status_code=404, detail=message)
    stock_records = stock_history_repository.get_all_by_company(company.id)
    history_info = {
        "name": company.name,
        "symbol": company.symbol,
        "records": [
            {
                "price": record.currency_symbol + str(record.price),
                "date": record.date,
            }
            for record in stock_records
        ],
    }

    return {"stock_history": history_info}
