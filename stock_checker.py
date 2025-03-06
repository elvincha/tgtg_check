import streamlit as st
from datetime import datetime, timedelta
import time
from utils.logger import log_message
from tgtg_client import get_tgtg_client
from email_service import send_email
from email_service import send_msg_instagram
def check_stock(data):
    """
    Analyse les données pour identifier les boutiques avec et sans stock.
    
    Args:
        data (list): Liste d'items TGTG
        
    Returns:
        tuple: (contenu_email, disponibilité)
    """
    stores_with_stock = []
    stores_without_stock = []
    
    for item_data in data:
        item_tags = item_data.get('item_tags', [])
        items_available = item_data.get('items_available', 0)
        store_name = item_data.get('store', {}).get('store_name', 'Unknown Store')
        store_id = item_data.get('store', {}).get('store_id', 'Unknown ID')

        # Vérifier si des items sont disponibles
        if items_available > 0:
            for tag in item_tags:
                if tag.get('short_text') and tag.get('short_text') != 'Nothing today':
                    stores_with_stock.append(f"Boutique: {store_name} (ID: {store_id})")
                    break
        else:
            stores_without_stock.append(f"Boutique: {store_name} (ID: {store_id})")

    email_content = ""

    if stores_with_stock:
        email_content += "Boutiques avec des items disponibles :\n"
        for store in stores_with_stock:
            email_content += f"  - {store}\n"
    else:
        email_content += "Aucune boutique avec des items disponibles.\n"
    
    if stores_without_stock:
        email_content += "\nBoutiques sans stock actuellement :\n"
        for store in stores_without_stock:
            email_content += f"  - {store}\n"
    else:
        email_content += "\nToutes les boutiques ont du stock."

    return email_content, len(stores_with_stock) > 0

def check_and_notify():
    """
    Vérifie les offres TGTG et envoie une notification si nécessaire.
    """
    try:
        # Mise à jour de la dernière vérification
        now = datetime.now()
        st.session_state.last_check = now.strftime("%d/%m/%Y %H:%M:%S")
        st.session_state.last_check_time = now
        
        log_message(f"🔍 Vérification des offres TGTG à {st.session_state.last_check}...")
        
        # Initialisation du client TGTG
        client = get_tgtg_client()
        
        # Récupérer les items favoris
        log_message("📋 Récupération des favoris...")
        favorites = client.get_favorites()
        
        # Vérifier le stock
        log_message("🔢 Analyse du stock...")
        stock_info, has_available_items = check_stock(favorites)
        
        # Envoyer l'email seulement s'il y a des items disponibles
        if has_available_items:
            log_message("🍽️ Items disponibles! Envoi d'une notification...")
            send_msg_instagram(
                st.session_state.insta_username,
                st.session_state.insta_password,
                st.session_state.recipient_username,
                stock_info)
                #arreter le script 
            subject = f"Alerte TGTG - Items disponibles - {now.strftime('%d/%m/%Y %H:%M')}"
            send_email(
            subject, 
            stock_info, 
            st.session_state.email_sender, 
            st.session_state.email_password, 
            st.session_state.email_recipient
        ) 
            st.write("The condition was met, stopping execution here")
            st.stop()

        else:
            log_message("😕 Aucun item disponible pour le moment.")
            
        subject = f"Alerte TGTG - Items disponibles - {now.strftime('%d/%m/%Y %H:%M')}"
        send_email(
            subject, 
            stock_info, 
            st.session_state.email_sender, 
            st.session_state.email_password, 
            st.session_state.email_recipient
        ) 
        
        log_message("✅ Vérification complète")
        
        # Calculer et stocker la prochaine vérification
        next_check_time = now + timedelta(minutes=st.session_state.interval_minutes)
        st.session_state.next_check = next_check_time.strftime("%d/%m/%Y %H:%M:%S")
        
    except Exception as e:
        log_message(f"❌ Erreur lors de la vérification : {str(e)}")