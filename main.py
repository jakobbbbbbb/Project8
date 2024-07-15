import streamlit as st
# Main menu for Project 8

st.title("Project 8X")

pg = st.navigation([
    st.Page("mainMenu.py", title = 'Hovedmeny', icon = ':material/home:'),
    st.Page("addUsers.py", title = 'Ny bruker', icon = ':material/person_add:'),
    st.Page("registrerResult.py", title = 'Registrer resultat', icon = ':material/exposure_plus_1:'),
    st.Page("stats.py", title = 'Statistikk', icon = ':material/trophy:'),
    st.Page("admin.py", title = 'Admin', icon = ':material/admin_panel_settings:')
])

pg.run()