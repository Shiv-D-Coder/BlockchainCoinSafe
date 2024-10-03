import unittest
from token_wallet import TokenWallet

class TestTokenWallet(unittest.TestCase):
    def setUp(self):
        # Initialize the TokenWallet instance and create two wallets for testing
        self.wallet = TokenWallet()
        self.wallet.create_wallet('user1')
        self.wallet.create_wallet('user2')

    def test_wallet_creation(self):
        """Test if wallet creation works and assigns a balance of 0."""
        self.wallet.create_wallet('user3')
        self.assertEqual(self.wallet.get_balance('user3'), 0, "New wallet should have a balance of 0.")

    def test_receive_token(self):
        """Test if receiving tokens increases wallet balance correctly."""
        self.wallet.receive_token('user1', 1000)
        self.assertEqual(self.wallet.get_balance('user1'), 1000, "Balance should be updated after receiving tokens.")

    def test_send_token(self):
        """Test if sending tokens deducts from sender and adds to receiver."""
        self.wallet.receive_token('user1', 1000)  # Add 1000 tokens to user1
        result = self.wallet.send_token('user1', 'user2', 500)  # Transfer 500 tokens
        print(f"Actual result: {result}")  # Debugging output
        print(f"Expected result: 'Transaction successful! Sent 500 tokens from user1 to user2.'")
        self.assertEqual(result.strip(), 'Transaction successful! Sent 500 tokens from user1 to user2.'.strip(), "Transaction message should be correct.")
        self.assertEqual(self.wallet.get_balance('user1'), 500, "Sender's balance should be reduced by the transferred amount.")
        self.assertEqual(self.wallet.get_balance('user2'), 500, "Receiver's balance should be increased by the transferred amount.")

    def test_insufficient_balance(self):
        """Test if sending tokens fails when balance is insufficient."""
        result = self.wallet.send_token('user1', 'user2', 500)  # user1 has 0 tokens initially
        print(f"Actual result: {result}")  # Debugging output
        print(f"Expected result: 'Insufficient balance in user1\'s wallet.'")
        self.assertEqual(result.strip(), 'Insufficient balance in user1\'s wallet.'.strip(), "Should return an insufficient balance message.")

    def test_transaction_history(self):
        """Test if the transaction history is recorded properly."""
        self.wallet.receive_token('user1', 1000)
        self.wallet.send_token('user1', 'user2', 500)
        history = self.wallet.get_transaction_history()

        # Create a helper function to strip timestamps for comparison
        def strip_timestamps(transaction):
            return {key: value for key, value in transaction.items() if key != 'timestamp'}

        expected_transactions = [
            {'sender': 'SYSTEM', 'receiver': 'user1', 'amount': 1000},
            {'sender': 'user1', 'receiver': 'user2', 'amount': 500},
        ]

        # Strip timestamps from the actual history
        history_without_timestamps = [strip_timestamps(tx) for tx in history]
        print(f"Actual history: {history_without_timestamps}")  # Debugging output
        print(f"Expected history: {expected_transactions}")
        
        self.assertEqual(history_without_timestamps, expected_transactions, "Transaction history should contain the correct transaction details.")

if __name__ == '__main__':
    unittest.main()
