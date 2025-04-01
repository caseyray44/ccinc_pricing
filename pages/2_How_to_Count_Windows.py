import streamlit as st

# Initialize session state for navigation
if "window_type_page" not in st.session_state:
    st.session_state.window_type_page = "main"

# Main page content: grid of window types
if st.session_state.window_type_page == "main":
    st.title("How to Count Windows")
    st.write("Click on a window type to learn how to count its panes.")

    # Create a grid layout with 3 columns (adjust if needed)
    cols = st.columns(3)

    # Column 0: Top Grids 2 by 2
    with cols[0]:
        st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2", use_container_width=True)
        if st.button("Select", key="top_grids_2_by_2"):
            st.session_state.window_type_page = "top_grids_2_by_2"
            st.rerun()

    # Column 1: Single Window
    with cols[1]:
        st.image("images/Single_window.png", caption="Single Window", use_container_width=True)
        if st.button("Select", key="single_window"):
            st.session_state.window_type_page = "single_window"
            st.rerun()

    # Column 2: (You can add additional window types here in the future.)

# Render content for "Top Grids 2 by 2" window type
elif st.session_state.window_type_page == "top_grids_2_by_2":
    st.title("Counting Top Grids 2 by 2 Windows")
    st.write("Follow these steps to count the panes for a Top Grids 2 by 2 Window:")

    # Original image for reference
    st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2 Window", use_container_width=True)
    # Annotated image showing counting instructions
    st.image("images/top_grids_2_by_2_count.jpg", caption="Counting the Panes", use_container_width=True)

    st.write("### Instructions")
    st.write("- Each red line represents one pane of glass.")
    st.write("- Count the number of red lines to determine the total number of panes.")
    st.write("- In this example, there are 6 red lines, so this window has **6 panes of glass**.")

    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()

# Render content for "Single Window" type
elif st.session_state.window_type_page == "single_window":
    st.title("Counting Single Windows")
    st.write("Follow these steps to count the panes for a Single Window:")

    # Original image for reference
    st.image("images/Single_window.png", caption="Single Window", use_container_width=True)
    # Annotated image showing counting instructions
    st.image("images/Single_window_counted.png", caption="Counting the Panes", use_container_width=True)

    st.write("### Instructions")
    st.write("- Each red line represents one pane of glass.")
    st.write("- Count the number of red lines to determine the total number of panes.")
    # You can adjust or add more detailed instructions if needed.

    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()
