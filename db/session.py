from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from models.payment import Payment, Customer
import os

load_dotenv()

mongo_url = os.getenv('MONGO_URL')
client = MongoClient(mongo_url)



def get_db():
    return client['paymentsdb']

def insert_customer(data: Customer, db):
    try:
        collection_customer = db['customers']
        collection_customer.insert_one(dict(data))

        print('Dados inseridos! - ✅')
    except Exception as e:
            print('❌', e)

def insert_payment(data: Payment, db):
    try:
        collection_payment = db['payments']
        collection_payment.insert_one(dict(data))
                        
        print('Dados inseridos! - ✅')
    except Exception as e:
        print('❌', e)