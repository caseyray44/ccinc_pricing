import streamlit as st

# Initialize session state for navigation
if "window_type_page" not in st.session_state:
    st.session_state.window_type_page = "main"

# Main page content
if st.session_state.window_type_page == "main":
    st.title("How to Count Windows")
    st.write("Click on a window type to learn how to count its panes.")

    # Create a grid layout with 3 columns (we'll adjust this later for more images)
    cols = st.columns(3)

    # Add the first image in the first column
    with cols[0]:
        st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2", use_container_width=True)
        if st.button("Select", key="top_grids_2_by_2"):
            st.session_state.window_type_page = "top_grids_2_by_2"
            st.rerun()

# Render the Top Grids 2 by 2 page content directly
elif st.session_state.window_type_page == "top_grids_2_by_2":
    st.title("Counting Top Grids 2 by 2 Windows")
    st.write("Follow these steps to count the panes for a Top Grids 2 by 2 Window:")

    # Display the original image for reference
    st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2 Window", use_container_width=True)

    # Display the annotated image to show how to count panes
    st.image("images/top_grids_2_by_2_count.jpg", caption="Counting the Panes", use_container_width=True)

    # Instructions
    st.write("### Instructions")
    st.write("- Each red line represents one pane of glass.")
    st.write("- Count the number of red lines to determine the total number of panes.")
    st.write("- In this example, there are 6 red lines, so this window has **6 panes of glass**.")

    # Back button to return to the main "How to Count Windows" page
    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()
