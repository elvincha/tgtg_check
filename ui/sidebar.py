import streamlit as st
from utils.logger import log_message
from stock_checker import check_and_notify
from tgtg_client import get_tgtg_client
def render_sidebar():
    """Affiche les éléments de la sidebar."""
    st.sidebar.header("Configuration")

    # Paramètres d'email
    with st.sidebar.expander("Paramètres d'email", expanded=True):
        st.session_state.email_sender = st.text_input("Email expéditeur", st.session_state.email_sender)
        st.session_state.email_password = st.text_input("Mot de passe", st.session_state.email_password, type="password")
        st.session_state.email_recipient = st.text_input("Email destinataire", st.session_state.email_recipient)

    with st.sidebar.expander("Paramètres Instagram", expanded=True):
        st.session_state.insta_username = st.text_input("Nom d'utilisateur Instagram")
        st.session_state.insta_password = st.text_input("Mot de passe Instagram", type="password")
        st.session_state.recipient_username = st.text_input("Nom d'utilisateur du destinataire")
       


    # Paramètres de vérification
    with st.sidebar.expander("Paramètres de vérification", expanded=True):
        st.session_state.interval_minutes = st.slider("Intervalle de vérification (minutes)", 
                                                    min_value=1, 
                                                    max_value=60, 
                                                    value=st.session_state.interval_minutes,
                                                    step=1)
        
        # Boutons pour démarrer/arrêter la vérification
        col1, col2 = st.columns(2)
        
        with col1:
            if not st.session_state.is_running:
                if st.button("Activer les vérifications"):
                    if st.session_state.email_password:
                        st.session_state.is_running = True
                        log_message(f"🔄 Vérifications activées toutes les {st.session_state.interval_minutes} minutes")
                        # La première vérification sera déclenchée par le code dans main.py
                        st.rerun()
                    else:
                        st.error("Veuillez saisir le mot de passe de l'email expéditeur.")
        
        with col2:
            if st.session_state.is_running:
                if st.button("Désactiver les vérifications"):
                    st.session_state.is_running = False
                    log_message("⏹️ Vérifications désactivées")
                    st.session_state.next_check = None

    # Exécution manuelle
    if st.sidebar.button("Vérifier maintenant"):
        if st.session_state.email_password:
            check_and_notify()
            st.rerun()
        else:
            st.sidebar.error("Veuillez saisir le mot de passe de l'email expéditeur.")