import streamlit as st



# Main menu for Project 8

st.title("Project 8X")

pg = st.navigation([
    st.Page("mainMenu.py", title = 'Hovedmeny', icon = ':material/home:'),
    st.Page("addUsers.py", title = 'Ny Bruker', icon = ':material/person_add:'),
    st.Page("registrerResult.py", title = 'Registrer Resultat', icon = ':material/exposure_plus_1:')
])

pg.run()