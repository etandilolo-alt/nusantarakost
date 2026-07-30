import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import Config
from database.db import fetch_rooms, add_room_db, update_room_db, delete_room_db

admin_kamar_bp = Blueprint('admin_kamar', __name__, url_prefix='/admin/kamar')

@admin_kamar_bp.route('/')
def index():
    rooms = fetch_rooms()
    return render_template('admin/kamar/index.html', rooms=rooms)

@admin_kamar_bp.route('/tambah', methods=['POST'])
def tambah():
    nomor = request.form.get('nomor')
    tipe = request.form.get('tipe')
    harga = request.form.get('harga')
    fasilitas = request.form.get('fasilitas')
    deskripsi = request.form.get('deskripsi')
    
    gambar_filename = 'kamar-standard.png'
    file = request.files.get('gambar')
    if file and file.filename:
        filename = secure_filename(file.filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        gambar_filename = filename
        
    add_room_db(nomor, tipe, harga, fasilitas, deskripsi, gambar_filename)
    flash('Kamar berhasil ditambahkan!', 'success')
    return redirect(url_for('admin_kamar.index'))

@admin_kamar_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    nomor = request.form.get('nomor')
    tipe = request.form.get('tipe')
    harga = request.form.get('harga')
    fasilitas = request.form.get('fasilitas')
    deskripsi = request.form.get('deskripsi')
    
    gambar_filename = None
    file = request.files.get('gambar')
    if file and file.filename:
        filename = secure_filename(file.filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        gambar_filename = filename
        
    update_room_db(id, nomor, tipe, harga, fasilitas, deskripsi, gambar_filename)
    flash('Data kamar berhasil diperbarui!', 'success')
    return redirect(url_for('admin_kamar.index'))

@admin_kamar_bp.route('/hapus/<int:id>', methods=['POST', 'GET'])
def hapus(id):
    success, msg = delete_room_db(id)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')
    return redirect(url_for('admin_kamar.index'))
