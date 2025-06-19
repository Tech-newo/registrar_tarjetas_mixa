from src.infrastructure.db import SupabaseConn
from datetime import timedelta
from src.utils import get_current_epoch_seconds, add_timedelta_and_get_epoch_seconds

db_conn = SupabaseConn()
db_exec = db_conn.connect()
 
def set_validation_code_func(validation_code:str, indentificacion:str):
    
    try:
        data = {
            'codigo_validacion':validation_code,
            'fecha_expiracion_codigo_validacion':add_timedelta_and_get_epoch_seconds(timedelta(minutes=10)),
            'fecha_actualizacion':get_current_epoch_seconds()
        }
        print('updating', data)
        
        db_exec.table('empresa').update(data).eq('identificacion', indentificacion).execute()
        
        return
    except Exception as e:
        print(e)