from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_simulate_loan():
    payload = {
        "loan_amount": 10000,
        "birth_date": "1990-05-15",
        "months": 12
    }
    response = client.post("/simulate", json=payload)
    assert response.status_code == 200
    assert "loan_amount" in response.json()
    assert "results" in response.json()
    assert "monthly_payment" in response.json()["results"]
