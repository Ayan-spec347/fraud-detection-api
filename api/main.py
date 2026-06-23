import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="Real-Time Fraud Detection Engine", version="1.0")

# 1. Get the directory where main.py is currently running (/app/api inside Docker)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Safely navigate up one level, then into the models folder
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "models", "xgboost_fraud_model.pkl"))

try:
    print(f"Loading XGBoost model from: {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully into RAM!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# 3. Define the exact shape of an incoming transaction
# This acts as a strict bouncer; if an API request is missing one of these, it rejects it automatically.
class TransactionData(BaseModel):
    TransactionAmt: float
    DeviceInfo_risk_score: float  # The target-encoded value we built
    card_degree: int
    device_degree: int
    network_cluster_size: int
    time_since_last_txn: float
    Card_Txn_Count_24h: int
    Device_Txn_Count_1h: int
    spend_ratio: float

@app.post("/predict")
def predict_fraud(transaction: TransactionData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server.")
    
    # 1. Reordered to perfectly match the Pandas DataFrame from Phase 3
    # DeviceInfo_risk_score MUST be at the very end.
    features = [[
        transaction.TransactionAmt,
        transaction.card_degree,
        transaction.device_degree,
        transaction.network_cluster_size,
        transaction.time_since_last_txn,
        transaction.Card_Txn_Count_24h,
        transaction.Device_Txn_Count_1h,
        transaction.spend_ratio,
        transaction.DeviceInfo_risk_score
    ]]
    
    feature_names = [
        'TransactionAmt', 'card_degree', 'device_degree', 
        'network_cluster_size', 'time_since_last_txn', 'Card_Txn_Count_24h', 
        'Device_Txn_Count_1h', 'spend_ratio', 'DeviceInfo_risk_score'
    ]
    
    X_input = pd.DataFrame(features, columns=feature_names)
    
    # 2. Force the XGBoost output into a standard Python float to prevent JSON crashes
    fraud_probability = float(model.predict_proba(X_input)[0][1])
    
    # 3. Determine the strict verdict based on a threshold (e.g., 0.5)
    is_fraud = bool(fraud_probability > 0.5)
    
    # Return the split-second decision to the bank
    return {
        "status": "success",
        "fraud_probability": round(fraud_probability, 4),
        "verdict": "DECLINED" if is_fraud else "APPROVED",
        "risk_level": "HIGH" if fraud_probability > 0.8 else "MEDIUM" if fraud_probability > 0.4 else "LOW"
    }

# Health check endpoint to ensure server is awake
@app.get("/")
def health_check():
    return {"status": "Active", "message": "Fraud Detection API is running."}