from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.db import get_db
from api.stocks.schemas.models import TransactionSchemaInput, ShareTransactionSchema
from api.stocks.repositories import ShareTransactionRepository

stock = APIRouter()

@stock.get('/status')
def healthcheck():
    return {'message': 'Hola'}

@stock.post('/transfers', response_model=ShareTransactionSchema)
def transfer_stocks(transaction: TransactionSchemaInput, db: Session=Depends(get_db)):

    share_transaction_repository = ShareTransactionRepository(db)

    transaction_obj = share_transaction_repository.create(transaction)

    return transaction_obj