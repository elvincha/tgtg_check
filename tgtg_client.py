import os
import json
from tgtg import TgtgClient
from utils.logger import log_message
import streamlit as st
from config import CREDENTIALS_FILE

def save_credentials(credentials):
    """Sauvegarde les credentials dans un fichier JSON."""
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(credentials, file)

def load_credentials():
    """Charge les credentials depuis un fichier JSON si disponible."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return None

def get_tgtg_client():
    """Récupère ou actualise les credentials automatiquement."""
    credentials = load_credentials()
    
    if credentials:
        log_message("🔄 Chargement des credentials existants...")
        client = TgtgClient(
            access_token=credentials["access_token"],
            refresh_token=credentials["refresh_token"],
            cookie=credentials["cookie"]
        )
        try:
            # Vérifier si le token est toujours valide en testant une requête
            client.get_items()
            log_message("✅ Credentials valides.")
            return client
        except Exception as e:
            log_message(f"⚠️ Token expiré ou invalide : {str(e)}")
            log_message("🔄 Tentative de rafraîchissement...")
            new_credentials = client.refresh_token()  # Rafraîchit le token
            save_credentials(new_credentials)  # Sauvegarde les nouveaux credentials
            return TgtgClient(**new_credentials)
    
    else:
        log_message("🆕 Aucun credentials trouvé, authentification requise.")
        email = st.session_state.email_recipient
        log_message(f"🔑 Demande d'authentification pour {email}...")
        
        # Ici, nous allons ouvrir une boîte de dialogue pour l'authentification interactive
        client = TgtgClient(email=email)
        credentials = client.get_credentials()  # Demande les nouveaux credentials
        save_credentials(credentials)  # Sauvegarde des credentials
        log_message("✅ Authentification réussie et credentials sauvegardés.")
        return client

def first_auth_ui():
    """Interface utilisateur pour la première authentification."""
    if not os.path.exists(CREDENTIALS_FILE) and st.session_state.email_recipient:
        with st.expander("Première authentification TGTG", expanded=True):
            st.warning("Aucun fichier de credentials TGTG trouvé. Une première authentification est nécessaire.")
            if st.button("Effectuer l'authentification TGTG"):
                try:
                    get_tgtg_client()
                    st.success("Authentification réussie ! Les credentials ont été sauvegardés.")
                    
                except Exception as e:
                    st.error(f"Erreur d'authentification : {str(e)}")