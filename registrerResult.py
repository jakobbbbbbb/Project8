import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

# Initialize database engine
engine = create_engine('sqlite:///billiards.db')

# Function to create the results table if it doesn't exist
def create_results_table(engine):
    meta = MetaData()
    results = Table(
        'results', meta,
        Column('id', Integer, primary_key=True),
        Column('winner_id', Integer, nullable=False, index=True),
        Column('loser_id', Integer, nullable=False, index=True),
        Column('date', String)
    )
    meta.create_all(engine)

# Call the function to create the table
create_results_table(engine)

# Define the database interaction functions
def add_result(winner_id, loser_id):
    result_data = pd.DataFrame({'winner_id': [winner_id], 'loser_id': [loser_id], 'date': [pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')]})
    result_data.to_sql('results', con=engine, if_exists='append', index=False)
    st.experimental_rerun()  # Rerun to refresh data

def get_users():
    query = "SELECT * FROM users"
    return pd.read_sql(query, con=engine)

def get_user_stats(user_id):
    wins_query = f"SELECT COUNT(*) AS wins FROM results WHERE winner_id = {user_id}"
    losses_query = f"SELECT COUNT(*) AS losses FROM results WHERE loser_id = {user_id}"

    wins = pd.read_sql(wins_query, con=engine).iloc[0]['wins']
    losses = pd.read_sql(losses_query, con=engine).iloc[0]['losses']

    return wins, losses

def get_all_users_stats():
    users = get_users()
    stats = []
    for index, user in users.iterrows():
        user_id = user['id']
        nick_name = user['nick_name']
        wins, losses = get_user_stats(user_id)
        total_games = wins + losses
        win_rate = (wins / total_games) * 100 if total_games > 0 else 0
        stats.append({'nick_name': nick_name, 'win_rate': win_rate})
    return pd.DataFrame(stats)

def get_head_to_head_stats(user_id, opponent_id):
    wins_query = f"SELECT COUNT(*) AS wins FROM results WHERE winner_id = {user_id} AND loser_id = {opponent_id}"
    losses_query = f"SELECT COUNT(*) AS losses FROM results WHERE loser_id = {user_id} AND winner_id = {opponent_id}"

    wins = pd.read_sql(wins_query, con=engine).iloc[0]['wins']
    losses = pd.read_sql(losses_query, con=engine).iloc[0]['losses']

    return wins, losses

# Streamlit app
st.header("Registrer resultat")

# Fetch users from the database
users_df = get_users()
nicknames = users_df['nick_name'].tolist()

with st.form(key='Add new result'):
    winner = st.selectbox('Hvem vant?', nicknames, index=None, placeholder='Velg en vinner', key='winner')
    loser = st.selectbox('Hvem tapte?', nicknames, index=None, placeholder='Velg en taper', key='loser')
    submit_result = st.form_submit_button(label='Registrer resultat')

    if submit_result:
        if winner != loser:
            winner_id = users_df[users_df['nick_name'] == winner]['id'].values[0]
            loser_id = users_df[users_df['nick_name'] == loser]['id'].values[0]
            add_result(winner_id, loser_id)
            st.success('Resultatet er registrert!')
        else:
            st.error('Idiot, en spiller kan ikke spille mot seg selv.')

