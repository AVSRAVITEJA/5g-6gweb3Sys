class BlockchainClient:
    def __init__(self):
        print("Blockchain client initialized (demo mode)")

    def log_decision(self, decision):
        print("🔗 [Blockchain] Logging decision:")
        print(decision)
        print("Logged on-chain: 0xDEMO_TRANSACTION_HASH")
