from flask import Flask, request, jsonify
from ai.ml_decision_engine import MLDecisionEngine
from blockchain.web3_clients import BlockchainClient
from datetime import datetime

app = Flask(__name__)

ai_engine = MLDecisionEngine()
blockchain = BlockchainClient()

@app.route("/telemetry", methods=["POST"])
def receive_telemetry():
    data = request.json

    network_state = {
        "timestamp": datetime.utcnow().isoformat(),
        "latency_ms": data["latency_ms"],
        "packet_loss": data["packet_loss"],
        "congestion_level": data["congestion_level"],
        "active_users": data["active_users"],
        "traffic_type": data["traffic_type"]
    }

    decision = ai_engine.predict(network_state)
    blockchain.log_decision(decision)

    return jsonify({
        "slice": decision["decision"],
        "bandwidth": decision["bandwidth_allocated"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
