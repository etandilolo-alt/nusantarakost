/**
 * NusantaraKos - Admin Dashboard JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {

    // --------------------------------------------------------------------------
    // 1. CHART.JS INITIALIZATION (DASHBOARD)
    // --------------------------------------------------------------------------
    const roomStatusCanvas = document.getElementById('roomStatusChart');
    if (roomStatusCanvas) {
        const availableCount = parseInt(roomStatusCanvas.getAttribute('data-available')) || 0;
        const occupiedCount = parseInt(roomStatusCanvas.getAttribute('data-occupied')) || 0;

        new Chart(roomStatusCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Tersedia', 'Terisi'],
                datasets: [{
                    data: [availableCount, occupiedCount],
                    backgroundColor: ['#10B981', '#64748B'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    const incomeCanvas = document.getElementById('incomeChart');
    if (incomeCanvas) {
        new Chart(incomeCanvas, {
            type: 'bar',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Pendapatan Sewa (Rp)',
                    data: [8500000, 9200000, 9800000, 10200000, 10200000, 11500000, 12200000],
                    backgroundColor: '#0F766E',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'Rp ' + (value / 1000000) + ' Jt';
                            }
                        }
                    }
                }
            }
        });
    }

    // --------------------------------------------------------------------------
    // 2. AUTOMATIC RENTAL DURATION & TOTAL PAYMENT CALCULATOR
    // --------------------------------------------------------------------------
    const selectKamar = document.getElementById('selectKamar');
    const tglMasuk = document.getElementById('tglMasuk');
    const tglKeluar = document.getElementById('tglKeluar');
    const lamaSewaInput = document.getElementById('lamaSewa');
    const totalBayarInput = document.getElementById('totalBayar');

    function calculateRentalTotal() {
        if (!selectKamar || !tglMasuk || !tglKeluar) return;

        const selectedOption = selectKamar.options[selectKamar.selectedIndex];
        const hargaPerBulan = parseInt(selectedOption ? selectedOption.getAttribute('data-harga') : 0) || 0;

        const date1 = new Date(tglMasuk.value);
        const date2 = new Date(tglKeluar.value);

        if (tglMasuk.value && tglKeluar.value && date2 > date1) {
            // Estimate duration in months
            const diffTime = Math.abs(date2 - date1);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
            let months = Math.max(1, Math.round(diffDays / 30));

            lamaSewaInput.value = months;
            totalBayarInput.value = months * hargaPerBulan;
        } else if (hargaPerBulan > 0) {
            const months = parseInt(lamaSewaInput.value) || 1;
            totalBayarInput.value = months * hargaPerBulan;
        }
    }

    if (selectKamar && tglMasuk && tglKeluar) {
        selectKamar.addEventListener('change', calculateRentalTotal);
        tglMasuk.addEventListener('change', calculateRentalTotal);
        tglKeluar.addEventListener('change', calculateRentalTotal);
    }

    // --------------------------------------------------------------------------
    // 3. SWEETALERT CONFIRMATION FOR DELETIONS
    // --------------------------------------------------------------------------
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            const status = this.getAttribute('data-status');
            const nomor = this.getAttribute('data-nomor');

            if (status === 'Terisi') {
                Swal.fire({
                    icon: 'error',
                    title: 'Tidak Dapat Dihapus!',
                    text: `Kamar ${nomor} sedang dalam status TERISI sewa aktif! Selesaikan sewa terlebih dahulu.`,
                    confirmButtonColor: '#0F766E'
                });
                return;
            }

            Swal.fire({
                title: `Hapus Kamar ${nomor}?`,
                text: "Data kamar yang dihapus tidak dapat dikembalikan!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#DC2626',
                cancelButtonColor: '#64748B',
                confirmButtonText: 'Ya, Hapus Kamar',
                cancelButtonText: 'Batal'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = href;
                }
            });
        });
    });

    const deleteTenantButtons = document.querySelectorAll('.btn-confirm-delete-tenant');
    deleteTenantButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            const nama = this.getAttribute('data-nama');

            Swal.fire({
                title: `Hapus Penghuni ${nama}?`,
                text: "Data identitas penghuni akan dihapus permanen!",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#DC2626',
                cancelButtonColor: '#64748B',
                confirmButtonText: 'Ya, Hapus',
                cancelButtonText: 'Batal'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = href;
                }
            });
        });
    });

    const endRentalButtons = document.querySelectorAll('.btn-confirm-end-rental');
    endRentalButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');

            Swal.fire({
                title: 'Selesaikan Masa Sewa?',
                text: "Status kamar akan otomatis kembali menjadi TERSEDIA.",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#0F766E',
                cancelButtonColor: '#64748B',
                confirmButtonText: 'Ya, Selesaikan',
                cancelButtonText: 'Batal'
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = href;
                }
            });
        });
    });

});
