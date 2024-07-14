import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
import plotly.graph_objects as go

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

def get_users():
    query = "SELECT * FROM users"
    return pd.read_sql(query, con=engine)

def get_user_stats(user_id):
    wins_query = f"SELECT COUNT(*) AS wins FROM results WHERE winner_id = {user_id}"
    losses_query = f"SELECT COUNT(*) AS losses FROM results WHERE loser_id = {user_id}"

    wins = pd.read_sql(wins_query, con=engine).iloc[0]['wins']
    losses = pd.read_sql(losses_query, con=engine).iloc[0]['losses']

    return wins, losses

def get_head_to_head_stats(user_id, opponent_id):
    wins_query = f"SELECT COUNT(*) AS wins FROM results WHERE winner_id = {user_id} AND loser_id = {opponent_id}"
    losses_query = f"SELECT COUNT(*) AS losses FROM results WHERE loser_id = {user_id} AND winner_id = {opponent_id}"

    wins = pd.read_sql(wins_query, con=engine).iloc[0]['wins']
    losses = pd.read_sql(losses_query, con=engine).iloc[0]['losses']

    return wins, losses

# Streamlit app
st.header("Registrer Resultat")

# Fetch users from the database
users_df = get_users()
nicknames = users_df['nick_name'].tolist()

with st.form(key='Add new result'):
    winner = st.selectbox('Hvem vant?', nicknames, index=0, key='winner')
    loser = st.selectbox('Hvem tapte?', nicknames, index=1, key='loser')
    submit_result = st.form_submit_button(label='Registrer resultat')

    if submit_result:
        if winner != loser:
            winner_id = users_df[users_df['nick_name'] == winner]['id'].values[0]
            loser_id = users_df[users_df['nick_name'] == loser]['id'].values[0]
            add_result(winner_id, loser_id)
            st.success('Resultatet er registrert!')
        else:
            st.error('Idiot, en spiller kan ikke spille mot seg selv.')

# Display all results in the database for verification
results_df = pd.read_sql('SELECT * FROM results', con=engine)

# Additional section for user stats
st.header("Brukerstatistikk")

selected_user = st.selectbox('Velg bruker for statistikk', nicknames, key='selected_user')
selected_user_id = users_df[users_df['nick_name'] == selected_user]['id'].values[0]

wins, losses = get_user_stats(selected_user_id)
total_games = wins + losses
win_rate = (wins / total_games) * 100 if total_games > 0 else 0

# Display win/loss stats
st.write(f'{selected_user} har {wins} seiere og {losses} tap.')

# Display win rate as a gauge chart
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=win_rate,
    title={'text': "Seiersprosent"},
    gauge={'axis': {'range': [0, 100]},
           'bar': {'color': "darkblue"},
           'steps': [
               {'range': [0, 50], 'color': "lightgray"},
               {'range': [50, 100], 'color': "gray"}]}))

st.plotly_chart(fig)

opponent = st.selectbox('Velg en motstander du vil sammenligne deg med', nicknames, key='opponent')
if opponent != selected_user:
    opponent_id = users_df[users_df['nick_name'] == opponent]['id'].values[0]
    head_to_head_wins, head_to_head_losses = get_head_to_head_stats(selected_user_id, opponent_id)
    total_head_to_head_games = head_to_head_wins + head_to_head_losses
    head_to_head_win_rate = (head_to_head_wins / total_head_to_head_games) * 100 if total_head_to_head_games > 0 else 0
    st.write(f'{selected_user} har {head_to_head_wins} seiere og {head_to_head_losses} tap mot {opponent}.')
    st.write(f'Vinnerprosent mot {opponent}: {head_to_head_win_rate:.2f}%')
else:
    st.error('Idiot, velg en annen motstander enn deg selv.')
