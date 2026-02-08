import time
import random
import requests

BACKEND_URL = "http://127.0.0.1:5001/ingest"

def generate_network_state():
    return {
        "latency_ms": random.randint(20, 150),
        "packet_loss": round(random.uniform(0.1, 5.0), 2),
        "congestion_level": random.randint(1, 10),
        "active_users": random.randint(10, 500),
        "traffic_type": random.choice(["NORMAL", "EMERGENCY", "RURAL"])
    }

while True:
    state = generate_network_state()
    try:
        requests.post(BACKEND_URL, json=state)
        print(" Sent:", state)
    except Exception as e:
        print(" Error:", e)

    time.sleep(2)
