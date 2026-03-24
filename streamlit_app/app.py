import os
import requests
import streamlit as st
from loguru import logger

# --- Configuration Loguru ---
# On configure le logger pour envoyer les logs du frontend dans le dossier partagé /logs
logger.add("/logs/streamlit.log", rotation="500 MB", level="INFO")

def main():
    """Gère l'interface utilisateur et la communication avec l'API.

    Récupère la valeur saisie par l'utilisateur, l'envoie à l'API via le réseau Docker
    et affiche la réponse JSON obtenue.
    """
    st.title("Interface Frontend - Monitoring")

    # On récupère l'URL de l'API depuis les variables d'environnement.
    # Dans Docker, api:8080 correspond au nom du service défini dans le Compose.
    api_url = os.getenv("API_URL", "http://api:8080")

    val = st.text_input("Saisissez une valeur à envoyer à l'API")

    if st.button("Envoyer la donnée"):
        try:
            # Appel de l'endpoint /predict de l'API en mode POST Form Data
            res = requests.post(f"{api_url}/predict", data={"data": val}, timeout=5)
            
            # Affichage de la réponse JSON de l'API
            st.success("Donnée transmise avec succès !")
            st.json(res.json())
            
            # On enregistre cet appel dans les logs pour le debugging
            logger.info(f"Appel API réussi : '{val}' envoyé à {api_url}")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Erreur lors de la communication avec l'API : {e}")
            logger.error(f"Echec de l'appel API vers {api_url} : {e}")

if __name__ == "__main__":
    main()
