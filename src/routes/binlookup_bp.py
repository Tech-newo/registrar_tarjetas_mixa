from flask import Blueprint, jsonify, request
import requests
import re
import logging
from datetime import datetime
from src.infrastructure.executables.bin import BinService

# Configuración de logging más detallada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

binlookup_bp = Blueprint("binlookup", __name__)

class BinLookupService:
    def __init__(self):
        self.max_prefix_length = 8  # buscamos desde 8 dígitos hacia abajo
        logger.info("BinLookupService inicializado con max_prefix_length=%d", self.max_prefix_length)

    def lookup(self, bin_number: str):
        """Busca un BIN en Supabase usando BinService"""
        logger.info("Iniciando búsqueda de BIN: %s", bin_number)
        
        try:
            # Probar desde prefijo más largo a más corto
            for length in range(min(len(bin_number), self.max_prefix_length), 0, -1):
                prefijo = bin_number[:length]
                logger.debug("Buscando prefijo: %s (longitud: %d)", prefijo, length)
                
                response = BinService.get_bin(prefijo)
                logger.debug("Respuesta de BinService para prefijo %s: %s", prefijo, response)

                if response.data and len(response.data) > 0:
                    record = response.data[0]
                    logger.info("BIN encontrado para prefijo %s: %s", prefijo, record)
                    
                    result = {
                        "tipo": record.get("tipo", "desconocido"),
                        "marca": record.get("marca", "desconocida"),
                        "categoria": record.get("categoria", "desconocida"),
                        "banco": record.get("banco"),
                        "pais": {
                            "nombre": record.get("pais_nombre"),
                            "codigo": record.get("pais_codigo")
                        } if record.get("pais_nombre") else None,
                        "prefijo_encontrado": prefijo,
                        "fuente": record.get("fuente", "supabase"),
                        "longitud_prefijo": length
                    }
                    
                    logger.info("Resultado procesado para BIN %s: %s", bin_number, result)
                    return result
                else:
                    logger.debug("No se encontraron datos para prefijo %s", prefijo)
                    
        except Exception as e:
            logger.error("Error al consultar BIN %s en Supabase: %s", bin_number, str(e), exc_info=True)
            
        logger.warning("No se encontró información para BIN: %s", bin_number)
        return None


bin_service = BinLookupService()

@binlookup_bp.route("/<bin_number>", methods=["GET"])
def bin_lookup(bin_number):
    """Endpoint principal de consulta de BIN"""
    logger.info("Recibida solicitud de BIN lookup: %s", bin_number)
    
    try:
        # Limpiar y validar BIN
        clean_bin = re.sub(r'\D', '', str(bin_number))
        logger.debug("BIN limpio: %s (original: %s)", clean_bin, bin_number)
        
        if not clean_bin or len(clean_bin) < 4:
            logger.warning("BIN inválido recibido: %s (longitud: %d)", clean_bin, len(clean_bin) if clean_bin else 0)
            return jsonify({"error": "BIN inválido (mínimo 4 dígitos)"}), 400

        if len(clean_bin) > 8:
            original_bin = clean_bin
            clean_bin = clean_bin[:8]
            logger.debug("BIN truncado de %s a %s", original_bin, clean_bin)

        result = {
            "bin": clean_bin, 
            "timestamp": datetime.now().isoformat(), 
            "resultados": {}
        }

        # Buscar en Supabase
        logger.info("Iniciando búsqueda en Supabase para BIN: %s", clean_bin)
        local = bin_service.lookup(clean_bin)
        
        if local:
            logger.info("Resultado encontrado en Supabase: %s", local)
            result["resultados"]["supabase"] = local
            result["principal"] = local
        else:
            logger.info("No se encontró resultado en Supabase para BIN: %s", clean_bin)

        # Si no hay resultados, devolver desconocido
        if "principal" not in result:
            
            response = requests.get(
                f'https://lookup.binlist.net/{clean_bin}', 
                headers={'Accept-Version': '3'}
            )
            
            BinService.insert_bin(
                prefijo=clean_bin,
                tipo=response.json().get("type", "desconocido"),
                marca=response.json().get("brand", "desconocida"),
                categoria=response.json().get("category", "desconocida"),
                pais_nombre=response.json().get("country", {}).get("name", "desconocido"),
                pais_codigo=response.json().get("country", {}).get("alpha2", "desconocido"),
                banco=response.json().get("bank", "desconocido").get("name", "desconocido"),
                fuente="binlist"
            )
            logger.warning("Respuesta de BIN List: %s", response.text)
            logger.warning("No se encontraron resultados para BIN %s, devolviendo 'desconocido'", clean_bin)
            result["principal"] = {
                "tipo": response.json().get("type", "desconocido"),
                "marca": response.json().get("brand", "desconocida"),
                "categoria": response.json().get("category", "desconocida"),
                "fuente": "binlist"
            }

        # Respuesta simplificada con campos compatibles para frontend
        simple = {
            "bin": clean_bin,
            "tipo": result["principal"]["tipo"],
            "marca": result["principal"]["marca"],
            "categoria": result["principal"]["categoria"],
            "fuente": result["principal"]["fuente"],
            # Campos adicionales para compatibilidad con frontend
            "type": result["principal"]["tipo"],  # Alias para 'tipo'
            "brand": result["principal"]["marca"]  # Alias para 'marca'
        }
        
        # Campos opcionales
        if result["principal"].get("banco"):
            simple["banco"] = result["principal"]["banco"]
            
        if result["principal"].get("pais"):
            simple["pais"] = result["principal"]["pais"]
            simple["country"] = {  # Alias para 'pais'
                "name": result["principal"]["pais"]["nombre"],
                "code": result["principal"]["pais"]["codigo"]
            }

        # Determinar tipo de respuesta
        detallado = request.args.get("detallado", "false").lower() == "true"
        logger.info("Respuesta %s para BIN %s: %s", 
                   "detallada" if detallado else "simple", 
                   clean_bin, 
                   result if detallado else simple)

        if detallado:
            return jsonify(result), 200
        return jsonify(simple), 200

    except Exception as e:
        logger.error("Error inesperado en lookup para BIN %s: %s", bin_number, str(e), exc_info=True)
        return jsonify({"error": "Error interno del servidor"}), 500  # Corregido de 5 a 500