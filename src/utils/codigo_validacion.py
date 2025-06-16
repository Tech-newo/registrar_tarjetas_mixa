import random

def generar_numero_validacion():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))
