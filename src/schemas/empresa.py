from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class SEmpresa (BaseModel):
    id: UUID
    razon_social: str
    identificacion: str
    persona_juridica: bool
    correo: str
    celular: str
    activo: bool
    codigo_validacion: Optional[str]
    fecha_creacion: int  # timestamp en segundos
    fecha_actualizacion: int  # timestamp en segundos
    fecha_expiracion_codigo_validacion: Optional[int]  # timestamp en segundos
