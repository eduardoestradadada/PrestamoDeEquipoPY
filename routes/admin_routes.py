from flask import Blueprint, render_template, request
from flask_login import login_required
from models.ModelPanel import ModelPanel
from database.db import get_connection

admin_bp = Blueprint('admin', __name__)
db = get_connection()

@admin_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    try:
        if request.method == 'POST':
            estadisticas = ModelPanel.Estadistics_panel(db)
            return render_template('Admin/home.html', **estadisticas)
        else:
            estadisticas = ModelPanel.Estadistics_panel(db)
            return render_template('Admin/home.html', **estadisticas)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('Admin/home.html', 
                             pedidos_activos=0,
                             total_solicitudes=0,
                             total_observaciones=0,
                             equipos_disponibles=0)