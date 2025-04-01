import streamlit as st
from router import render_page

# Set up the app configuration
st.set_page_config(page_title="CC Inc. Pricing Calculator")

# Render the current page using the router
render_page()
