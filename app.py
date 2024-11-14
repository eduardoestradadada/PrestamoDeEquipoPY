from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import config

# Routes
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp

# Models
from models.ModelUser import ModelUser
from database.db import get_connection

app = Flask(__name__)
csrf = CSRFProtect()
db = get_connection()

login_manager_app = LoginManager(app)
login_manager_app.login_view = 'auth.login'

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

def status_401(error):
    return redirect(url_for('auth.login'))

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

def create_app():
    app.config.from_object(config['development'])
    
    # Registrar los blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Registrar manejadores de error
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    
    # Inicializar CSRF
    csrf.init_app(app)
    
    return app

if __name__ == '__main__':
    create_app()
    app.run()