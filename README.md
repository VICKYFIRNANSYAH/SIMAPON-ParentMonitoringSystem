# SIMAPON — Sistem Monitoring Pondok

SIMAPON adalah aplikasi web monitoring santri berbasis Django. Sistem ini dirancang untuk memudahkan pemantauan informasi santri, SPP, perizinan, dan catatan perilaku oleh Admin, Guru, dan Wali Murid.

## Persyaratan

- Python 3.12+
- pip
- Git

## Instalasi dan Jalankan

1. Buat virtual environment
   - Linux/macOS: `python3 -m venv venv_linux`
   - Windows: `python -m venv venv_windows`

2. Aktifkan virtual environment
   - Linux/macOS: `source venv_linux/bin/activate`
   - Windows: `venv_windows\\Scripts\\activate`

3. Pasang dependensi

   ```bash
   pip install -r requirements.txt
   ```

4. Migrasi database

   ```bash
   python manage.py migrate
   ```

5. Jalankan server

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

6. Buka browser:
   `http://localhost:8000`

## Struktur Proyek Utama

- `manage.py` - entry point Django
- `SIMAPON/` - konfigurasi utama proyek Django
- `users/` - aplikasi untuk autentikasi, dashboard, dan user role
- `students/` - aplikasi data santri
- `finance/` - aplikasi pembayaran SPP
- `permits/` - aplikasi perizinan santri
- `behavior/` - aplikasi catatan perilaku santri
- `templates/` - HTML templates
- `screenshots/` - aset dokumentasi UI
- `XLSX_FORMAT.md` - format import Excel
- `requirements.txt` - daftar paket Python

## Catatan Struktur

- `__init__.py` kosong
  - Ini normal. File kosong ini menandakan folder sebagai Python package.
- `templates/index.html`
  - File ini tidak digunakan oleh URL routing dan telah dihapus.
- `static/`
  - Direktori kosong untuk aset statis. Saya menambahkan file `.gitkeep` untuk menjaga struktur direktori.
- `media/`
  - Digunakan untuk upload file runtime, khususnya `payments/`.
- `db.sqlite3`
  - Basis data lokal pengembangan. Idealnya tidak dibagikan ke Git.
- `venv_linux/` dan `venv_windows/`
  - Virtual environment tidak direkomendasikan dimasukkan ke repository.

## OOP di Dalam Proyek

Aplikasi ini dibangun menggunakan prinsip OOP yang diterapkan di Django:

- **Inheritance / Pewarisan**
  - `User` mewarisi dari `django.contrib.auth.models.AbstractUser`.
  - Semua model mewarisi dari `django.db.models.Model`.
  - Form mewarisi dari `django.forms.ModelForm`.
- **Encapsulation / Enkapsulasi**
  - Data model dan logika validasi tersembunyi di dalam kelas.
  - View memisahkan logika request/response dari template.
- **Abstraction / Abstraksi**
  - Django ORM mengabstraksi SQL menjadi operasi Python.
  - Forms mengabstraksi HTML dan validasi input.
- **Polymorphism / Polimorfisme**
  - Metode umum seperti `save()` dan `is_valid()` dipakai di banyak kelas form.

## Catatan Tambahan

- `.gitignore` sudah diperbarui agar `venv_linux/` dan `venv_windows/` tidak ikut di-Git.
- Jangan masukkan folder virtual environment ke repositori.
- `run.txt` sekarang hanya berisi instruksi setup singkat.
