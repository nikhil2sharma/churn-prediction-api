from typing import Literal

from pydantic import BaseModel, Field


class CustomerFeatures(BaseModel):
    age: int = Field(ge=18, le=100, examples=[35])
    contract_type: Literal[0, 1] = Field(description="0 = monthly, 1 = yearly", examples=[0])
    monthly_charges: float = Field(ge=0, examples=[320.5])
    support_calls: int = Field(ge=0, le=100, examples=[6])


class PredictionResponse(BaseModel):
    churn: bool
    probability: float = Field(ge=0, le=1)
    model_version: str


class HealthResponse(BaseModel):
    status: Literal["ok", "model_missing"]
    model_version: str | None = None
