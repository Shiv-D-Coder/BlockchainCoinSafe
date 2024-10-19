# import hashlib
# from datetime import datetime

# class TokenWallet:
#     def __init__(self):
#         self.wallets = {}
#         self.transaction_file = "transaction_history.txt"
#         self.transaction_fee = 0.01  # 1% fee

#     def hash_address(self, address):
#         return hashlib.sha256(address.encode()).hexdigest()

#     def create_wallet(self, address):
#         hashed_address = self.hash_address(address)
#         if hashed_address in self.wallets:
#             return "Wallet already exists!"
#         self.wallets[hashed_address] = {'balance': {}, 'private_key': 'dummy_private_key'}
#         return f"Wallet created for {address}."

#     def get_balance(self, address):
#         hashed_address = self.hash_address(address)
#         if hashed_address not in self.wallets:
#             return "Wallet not found!"
#         return self.wallets[hashed_address]['balance']

#     def log_transaction(self, from_address, to_address, token_type, amount):
#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         with open(self.transaction_file, 'a') as file:
#             file.write(f"{timestamp} | From: {from_address} | To: {to_address} | Token: {token_type} | Amount: {amount}\n")

#     def receive_token(self, address, token_type, amount):
#         if amount < 0:
#             return "Amount must be positive!"
        
#         hashed_address = self.hash_address(address)
#         if hashed_address not in self.wallets:
#             return "Wallet not found!"
        
#         if token_type in self.wallets[hashed_address]['balance']:
#             self.wallets[hashed_address]['balance'][token_type] += amount
#         else:
#             self.wallets[hashed_address]['balance'][token_type] = amount

#         self.log_transaction('system', address, token_type, amount)  # Log system-generated transaction
#         return f"{amount} {token_type} received in {address}'s wallet."

#     def send_token(self, from_address, to_address, token_type, amount):
#         if amount < 0:
#             return "Amount must be positive!"

#         from_hashed = self.hash_address(from_address)
#         to_hashed = self.hash_address(to_address)

#         if from_hashed not in self.wallets:
#             return "Sender wallet not found!"
#         if to_hashed not in self.wallets:
#             return "Recipient wallet not found!"
        
#         if token_type not in self.wallets[from_hashed]['balance'] or self.wallets[from_hashed]['balance'][token_type] < amount:
#             return "Insufficient balance in sender's wallet."
        
#         # Update balances
#         self.wallets[from_hashed]['balance'][token_type] -= amount
#         if token_type in self.wallets[to_hashed]['balance']:
#             self.wallets[to_hashed]['balance'][token_type] += amount
#         else:
#             self.wallets[to_hashed]['balance'][token_type] = amount
        
#         # Record the transaction
#         self.log_transaction(from_address, to_address, token_type, amount)  # Log the actual transaction
#         return f"Transaction successful! Sent {amount} {token_type} from {from_address} to {to_address}."

#     def get_transaction_history(self):
#         with open(self.transaction_file, 'r') as file:
#             return file.readlines()

#     def send_token(self, from_address, to_address, token_type, amount):
#         if amount < 0:
#             raise ValueError("Amount must be positive!")

#         from_hashed = self.hash_address(from_address)
#         to_hashed = self.hash_address(to_address)

#         if from_hashed not in self.wallets:
#             raise ValueError("Sender wallet not found!")
#         if to_hashed not in self.wallets:
#             raise ValueError("Recipient wallet not found!")

#         total_amount = amount + (amount * self.transaction_fee)  # Include fee

#         if token_type not in self.wallets[from_hashed]['balance'] or self.wallets[from_hashed]['balance'][token_type] < total_amount:
#             raise ValueError("Insufficient balance in sender's wallet.")

#         # Update balances
#         self.wallets[from_hashed]['balance'][token_type] -= total_amount
#         if token_type in self.wallets[to_hashed]['balance']:
#             self.wallets[to_hashed]['balance'][token_type] += amount
#         else:
#             self.wallets[to_hashed]['balance'][token_type] = amount

