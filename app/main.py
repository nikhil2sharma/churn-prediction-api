# app/main.py
from fastapi import FastAPI, HTTPException
from app.schemas import CustomerFeatures, PredictionResponse
from app.model_loader import get_model
import numpy as np
import logging

# Set up the restaurant
app = FastAPI(title="Churn Prediction API", version="1.0.0")

# Kitchen logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/health")
def health_check():
    """Is the restaurant open?"""
    return {"status": "healthy", "model_loaded": get_model() is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict(features: CustomerFeatures):
    """Customer places an order — chef predicts churn"""
    try:
        model = get_model()

        # Arrange the order on a plate
        X = np.array([[
            features.age,
            features.contract_type,
            features.monthly_charges,
            features.support_calls
        ]])

        # Chef makes the call
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0][1]

        logger.info(f"Prediction made: {prediction}, prob: {probability:.3f}")

        return PredictionResponse(
            prediction=int(prediction),
            probability=round(float(probability), 4),
            model_version="1.0.0"
        )

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Prediction failed")