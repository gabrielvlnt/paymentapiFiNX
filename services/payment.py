from fastapi import HTTPException, status
from abacatepay import AbacatePay
from db.session import insert_customer, insert_payment
from abacatepay.products import Product
from dotenv import load_dotenv
from models.payment import Payment, Customer
import logging
import httpx
import os

load_dotenv()
api_key = os.getenv('API_KEY')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

async def pay_url(db: any) -> dict:
    ''' Function to return the url of checkout hos

    Args: 
    db: Database connection

    Return: 
    checkout: dict that contains URL
    '''

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
            logger.info('Response status code:', response.status_code)
        response.raise_for_status()
        logger.info('Type of response', type(response.json))
        checkout = response.json()

        if 'data' not in checkout:
            logger.error('Data do not exist on checkout')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Payload error, data do not exist ')
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
        logger.exception("❌", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    except httpx.RequestError as e:
        logger.exception('🌐', e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        

async def create_customer(db: any) -> dict:
    '''Function to return the customer data

    Args: 
    db: Database connection

    Return: 
    checkout: dict that contains customer data
    '''

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
        logger.info('Create a costume response status code:', response.status_code)
        response.raise_for_status()
        checkout = response.json()
        
        if 'data' not in checkout:
            logger.error('Data do not exist on checkout')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Payload error, data do not exist ')

        customer_dict = {
            'customer_id': checkout['data']['id'],
            'name': checkout['data']['metadata']['name'],
            'email': checkout['data']['metadata']['email'],
            'taxId': checkout['data']['metadata']['taxId'],
            'cellphone': checkout['data']['metadata']['cellphone']
        }

        customer = Customer(**customer_dict)
        insert_customer(customer, db)
        return checkout
    except Exception as e:
        logger.exception("❌", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    except httpx.RequestError as e:
        logger.exception('🌐', e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


    

