from fastapi import HTTPException, status
from abacatepay import AbacatePay
from abacatepay.products import Product
from dotenv import load_dotenv
from models.payment import Payment, Customer
import httpx
import os

load_dotenv()
api_key = os.getenv('API_KEY')

async def create_product(db):
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
            print(response.status_code)
            print(response.text)
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Erro ao criar QR Code')
        else:
            checkout_url = response.json()
            print(checkout_url)
            return checkout_url
    except Exception as e:
        print(e)

async def create_client(billing_data: Customer):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://api.abacatepay.com/v1/customer/create',
                json={
                    "name": billing_data.name,
                    "cellphone": billing_data.cellphone,
                    "email": billing_data.email,
                    "taxId": billing_data.taxId
                },
                headers={
                    "Content-type": 'application/json',  
                    "Authorization": f"Bearer {api_key}",
                }
            )
            print(response.status_code)
            print(response.text)
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Erro ao criar QR Code')
        else:
            checkout_url = response.json()
            print(checkout_url)
            return checkout_url
    except Exception as e:
        print("❌", e)


    

