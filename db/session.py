from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from models.payment import Payment, Customer
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url = os.getenv("MONGO_URL")

class Database:
    def __init__(self, mongo_url): 
        self.mongo_url = mongo_url
        self.db = None
        self.collection_payment = None
        self.collection_customer = None

    def create_database(self):
        client = MongoClient(self.mongo_url)
        db = client['payments']

        self.collection_payment = db['payments']
        self.collection_customer = db['customers']

        print('Tabelas criadas - ✅')
        return 

    def insert_payment(self, data: Payment):
        try:
            self.collection_customer.insert_one(dict(data))

            print('Dados inseridos! - ✅')
        except Exception as e:
            print('❌', e)