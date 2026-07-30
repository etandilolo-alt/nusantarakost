import mysql.connector
from config import Config
from models.kamar import Kamar
from models.penghuni import Penghuni
from models.sewa import Sewa

# ══════════════════════════════════════════════════════════════════════════════
# Column name mapping between MySQL table schema and application models:
#
# MySQL kamar:    id_kamar, nomor_kamar, tipe_kamar, ukuran_kamar, harga_perbulan, status_kamar
# App Kamar:      id,       nomor,       tipe,       (ukuran),     harga,          status,       fasilitas, deskripsi, gambar
#
# MySQL penghuni: id_penghuni, nama, telepon,  email, instansi
# App Penghuni:   id,          nama, no_hp,    email, alamat(=''), pekerjaan(=instansi), foto_ktp
#
# MySQL sewa:     id_sewa, id_penghuni, id_kamar, tanggal_masuk, tanggal_selesai, lama_sewa, harga_sewa,  status_sewa
# App Sewa:       id,      id_penghuni, id_kamar, tanggal_masuk, tanggal_keluar,  lama_sewa, total_bayar, status_sewa
# ══════════════════════════════════════════════════════════════════════════════

# Default gambar mapping by tipe
TIPE_GAMBAR_MAP = {
    'Standard': 'kamar-standard.png',
    'Deluxe AC': 'kamar-deluxe.png',
    'Deluxe': 'kamar-deluxe.png',
    'VIP Suite': 'kamar-vip.png',
    'VIP': 'kamar-vip.png',
}

TIPE_FASILITAS_MAP = {
    'Standard': ['Wi-Fi 100M', 'Kasur Springbed', 'Lemari', 'Kipas Angin'],
    'Deluxe AC': ['AC Cool', 'Kamar Mandi Dalam', 'Water Heater', 'Wi-Fi 100M'],
    'Deluxe': ['AC Cool', 'Kamar Mandi Dalam', 'Water Heater', 'Wi-Fi 100M'],
    'VIP Suite': ['Balkon Privat', 'AC 1 PK', 'Smart TV 32"', 'Kulkas Mini'],
    'VIP': ['Balkon Privat', 'AC 1 PK', 'Smart TV 32"', 'Kulkas Mini'],
}

# ── In-Memory Fallback Data ─────────────────────────────────────────────────
MEMORY_KAMAR = [
    Kamar(id=1, nomor='101', tipe='Standard', harga=1100000, status='Tersedia', fasilitas=['Wi-Fi 100M', 'Kasur Springbed', 'Lemari', 'Kipas Angin'], deskripsi='Kamar bersih dan tenang.', gambar='kamar-standard.png'),
    Kamar(id=2, nomor='102', tipe='Standard', harga=1150000, status='Tersedia', fasilitas=['Wi-Fi 100M', 'Meja Belajar', 'Lemari', 'Kipas Angin'], deskripsi='Kamar tipe standard dekat garasi.', gambar='kamar-standard.png'),
    Kamar(id=3, nomor='201', tipe='Deluxe AC', harga=1650000, status='Tersedia', fasilitas=['AC Cool', 'Kamar Mandi Dalam', 'Water Heater', 'Wi-Fi 100M'], deskripsi='Kamar modern ber-AC.', gambar='kamar-deluxe.png'),
    Kamar(id=4, nomor='202', tipe='Deluxe AC', harga=1700000, status='Terisi', fasilitas=['AC Cool', 'Kamar Mandi Dalam', 'Kasur Queen', 'Wi-Fi 100M'], deskripsi='Kamar Deluxe lantai 2.', gambar='kamar-deluxe.png'),
    Kamar(id=5, nomor='301', tipe='VIP Suite', harga=2200000, status='Tersedia', fasilitas=['Balkon Privat', 'AC 1 PK', 'Smart TV 32"', 'Kulkas Mini'], deskripsi='Kamar VIP dengan balkon.', gambar='kamar-vip.png'),
    Kamar(id=6, nomor='302', tipe='VIP Suite', harga=2300000, status='Tersedia', fasilitas=['Balkon Privat', 'AC 1 PK', 'Smart TV 43"', 'Kulkas Mini'], deskripsi='Kamar VIP paling terluas.', gambar='kamar-vip.png')
]

MEMORY_PENGHUNI = [
    Penghuni(id=1, nama='Budi Santoso', no_hp='081234567891', email='budi@mail.com', alamat='Jl. Malioboro No. 45, Yogyakarta', pekerjaan='Mahasiswa UGM'),
    Penghuni(id=2, nama='Siti Nurhaliza', no_hp='081298765432', email='siti@mail.com', alamat='Jl. Gejayan No. 12, Sleman', pekerjaan='Mahasiswa UNY')
]

