import os
import streamlit as st
from datetime import datetime

# Chemin du fichier pour stocker les credentials
CREDENTIALS_FILE = "tgtg_credentials.json"

# Initialisation des variables de session
def init_session_state():
    if 'email_sender' not in st.session_state:
        st.session_state.email_sender = "elvin.cha08@gmail.com"
    if 'email_password' not in st.session_state:
        st.session_state.email_password = ""
    if 'email_recipient' not in st.session_state:
        st.session_state.email_recipient = "chaelvin30@gmail.com"
    if 'interval_minutes' not in st.session_state:
        st.session_state.interval_minutes = 1
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
    if 'last_check' not in st.session_state:
        st.session_state.last_check = None
    if 'next_check' not in st.session_state:
        st.session_state.next_check = None
    if 'log_messages' not in st.session_state:
        st.session_state.log_messages = []
    if 'last_check_time' not in st.session_state:
        st.session_state.last_check_time = None 

# Configuration de la page Streamlit
def setup_page():
    st.set_page_config(page_title="Too Good To Go Bot", page_icon="🥡", layout="wide")
    st.title("Too Good To Go - Bot de surveillance")