import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.logger import log_message
from instagrapi import Client

def send_email(subject, body, from_email, password, to_email):
    """
    Envoie un email avec les informations fournies.
    
    Args:
        subject (str): Sujet de l'email
        body (str): Contenu de l'email
        from_email (str): Adresse email de l'expéditeur
        password (str): Mot de passe de l'expéditeur
        to_email (str): Adresse email du destinataire
        
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon
    """
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Connexion au serveur SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        log_message("📧 Email envoyé avec succès !")
        return True
    except Exception as e:
        log_message(f"❌ Erreur lors de l'envoi de l'email : {str(e)}")
        return False
    
def send_msg_instagram(username, password, recipient_username, message):

    cl = Client()
    cl.login(username, password)

    # Récupération de l'ID du destinataire
    user_id = cl.user_id_from_username(recipient_username)

    # Envoi du message
    cl.direct_send(message, [user_id])

    