from network.simulator import NetworkSimulator
from ai.ml_decision_engine import MLDecisionEngine
from blockchain.web3_clients import BlockchainClient
import time

print("\nDeTrust-RAN System Started\n")

simulator = NetworkSimulator()
ai_engine = MLDecisionEngine()
blockchain = BlockchainClient()

while True:
    state = simulator.get_state()
    print("\n📡 Network State:")
    print(state)

    decision = ai_engine.decide(state)
    print("AI Decision:")
    print(decision)

    blockchain.log_decision(decision)
    time.sleep(2)
