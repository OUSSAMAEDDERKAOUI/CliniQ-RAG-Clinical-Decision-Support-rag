import streamlit as st
from components.api import login

def require_auth():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "username" not in st.session_state:
        st.session_state.username = None

    if st.session_state.token:
        return True

    st.title("CliniQ — Connexion")
    with st.form("login_form"):
        username = st.text_input("Nom d'utilisateur")  
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

    if submitted:
        try:
            token = login(username, password)
            st.session_state.token = token
            st.session_state.username = username  
            st.success("Connecté ✅")
            st.rerun()
        except Exception as e:
            st.error(f"Échec de connexion : {e}")

    return False

def logout_button():
    if st.button("Se déconnecter"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()