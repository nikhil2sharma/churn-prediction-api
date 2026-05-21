# app/model_loader.py
import pickle

_model = None

def get_model():
    """
    Lazy loader — chef wakes up only when first order arrives.
    Avoids reloading on every request (MLOps best practice).
    """
    global _model
    if _model is None:
        import os
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "day1_ml", "model.pkl")
        with open(model_path, "rb") as f:
            _model = pickle.load(f)
    return _model