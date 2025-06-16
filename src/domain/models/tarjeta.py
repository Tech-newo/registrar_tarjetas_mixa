from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass
class MedioPago:
    id:str
    id_empresa: Optional[UUID]
    numero_tarjeta: str
    cvc: str
    mes_vencimiento: str
    anio_vencimiento: str
    nombre_titular: str
    email:str
    
