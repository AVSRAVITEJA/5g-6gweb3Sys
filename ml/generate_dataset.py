import csv
import random

FILE = "ml/network_dataset.csv"

FIELDS = [
    "latency",
    "packet_loss",
    "congestion",
    "active_users",
    "traffic_type",
    "decision"
]

TRAFFIC_TYPES = ["EMERGENCY", "RURAL", "NORMAL"]

def rule_decision(state):
    if state["traffic_type"] == "EMERGENCY":
        return "HIGH"
    if state["congestion"] > 7:
        return "HIGH"
    if state["traffic_type"] == "RURAL":
        return "MEDIUM"
    return "LOW"

with open(FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(FIELDS)

    for _ in range(3000):
        state = {
            "latency": random.randint(20, 150),
            "packet_loss": round(random.uniform(0, 5), 2),
            "congestion": random.randint(1, 10),
            "active_users": random.randint(10, 500),
            "traffic_type": random.choice(TRAFFIC_TYPES)
        }

        writer.writerow([
            state["latency"],
            state["packet_loss"],
            state["congestion"],
            state["active_users"],
            state["traffic_type"],
            rule_decision(state)
        ])

print("Dataset generated")
