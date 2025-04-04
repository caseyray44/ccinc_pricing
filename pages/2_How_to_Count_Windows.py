import streamlit as st

# Inject custom CSS to improve image layout
st.markdown(
    """
    <style>
    /* Style for the image containers */
    .image-container {
        text-align: center;
        padding: 15px;
        min-height: 300px; /* Ensure enough vertical space */
    }

    /* Style for the images */
    .image-container img {
        min-width: 300px; /* Minimum width to ensure images aren't too small */
        max-width: 100%; /* Ensure images scale down on smaller screens */
        height: auto; /* Maintain aspect ratio */
        object-fit: contain; /* Ensure the entire image is visible */
    }

    /* Style for the buttons */
    .stButton > button {
        width: 100%; /* Make buttons full width of the column */
        margin-top: 10px; /* Add spacing above the button */
    }

    /* Adjust column spacing and width */
    .stColumns > div {
        padding: 15px; /* Increased padding between columns */
        flex: 1 1 50%; /* Adjust column width to 50% for 2-column layout */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for navigation
if "window_type_page" not in st.session_state:
    st.session_state.window_type_page = "main"

# Main page content
if st.session_state.window_type_page == "main":
    st.title("How to Count Windows")
    st.write("Click on a window type to learn how to count its panes.")

    # Create a 2x2 grid layout with two rows of two columns each
    # First row
    row1_cols = st.columns(2)

    # Top Grids 2 by 2 in the first column of the first row
    with row1_cols[0]:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2", use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Select", key="top_grids_2_by_2"):
            st.session_state.window_type_page = "top_grids_2_by_2"
            st.rerun()

    # Single Window in the second column of the first row
    with row1_cols[1]:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("images/single_window.jpg", caption="Single Window", use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Select", key="single_window"):
            st.session_state.window_type_page = "single_window"
            st.rerun()

    # Second row
    row2_cols = st.columns(2)

    # Sliding Glass Door in the first column of the second row
    with row2_cols[0]:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("images/slidinsliding_glass_door.jpg", caption="Sliding Glass Door", use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Select", key="sliding_glass_door"):
            st.session_state.window_type_page = "sliding_glass_door"
            st.rerun()

    # Frenchie in the second column of the second row
    with row2_cols[1]:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image("images/frenchie.jpg", caption="Frenchie", use_container_width=False)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Select", key="frenchie"):
            st.session_state.window_type_page = "frenchie"
            st.rerun()

# Render the Top Grids 2 by 2 page content
elif st.session_state.window_type_page == "top_grids_2_by_2":
    st.title("Counting Top Grids 2 by 2 Windows")
    st.write("Follow these steps to count the panes for a Top Grids 2 by 2 Window:")

    # Display the original image for reference
    st.image("images/top_grids_2_by_2.jpg", caption="Top Grids 2 by 2 Window", use_container_width=False)
    st.image("images/top_grids_2_by_2_count.jpg", caption="Counting the Panes", use_container_width=False)

    # Instructions
    st.write("### Instructions")
    st.write("- Each red line represents one pane of glass.")
    st.write("- Count the number of red lines to determine the total number of panes.")
    st.write("- In this example, there are 6 red lines, so this window has **6 panes of glass**.")

    # Back button to return to the main "How to Count Windows" page
    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()

# Render the Single Window page content
elif st.session_state.window_type_page == "single_window":
    st.title("Counting Single Windows")
    st.write("Follow these steps to count the panes for a Single Window:")

    # Display the annotated image to show how to count panes
    st.image("images/single_window_counted.png", caption="Counting the Panes", use_container_width=False)

    # Instructions for the counted image
    st.write("### Instructions")
    st.write("- This is a single window. The red lines equal one pane of glass.")
    st.write("- In this example, there’s **1 pane of glass**.")

    # Display the divided image with a note
    st.image("images/single_window_divided.jpg", caption="Divided Single Window", use_container_width=False)
    st.write("- If the windows are large, the panes of glass will be divided such as in this example.")
    st.write("- In this example, this is **three panes of glass**.")

    # Back button to return to the main "How to Count Windows" page
    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()

# Render the Sliding Glass Door page content
elif st.session_state.window_type_page == "sliding_glass_door":
    st.title("Counting Sliding Glass Doors")
    st.write("Follow these steps to count the panes for a Sliding Glass Door:")

    # Display the annotated image to show how to count panes
    st.image("images/slidinsliding_glass_door_count.jpg", caption="Counting the Panes", use_container_width=False)

    # Instructions
    st.write("### Instructions")
    st.write("- Doors we break into two panes of glass. The blue line represents the split and the red lines represent each pane of glass.")
    st.write("- In this example, there are **8 panes of glass**.")

    # Back button to return to the main "How to Count Windows" page
    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()

# Render the Frenchie page content
elif st.session_state.window_type_page == "frenchie":
    st.title("Counting French Windows")
    st.write("**Important Note:** When counting French windows and the entire house consists of French windows, you must reduce the total pane count by 10% after completing the count. For example, if the total is 16 panes, the adjusted count is 14.4 panes, which we round down to 14.")
    st.write("Follow these steps to count the panes for a French Window:")

    # Display the annotated image to show how to count panes
    st.image("images/frenchie_counted.jpg", caption="Counting the Panes", use_container_width=False)

    # Instructions
    st.write("### Instructions")
    st.write("- Most of the time, depending on size, for Frenchies, 2 panes of glass count as one. All the red lines represent one pane of glass.")
    st.write("- In this example, there are **16 panes of glass** to be accounted for.")

    # Back button to return to the main "How to Count Windows" page
    if st.button("Back to Window Types"):
        st.session_state.window_type_page = "main"
        st.rerun()
