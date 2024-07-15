import streamlit as st

# Set a password for the admin page
ADMIN_PASSWORD = "boat"

# Function to check password
def check_password():
    def password_entered():
        if st.session_state["password"] == ADMIN_PASSWORD:
            st.session_state["admin_authenticated"] = True
        else:
            st.session_state["admin_authenticated"] = False

    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    if not st.session_state["admin_authenticated"]:
        st.header("Admin")
        st.markdown("Hold deg unna du🧌", unsafe_allow_html=True)
        st.text_input("Enter Admin Password", type="password", on_change=password_entered, key="password")
        if not st.session_state["admin_authenticated"]:
            st.error("Incorrect password")
        return False
    else:
        return True

if check_password():
    st.header("Admin")
    st.write("Velkommen til innsiden.")
    # Add your admin functionalities here
