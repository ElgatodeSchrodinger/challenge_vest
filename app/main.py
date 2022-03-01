from typing import Optional
from api.stocks.dtos.stock import StockNasdaqDTO
from api.stocks.repositories.company_repository import SQLAlchemyCompanyRepository
from api.stocks.repositories.stock_history_repository import StockHistoryRepository
from api.stocks.schemas.models.stock_history import StockHistoryInput

from fastapi import FastAPI

from api.stocks.routers import stock
from services.db import Base, engine, sessionmakerFastAPI
from fastapi_utils.tasks import repeat_every

Base.metadata.create_all(bind=engine)

app = FastAPI()

nasdaq_service = StockNasdaqDTO()

@app.on_event("startup")
@repeat_every(seconds=60*60)
def track_stock_history():
    with sessionmakerFastAPI.context_session() as db:
        company_repository = SQLAlchemyCompanyRepository(db)
        stock_history_repository = StockHistoryRepository(db)
        companies = company_repository.get_all()
        for company in companies:
            stock_dto = nasdaq_service.get_current_info_nasdaq(company.symbol)
            current_stock_info = stock_dto.extract_stock_info()
            stock_history_repository.create(
                StockHistoryInput(**current_stock_info),
                symbol=company.symbol
            )

app.include_router(stock)