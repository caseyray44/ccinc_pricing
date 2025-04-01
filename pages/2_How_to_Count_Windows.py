import streamlit as st

st.title("How to Count Windows")

# Dropdown to select a window type
window_types = ["Select a window type", "Side-by-Side Window", "French Pane Window", "French Pane on Top", "Large Window"]
selected_window = st.selectbox("Select a window type to learn how to count its panes:", window_types)

# Display a message based on the selected window type
if selected_window != "Select a window type":
    st.write(f"You selected: **{selected_window}**")
    st.write("Instructions for counting panes will go here.")
else:
    st.write("Please select a window type to see the counting instructions.")
