import streamlit as st

# Dictionary mapping page names to their file paths
PAGES = {
    "estimate": "pages/1_Estimate.py",
    "how_to_count_windows": "pages/2_How_to_Count_Windows.py",
    "view_estimates": "pages/2_View_Estimates.py",
    "top_grids_2_by_2": "pages/window_types/3_Top_Grids_2_by_2.py",
}

def navigate_to(page_name):
    if page_name in PAGES:
        st.session_state.current_page = page_name
    else:
        st.error(f"Page {page_name} not found!")

def get_current_page():
    return st.session_state.get("current_page", "estimate")

def render_page():
    current_page = get_current_page()
    if current_page in PAGES:
        # Dynamically import and run the page
        page_path = PAGES[current_page]
        with open(page_path, "r") as f:
            code = f.read()
        exec(code, globals())
    else:
        st.error(f"Cannot render page {current_page}")
