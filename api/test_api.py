import requests
import json

# The address of your local FastAPI server
API_URL = "http://127.0.0.1:8000/predict"

print("--- INITIATING LIVE INFERENCE TEST ---\n")

# ==========================================
# TEST 1: The Normal Customer
# ==========================================
# An established user buying lunch on a generic device.
normal_transaction = {
    "TransactionAmt": 15.50,
    "DeviceInfo_risk_score": 0.02,   # Generic Windows/iOS baseline
    "card_degree": 2,
    "device_degree": 5,
    "network_cluster_size": 1,       # No graph anomaly
    "time_since_last_txn": 86400.0,  # 1 day since last purchase
    "Card_Txn_Count_24h": 1,         # Normal velocity
    "Device_Txn_Count_1h": 0,
    "spend_ratio": 1.05              # Right on average for this user
}

print("Sending Transaction 1: Normal Lunch Purchase...")
response_1 = requests.post(API_URL, json=normal_transaction)
print(f"API Response: {json.dumps(response_1.json(), indent=2)}\n")


# ==========================================
# TEST 2: The Coordinated Botnet Strike
# ==========================================
# A stolen card used for the first time on a highly specific, suspicious device
# that has already attempted 12 other transactions in the last hour.
fraud_transaction = {
    "TransactionAmt": 850.00,
    "DeviceInfo_risk_score": 0.85,   # High-risk specific fingerprint
    "card_degree": 1,
    "device_degree": 45,             # Device has been used with 45 different cards
    "network_cluster_size": 15,      # Caught in a massive graph cluster
    "time_since_last_txn": -999.0,   # First time this card is seen
    "Card_Txn_Count_24h": 0,
    "Device_Txn_Count_1h": 12,       # Massive 1-hour velocity spike
    "spend_ratio": 45.0              # 45x their normal spending behavior!
}

print("Sending Transaction 2: High-Velocity Bot Strike...")
response_2 = requests.post(API_URL, json=fraud_transaction)
print(f"API Response: {json.dumps(response_2.json(), indent=2)}")