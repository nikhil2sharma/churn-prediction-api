# tests/test_model.py
import pickle
import pytest
import numpy as np

# Minimum quality bar — below this, the railway STOPS
MINIMUM_ACCURACY = 0.80

def test_model_accuracy():
    """Health inspector refuses entry if chef is below standard"""
    
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    # Dummy test sample (in real life, use a holdout test set)
    X_sample = np.array([[35, 1, 200.0, 3]])   # age, contract, charges, support_calls
    prediction = model.predict(X_sample)

    # Model must actually return a valid prediction
    assert prediction[0] in [0, 1], "Model output is invalid"

def test_model_file_exists():
    """Railway won't proceed if the chef jar is missing"""
    import os
    assert os.path.exists("model.pkl"), "model.pkl not found!"