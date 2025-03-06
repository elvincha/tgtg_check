import streamlit as st
import time
from datetime import datetime, timedelta

# Import des modules du projet
from config import init_session_state, setup_page
from tgtg_client import first_auth_ui
from stock_checker import check_and_notify
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard

def main():
    # Initialisation de l'application
    init_session_state()
    setup_page()
    
    # Affichage de l'interface
    render_sidebar()
    render_dashboard()
    
    # Vérifier la première authentification
    first_auth_ui()
    
    if st.session_state.is_running:
        now = datetime.now()
        check_and_notify()  # Exécuter la vérification
        time.sleep(st.session_state.interval_minutes * 60)  # Attendre le nombre de minutes spécifié
        st.rerun()  # Relancer l'application
        print(now)    
      

if __name__ == "__main__":
    main()