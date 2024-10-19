import streamlit as st
from token_wallet import TokenWallet

# Initialize session state
if 'wallet' not in st.session_state:
    st.session_state.wallet = TokenWallet()

def main():
    st.set_page_config(page_title="TokenWallet App", page_icon="💰", layout="wide")
    
    st.title("🏦 TokenWallet App with Blockchain")
    
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
            return
    
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
        receive_label = st.text_input("Label for transaction (optional)", key="receive_label")
        if st.button("Receive"):
            result = st.session_state.wallet.receive_token(selected_wallet, receive_amount, receive_label)
            st.success(result)
    
    with col2:
        st.subheader("📤 Send Tokens")
        receiver_options = [w for w in wallet_options if w != selected_wallet]
        if receiver_options:
            receiver = st.selectbox("Select receiver", options=receiver_options)
            send_amount = st.number_input("Amount to send", min_value=0, step=1, key="send")
            send_label = st.text_input("Label for transaction (optional)", key="send_label")
            if st.button("Send"):
                try:
                    result = st.session_state.wallet.send_token(selected_wallet, receiver, send_amount, send_label)
                    if "successful" in result:
                        st.success(result)
                    else:
                        st.error(result)
                except TypeError as e:
                    st.error(f"Error: {str(e)}. Please check the TokenWallet implementation.")
        else:
            st.warning("No other wallets available to send tokens to.", icon="⚠️")
    
    # Proof of Work (PoW) Section
    st.subheader("🔨 Proof of Work Simulation")
    st.info("Adjust the difficulty level of the mining process and simulate block creation.")
    
    difficulty = st.slider("Set Mining Difficulty (Number of leading zeros)", 1,5, value=2)
    if st.button("Set Difficulty"):
        result = st.session_state.wallet.set_difficulty(difficulty)
        st.info(result)

    # Blockchain Display
    st.subheader("🔗 Blockchain Overview")
    blockchain = st.session_state.wallet.get_blockchain()
    if blockchain:
        for block in blockchain:
            st.write(f"**Block {block['index']}**")
            st.write(f"Timestamp: {block['timestamp']}")
            st.write(f"Transactions: {block['transactions']}")
            st.write(f"Previous Hash: {block['previous_hash']}")
            st.write(f"Merkle Root: {block['merkle_root']}")
            st.write(f"Hash: {block['hash']}")
            st.write("---")
        
        # Download button for blockchain data
        blockchain_text = "\n".join([
            f"Block {block['index']} - Timestamp: {block['timestamp']}, Transactions: {block['transactions']}, "
            f"Previous Hash: {block['previous_hash']}, Merkle Root: {block['merkle_root']}, Hash: {block['hash']}"
            for block in blockchain
        ])
        st.download_button(
            label="Download Blockchain Data",
            data=blockchain_text,
            file_name="blockchain_data.txt",
            mime="text/plain",
        )
    else:
        st.warning("Blockchain is empty.", icon="⚠️")

if __name__ == "__main__":
    main()
