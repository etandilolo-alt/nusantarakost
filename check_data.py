import mysql.connector
from config import Config

def check_database():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if conn.is_connected():
            print("=== Terkoneksi ke MySQL Server ===")
            cursor = conn.cursor(dictionary=True)
            
            # 1. Tampilkan Data Kamar
            print("\n--- DATA KAMAR ---")
            cursor.execute("SELECT id_kamar, nomor_kamar, tipe_kamar, harga_perbulan, status_kamar FROM kamar")
            rooms = cursor.fetchall()
            for r in rooms:
                print(f"ID: {r['id_kamar']} | No: {r['nomor_kamar']} | Tipe: {r['tipe_kamar']} | Harga: Rp{r['harga_perbulan']:,} | Status: {r['status_kamar']}")
                
            # 2. Tampilkan Data Penghuni
            print("\n--- DATA PENGHUNI ---")
            cursor.execute("SELECT id_penghuni, nama, telepon, email, instansi FROM penghuni")
            tenants = cursor.fetchall()
            for t in tenants:
                print(f"ID: {t['id_penghuni']} | Nama: {t['nama']} | Telp: {t['telepon']} | Email: {t['email']} | Instansi: {t['instansi']}")
                
            # 3. Tampilkan Data Sewa
            print("\n--- DATA TRANSAKSI SEWA ---")
            cursor.execute("SELECT id_sewa, id_kamar, id_penghuni, tanggal_masuk, tanggal_selesai, lama_sewa, harga_sewa, status_sewa FROM sewa")
            rentals = cursor.fetchall()
            for s in rentals:
                print(f"ID Sewa: {s['id_sewa']} | Kamar: {s['id_kamar']} | Penghuni: {s['id_penghuni']} | Masuk: {s['tanggal_masuk']} | Keluar: {s['tanggal_selesai']} | Durasi: {s['lama_sewa']} bulan | Total: Rp{s['harga_sewa']:,} | Status: {s['status_sewa']}")
                
            cursor.close()
            conn.close()
    except Exception as e:
        print("Gagal menghubungkan ke database:", e)

if __name__ == "__main__":
    check_database()
