import streamlit as st

def app():
    # Customizing page layout
    st.markdown(
        """
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            color: #2E86C1;
            text-align: center;
        }
        .subtext {
            font-size:18px;
            color: #5D6D7E;
            text-align: center;
        }
        .container {
            padding: 20px;
            border-radius: 10px;
            background-color: #F8F9F9;
            box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Title and subtitle
    st.markdown('<p class="big-font">Welcome to Language Tutor</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtext">Enhance your language skills with tailored exercises.</p>', unsafe_allow_html=True)

    # Interactive Buttons
    st.markdown(
        """
        <div style="
            background-color: #F8F9F9; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center; 
            font-size: 22px; 
            font-weight: bold; 
            color: #2E86C1; 
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
            🚀 Choose Your Learning Path
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write("")  # Adds some spacing

    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    with col1:
        if st.button("📷 Image Comprehension", use_container_width=True):
            st.session_state["selected_page"] = "📷 Image Comprehension"
            st.rerun()

    with col2:
        if st.button("📝 Grammar & Fun", use_container_width=True):
            st.session_state["selected_page"] = "📝 Grammar & Fun"
            st.rerun()

    with col3:
        if st.button("📖 Reading & Translation", use_container_width=True):
            st.session_state["selected_page"] = "📖 Reading & Translation"
            st.rerun()

 

    # Adding footer
    st.markdown("---")
    st.markdown('<p class="subtext">🚀 Designed for IT professionals looking to refine their language skills.</p>', unsafe_allow_html=True)
