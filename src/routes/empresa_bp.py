from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.infrastructure.executables import get_empresas_func, create_empresas_func, set_validation_code_func
from src.utils import generar_numero_validacion
from src.infrastructure.make import send_validation_code

# Creamos el blueprint
empresa_bp = Blueprint("empresa_bp", __name__)

# Definimos rutas
@empresa_bp.route("/", methods=["GET"])
def validar_empresa():
    return render_template('content/save_empresa.html')

@empresa_bp.route("/act", methods=["GET", "POST"])
def validar_empresa_act():
    
    if request.method == "POST":
        
        print('estoy ingresando al post')
        identificacion = request.form.get("identificacion")
        print('estoy obteniedo la identificacion', identificacion)
        
        if not identificacion:
            flash("La identificación es requerida", "error")
            return render_template('empresa_bp.response_fail.html')
        
        try:
            empresas = get_empresas_func(identificacion)
            print(f"Empresas encontradas: {empresas}")
            
            if empresas:
                validation_code = generar_numero_validacion()
                print('estoy generando codigo de validacion', validation_code)
                set_validation_code_func(validation_code, identificacion)
                print('estoy guardando mi codigo de validacion')
                send_validation_code(empresas[0]['correo'], validation_code)
                
                return render_template('content/check_empresa.html', 
                                     empresas=empresas, 
                                     identificacion=identificacion)
            else:
                return redirect(url_for('empresa_bp.crear_empresa', identificacion=identificacion))
                
        except Exception as e:
            flash(f"Error al consultar empresa: {str(e)}", "error")
            return redirect(url_for('empresa_bp.validar_empresa'))
    
    identificacion = request.args.get('identificacion')
    return render_template('content/check_empresa.html', identificacion=identificacion)

@empresa_bp.route("/create_empresa", methods=["GET", "POST"])
def crear_empresa():
    identificacion = request.args.get('identificacion')
    
    if not identificacion:
        return redirect(url_for('empresa_bp.validar_empresa'))
    
    return render_template('content/create_empresa.html', identificacion=identificacion)

@empresa_bp.route("/create_empresa/act", methods=["GET", "POST"])
def crear_empresa_act():
    identificacion = request.form.get('identificacion')
    razon_social = request.form.get('razon_social')
    correo = request.form.get('correo')
    celular = request.form.get('celular')
    persona_juridica = request.form.get('persona_juridica')
    
    empresa_check = get_empresas_func(identificacion)
    print (identificacion)
    
    if not identificacion:
        return render_template('content/response_fail.html')

    if  not empresa_check:
        create_empresas_func(identificacion, razon_social, correo, celular, persona_juridica)
        return render_template('content/response_success.html')
    
    return render_template('content/response_fail.html')
        
    
    