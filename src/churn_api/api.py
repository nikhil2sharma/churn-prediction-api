"""FastAPI service that serves churn predictions."""

import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request

from . import __version__
from .data import FEATURES
from .schemas import CustomerFeatures, HealthResponse, PredictionResponse

log = logging.getLogger("churn_api")


def model_dir() -> Path:
    return Path(os.environ.get("CHURN_MODEL_DIR", "models"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load once at startup; a missing model keeps the API up but /predict returns 503.
    path = model_dir() / "model.joblib"
    app.state.model = None
    app.state.model_version = None
    if path.exists():
        app.state.model = joblib.load(path)
        meta_path = path.with_name("metadata.json")
        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            app.state.model_version = meta.get("model_version")
        log.info("Loaded model from %s", path)
    else:
        log.warning("No model at %s; run churn-train first", path)
    yield


app = FastAPI(title="Churn Prediction API", version=__version__, lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health(request: Request) -> HealthResponse:
    if request.app.state.model is None:
        return HealthResponse(status="model_missing")
    return HealthResponse(status="ok", model_version=request.app.state.model_version)


@app.post("/predict", response_model=PredictionResponse)
def predict(features: CustomerFeatures, request: Request) -> PredictionResponse:
    model = request.app.state.model
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    row = pd.DataFrame([features.model_dump()], columns=FEATURES)
    probability = float(model.predict_proba(row)[0, 1])
    return PredictionResponse(
        churn=probability >= 0.5,
        probability=round(probability, 4),
        model_version=request.app.state.model_version or "unknown",
    )
