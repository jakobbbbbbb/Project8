import streamlit as st
import pandas as pd
import os
from supplyInfo import counties

# File path for the Excel database
EXCEL_FILE = 'billiards_users.xlsx'

# Set a password for the admin page
ADMIN_PASSWORD = "boat"

# Function to check password
def check_password():
    def password_entered():
        if st.session_state["password"] == ADMIN_PASSWORD:
            st.session_state["admin_authenticated"] = True
        else:
            st.session_state["admin_authenticated"] = False
            st.session_state["password_attempted"] = True

    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False
        st.session_state["password_attempted"] = False

    if not st.session_state["admin_authenticated"]:
        st.header("Admin")
        st.markdown("Hold deg unna du🧌", unsafe_allow_html=True)
        st.text_input("Enter Admin Password", type="password", on_change=password_entered, key="password")
        if st.session_state["password_attempted"] and not st.session_state["admin_authenticated"]:
            st.error("Incorrect password")
        return False
    else:
        return True

# Function to fetch all users
def get_users():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    else:
        return pd.DataFrame(columns=['id', 'user_name', 'nick_name', 'county'])

# Function to update a user
def update_user(user_id, new_name, new_nick, new_county):
    df = pd.read_excel(EXCEL_FILE)
    df.loc[df['id'] == user_id, ['user_name', 'nick_name', 'county']] = [new_name, new_nick, new_county]
    df.to_excel(EXCEL_FILE, index=False)

# Function to delete a user
def delete_user(user_id):
    df = pd.read_excel(EXCEL_FILE)
    df = df[df['id'] != user_id]
    df.to_excel(EXCEL_FILE, index=False)

# Admin functionalities
if check_password():
    st.header("Admin")
    st.write("Velkommen til innsiden.")

    # Display existing users
    users = get_users()
    st.subheader("Existing Users")

    for index, user in users.iterrows():
        with st.expander(f"{user['user_name']} ({user['nick_name']})"):
            new_name = st.text_input(f"Edit Full Name for user {user['id']}", value=user['user_name'], key=f"name_{user['id']}")
            new_nick = st.text_input(f"Edit Nickname for user {user['id']}", value=user['nick_name'], key=f"nick_{user['id']}")
            new_county = st.selectbox(f"Edit County for user {user['id']}", counties, index=counties.index(user['county']), key=f"county_{user['id']}")

            if st.button("Update User", key=f"update_{user['id']}"):
                update_user(user['id'], new_name, new_nick, new_county)
                st.success(f"User {user['user_name']} updated successfully!")
                st.rerun()

            if st.button("Remove User", key=f"remove_{user['id']}"):
                delete_user(user['id'])
                st.success(f"User {user['user_name']} removed successfully!")
                st.rerun()
