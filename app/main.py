
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import joblib
import pandas as pd
from pathlib import Path

# --- Load trained model ---
MODEL_PATH = Path("../models/log_reg_model.joblib")
MODEL = joblib.load(MODEL_PATH)

# --- Input validation ---
EXPECTED_FIELDS = {
    "gender": ["Male", "Female", "Other"],
    "age": (0, 120),
    "ever_married": ["Yes", "No"],
    "work_type": ["Private", "Self-employed", "Govt_job", "children", "Never_worked"],
    "Residence_type": ["Urban", "Rural"],
    "avg_glucose_level": (0, 400),
    "bmi": (10, 100),
    "smoking_status": ["formerly smoked", "never smoked", "smokes", "Unknown"],
    "hypertension": [0,1],
    "heart_disease": [0,1],
}

def validate_payload(payload: dict) -> pd.DataFrame:
    # check for missing keys
    missing = [k for k in EXPECTED_FIELDS if k not in payload]
    if missing:
        raise ValueError(f"Missing keys: {missing}")
    
    # check for extras
    extras = [k for k in payload if k not in EXPECTED_FIELDS]
    if extras:
        raise ValueError(f"Unexpected keys: {extras}")
    
    validated = {}
    for key, rule in EXPECTED_FIELDS.items():
        value = payload[key]
        if isinstance(rule, tuple):  # numeric
            if not isinstance(value, (int, float)):
                raise ValueError(f"{key} must be numeric")
            low, high = rule
            if not (low <= value <= high):
                raise ValueError(f"{key}={value} outside range {rule}")
            validated[key] = float(value)
        elif isinstance(rule, list):  # categorical
            if value not in rule:
                raise ValueError(f"{key} must be one of {rule}")
            validated[key] = value
    return pd.DataFrame([validated])

# --- FastAPI app ---
app = FastAPI(title="Stroke Predictor")

@app.get("/", response_class=HTMLResponse)
def home():
    """
    Serve the HTML frontend for the stroke predictor.
    """
    index_path = Path("app/static/index.html")  # make sure this path is correct
    if not index_path.exists():
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)
    return index_path.read_text()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: dict):
    try:
        X = validate_payload(payload)
        prob = float(MODEL.predict_proba(X)[:, 1][0])
        return {"stroke_probability": prob}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")
