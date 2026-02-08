import random
import time
import csv
from datetime import datetime

TRAFFIC_TYPES = ["EMERGENCY", "HEALTHCARE", "RURAL", "NORMAL"]

def generate_network_state():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "latency_ms": random.randint(10, 300),
        "packet_loss": round(random.uniform(0.0, 5.0), 2),
        "congestion_level": random.randint(1, 10),  # 1 = low, 10 = severe
        "active_users": random.randint(50, 500),
        "traffic_type": random.choices(
            TRAFFIC_TYPES,
            weights=[0.1, 0.15, 0.25, 0.5]
        )[0]
    }

def run_simulation(iterations=50, delay=1):
    print("Starting DeTrust-RAN Network Simulation...\n")

    with open("data/simulated_logs.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "latency_ms",
                "packet_loss",
                "congestion_level",
                "active_users",
                "traffic_type"
            ]
        )
        writer.writeheader()

        for i in range(iterations):
            state = generate_network_state()
            writer.writerow(state)

            print(f"[{i+1}] Network State → {state}")
            time.sleep(delay)

if __name__ == "__main__":
    run_simulation()
