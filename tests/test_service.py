import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import HTTPStatusError, Request
from db.session import get_db
from main import app


@pytest.fixture
def mock_mongo():
    client = MongoClient()
    db = client['testdb']
    yield db
    
@pytest.fixture(autouse=True)
def override_db_dependency(mock_mongo):
    def _get_db_override():
        return mock_mongo
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_create_payment(test_client, mock_mongo):
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = AsyncMock()
    mock_response.json = MagicMock(return_value={
        "data": {
            "products": [
                {
                    "id": "prod_KyKcW2j6dSyx4fq51QuQQp5u",
                    "externalId": "prod-1234",
                    "quantity": 1
                }
            ],
            "amount": 100,
            "methods": ["PIX"],
            "metadata": {
                "returnUrl": "https://example.com/billing",
                "completionUrl": "https://example.com/completion"
            },
            "createdAt": "2025-07-23T19:11:48.274Z",
            "customer": {
                "id": "cust_0NWbshbuBTP43UnuT1nmrHrE",
                "metadata": {
                    "name": "string",
                    "cellphone": "string",
                    "taxId": "023.832.982-80",
                    "email": "user@example.com"
                }
            },
            "id": "bill_Ksg50QSQUnNdkQfNtceC2A5Q"
        }
    })

    with patch('httpx.AsyncClient.post', AsyncMock(return_value=mock_response)):
        response = test_client.post('/payment/create-payment')
        data = response.json()
        assert response.status_code == 202
        assert data['data']['id'] == 'bill_Ksg50QSQUnNdkQfNtceC2A5Q'
        db = [db for db in mock_mongo.list_collection_names()] 
        payment = mock_mongo['payments'].find_one({'payment_id': 'bill_Ksg50QSQUnNdkQfNtceC2A5Q'})
        assert payment is not None
        assert payment['amount'] == 100
        assert payment['customer_id'] == 'cust_0NWbshbuBTP43UnuT1nmrHrE'


@pytest.mark.asyncio
async def test_create_customer(test_client, mock_mongo):
    mock_response = AsyncMock
    mock_response.status_code = 200
    mock_response.raise_for_status = AsyncMock()
    mock_response.json = MagicMock(return_value={
        "error": None,
        "data": {
            "id": "cust_454ARWjm1XMUf6FkAuCrTnbg",
            "metadata": {
            "name": "Gabriel Valente de Oliveira",
            "cellphone": "92984181237",
            "taxId": "02383298280",
            "email": "gabriel@email.com"
            }
        }
    })
    with patch('httpx.AsyncClient.post', AsyncMock(return_value=mock_response)):
        response = test_client.post('/payment/create-client')
        data = response.json()
        assert data['data']['id'] == 'cust_454ARWjm1XMUf6FkAuCrTnbg'
        assert response.status_code == 201
        customers = mock_mongo['customers'].find_one({'customer_id': 'cust_454ARWjm1XMUf6FkAuCrTnbg'})
        assert customers is not None
        assert customers['name'] == 'Gabriel Valente de Oliveira'

