from flask import Blueprint, render_template, request
import requests
from src.domain.models import Empresa, MedioPago
from src.infrastructure.executables import get_empresas_func
from src.infrastructure.make import create_card
from src.utils import get_current_epoch_seconds
import json
import ast
from uuid import uuid4

# Creamos el blueprint
pagos_bp = Blueprint("pagos_bp", __name__)

# Definimos rutas
@pagos_bp.route("/create_card", methods=["GET", "POST"])
def crear_tarjeta():
    print('hello')
    if request.method == "GET":
        # 👇 Aquí debes pasar el objeto empresa al formulario
        # Simulamos empresa vacía si no se pasa como query param
        empresa = request.form.get("empresa")
        empresa_obj = json.loads(empresa) if empresa else {}
        return render_template('content/create_card.html', empresas=json.dumps(empresa_obj))
    elif request.method == "POST":
        try:
            code = request.form.get('code')
            empresa_raw = json.loads(request.form.get('empresa'))
            
            print("📩 DATOS RECIBIDOS:")
            print(f"   Código: {code}")
            print(f"   Empresa: {empresa_raw}")
            
            if code and len(code) == 6:
                print(f"✅ Código válido: {code}")
                check_empresa = get_empresas_func(empresa_raw[0]['identificacion'])
                
                if check_empresa[0]['codigo_validacion'] is None:
                    print('no hay codigo de validacion')
                    return render_template('content/response_fail.html')
                
                if check_empresa[0]['codigo_validacion'] != code:
                    print('el codigo de validacion no es correcto')
                    return render_template('content/response_fail.html')
                
                if check_empresa[0]['fecha_expiracion_codigo_validacion'] < get_current_epoch_seconds():
                    print('el codigo de validacion ha expirado')
                    return render_template('content/response_fail.html')
                
                return render_template('content/create_card.html', empresa=json.dumps(empresa_raw))
            else:
                print(f"❌ Código inválido: {code}")
                return render_template('content/response_fail.html')
        except Exception as e:
            print(f"❌ Error procesando la petición: {str(e)}")
            return render_template('content/response_fail.html')

@pagos_bp.route("/create_card_act", methods=["GET", "POST"])
def crear_tarjeta_act():
    if request.method == "POST":
        try:
            empresa_raw = json.loads(request.form.get('empresa'))
            print(f"Empresa raw recibida: {empresa_raw}")
            
            # Validar que empresa_raw no esté vacío
            if not empresa_raw:
                print("❌ No se recibieron datos de empresa")
                return render_template('content/response_fail.html')
            
            # Parsear JSON de forma segura
            try:
                empresa_data = json.loads(empresa_raw)
                print(f"Empresa data parseada: {empresa_data}")
            except json.JSONDecodeError as json_error:
                print(f"❌ Error parseando JSON de empresa: {json_error}")
                print(f"Contenido problemático: {repr(empresa_raw)}")
                return render_template('content/response_fail.html')
            
            # Verificar si empresa_data es una lista y tomar el primer elemento
            if isinstance(empresa_data, list) and len(empresa_data) > 0:
                empresa_info = empresa_data[0]
            elif isinstance(empresa_data, dict):
                empresa_info = empresa_data
            else:
                print("❌ Formato de datos de empresa no válido")
                return render_template('content/response_fail.html')
            
            print(f"Información de empresa: {empresa_info}")
            print(f"Form data completa: {dict(request.form)}")
            
            # Crear objeto tarjeta
            tarjeta = MedioPago(
                id=str(uuid4()),
                id_empresa=str(empresa_info.get('id')),  # Usar empresa_info en lugar de request.form
                numero_tarjeta=request.form.get('numero_tarjeta').replace(' ', ''),
                cvc=request.form.get('cvc'),
                mes_vencimiento=request.form.get('mes_vencimiento'),
                anio_vencimiento=request.form.get('anio_vencimiento')[-2:],
                nombre_titular=request.form.get('nombre_titular'),
                email=request.form.get('email'),
                cuotas=int(request.form.get('cuotas', 1))
            )
            
            # Crear objeto empresa con datos existentes
            empresa = Empresa(
                id=str(empresa_info.get('id')),
                razon_social=empresa_info.get('razon_social'),
                identificacion=empresa_info.get('identificacion'),
                persona_juridica=empresa_info.get('persona_juridica'),
                correo=empresa_info.get('correo'),
                celular=empresa_info.get('celular'),
                activo=empresa_info.get('activo'),
                codigo_validacion=empresa_info.get('codigo_validacion'),
                fecha_creacion=empresa_info.get('fecha_creacion'),
                fecha_actualizacion=empresa_info.get('fecha_actualizacion'),
                fecha_expiracion_codigo_validacion=empresa_info.get('fecha_expiracion_codigo_validacion')
            )
            
            print("📩 DATOS PROCESADOS:")
            print(f"   Empresa: {empresa}")
            print(f"   Tarjeta: {tarjeta}")
            
            # Aquí deberías llamar a la función para guardar la tarjeta
            resultado = create_card(empresa=empresa, card=tarjeta)
            
            print ('Este es el resultado de la operación ', resultado)
            
            if resultado == 400:
                print("❌ Error al crear la tarjeta")
                return render_template('content/response_fail.html')
            
            return render_template('content/response_success.html')
            
        except Exception as e:
            print(f"❌ Error procesando tarjeta: {str(e)}")
            import traceback
            traceback.print_exc()  # Esto te dará más detalles del error
            return render_template('content/response_fail.html')
    
    return "Método GET no permitido"