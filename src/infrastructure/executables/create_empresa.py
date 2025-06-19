from src.infrastructure.db import SupabaseConn
from src.utils import get_current_epoch_seconds

db_conn = SupabaseConn()
db_exec = db_conn.connect()
 
def create_empresas_func(identificacion:str, razon_social:str, correo:str, celular:str, es_empresa:bool):
    
    data = {
        'activo':True,
        'identificacion':identificacion,
        'razon_social':razon_social,
        'correo':correo,
        'celular':celular,
        'persona_juridica':es_empresa,
        'codigo_validacion':None,
        'fecha_expiracion_codigo_validacion':None,
        'fecha_actualizacion':get_current_epoch_seconds(),
        'fecha_creacion':get_current_epoch_seconds()
    }
    print('estoy creando empresa', data)
    db_exec.table('empresa').insert(data).execute()