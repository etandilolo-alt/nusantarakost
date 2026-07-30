from flask import Blueprint, render_template
from database.db import fetch_rooms, fetch_tenants, fetch_rentals

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    rooms = fetch_rooms()
    tenants = fetch_tenants()
    rentals = fetch_rentals()
    
    total_rooms = len(rooms)
    available_rooms = len([r for r in rooms if r.status == 'Tersedia'])
    occupied_rooms = total_rooms - available_rooms
    active_tenants = len(tenants)
    active_rentals = len([s for s in rentals if s.status_sewa == 'Aktif'])
    
    total_income = sum([s.total_bayar for s in rentals if s.status_sewa == 'Aktif'])
    
    return render_template('admin/dashboard.html',
                           total_rooms=total_rooms,
                           available_rooms=available_rooms,
                           occupied_rooms=occupied_rooms,
                           active_tenants=active_tenants,
                           active_rentals=active_rentals,
                           total_income=total_income,
                           recent_rentals=rentals[:5])

@admin_bp.route('/laporan')
def laporan():
    rooms = fetch_rooms()
    tenants = fetch_tenants()
    rentals = fetch_rentals()
    total_income = sum([s.total_bayar for s in rentals])
    return render_template('admin/laporan/index.html', rooms=rooms, tenants=tenants, rentals=rentals, total_income=total_income)
