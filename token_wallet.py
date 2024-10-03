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


import hashlib
from datetime import datetime
class TokenWallet:
    def __init__(self):
        self.wallets = {}
        self.transaction_history = []

    def create_wallet(self, name):
        if name not in self.wallets:
            self.wallets[name] = 0
            return f"Wallet '{name}' created successfully"
        return f"Wallet '{name}' already exists"

    def get_balance(self, name):
        return self.wallets.get(name)

    def receive_token(self, name, amount):
        if name in self.wallets:
            self.wallets[name] += amount
            self.transaction_history.append({
                'timestamp': datetime.now().isoformat(),
                'sender': 'SYSTEM',
                'receiver': name,
                'amount': amount
            })
            return f"Received {amount} tokens for {name}"
        return f"Wallet '{name}' not found"

    def send_token(self, sender, receiver, amount):
        if sender in self.wallets and receiver in self.wallets:
            if self.wallets[sender] >= amount:
                self.wallets[sender] -= amount
                self.wallets[receiver] += amount
                self.transaction_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'sender': sender,
                    'receiver': receiver,
                    'amount': amount
                })
                return f"Transaction successful! Sent {amount} tokens from {sender} to {receiver}"
            return f"Insufficient balance in {sender}'s wallet"
        return "One or both wallets do not exist"

    def get_transaction_history(self):
        return self.transaction_history