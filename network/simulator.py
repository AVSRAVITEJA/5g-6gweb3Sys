import random
from datetime import datetime

class NetworkSimulator:
    def get_state(self):
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "latency_ms": random.randint(20, 150),
            "packet_loss": round(random.uniform(0, 5), 2),
            "congestion_level": random.randint(1, 10),
            "active_users": random.randint(10, 500),
            "traffic_type": random.choice(["EMERGENCY", "RURAL", "NORMAL"])
        }
