import mysql.connector
from config import Config

def run_terminal():
    print("=== NusantaraKos MySQL Terminal Emulation ===")
    print(f"Menghubungkan ke {Config.MYSQL_HOST}:{Config.MYSQL_PORT} ({Config.MYSQL_DB})...")
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if conn.is_connected():
            print("Koneksi Berhasil! Anda sekarang terhubung ke database remote di Filess.io.")
            print("Ketik query SQL Anda (contoh: SELECT * FROM kamar;). Ketik 'exit' atau 'quit' untuk keluar.\n")
            
            cursor = conn.cursor(dictionary=True)
            while True:
                try:
                    query = input("mysql_remote> ")
                    if not query.strip():
                        continue
                    if query.strip().lower() in ['exit', 'quit']:
                        break
                    
                    cursor.execute(query)
                    
                    if cursor.description:
                        # Ini adalah query SELECT
                        rows = cursor.fetchall()
                        if rows:
                            # Menampilkan header kolom
                            headers = list(rows[0].keys())
                            print("\n" + " | ".join(headers))
                            print("-" * (sum(len(h) for h in headers) + len(headers) * 3))
                            for r in rows:
                                print(" | ".join(str(val) for val in r.values()))
                            print(f"\n({len(rows)} baris dikembalikan)\n")
                        else:
                            print("\nHasil kosong.\n")
                    else:
                        # Ini adalah query INSERT/UPDATE/DELETE/CREATE
                        conn.commit()
                        print(f"\nQuery OK, {cursor.rowcount} baris terpengaruh.\n")
                except mysql.connector.Error as query_err:
                    print("\nError SQL:", query_err, "\n")
                except KeyboardInterrupt:
                    print("\nKeluar...")
                    break
                except Exception as general_err:
                    print("\nError:", general_err, "\n")
                    
            cursor.close()
            conn.close()
            print("Koneksi ditutup.")
    except Exception as e:
        print("Gagal terhubung ke database:", e)

if __name__ == "__main__":
    run_terminal()
