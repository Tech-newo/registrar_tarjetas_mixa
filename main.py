from flask import Flask, redirect, url_for
from src.routes.pagos_bp import pagos_bp
from src.routes.empresa_bp import empresa_bp
import dotenv
import os

dotenv.load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY or "clave-por-defecto-insegura"

    # Registrar Blueprints (routers)
    app.register_blueprint(empresa_bp, url_prefix="/empresa")
    app.register_blueprint(pagos_bp, url_prefix="/pagos")
    
    # Redireccionar la ruta raíz a /empresa
    @app.route('/')
    def index():
        return redirect(url_for('empresa_bp.validar_empresa'))
        # Reemplaza <nombre_de_la_funcion_principal> con la función que maneja las rutas en empresa_bp
        
    return app

app = create_app()

# Solo se ejecuta si corres directamente este archivo (no en tests, por ejemplo)
if __name__ == "__main__":
    # Solo para desarrollo local
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, port=port)

    app.run(debug=True, port=3000)