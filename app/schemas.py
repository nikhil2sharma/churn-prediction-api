# app/schemas.py
from pydantic import BaseModel

class CustomerFeatures(BaseModel):
    age: int
    contract_type: int        # 0=month-to-month, 1=yearly
    monthly_charges: float
    support_calls: int

class PredictionResponse(BaseModel):
    prediction: int           # 0=stays, 1=churns
    probability: float
    model_version: str