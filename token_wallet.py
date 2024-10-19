import hashlib
import time
from datetime import datetime

class MerkleTree:
    def __init__(self):
        self.leaves = []
        self.tree = []

    def add_leaf(self, data):
        """Add a transaction as a leaf."""
        self.leaves.append(self.hash(data))
        self.build_tree()

    def hash(self, data):
        """Create a SHA-256 hash of the data."""
        return hashlib.sha256(data.encode()).hexdigest()

    def build_tree(self):
        """Build the Merkle Tree."""
        if not self.leaves:
            return
        
        self.tree = [self.leaves]
        current_level = self.leaves

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    combined = current_level[i] + current_level[i + 1]
                else:
                    combined = current_level[i]  # Odd leaf, carry forward
                next_level.append(self.hash(combined))
            self.tree.append(next_level)
            current_level = next_level

    def get_merkle_root(self):
        """Return the Merkle Root."""
        if self.tree:
            return self.tree[-1][0]
        return None

    def get_tree_structure(self):
        """Return the full tree structure for visualization."""
        return self.tree

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class TokenWallet:
    def __init__(self):
        self.wallets = {}
        self.blockchain = []
        self.difficulty = 2  # Number of leading zeros required in hash
        self.merkle_tree = MerkleTree()
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], int(time.time()), "0")
        self.mine_block(genesis_block)
        self.blockchain.append(genesis_block)

    def create_wallet(self, wallet_name):
        if wallet_name in self.wallets:
            return f"Wallet '{wallet_name}' already exists."
        self.wallets[wallet_name] = {"balance": 0, "transaction_history": []}
        return f"Wallet '{wallet_name}' created successfully."

    def get_balance(self, wallet_name):
        if wallet_name in self.wallets:
            return self.wallets[wallet_name]['balance']
        return None

    def receive_token(self, wallet_name, amount, label=None):
        if wallet_name not in self.wallets:
            return f"Wallet '{wallet_name}' does not exist."
        if amount <= 0:
            return "Amount must be positive."

        self.wallets[wallet_name]['balance'] += amount

        transaction = {
            "sender": "external_source",
            "receiver": wallet_name,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "label": label if label else "No label provided"
        }

        self.wallets[wallet_name]["transaction_history"].append(transaction)

        # Add transaction to Merkle Tree
        self.merkle_tree.add_leaf(f"{transaction['sender']},{transaction['receiver']},{transaction['amount']},{transaction['timestamp']},{transaction['label']}")

        # Create a new block for this transaction
        self.create_block([transaction])

        return f"Received {amount} tokens in wallet '{wallet_name}' with label '{transaction['label']}'"

    def send_token(self, sender_wallet, receiver_wallet, amount, label=None):
        if sender_wallet not in self.wallets:
            return f"Wallet '{sender_wallet}' does not exist."
        if receiver_wallet not in self.wallets:
            return f"Wallet '{receiver_wallet}' does not exist."
        if amount <= 0:
            return "Amount must be positive."
        if self.wallets[sender_wallet]['balance'] < amount:
            return "Insufficient balance."

        self.wallets[sender_wallet]['balance'] -= amount
        self.wallets[receiver_wallet]['balance'] += amount

        transaction = {
            "sender": sender_wallet,
            "receiver": receiver_wallet,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "label": label if label else "No label provided"
        }

        self.wallets[sender_wallet]["transaction_history"].append(transaction)
        self.wallets[receiver_wallet]["transaction_history"].append(transaction)

        # Add transaction to Merkle Tree
        self.merkle_tree.add_leaf(f"{transaction['sender']},{transaction['receiver']},{transaction['amount']},{transaction['timestamp']},{transaction['label']}")

        # Create a new block for this transaction
        self.create_block([transaction])

        return f"Sent {amount} tokens from '{sender_wallet}' to '{receiver_wallet}' with label '{transaction['label']}'"

    def create_block(self, transactions):
        last_block = self.blockchain[-1]
        new_block = Block(len(self.blockchain), transactions, int(time.time()), last_block.hash)
        self.mine_block(new_block)
        self.blockchain.append(new_block)

    def mine_block(self, block):
        target = "0" * self.difficulty
        while block.hash[:self.difficulty] != target:
            block.nonce += 1
            block.hash = block.calculate_hash()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        return f"Mining difficulty set to {difficulty}"

    def get_blockchain(self):
        return [vars(block) for block in self.blockchain]

    def get_transaction_history(self, wallet_name):
        if wallet_name not in self.wallets:
            return f"Wallet '{wallet_name}' does not exist."

        history_lines = ["Sender,Receiver,Amount,Timestamp,Label"]
        for transaction in self.wallets[wallet_name]["transaction_history"]:
            history_lines.append(
                f"{transaction['sender']},{transaction['receiver']},{transaction['amount']},{transaction['timestamp']},{transaction['label']}"
            )
        return "\n".join(history_lines)

    def get_merkle_tree(self):
        """Return the Merkle tree for the entire blockchain."""
        return self.merkle_tree.get_tree_structure()