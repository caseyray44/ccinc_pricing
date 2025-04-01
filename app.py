import streamlit as st
from router import render_page, navigate_to, get_current_page

# Set up the app configuration
st.set_page_config(page_title="CC Inc. Pricing Calculator")

# Custom sidebar navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("Estimate"):
        navigate_to("estimate")
    if st.button("How to Count Windows"):
        navigate_to("how_to_count_windows")
    if st.button("View Estimates"):
        navigate_to("view_estimates")

# Render the current page using the router
render_page()
