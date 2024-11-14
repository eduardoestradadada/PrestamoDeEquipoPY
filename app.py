from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required

from config import config

# Models:
from models.ModelUser import ModelUser
from models.ModelPanel import ModelPanel

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
try:
    db = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=EQUIPO2\SQLEXPRESS;'
        'DATABASE=sistema_de_prestamo;'
        'Trusted_Connection=yes;'
    )
    print("Conexión exitosa")
except Exception as ex:
    print(f"Error de conexión: {ex}")

login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)



######::___ROUTES_____::#####
@app.route('/')
def index():
    return redirect(url_for('login'))
    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, 0, request.form['password'], 0,0,0,0,request.form['email'],0)
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'carrera': request.form['carrera'],
            'telefono': request.form['telefono'],
            'rol': request.form['rol'],
            'email': request.form['email'],
            'password': request.form['password'],
            'confirm_password': request.form['confirm_password']
        }

 
        if user_data['password'] != user_data['confirm_password']:
             flash("Las contraseñas no coinciden", 'error') 
             return render_template('auth/register.html') 

        hashed_password = User.hash_password(user_data['password'])
        user_data['password'] = hashed_password


        success, message = ModelUser.register(db, user_data)
        if success:
            flash(message, 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
#@login_required
def home():
    try:
        if request.method == 'POST':
            # Lógica para POST si la necesitas
            estadisticas = ModelPanel.Estadistics_panel(db)
            return render_template('Admin/home.html', **estadisticas)
        else:
            # Lógica para GET
            estadisticas = ModelPanel.Estadistics_panel(db)
            return render_template('Admin/home.html', **estadisticas)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('Admin/home.html', 
                             pedidos_activos=0,
                             total_solicitudes=0,
                             total_observaciones=0,
                             equipos_disponibles=0)




######ROUTES######

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
