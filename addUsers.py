import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from supplyInfo import counties

# Initialize database engine
engine = create_engine('sqlite:///billiards.db')

# Function to create the users table if it doesn't exist
def create_users_table(engine):
    meta = MetaData()
    users = Table(
        'users', meta,
        Column('id', Integer, primary_key=True),
        Column('user_name', String, unique=True, nullable=False),
        Column('nick_name', String),
        Column('county', String)
    )
    meta.create_all(engine)

# Call the function to create the table
create_users_table(engine)

# Define the database interaction functions
def addUser(user_name, nick_name, county):
    user_data = pd.DataFrame({'user_name': [user_name], 'nick_name': [nick_name], 'county': [county]})
    user_data.to_sql('users', con=engine, if_exists='append', index=False)

def checkUser(user_name, nick_name):
    query = f"SELECT * FROM users WHERE user_name='{user_name}' AND nick_name='{nick_name}'"
    result = pd.read_sql(query, con=engine)
    return not result.empty

def wipe_database(engine):
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)
    create_users_table(engine)  # Recreate the table after wiping

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
st.sidebar.subheader("Legg til ny bruker")

with st.sidebar.form(key='Add new user'):
    name = st.text_input("Fullt navn", placeholder='Skriv navn her', value=st.session_state['name'], key='name_input')
    nickName = st.text_input("Legg til kallenavn", placeholder='Skriv kallenavn her', value=st.session_state['nickName'], key='nickName_input')
    county = st.selectbox('Velg fylke', counties, index=counties.index(st.session_state['county']), placeholder='Velg fra liste', key='county_select')
    submitButton = st.form_submit_button(label='Legg til')

    if submitButton:
        if name and nickName and county:
            if checkUser(name, nickName):
                st.sidebar.error('Brukeren finnes allerede.')
            else:
                addUser(name, nickName, county)
                st.session_state['submitted'] = True
                st.session_state['name'] = ''
                st.session_state['nickName'] = ''
                st.session_state['county'] = counties[0]
                st.experimental_rerun()
        else:
            st.sidebar.error('Et felt mangler, skjerp deg.')

# Add a button to wipe the database
if st.sidebar.button('Wipe Database'):
    wipe_database(engine)
    st.sidebar.success('Database wiped successfully!')

# Feedback after form submission
if st.session_state['submitted']:
    st.sidebar.success('Bruker lagt til!')
    st.session_state['submitted'] = False

# Display all users in the database for verification
users_df = pd.read_sql('SELECT * FROM users', con=engine)
st.write(users_df)
