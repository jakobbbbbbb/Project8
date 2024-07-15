import streamlit as st
from registrerResult import users_df, nicknames, get_user_stats, get_head_to_head_stats, get_all_users_stats
import plotly.graph_objects as go

# Additional section for user stats
st.markdown("<h3>🥇Brukerstatistikk</h3>", unsafe_allow_html=True)

selected_user = st.selectbox('Se statistikk for bruker', nicknames, placeholder='Velg en bruker', key='selected_user')
selected_user_id = users_df[users_df['nick_name'] == selected_user]['id'].values[0]

wins, losses = get_user_stats(selected_user_id)
total_games = wins + losses
win_rate = (wins / total_games) * 100 if total_games > 0 else 0

# Display win/loss stats
st.write(f'{selected_user} har {wins} seiere og {losses} tap.')

# Display win rate as styled text
st.markdown(f"Seiersprosent: {win_rate:.2f}%")
st.divider()
opponent = st.selectbox('Sammenlign med en motstander', nicknames, index = 1, placeholder='Velg motstander',key='opponent')
if opponent != selected_user:
    opponent_id = users_df[users_df['nick_name'] == opponent]['id'].values[0]
    head_to_head_wins, head_to_head_losses = get_head_to_head_stats(selected_user_id, opponent_id)
    total_head_to_head_games = head_to_head_wins + head_to_head_losses
    head_to_head_win_rate = (head_to_head_wins / total_head_to_head_games) * 100 if total_head_to_head_games > 0 else 0
    st.write(f'{selected_user} har {head_to_head_wins} seiere og {head_to_head_losses} tap mot {opponent}.')
    st.write(f'Vinnerprosent mot {opponent}: {head_to_head_win_rate:.1f}%')
else:
    st.error('Idiot, velg en annen motstander enn deg selv.')
st.divider()
# Podium for top 3 players
st.markdown("<h3> Topp 3 👑</h3>", unsafe_allow_html=True)

stats_df = get_all_users_stats()
top_3 = stats_df.nlargest(3, 'win_rate')

fig = go.Figure()
fig.add_trace(go.Bar(
    x=top_3['nick_name'],
    y=top_3['win_rate'],
    text=top_3['win_rate'].apply(lambda x: f'{x:.2f}%'),
    textposition='auto',
    marker_color=['gold', 'silver', '#cd7f32'],  # Colors for 1st, 2nd, and 3rd place
))

fig.update_layout(
    xaxis_title='Spillere',
    yaxis_title='Seiersprosent',
    yaxis_range=[0, 100]
)

st.plotly_chart(fig)
