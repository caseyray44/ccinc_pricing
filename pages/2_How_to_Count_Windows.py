import streamlit as st

st.title("How to Count Windows")
st.write("Click on a window type to learn how to count its panes.")

# Create a grid layout with 3 columns (we'll adjust this later for more images)
cols = st.columns(3)

# Add the first image in the first column
with cols[0]:
    st.image("images/nicolas-solerieu-4gRNmhGzYZE-unsplash.jpg", caption="Side-by-Side Window", use_column_width=True)
    if st.button("Select Side-by-Side Window", key="side_by_side"):
        st.write("You selected: **Side-by-Side Window**")
        st.write("Instructions for counting panes will go here.")
