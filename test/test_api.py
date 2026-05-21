# tests/test_api.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Restaurant door must open"""
    response = client.get("/health")
    assert response.status_code == 200

def test_predict_endpoint():
    """Chef must respond to a valid order"""
    payload = {
        "age": 35,
        "contract_type": 1,
        "monthly_charges": 200.0,
        "support_calls": 3
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] in [0, 1]