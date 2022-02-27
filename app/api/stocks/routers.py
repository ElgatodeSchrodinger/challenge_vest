from fastapi import APIRouter

stock = APIRouter()

@stock.get('/status')
def healthcheck():
    return {'message': 'Hola'}