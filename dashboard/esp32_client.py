import requests

ESP32_BACKEND_URL = "http://localhost:5000/latest"

def fetch_esp32_data():
    try:
        response = requests.get(ESP32_BACKEND_URL, timeout=2)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {
            "timestamp": "N/A",
            "latency_ms": 0,
            "packet_loss": 0,
            "congestion_level": 0,
            "active_users": 0,
            "traffic_type": "NO_DATA",
            "decision": "NO_SIGNAL",
            "bandwidth_allocated": 0,
            "tx_hash": "N/A"
        }
