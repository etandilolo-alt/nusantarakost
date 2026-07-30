from datetime import datetime

class Sewa:
    def __init__(self, id=None, id_kamar=None, id_penghuni=None, tanggal_masuk=None, tanggal_keluar=None, lama_sewa=1, total_bayar=0, status_sewa="Aktif", kamar_nomor="", penghuni_nama=""):
        self.id = id
        self.id_kamar = id_kamar
        self.id_penghuni = id_penghuni
        self.tanggal_masuk = tanggal_masuk
        self.tanggal_keluar = tanggal_keluar
        self.lama_sewa = lama_sewa
        self.total_bayar = total_bayar
        self.status_sewa = status_sewa
        self.kamar_nomor = kamar_nomor
        self.penghuni_nama = penghuni_nama

    def hitung_total(self, harga_per_bulan):
        return int(self.lama_sewa) * int(harga_per_bulan)

    def is_active(self):
        return self.status_sewa == "Aktif"