MEMORY_SEWA = [
    Sewa(id=1, id_kamar=4, id_penghuni=2, tanggal_masuk='2026-01-01', tanggal_keluar='2026-07-01', lama_sewa=6, total_bayar=10200000, status_sewa='Aktif', kamar_nomor='202', penghuni_nama='Siti Nurhaliza')
]


# ── Database Connection ──────────────────────────────────────────────────────
def get_db():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            connection_timeout=3
        )
        if conn.is_connected():
            return conn
    except Exception as e:
        print(f"DB connection error: {e}")
    return None


# ── FETCH functions ──────────────────────────────────────────────────────────

def fetch_rooms():
    """Fetch rooms from MySQL with column mapping, fallback to in-memory."""
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM kamar")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if rows:
                result = []
                for r in rows:
                    tipe = r.get('tipe_kamar', 'Standard')
                    gambar = TIPE_GAMBAR_MAP.get(tipe, 'kamar-standard.png')
                    fasilitas = TIPE_FASILITAS_MAP.get(tipe, ['Wi-Fi 100M'])
                    status_raw = r.get('status_kamar', 'Tersedia')
                    # Normalize status (TERSEDIA -> Tersedia, TERISI -> Terisi)
                    if status_raw.upper() == 'TERSEDIA':
                        status = 'Tersedia'
                    elif status_raw.upper() == 'TERISI':
                        status = 'Terisi'
                    else:
                        status = status_raw.capitalize()
                    result.append(Kamar(
                        id=r['id_kamar'],
                        nomor=r['nomor_kamar'],
                        tipe=tipe,
                        harga=int(r.get('harga_perbulan', 0)),
                        status=status,
                        fasilitas=fasilitas,
                        deskripsi=f"Kamar {tipe} - Ukuran {r.get('ukuran_kamar', '-')}",
                        gambar=gambar
                    ))
                return result
        except Exception as e:
            print(f"fetch_rooms error: {e}")
    return MEMORY_KAMAR


def fetch_tenants():
    """Fetch tenants from MySQL with column mapping, fallback to in-memory."""
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM penghuni")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if rows:
                return [Penghuni(
                    id=r['id_penghuni'],
                    nama=r.get('nama', ''),
                    no_hp=str(r.get('telepon', '')),
                    email=r.get('email', ''),
                    alamat='',  # Column not in your DB
                    pekerjaan=r.get('instansi', 'Mahasiswa'),
                    foto_ktp=''
                ) for r in rows]
        except Exception as e:
            print(f"fetch_tenants error: {e}")
    return MEMORY_PENGHUNI


def fetch_rentals():
    """Fetch rentals from MySQL with column mapping, fallback to in-memory."""
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.*, k.nomor_kamar, p.nama as penghuni_nama 
                FROM sewa s 
                JOIN kamar k ON s.id_kamar = k.id_kamar 
                JOIN penghuni p ON s.id_penghuni = p.id_penghuni
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if rows:
                return [Sewa(
                    id=r['id_sewa'],
                    id_kamar=r['id_kamar'],
                    id_penghuni=r['id_penghuni'],
                    tanggal_masuk=str(r['tanggal_masuk']),
                    tanggal_keluar=str(r.get('tanggal_selesai', '')),
                    lama_sewa=r.get('lama_sewa', 1),
                    total_bayar=int(r.get('harga_sewa', 0)),
                    status_sewa=r.get('status_sewa', 'Aktif').capitalize(),
                    kamar_nomor=r.get('nomor_kamar', ''),
                    penghuni_nama=r.get('penghuni_nama', '')
                ) for r in rows]
        except Exception as e:
            print(f"fetch_rentals error: {e}")
    return MEMORY_SEWA


# ── WRITE functions (KAMAR) ──────────────────────────────────────────────────

def add_room_db(nomor, tipe, harga, fasilitas, deskripsi, gambar):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO kamar (id_kamar, nomor_kamar, tipe_kamar, ukuran_kamar, harga_perbulan, status_kamar) VALUES (%s, %s, %s, %s, %s, %s)",
                (nomor, nomor, tipe, '3x4m', harga, 'Tersedia'))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB add room err:", e)
    # Memory fallback
    new_id = len(MEMORY_KAMAR) + 1
    MEMORY_KAMAR.append(Kamar(new_id, nomor, tipe, int(harga), 'Tersedia', fasilitas, deskripsi, gambar))
    return True


def update_room_db(id_kamar, nomor, tipe, harga, fasilitas, deskripsi, gambar=None):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE kamar SET nomor_kamar=%s, tipe_kamar=%s, harga_perbulan=%s WHERE id_kamar=%s",
                (nomor, tipe, harga, id_kamar))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB update room err:", e)
    # Memory fallback
    for k in MEMORY_KAMAR:
        if str(k.id) == str(id_kamar):
            k.nomor = nomor
            k.tipe = tipe
            k.harga = int(harga)
            k.fasilitas = fasilitas if isinstance(fasilitas, list) else [f.strip() for f in (fasilitas or "").split(',') if f.strip()]
            k.deskripsi = deskripsi
            if gambar:
                k.gambar = gambar
            break
    return True


