-- Schema for Sistem Manajemen Kos Nusantara (NusantaraKos)
-- Compatible with database/db.py column structure

-- Table 1: Kamar
CREATE TABLE IF NOT EXISTS `kamar` (
    `id_kamar` VARCHAR(50) NOT NULL PRIMARY KEY,
    `nomor_kamar` VARCHAR(50) NOT NULL,
    `tipe_kamar` VARCHAR(50) NOT NULL,
    `ukuran_kamar` VARCHAR(50) DEFAULT '3x4m',
    `harga_perbulan` INT NOT NULL,
    `status_kamar` VARCHAR(50) DEFAULT 'Tersedia'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table 2: Penghuni
CREATE TABLE IF NOT EXISTS `penghuni` (
    `id_penghuni` VARCHAR(50) NOT NULL PRIMARY KEY,
    `nama` VARCHAR(100) NOT NULL,
    `telepon` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100),
    `instansi` VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table 3: Sewa
CREATE TABLE IF NOT EXISTS `sewa` (
    `id_sewa` INT AUTO_INCREMENT PRIMARY KEY,
    `id_kamar` VARCHAR(50) NOT NULL,
    `id_penghuni` VARCHAR(50) NOT NULL,
    `tanggal_masuk` DATE NOT NULL,
    `tanggal_selesai` DATE NOT NULL,
    `lama_sewa` INT NOT NULL,
    `harga_sewa` INT NOT NULL,
    `status_sewa` VARCHAR(50) DEFAULT 'Aktif',
    FOREIGN KEY (`id_kamar`) REFERENCES `kamar`(`id_kamar`) ON DELETE RESTRICT,
    FOREIGN KEY (`id_penghuni`) REFERENCES `penghuni`(`id_penghuni`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed Data
INSERT INTO `kamar` (`id_kamar`, `nomor_kamar`, `tipe_kamar`, `ukuran_kamar`, `harga_perbulan`, `status_kamar`) VALUES
('101', '101', 'Standard', '3x4m', 1100000, 'Tersedia'),
('102', '102', 'Standard', '3x4m', 1150000, 'Tersedia'),
('201', '201', 'Deluxe AC', '3x4m', 1650000, 'Tersedia'),
('202', '202', 'Deluxe AC', '3x4m', 1700000, 'Terisi'),
('301', '301', 'VIP Suite', '3x4m', 2200000, 'Tersedia'),
('302', '302', 'VIP Suite', '3x4m', 2300000, 'Tersedia')
ON DUPLICATE KEY UPDATE `nomor_kamar`=VALUES(`nomor_kamar`);

INSERT INTO `penghuni` (`id_penghuni`, `nama`, `telepon`, `email`, `instansi`) VALUES
('081234567891', 'Budi Santoso', '081234567891', 'budi@mail.com', 'Mahasiswa UGM'),
('081298765432', 'Siti Nurhaliza', '081298765432', 'siti@mail.com', 'Mahasiswa UNY')
ON DUPLICATE KEY UPDATE `nama`=VALUES(`nama`);

INSERT INTO `sewa` (`id_sewa`, `id_kamar`, `id_penghuni`, `tanggal_masuk`, `tanggal_selesai`, `lama_sewa`, `harga_sewa`, `status_sewa`) VALUES
(1, '202', '081298765432', '2026-01-01', '2026-07-01', 6, 10200000, 'Aktif')
ON DUPLICATE KEY UPDATE `id_kamar`=VALUES(`id_kamar`);
