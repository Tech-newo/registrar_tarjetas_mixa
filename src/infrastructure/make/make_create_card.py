import os
import requests
from src.domain.models import MedioPago, Empresa
from dataclasses import asdict

url = os.getenv('MAKE_WH_CREATE_CARD')

def create_card(empresa: Empresa, card: MedioPago):
    """Create a card for a company by calling the external service"""
    headers = {"Content-Type": "application/json"}
    payload = {
        "empresa": asdict(empresa),
        "card": asdict(card)
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # Retornamos el objeto Response completo
    return response.status_code
