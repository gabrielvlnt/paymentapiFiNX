from fastapi import HTTPException, status
from abacatepay import AbacatePay
from db.session import insert_customer, insert_payment
from abacatepay.products import Product
from dotenv import load_dotenv
from models.payment import Payment, Customer
import httpx
import os

load_dotenv()
api_key = os.getenv('API_KEY')

async def pay_url(db):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.abacatepay.com/v1/billing/create',
                json={
                    "frequency": "ONE_TIME",
                    "methods": [
                        "PIX"
                    ],
                    "products": [
                        {
                        "externalId": "prod-1234",
                        "name": "Assinatura de Programa Fitness",
                        "description": "Acesso ao programa fitness premium por 1 mês.",
                        "quantity": 1,
                        "price": 100
                        }
                    ],
                    "returnUrl": "https://example.com/billing",
                    "completionUrl": "https://example.com/completion",
                    "customerId": "cust_0NWbshbuBTP43UnuT1nmrHrE",
                },
                headers={
                    "Content-type": 'application/json',  
                    "Authorization": f"Bearer {api_key}",
                }
            )
            print('response status code', response.status_code)
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Erro ao criar QR Code')

        checkout = await response.json()
        payment_dict = {
            'payment_id': checkout['data']['id'],
            'product_id': checkout['data']['products'][0]['id'],
            'amount': checkout['data']['amount'],
            'methods': checkout['data']['methods'][0],
            'created_at': checkout['data']['createdAt'],
            'customer_id': checkout['data']['customer']['id'],
            'customer_name': checkout['data']['customer']['metadata']['name'],
            'customer_email': checkout['data']['customer']['metadata']['email']
        }
        payment = Payment(**payment_dict)
        insert_payment(payment, db)
        return checkout
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

async def create_customer(db):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.abacatepay.com/v1/customer/create',
                json={
                    "name": 'Gabriel Valente de Oliveira',
                    "cellphone": '92984181237',
                    "email": 'gabriel@email.com',
                    "taxId": '02383298280'
                },
                headers={
                    "Content-type": 'application/json',  
                    "Authorization": f"Bearer {api_key}",
                }
            )

        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Erro ao criar QR Code')
        checkout = await response.json()
        customer_dict = {
            'customer_id': checkout['data']['id'],
            'name': checkout['data']['metadata']['name'],
            'email': checkout['data']['metadata']['email'],
            'taxId': checkout['data']['metadata']['taxId'],
            'cellphone': checkout['data']['metadata']['cellphone']
        }

        customer = Customer(**customer_dict)
        print(customer)
        insert_customer(customer, db)
        return checkout
    except Exception as e:
        print("❌", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


    

