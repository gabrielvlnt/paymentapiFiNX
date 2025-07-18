from pydantic import BaseModel, EmailStr
from datetime import datetime

class Payment(BaseModel):
    payment_id: str
    product_id: str
    amount: int
    methods: str
    created_at: datetime
    customer_id: str
    customer_name: str
    customer_email: str

class Customer(BaseModel):
    name: str
    cellphone: str
    email: EmailStr
    taxId: str 
    customer_id: str
