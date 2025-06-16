from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class SMedioPago(BaseModel):
    id: UUID
    empresa_id: Optional[UUID]
    correo_titular: Optional[str]
    token: Optional[str]
    cuotas: Optional[int]
    favorito: Optional[bool]
    activo: Optional[bool]
    fecha_creacion: Optional[int]
    fecha_actualizacion: Optional[int]
