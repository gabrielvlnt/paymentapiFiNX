from fastapi import APIRouter, status, Form, HTTPException, Depends
from models.payment import Customer
from db.session import get_db
from pymongo.mongo_client import MongoClient
from services.payment import pay_url, create_customer


payment_router = APIRouter(prefix='/payment', tags=['payment'])


@payment_router.post('/create-payment', status_code=status.HTTP_202_ACCEPTED)
async def create_payment(db = Depends(get_db)):
    return await pay_url(db)

@payment_router.post('/create-client', status_code=status.HTTP_201_CREATED)
async def create_client(db = Depends(get_db)):
    return await create_customer(db)