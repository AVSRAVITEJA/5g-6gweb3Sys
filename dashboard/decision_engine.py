def decide_slice(state):
    if state["traffic_type"] == "EMERGENCY":
        return "HIGH_PRIORITY_SLICE", 80
    elif state["congestion_level"] > 7:
        return "BEST_EFFORT", 30
    elif state["traffic_type"] == "RURAL":
        return "MEDIUM_PRIORITY_SLICE", 50
    else:
        return "MEDIUM_PRIORITY_SLICE", 50
