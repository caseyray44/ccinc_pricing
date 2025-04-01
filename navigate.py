import streamlit as st

def navigate_to_page(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()
