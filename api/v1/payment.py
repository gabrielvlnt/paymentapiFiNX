from fastapi import APIRouter, status, Form, HTTPException
from schema.payment import UserPayment
from services.payment import create_product, create_client

payment_router = APIRouter(prefix='/payment', tags=['payment'])

@payment_router.post('/create-payment', status_code=status.HTTP_202_ACCEPTED)
async def criar_pagamento(form_data: UserPayment):
    return await create_product(form_data)

@payment_router.post('/create-client', status_code=status.HTTP_201_CREATED)
async def criar_cliente(form_data: UserPayment):
    return await create_client(form_data)