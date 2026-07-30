import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from config import Config
from database.db import fetch_tenants, add_tenant_db, edit_tenant_db, delete_tenant_db

admin_penghuni_bp = Blueprint('admin_penghuni', __name__, url_prefix='/admin/penghuni')

@admin_penghuni_bp.route('/')
def index():
    tenants = fetch_tenants()
    return render_template('admin/penghuni/index.html', tenants=tenants)

@admin_penghuni_bp.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form.get('nama')
    no_hp = request.form.get('no_hp')
    email = request.form.get('email')
    alamat = request.form.get('alamat')
    pekerjaan = request.form.get('pekerjaan')
    
    ktp_filename = ''
    file = request.files.get('foto_ktp')
    if file and file.filename:
        filename = secure_filename(file.filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        ktp_filename = filename
        
    add_tenant_db(nama, no_hp, email, alamat, pekerjaan, ktp_filename)
    flash('Data penghuni berhasil ditambahkan!', 'success')
    return redirect(url_for('admin_penghuni.index'))

@admin_penghuni_bp.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    nama = request.form.get('nama')
    no_hp = request.form.get('no_hp')
    email = request.form.get('email')
    alamat = request.form.get('alamat')
    pekerjaan = request.form.get('pekerjaan')
    
    ktp_filename = None
    file = request.files.get('foto_ktp')
    if file and file.filename:
        filename = secure_filename(file.filename)
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        ktp_filename = filename
        
    edit_tenant_db(id, nama, no_hp, email, alamat, pekerjaan, ktp_filename)
    flash('Data penghuni berhasil diperbarui!', 'success')
    return redirect(url_for('admin_penghuni.index'))

@admin_penghuni_bp.route('/hapus/<int:id>', methods=['POST', 'GET'])
def hapus(id):
    delete_tenant_db(id)
    flash('Penghuni berhasil dihapus!', 'success')
    return redirect(url_for('admin_penghuni.index'))
