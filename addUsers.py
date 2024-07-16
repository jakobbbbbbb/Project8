import streamlit as st
import pandas as pd
from supplyInfo import counties
import os

# File path for the Excel database
EXCEL_FILE = 'billiards_users.xlsx'

# Function to create the users Excel file if it doesn't exist
def create_users_excel():
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=['id', 'user_name', 'nick_name', 'county'])
        df.to_excel(EXCEL_FILE, index=False)

# Call the function to create the file
create_users_excel()

# Function to get the next available user ID
def get_next_user_id():
    df = pd.read_excel(EXCEL_FILE)
    if df.empty:
        return 1
    else:
        return df['id'].max() + 1

# Function to add a user
def addUser(user_name, nick_name, county):
    df = pd.read_excel(EXCEL_FILE)
    new_user = pd.DataFrame({
        'id': [get_next_user_id()],
        'user_name': [user_name],
        'nick_name': [nick_name],
        'county': [county]
    })
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

# Function to check if a user exists
def checkUser(user_name, nick_name):
    df = pd.read_excel(EXCEL_FILE)
    return not df[(df['user_name'] == user_name) & (df['nick_name'] == nick_name)].empty

# Function to wipe the Excel file
def wipe_database():
    df = pd.DataFrame(columns=['id', 'user_name', 'nick_name', 'county'])
    df.to_excel(EXCEL_FILE, index=False)

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if 'name' not in st.session_state:
    st.session_state['name'] = ''

if 'nickName' not in st.session_state:
    st.session_state['nickName'] = ''

if 'county' not in st.session_state:
    st.session_state['county'] = counties[0]

# Streamlit app
st.header("Brukere")
st.subheader("Legg til ny bruker")

with st.form(key='Add new user'):
    name = st.text_input("Fullt navn", placeholder='Skriv navn her', value=st.session_state['name'], key='name_input')
    nickName = st.text_input("Legg til kallenavn", placeholder='Skriv kallenavn her', value=st.session_state['nickName'], key='nickName_input')
    county = st.selectbox('Velg fylke', counties, index=None, placeholder='Velg fra liste', key='county_select')
    submitButton = st.form_submit_button(label='Legg til')

    if submitButton:
        if name and nickName and county:
            if checkUser(name, nickName):
                st.error('Brukeren finnes allerede.')
            else:
                addUser(name, nickName, county)
                st.session_state['submitted'] = True
                st.session_state['name'] = ''
                st.session_state['nickName'] = ''
                st.session_state['county'] = counties[0]
                st.rerun()
        else:
            st.error('Et felt mangler, skjerp deg.')

# Add a button to wipe the database
if st.button('Wipe Database'):
    wipe_database()
    st.success('Database wiped successfully!')

# Feedback after form submission
if st.session_state['submitted']:
    st.success('Bruker lagt til!')
    st.session_state['submitted'] = False
