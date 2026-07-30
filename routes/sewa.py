from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.db import fetch_rooms, fetch_tenants, fetch_rentals, add_rental_db, end_rental_db

admin_sewa_bp = Blueprint('admin_sewa', __name__, url_prefix='/admin/sewa')

@admin_sewa_bp.route('/')
def index():
    rentals = fetch_rentals()
    rooms = fetch_rooms()
    tenants = fetch_tenants()
    
    # Filter available rooms for new rental form
    available_rooms = [r for r in rooms if r.status == 'Tersedia']
    
    return render_template('admin/sewa/index.html', 
                           rentals=rentals, 
                           available_rooms=available_rooms, 
                           tenants=tenants)

@admin_sewa_bp.route('/tambah', methods=['POST'])
def tambah():
    id_kamar = request.form.get('id_kamar')
    id_penghuni = request.form.get('id_penghuni')
    tanggal_masuk = request.form.get('tanggal_masuk')
    tanggal_keluar = request.form.get('tanggal_keluar')
    lama_sewa = request.form.get('lama_sewa')
    total_bayar = request.form.get('total_bayar')
    
    if not id_kamar or not id_penghuni:
        flash('Silakan pilih Kamar dan Penghuni!', 'danger')
        return redirect(url_for('admin_sewa.index'))
        
    add_rental_db(id_kamar, id_penghuni, tanggal_masuk, tanggal_keluar, lama_sewa, total_bayar)
    flash('Transaksi sewa baru berhasil dibuat dan kamar otomatis menjadi Terisi!', 'success')
    return redirect(url_for('admin_sewa.index'))

@admin_sewa_bp.route('/selesai/<int:id>', methods=['POST', 'GET'])
def selesai(id):
    end_rental_db(id)
    flash('Masa sewa berhasil diselesaikan dan status kamar kembali Tersedia!', 'success')
    return redirect(url_for('admin_sewa.index'))