def delete_room_db(id_kamar):
    # Rule check: cannot delete occupied room
    rooms = fetch_rooms()
    for r in rooms:
        if str(r.id) == str(id_kamar) and r.status == 'Terisi':
            return False, "Kamar yang sedang terisi sewa tidak dapat dihapus!"

    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kamar WHERE id_kamar=%s", (id_kamar,))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Kamar berhasil dihapus."
        except Exception as e:
            print("DB delete room err:", e)
    # Memory fallback
    global MEMORY_KAMAR
    MEMORY_KAMAR = [k for k in MEMORY_KAMAR if str(k.id) != str(id_kamar)]
    return True, "Kamar berhasil dihapus."


# ── WRITE functions (PENGHUNI) ───────────────────────────────────────────────

def add_tenant_db(nama, no_hp, email, alamat, pekerjaan, foto_ktp):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO penghuni (id_penghuni, nama, telepon, email, instansi) VALUES (%s, %s, %s, %s, %s)",
                (no_hp, nama, no_hp, email, pekerjaan))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB add tenant err:", e)
    # Memory fallback
    new_id = len(MEMORY_PENGHUNI) + 1
    MEMORY_PENGHUNI.append(Penghuni(new_id, nama, no_hp, email, alamat, pekerjaan, foto_ktp))
    return True


def edit_tenant_db(id_penghuni, nama, no_hp, email, alamat, pekerjaan, foto_ktp=None):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE penghuni SET nama=%s, telepon=%s, email=%s, instansi=%s WHERE id_penghuni=%s",
                (nama, no_hp, email, pekerjaan, id_penghuni))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB edit tenant err:", e)
    # Memory fallback
    for p in MEMORY_PENGHUNI:
        if str(p.id) == str(id_penghuni):
            p.nama = nama
            p.no_hp = no_hp
            p.email = email
            p.alamat = alamat
            p.pekerjaan = pekerjaan
            if foto_ktp:
                p.foto_ktp = foto_ktp
            break
    return True


def delete_tenant_db(id_penghuni):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM penghuni WHERE id_penghuni=%s", (id_penghuni,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB delete tenant err:", e)
    # Memory fallback
    global MEMORY_PENGHUNI
    MEMORY_PENGHUNI = [p for p in MEMORY_PENGHUNI if str(p.id) != str(id_penghuni)]
    return True


# ── WRITE functions (SEWA) ───────────────────────────────────────────────────

def add_rental_db(id_kamar, id_penghuni, tgl_masuk, tgl_keluar, lama_sewa, total_bayar):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor()
            # 1. Insert sewa
            cursor.execute(
                "INSERT INTO sewa (id_penghuni, id_kamar, tanggal_masuk, tanggal_selesai, lama_sewa, harga_sewa, status_sewa) VALUES (%s, %s, %s, %s, %s, %s, 'AKTIF')",
                (id_penghuni, id_kamar, tgl_masuk, tgl_keluar, lama_sewa, total_bayar))
            # 2. Update room status -> Terisi
            cursor.execute("UPDATE kamar SET status_kamar='Terisi' WHERE id_kamar=%s", (id_kamar,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB add rental err:", e)

    # Memory fallback
    new_id = len(MEMORY_SEWA) + 1
    kmr_num = ""
    pnh_nama = ""
    for k in MEMORY_KAMAR:
        if str(k.id) == str(id_kamar):
            k.status = 'Terisi'
            kmr_num = k.nomor
            break
    for p in MEMORY_PENGHUNI:
        if str(p.id) == str(id_penghuni):
            pnh_nama = p.nama
            break
    MEMORY_SEWA.append(Sewa(new_id, int(id_kamar), int(id_penghuni), tgl_masuk, tgl_keluar, int(lama_sewa), int(total_bayar), 'Aktif', kmr_num, pnh_nama))
    return True


def end_rental_db(id_sewa):
    conn = get_db()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_kamar FROM sewa WHERE id_sewa=%s", (id_sewa,))
            row = cursor.fetchone()
            if row:
                id_kamar = row['id_kamar']
                cursor.execute("UPDATE sewa SET status_sewa='SELESAI' WHERE id_sewa=%s", (id_sewa,))
                cursor.execute("UPDATE kamar SET status_kamar='Tersedia' WHERE id_kamar=%s", (id_kamar,))
                conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("DB end rental err:", e)
    # Memory fallback
    for s in MEMORY_SEWA:
        if str(s.id) == str(id_sewa):
            s.status_sewa = 'Selesai'
            for k in MEMORY_KAMAR:
                if str(k.id) == str(s.id_kamar):
                    k.status = 'Tersedia'
                    break
            break
    return True
