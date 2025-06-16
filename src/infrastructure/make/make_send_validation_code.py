import os
import requests

url = os.getenv('MAKE_WH_SEND_CODIGO_VALIDACION')

def send_validation_code(email:str, code:str):
    
    header={'Content-Type': 'application/json'}
    data = {
        'email':email,
        'code':code
    }
    
    requests.post(url, headers=header, json=data)