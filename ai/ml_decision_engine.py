import joblib
import numpy as np

class MLDecisionEngine:
    def __init__(self):
        """
        Loads trained ML model (or uses fallback logic)
        """
        try:
            self.model = joblib.load("ai/models/slicing_model.pkl")
            self.trained = True
        except Exception:
            print("ML model not found, using rule-based fallback")
            self.trained = False

    def predict(self, state: dict) -> dict:
        """
        Unified inference interface used by:
        - Flask backend
        - ESP32 stream
        - Simulator
        """

        latency = state["latency_ms"]
        packet_loss = state["packet_loss"]
        congestion = state["congestion_level"]
        users = state["active_users"]
        traffic = state["traffic_type"]

        # -------------------------------
        # Fallback logic (VERY IMPORTANT)
        # -------------------------------
        if not self.trained:
            if traffic == "EMERGENCY":
                return {
                    "decision": "HIGH_PRIORITY_SLICE",
                    "bandwidth_allocated": 80,
                    "social_context": "EMERGENCY"
                }
            elif congestion > 7:
                return {
                    "decision": "MEDIUM_PRIORITY_SLICE",
                    "bandwidth_allocated": 50,
                    "social_context": traffic
                }
            else:
                return {
                    "decision": "BEST_EFFORT",
                    "bandwidth_allocated": 30,
                    "social_context": traffic
                }

        # -------------------------------
        # ML-based inference (future-safe)
        # -------------------------------
        features = np.array([[latency, packet_loss, congestion, users]])
        prediction = self.model.predict(features)[0]

        mapping = {
            0: ("BEST_EFFORT", 30),
            1: ("MEDIUM_PRIORITY_SLICE", 50),
            2: ("HIGH_PRIORITY_SLICE", 80),
        }

        decision, bw = mapping[prediction]

        return {
            "decision": decision,
            "bandwidth_allocated": bw,
            "social_context": traffic
        }
