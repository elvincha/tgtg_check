import streamlit as st
from datetime import datetime

def log_message(message):
    """
    Ajoute un message horodaté au journal d'activité
    
    Args:
        message (str): Le message à journaliser
    """
    # Ajouter un timestamp au message
    timestamp = datetime.now().strftime("%H:%M:%S")
    full_message = f"[{timestamp}] {message}"
    st.session_state.log_messages.append(full_message)
    
    # Limiter le nombre de messages dans les logs
    if len(st.session_state.log_messages) > 100:
        st.session_state.log_messages = st.session_state.log_messages[-100:]