from fastapi.testclient import TestClient
from main import app
import pytest
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def clear_app_state():
    app.rate_limit_store = {}
    app.idempotency_store = {}
    yield

client = TestClient(app)

def test_parse_single_content():
    response = client.post("/parse", json={"content": "Sugar – Rs. 6,000 (50 kg)"})
    assert response.status_code == 200
    assert response.json() == {
        "extracted_items": [
            {
                "product_name": "Sugar",
                "quantity": 50.0,
                "unit": "kg",
                "price": 6000.0,
                "unit_price": 120.0,
            }
        ]
    }

def test_parse_array_content():
    response = client.post(
        "/parse",
        json={
            "content": [
                "Sugar – Rs. 6,000 (50 kg)",
                "Wheat Flour (10kg @ 950)",
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "extracted_items": [
            {
                "product_name": "Sugar",
                "quantity": 50.0,
                "unit": "kg",
                "price": 6000.0,
                "unit_price": 120.0,
            },
            {
                "product_name": "Wheat Flour",
                "quantity": 10.0,
                "unit": "kg",
                "price": 9500.0,
                "unit_price": 950.0,
            },
        ]
    }

def test_parse_invalid_content():
    response = client.post("/parse", json={"content": "This is not an invoice line"})
    assert response.status_code == 200
    assert response.json() == {"extracted_items": []}

def test_payload_too_large():
    # Create a content string larger than 100KB
    large_content = "a" * (1024 * 101)  # 101 KB
    response = client.post("/parse", json={"content": large_content})
    assert response.status_code == 413
    assert response.json() == {"detail": "Payload too large"}

def test_rate_limiting():
    for _ in range(5):
        response = client.post("/parse", json={"content": "Salt - Rs. 100"})
        assert response.status_code == 200
    
    response = client.post("/parse", json={"content": "Salt - Rs. 100"})
    assert response.status_code == 429
    assert response.json() == {"detail": "Too many requests"}

def test_idempotency():
    request_id = "test-idempotent-request-123"
    content = "Cooking Oil: Qty 5 bottles Price 1200/bottle"

    response1 = client.post(
        "/parse",
        json={"content": content},
        headers={"request-id": request_id}
    )
    assert response1.status_code == 200
    
    response2 = client.post(
        "/parse",
        json={"content": content},
        headers={"request-id": request_id}
    )
    assert response2.status_code == 200
    assert response1.json() == response2.json()
