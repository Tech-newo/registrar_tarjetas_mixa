from src.infrastructure.db import SupabaseConn
from src.utils import get_current_epoch_seconds
import logging

# Configuración de logging
logger = logging.getLogger(__name__)

# Conexión a Supabase
db_conn = SupabaseConn()
db_exec = db_conn.connect()

class BinService:
    """
    Servicio para gestionar la tabla 'bin' en Supabase.
    """

    @staticmethod
    def insert_bin(prefijo: str, tipo: str, marca: str, categoria: str = None,
                   banco: str = None, pais_nombre: str = None, pais_codigo: str = None, fuente: str = "externa"):
        """
        Inserta un BIN en la tabla. Si ya existe, falla por la constraint única.
        """
        logger.info("Insertando nuevo BIN - Prefijo: %s, Tipo: %s, Marca: %s", prefijo, tipo, marca)
        
        try:
            data = {
                "prefijo": prefijo,
                "tipo": tipo,
                "marca": marca,
                "categoria": categoria,
                "banco": banco,
                "pais_nombre": pais_nombre,
                "pais_codigo": pais_codigo,
                "fuente": fuente,
                "fecha_creacion": get_current_epoch_seconds(),
                "fecha_actualizacion": get_current_epoch_seconds()
            }
            
            logger.debug("Datos a insertar: %s", data)
            response = db_exec.table("bin").insert(data).execute()
            logger.info("BIN insertado exitosamente - Prefijo: %s", prefijo)
            return response
            
        except Exception as e:
            logger.error("Error al insertar BIN %s: %s", prefijo, str(e), exc_info=True)
            raise

    @staticmethod
    def upsert_bin(prefijo: str, tipo: str, marca: str, categoria: str = None,
                   banco: str = None, pais_nombre: str = None, pais_codigo: str = None, fuente: str = "externa"):
        """
        Inserta o actualiza un BIN si ya existe.
        """
        logger.info("Upsert BIN - Prefijo: %s, Tipo: %s, Marca: %s", prefijo, tipo, marca)
        
        try:
            data = {
                "prefijo": prefijo,
                "tipo": tipo,
                "marca": marca,
                "categoria": categoria,
                "banco": banco,
                "pais_nombre": pais_nombre,
                "pais_codigo": pais_codigo,
                "fuente": fuente,
                "fecha_actualizacion": get_current_epoch_seconds()
            }
            
            logger.debug("Datos para upsert: %s", data)
            response = db_exec.table("bin").upsert(data).execute()
            logger.info("BIN upsert exitoso - Prefijo: %s", prefijo)
            return response
            
        except Exception as e:
            logger.error("Error en upsert de BIN %s: %s", prefijo, str(e), exc_info=True)
            raise

    @staticmethod
    def get_bin(prefijo: str):
        """
        Obtiene información de un BIN por prefijo.
        """
        logger.debug("Consultando BIN con prefijo: %s", prefijo)
        
        try:
            response = db_exec.table("bin").select("*").eq("prefijo", prefijo).execute()
            
            if response.data:
                logger.debug("BIN encontrado para prefijo %s: %d registros", prefijo, len(response.data))
                logger.debug("Datos encontrados: %s", response.data)
            else:
                logger.debug("No se encontró BIN para prefijo: %s", prefijo)
                
            return response
            
        except Exception as e:
            logger.error("Error al consultar BIN %s: %s", prefijo, str(e), exc_info=True)
            raise

    @staticmethod
    def delete_bin(prefijo: str):
        """
        Elimina un BIN de la tabla.
        """
        logger.info("Eliminando BIN con prefijo: %s", prefijo)
        
        try:
            response = db_exec.table("bin").delete().eq("prefijo", prefijo).execute()
            logger.info("BIN eliminado exitosamente - Prefijo: %s", prefijo)
            return response
            
        except Exception as e:
            logger.error("Error al eliminar BIN %s: %s", prefijo, str(e), exc_info=True)
            raise

    @staticmethod
    def get_all_bins():
        """
        Obtiene todos los BINs de la tabla (útil para depuración).
        """
        logger.info("Consultando todos los BINs")
        
        try:
            response = db_exec.table("bin").select("*").execute()
            logger.info("Total de BINs encontrados: %d", len(response.data) if response.data else 0)
            return response
            
        except Exception as e:
            logger.error("Error al consultar todos los BINs: %s", str(e), exc_info=True)
            raise

    @staticmethod
    def get_bins_by_type(tipo: str):
        """
        Obtiene BINs filtrados por tipo (débito/crédito).
        """
        logger.info("Consultando BINs por tipo: %s", tipo)
        
        try:
            response = db_exec.table("bin").select("*").eq("tipo", tipo).execute()
            logger.info("BINs encontrados para tipo %s: %d", tipo, len(response.data) if response.data else 0)
            return response
            
        except Exception as e:
            logger.error("Error al consultar BINs por tipo %s: %s", tipo, str(e), exc_info=True)
            raise