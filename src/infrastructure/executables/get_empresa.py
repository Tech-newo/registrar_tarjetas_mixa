from src.infrastructure.db import SupabaseConn

db_conn = SupabaseConn()
db_exec = db_conn.connect()
 
def get_empresas_func(identificacion:str):
    try:
        return db_exec.table('empresa').select('*').eq('identificacion',identificacion).execute().data
    except Exception as e:
        print(f"Error al consultar empresas: {str(e)}")
        return