from flask import Flask, jsonify, request
from flask_cors import CORS
from dashboard.realtime_stream import process_network_state, get_latest_decision

app = Flask(__name__)
CORS(app) 
@app.route("/ingest", methods=["POST"])
def ingest():
    state = request.get_json()

    if state is None:
        return jsonify({
            "error": "Invalid or missing JSON payload"
        }), 400

    decision = process_network_state(state)
    return jsonify(decision)


@app.route("/latest", methods=["GET"])
def latest():
    data = get_latest_decision()

    if not data:
        return jsonify({
            "status": "waiting",
            "message": "No network state received yet"
        })

    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
