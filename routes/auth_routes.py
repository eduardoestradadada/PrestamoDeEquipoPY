from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.ModelUser import ModelUser
from models.entities.User import User
from database.db import get_connection

auth_bp = Blueprint('auth', __name__)
db = get_connection()

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, 0, request.form['password'], 0,0,0,0,request.form['email'],0)
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('admin.home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
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
            return redirect(url_for('auth.login'))
        else:
            flash(message, 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))