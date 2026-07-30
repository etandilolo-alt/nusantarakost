class Kamar:
    def __init__(self, id=None, nomor="", tipe="Standard", harga=1000000, status="Tersedia", fasilitas="", deskripsi="", gambar="kamar-standard.png"):
        self.id = id
        self.nomor = nomor
        self.tipe = tipe
        self.harga = harga
        self.status = status
        self.fasilitas = fasilitas if isinstance(fasilitas, list) else [f.strip() for f in (fasilitas or "").split(',') if f.strip()]
        self.deskripsi = deskripsi
        self.gambar = gambar or "kamar-standard.png"

    def is_available(self):
        return self.status == "Tersedia"

    def to_dict(self):
        return {
            'id': self.id,
            'nomor': self.nomor,
            'tipe': self.tipe,
            'harga': self.harga,
            'status': self.status,
            'fasilitas': self.fasilitas,
            'deskripsi': self.deskripsi,
            'gambar': self.gambar
        }