import streamlit as st
from router import navigate_to

st.title("How to Count Windows")
st.write("Click on a window type to learn how to count its panes.")

# Create a grid layout with 3 columns (we'll adjust this later for more images)
cols = st.columns(3)

# Add the first image in the first column
with cols[0]:
    st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2", use_container_width=True)
    if st.button("Select Top Grids 2 by 2", key="top_grids_2_by_2"):
        navigate_to("top_grids_2_by_2")