#         self.log_transaction(from_address, to_address, token_type, amount)
#         return f"Transaction successful! Sent {amount} {token_type} from {from_address} to {to_address}."

# # Example usage
# if __name__ == "__main__":
#     wallet = TokenWallet()
#     print(wallet.create_wallet('user3'))
#     print(wallet.create_wallet('user4'))
#     print(wallet.receive_token('user3', 'IRCRC2', 1000))
#     print(wallet.send_token('user3', 'user4', 'IRCRC2', 500))
#     print(wallet.get_balance('user3'))
#     print(wallet.get_balance('user4'))

#     # Display transaction history
#     print("Transaction History:")
#     for transaction in wallet.get_transaction_history():
#         print(transaction.strip())


from datetime import datetime

class TokenWallet:
    def __init__(self):
        self.wallets = {}
        self.transaction_history = []

    def create_wallet(self, wallet_name):
        if wallet_name in self.wallets:
            return f"Wallet '{wallet_name}' already exists."
        self.wallets[wallet_name] = {"balance": 0}  # Store wallet with a balance as a dictionary
        return f"Wallet '{wallet_name}' created successfully."

    def get_balance(self, wallet_name):
        if wallet_name in self.wallets:
            return self.wallets[wallet_name]['balance']
        return None

    def receive_token(self, wallet_name, amount, label=None):
        # Ensure the wallet exists and amount is valid
        if wallet_name not in self.wallets:
            return f"Wallet '{wallet_name}' does not exist."
        if amount <= 0:
            return "Amount must be positive."
        
        # Add the received amount to the wallet's balance
        self.wallets[wallet_name]['balance'] += amount

        # Create a transaction record with a label
        transaction = {
            "sender": "external_source",
            "receiver": wallet_name,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "label": label if label else "No label provided"
        }

        # Add the transaction to the transaction history
        self.transaction_history.append(transaction)

        return f"Received {amount} tokens in wallet '{wallet_name}' with label '{transaction['label']}'"

    def send_token(self, sender_wallet, receiver_wallet, amount, label=None):
        # Ensure wallets exist and amount is valid
        if sender_wallet not in self.wallets:
            return f"Wallet '{sender_wallet}' does not exist."
        if receiver_wallet not in self.wallets:
            return f"Wallet '{receiver_wallet}' does not exist."
        if amount <= 0:
            return "Amount must be positive."
        if self.wallets[sender_wallet]['balance'] < amount:
            return "Insufficient balance."
        
        # Deduct the amount from the sender and add it to the receiver
        self.wallets[sender_wallet]['balance'] -= amount
        self.wallets[receiver_wallet]['balance'] += amount

        # Create a transaction record with a label
        transaction = {
            "sender": sender_wallet,
            "receiver": receiver_wallet,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "label": label if label else "No label provided"
        }

        # Add the transaction to the transaction history
        self.transaction_history.append(transaction)

        return f"Sent {amount} tokens from '{sender_wallet}' to '{receiver_wallet}' with label '{transaction['label']}'"

    def set_difficulty(self, difficulty):
        # Set the difficulty level for mining (this is just a placeholder for now)
        self.difficulty = difficulty
        return f"Difficulty set to {difficulty} leading zeros."

    def get_blockchain(self):
        # Simulate a simple blockchain with transaction history (no real mining logic)
        blockchain = []
        for index, transaction in enumerate(self.transaction_history, start=1):
            block = {
                "index": index,
                "timestamp": transaction['timestamp'],
                "transactions": transaction,
                "previous_hash": "0" if index == 1 else blockchain[-1]['hash'],
                "merkle_root": "mock_merkle_root",
                "hash": "mock_hash"  # In reality, you would calculate this based on block data
            }
            blockchain.append(block)
        return blockchain
