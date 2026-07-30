class Penghuni:
    def __init__(self, id=None, nama="", no_hp="", email="", alamat="", pekerjaan="Mahasiswa", foto_ktp=""):
        self.id = id
        self.nama = nama
        self.no_hp = no_hp
        self.email = email
        self.alamat = alamat
        self.pekerjaan = pekerjaan
        self.foto_ktp = foto_ktp

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'no_hp': self.no_hp,
            'email': self.email,
            'alamat': self.alamat,
            'pekerjaan': self.pekerjaan,
            'foto_ktp': self.foto_ktp
        }