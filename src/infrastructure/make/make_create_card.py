import os
import requests
from src.domain.models import MedioPago, Empresa
from dataclasses import asdict

url = os.getenv('MAKE_WH_CREATE_CARD')

def create_card(empresa:Empresa, card:MedioPago):
    
    header={'Content-Type': 'application/json'}
    data = {
        'empresa':asdict(empresa),
        'card':asdict(card)
    }
    
    requests.post(url, headers=header, json=data)