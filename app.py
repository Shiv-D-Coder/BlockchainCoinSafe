import streamlit as st
from token_wallet import TokenWallet

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = TokenWallet()

def main():
    st.set_page_config(page_title="TokenWallet App", page_icon="💰", layout="wide")
    
    st.title("🏦 TokenWallet App")
    
    # Sidebar for wallet creation and selection
    with st.sidebar:
        st.header("Wallet Management")
        new_wallet = st.text_input("Create a new wallet", key="new_wallet")
        if st.button("Create Wallet"):
            result = st.session_state.wallet.create_wallet(new_wallet)
            st.success(result)
        
        st.subheader("Select Wallet")
        wallet_options = list(st.session_state.wallet.wallets.keys())
        if wallet_options:
            selected_wallet = st.selectbox("Choose a wallet", options=wallet_options)
        else:
            st.info("No wallets created yet. Create a wallet to get started.")
            return  # Exit the function if no wallets exist
    
    # Main area
    st.subheader(f"💼 Wallet: {selected_wallet}")
    balance = st.session_state.wallet.get_balance(selected_wallet)
    if balance is not None:
        st.metric("Balance", f"{balance} tokens")
    else:
        st.error("Wallet not found!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📥 Receive Tokens")
        st.info("The 'Receive Tokens' feature simulates receiving tokens from an external source, like mining rewards or transfers from other blockchains.")
        receive_amount = st.number_input("Amount to receive", min_value=0, step=1, key="receive")
        if st.button("Receive"):
            result = st.session_state.wallet.receive_token(selected_wallet, receive_amount)
            st.success(result)
    
    with col2:
        st.subheader("📤 Send Tokens")
        receiver_options = [w for w in wallet_options if w != selected_wallet]
        if receiver_options:
            receiver = st.selectbox("Select receiver", options=receiver_options)
            send_amount = st.number_input("Amount to send", min_value=0, step=1, key="send")
            if st.button("Send"):
                try:
                    result = st.session_state.wallet.send_token(selected_wallet, receiver, send_amount)
                    if "successful" in result:
                        st.success(result)
                    else:
                        st.error(result)
                except TypeError as e:
                    st.error(f"Error: {str(e)}. Please check the TokenWallet implementation.")
        else:
            st.info("No other wallets available to send tokens to.")
    
    # Transaction History
    st.subheader("📜 Transaction History")
    if hasattr(st.session_state.wallet, 'get_transaction_history'):
        history = st.session_state.wallet.get_transaction_history()
        if history:
            # Filter transactions for the selected wallet
            wallet_history = [tx for tx in history if tx['sender'] == selected_wallet or tx['receiver'] == selected_wallet]
            if wallet_history:
                for tx in wallet_history:
                    if tx['sender'] == selected_wallet:
                        st.write(f"Sent {tx['amount']} tokens to {tx['receiver']} on {tx['timestamp']}")
                    else:
                        st.write(f"Received {tx['amount']} tokens from {tx['sender']} on {tx['timestamp']}")
                
                # Download button for transaction history
                history_text = "\n".join([f"{tx['timestamp']}: {tx['sender']} -> {tx['receiver']}: {tx['amount']} tokens" for tx in wallet_history])
                st.download_button(
                    label="Download Transaction History",
                    data=history_text,
                    file_name=f"{selected_wallet}_transaction_history.txt",
                    mime="text/plain",
                )
            else:
                st.info("No transactions for this wallet yet.")
        else:
            st.info("No transactions recorded yet.")
    else:
        st.error("Transaction history feature is not available in the current TokenWallet implementation.")

if __name__ == "__main__":
    main()