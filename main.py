import streamlit as st
# Main menu for Project 8

st.set_page_config(
    page_title="Project 8X",
    page_icon="/Users/jakobrudeovstaas/Project 8X/logo2.png",  # Update this path to your favicon file
    layout="centered",
    initial_sidebar_state="expanded",
)


pg = st.navigation([
    st.Page("mainMenu.py", title = 'Hovedmeny', icon = ':material/home:'),
    st.Page("addUsers.py", title = 'Ny bruker', icon = ':material/person_add:'),
    st.Page("registrerResult.py", title = 'Registrer resultat', icon = ':material/exposure_plus_1:'),
    st.Page("stats.py", title = 'Statistikk', icon = ':material/trophy:'),
    st.Page("admin.py", title = 'Admin', icon = ':material/admin_panel_settings:')
])

pg.run()