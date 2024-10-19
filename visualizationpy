import streamlit as st
import graphviz
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Any

def visualize_blockchain(blockchain: List[Dict[str, Any]]):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    for i, block in enumerate(blockchain):
        dot.node(f'block_{i}', f'Block {i}\nHash: {block["hash"][:6]}...\nTransactions: {len(block["transactions"])}', shape='rectangle')
        if i > 0:
            dot.edge(f'block_{i-1}', f'block_{i}')

    st.graphviz_chart(dot)

def visualize_merkle_tree(merkle_tree: List[List[str]]):
    if not merkle_tree:
        st.warning("No Merkle tree data available.")
        return

    G = nx.Graph()
    pos = {}
    labels = {}
    node_colors = []

    def add_nodes(level, index, x, y):
        if level >= len(merkle_tree):
            return

        if index >= len(merkle_tree[level]):
            return

        node_id = f"{level}_{index}"
        G.add_node(node_id)
        pos[node_id] = (x, -y)
        labels[node_id] = merkle_tree[level][index][:6] + "..."
        node_colors.append('lightblue' if level == 0 else 'lightgreen')

        if level + 1 < len(merkle_tree):
            left_child_index = index * 2
            right_child_index = index * 2 + 1
            
            if left_child_index < len(merkle_tree[level + 1]):
                left_child = f"{level+1}_{left_child_index}"
                G.add_edge(node_id, left_child)
                add_nodes(level + 1, left_child_index, x - 1 / (2 ** (level + 1)), y + 1)
            
            if right_child_index < len(merkle_tree[level + 1]):
                right_child = f"{level+1}_{right_child_index}"
                G.add_edge(node_id, right_child)
                add_nodes(level + 1, right_child_index, x + 1 / (2 ** (level + 1)), y + 1)

    add_nodes(0, 0, 0, 0)

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, node_color=node_colors, with_labels=False, node_size=3000, edge_color='gray')
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    plt.title("Merkle Tree Visualization (All Transactions)")
    plt.axis('off')
    st.pyplot(plt)

    # Interactive exploration
    st.write("Click on a node to see its details:")
    selected_node = st.selectbox("Select a node:", list(labels.keys()))
    if selected_node:
        level, index = map(int, selected_node.split('_'))
        st.write(f"Node: {merkle_tree[level][index]}")
        if level < len(merkle_tree) - 1:
            left_child_index = index * 2
            right_child_index = index * 2 + 1
            left_child = merkle_tree[level+1][left_child_index] if left_child_index < len(merkle_tree[level+1]) else "None"
            right_child = merkle_tree[level+1][right_child_index] if right_child_index < len(merkle_tree[level+1]) else "None"
            st.write(f"Left child: {left_child}")
            st.write(f"Right child: {right_child}")
        else:
            st.write("This is a leaf node (transaction hash)")

def visualize_transaction(transaction: Dict[str, Any]):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR')

    dot.node('sender', transaction['sender'])
    dot.node('receiver', transaction['receiver'])
    dot.edge('sender', 'receiver', label=f"{transaction['amount']} tokens\n{transaction['label']}")

    st.graphviz_chart(dot)