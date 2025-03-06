import streamlit as st
from datetime import datetime, timedelta

def render_dashboard():
    """Affiche les éléments principaux du tableau de bord."""
    # Affichage de l'état
    st.subheader("État du système")
    col1, col2, col3 = st.columns(3)
    with col1:
        status = "✅ Actif" if st.session_state.is_running else "⏹️ Inactif"
        st.metric("Statut", status)
    with col2:
        interval = f"Toutes les {st.session_state.interval_minutes} minutes" if st.session_state.is_running else "Non configuré"
        st.metric("Intervalle", interval)
    with col3:
        if st.session_state.is_running and st.session_state.last_check_time:
            next_time = st.session_state.last_check_time + timedelta(minutes=st.session_state.interval_minutes)
            next_check = next_time.strftime("%d/%m/%Y %H:%M:%S")
        else:
            next_check = "Non planifié"
        st.metric("Prochaine vérification", next_check)

    # Affichage des dernières vérifications
    if st.session_state.last_check:
        st.info(f"Dernière vérification effectuée le {st.session_state.last_check}")

    # Affichage des logs
    st.subheader("Journaux d'activité")
    log_container = st.container()
    with log_container:
        for log in reversed(st.session_state.log_messages):
            st.text(log)

    # Instructions
    with st.expander("Instructions d'utilisation"):
        st.markdown("""
        ### Comment utiliser cette application
        
        1. **Configuration de l'email**
           - Renseignez l'adresse email qui servira à envoyer les notifications
           - Saisissez le mot de passe de cette adresse email (pour Gmail, utilisez un mot de passe d'application)
           - Indiquez l'adresse email qui recevra les notifications
           
        2. **Vérifications périodiques**
           - Réglez l'intervalle de vérification souhaité (par défaut: 5 minutes)
           - Cliquez sur "Activer les vérifications" pour démarrer le processus automatique
           - L'application n'enverra un email que lorsqu'elle trouvera des items disponibles
           - **Important**: Gardez l'onglet du navigateur ouvert pour les vérifications automatiques
           
        3. **Vérification manuelle**
           - Vous pouvez cliquer sur "Vérifier maintenant" pour forcer une vérification immédiate
           
        4. **Surveillance**
           - Les journaux d'activité vous permettent de suivre les opérations effectuées
           - L'application recharge automatiquement la page pour maintenir les vérifications actives
        """)