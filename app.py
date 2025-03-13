import streamlit as st
from section_type import home, image_comprehension, grammar_fun, reading_translation

PAGES = {
    "Home": home,
    "📷 Image Comprehension": image_comprehension,
    "📝 Grammar & Fun": grammar_fun,
    "📖 Reading & Translation": reading_translation
}

def main():
    # Apply enhanced sidebar styling
    st.markdown(
        """
        <style>
        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: #F8F9F9;
            padding: 20px;
        }

        /* Sidebar Title */
        .sidebar-title {
            font-size: 26px;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Sidebar Options */
        .sidebar-radio label {
            font-size: 18px;
            color: #34495E;
            font-weight: 600;
            padding: 10px;
            display: block;
            transition: 0.3s;
        }

        .sidebar-radio label:hover {
            color: #1A5276;
            transform: scale(1.05);
        }

        </style>
        """, 
        unsafe_allow_html=True
    )

    # Initialize session state
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Home"

    # Sidebar with improved styling
    st.sidebar.markdown('<p class="sidebar-title">📌 Navigation</p>', unsafe_allow_html=True)

    # Sidebar Navigation
    selection = st.sidebar.radio(
        "Choose a section:",
        list(PAGES.keys()),
        key="nav",
        index=list(PAGES.keys()).index(st.session_state["selected_page"])
    )

    # Update session state and rerun only if the selection changes
    if selection != st.session_state["selected_page"]:
        st.session_state["selected_page"] = selection
        st.rerun()

    # Load the selected page
    PAGES[st.session_state["selected_page"]].app()

    # Footer Branding
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        '<p style="text-align: center; font-size: 14px; color: gray;">🚀 Language Tutor | AI-Powered Learning</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
