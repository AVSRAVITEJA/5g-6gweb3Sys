import random
from datetime import datetime
from decision_engine import decide_slice
from blockchain_logger import log_on_chain

TRAFFIC_TYPES = ["NORMAL", "RURAL", "EMERGENCY"]

def generate_state():
    return {
        "timestamp": datetime.now(),
        "latency_ms": random.randint(20, 150),
        "packet_loss": round(random.uniform(0, 5), 2),
        "congestion_level": random.randint(1, 10),
        "active_users": random.randint(20, 500),
        "traffic_type": random.choice(TRAFFIC_TYPES)
    }

def generate_decision():
    state = generate_state()
    decision, bandwidth = decide_slice(state)
    tx_hash = log_on_chain(decision)

    return {
        **state,
        "decision": decision,
        "bandwidth_allocated": bandwidth,
        "tx_hash": tx_hash
    }
