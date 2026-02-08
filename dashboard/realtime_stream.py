from ai.ml_decision_engine import MLDecisionEngine
from blockchain.web3_clients import BlockchainClient
from datetime import datetime

# Initialize engines once
ml_engine = MLDecisionEngine()
blockchain = BlockchainClient()

# Global cache for dashboard / API
latest_decision = None


def process_network_state(state: dict):
    """
    Receives network state from ESP32 / simulator / API
    """

    decision = ml_engine.predict(state)
    tx_hash = blockchain.log_decision(decision)

    global latest_decision
    latest_decision = {
        "timestamp": datetime.utcnow().isoformat(),
        **state,
        **decision,
        "tx_hash": tx_hash
    }

    return latest_decision


def get_latest_decision():
    """
    Used by Flask / Streamlit dashboards
    """
    if latest_decision is None:
        return {
            "status": "waiting",
            "message": "No network state received yet"
        }

    return latest_decision
def has_data():
    return latest_decision is not None
