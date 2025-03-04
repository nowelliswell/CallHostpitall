# Dokumentasi Aplikasi Sistem Pemanggilan Rumah Sakit

## Deskripsi Umum
Aplikasi Sistem Pemanggilan Rumah Sakit adalah aplikasi berbasis GUI yang dirancang untuk mengelola antrian pasien di berbagai poli rumah sakit. Aplikasi ini memungkinkan petugas untuk menambahkan pasien ke dalam antrian, memanggil pasien, dan mengelola riwayat pemanggilan.

## Fitur
1. **Manajemen Antrian**: 
   - Menambahkan pasien ke dalam antrian untuk poli yang dipilih.
   - Memanggil pasien berikutnya dari antrian.
   - Menghapus riwayat pemanggilan pasien.

2. **Restore Data**: 
   - Memulihkan data antrian dari file cadangan.

3. **Penyimpanan Data**: 
   - Menyimpan data antrian ke dalam file JSON dan database SQLite.

4. **Antarmuka Pengguna**: 
   - Antarmuka yang intuitif dan mudah digunakan dengan elemen GUI yang jelas.

5. **Pengumuman Suara**: 
   - Menggunakan text-to-speech untuk mengumumkan nomor antrian pasien.

## Cara Penggunaan
1. **Menjalankan Aplikasi**:
   - Jalankan file `main.py` untuk memulai aplikasi.

2. **Menambahkan Pasien**:
   - Pilih poli dari dropdown.
   - Masukkan nama pasien di kolom yang disediakan.
   - Klik tombol "Tambahkan Ke Antrian".

3. **Memanggil Pasien**:
   - Klik tombol "Panggil Berikutnya" untuk memanggil pasien berikutnya dari antrian.

4. **Menghapus Riwayat Pemanggilan**:
   - Pilih pasien dari daftar riwayat pemanggilan.
   - Klik tombol "DELETE HISTORY" untuk menghapus riwayat pemanggilan pasien yang dipilih.

5. **Memulihkan Data**:
   - Klik tombol "Restore Data" untuk memulihkan data dari file cadangan jika diperlukan.

## Struktur Kode
Aplikasi ini terdiri dari beberapa file Python yang terpisah untuk meningkatkan keterbacaan dan pemeliharaan kode:

1. **main.py**: 
   - Titik masuk aplikasi. Menginisialisasi Tkinter dan menjalankan aplikasi.

2. **app.py**: 
   - Mengandung kelas `HospitalApp` yang mengelola antarmuka pengguna dan interaksi.

3. **queue_manager.py**: 
   - Mengandung kelas `QueueManager` yang mengelola antrian pasien dan data terkait.

4. **database.py**: 
   - Mengandung fungsi untuk menyimpan dan memuat data dari database SQLite.

5. **tts.py**: 
   - Mengandung fungsi untuk melakukan text-to-speech menggunakan gTTS.

6. **utils.py**: 
   - Mengandung fungsi utilitas seperti logging, validasi nama, dan pemulihan data.

7. **styles.py**: 
   - Mengandung pengaturan gaya untuk antarmuka pengguna.

## Instalasi
1. Pastikan Anda memiliki Python 3.x terinstal di sistem Anda.
2. Instal dependensi yang diperlukan dengan menjalankan:
   ```bash
   pip install pygame gtts pyttsx3