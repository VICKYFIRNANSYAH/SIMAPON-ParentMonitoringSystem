# 🕌 SIMAPON — Sistem Monitoring Pondok (Parent Monitoring System)

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-6.0.5-092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Openpyxl](https://img.shields.io/badge/Openpyxl-3.1.5-orange.svg?style=for-the-badge) ![Pillow](https://img.shields.io/badge/Pillow-12.2.0-red.svg?style=for-the-badge) ![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE) ![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

<p align="center">
  <strong>Languages:</strong> English (default) · <a href="#readme-id">Bahasa Indonesia</a>
</p>

<a id="readme-en"></a>

<p align="center">
  <a href="https://www.unesa.ac.id/" title="State University of Surabaya">
    <img
      src="https://upload.wikimedia.org/wikipedia/commons/f/f4/State_University_of_Surabaya_logo.png"
      alt="State University of Surabaya (UNESA) logo"
      width="160"
    />
  </a>
</p>

<p align="center">
  <strong>Object-Oriented Programming — coursework / project</strong><br />
  <a href="https://www.unesa.ac.id/">State University of Surabaya (UNESA)</a>
</p>

---

**SIMAPON** (Sistem Monitoring Pondok) is an integrated Django-based parent monitoring web application designed for boarding schools (Pondok Pesantren). It enables real-time tracking of student academic and behavioral progress, monthly tuition payments (SPP), leave permits, and custom behavioral conduct logs, acting as a seamless communication bridge between administrators, teachers, and parents.

---

## 📸 Preview & Screenshots

Explore the user interface and main features of the **SIMAPON** web application below:

### 1. Landing Page (Halaman Utama)

A welcoming portal with modern branding introducing the boarding school environment and key platform highlights.

<p align="center">
  <img src="static/screenshots/HalamanUtama.jpeg" alt="SIMAPON Landing Page" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 2. Multi-Role Authentication

Secured entry pages allowing administrators, teachers, and parents to register and log in to access their respective dashboards.

<p align="center">
  <img src="static/screenshots/HalamanLogin.png" alt="SIMAPON Login Page" width="48%" style="border-radius: 8px; margin-right: 2%; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
  <img src="static/screenshots/HalamanRegister.png" alt="SIMAPON Registration Page" width="48%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 3. Administrator Dashboard (Dashboard Admin)

A comprehensive backend command center displaying key metrics, recent registrations, leave requests, and financial updates.

<p align="center">
  <img src="static/screenshots/DashboardAdmin.jpeg" alt="SIMAPON Admin Dashboard" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 4. Teacher Dashboard (Dashboard Guru)

A tailored classroom portal for instructors to review leave permissions, log student conduct scoring, and track class activities.

<p align="center">
  <img src="static/screenshots/DashboardGuru.jpeg" alt="SIMAPON Teacher Dashboard" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 5. Parent Monitoring Dashboard (Dashboard Wali)

A tailored, information-rich view for parents displaying real-time tracking of SPP payments, active leave permissions, and conduct logs.

<p align="center">
  <img src="static/screenshots/DashboardWali.png" alt="SIMAPON Parent Dashboard" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

---

## ✨ Core Features

- 🔐 **Multi-Role Authentication**: Customized dashboard and access control system for Admins, Teachers (Guru), and Parents (Wali).
- 📊 **Dynamic Dashboards**: Interactive metrics highlighting active permissions, payment history, and recent conduct records.
- 👨‍🎓 **Comprehensive Student Management**: Dynamic data entry, student registration profiles, and central database indexing.
- 📝 **Leave Permits System**: Digital permit requesting for parents/teachers with real-time approval status workflow handled by administrators.
- 📈 **Conduct Tracking**: Behavior log detailing positive behaviors and infraction reports to evaluate student character development.
- 💳 **Tuition & Finance (SPP)**: Easy upload of payment receipts for verification, tuition schedule lists, and dynamic status updates.
- 📥 **Bulk Import via Excel**: Excel parser built with `openpyxl` allowing rapid, bulk imports of student and user registry databases.
- 🔔 **Interactive Notification System**: Real-time pop-up alerts and persistent navigation dropdown notifications keeping parents, teachers, and admins informed instantly of database updates and status shifts.

---

## 🏗️ Object-Oriented Programming (OOP) Implementation

**SIMAPON** is built on top of the Django framework, strictly adhering to core OOP principles to ensure maintainability, scalability, and code reuse:

- **🧬 Inheritance (Pewarisan)**
  - `User` inherits from `django.contrib.auth.models.AbstractUser` to implement customized multi-role authentication attributes.
  - Core database entities (`Student`, `Payment`, `LeavePermit`, `BehaviorRecord`) inherit from `models.Model`, gaining robust ORM methods.
  - Form validation classes (e.g., `StudentForm`, `PaymentForm`) inherit from Django’s class-based forms `forms.ModelForm`.
- **🔒 Encapsulation (Encapsulasi)**
  - Data representation and transaction logic are safely packaged within the model classes, hiding implementation details from templates.
  - Controllers (Django Views) encapsulate request-handling routines, processing input payloads and returning specific responses while protecting internal data states.
- **👁️ Abstraction (Abstraksi)**
  - Django ORM abstracts deep, raw SQL queries into clean Python objects, protecting the application layer from changes in database engines.
  - Django forms abstract raw HTML component generation and client/server validation routines into high-level declarative logic.
- **🎭 Polymorphism (Polimorfisme)**
  - Standardized methods like `is_valid()` and `save()` operate polymorphic behaviors across distinct form types.
  - Overriding standard Django Admin methods (e.g., `ModelAdmin`) to dynamically construct access patterns, form views, and layout options based on roles.

---

## 📂 Project Structure

```text
SIMAPON-ParentMonitoringSystem/
├── manage.py                          # Django command-line execution entry point
├── db.sqlite3                         # Local development SQLite3 database file
├── requirements.txt                   # Project package dependencies
├── run.txt                            # Command reference sheet for local/public runs
├── XLSX_FORMAT.md                     # Documentation for bulk upload Excel formats
├── Data Dummy Guru Website SIMAPON.xlsx  # Sample teacher directory database
├── Data Dummy Santri Website SIMAPON.xlsx  # Sample student directory database
├── .gitignore
│
├── SIMAPON/                           # Core configuration directory
│   ├── __init__.py
│   ├── settings.py                    # Project configuration, database setup, installed apps
│   ├── urls.py                        # Root URL routing pathways
│   ├── wsgi.py                        # WSGI entrypoint for production deployment
│   └── asgi.py                        # ASGI entrypoint for production deployment
│
├── users/                             # App: Custom users, multi-role auth, and dashboard controllers
│   ├── admin.py                       # Regulates custom user views on Django Admin
│   ├── apps.py
│   ├── context_processors.py          # Custom context injector serving notification metrics globally
│   ├── forms.py                       # Registration, login, and profile forms
│   ├── models.py                      # Custom User model defining Admin, Guru, Wali, and Notification model
│   ├── signals.py                     # Trigger handlers establishing automated notification alerts
│   ├── urls.py                        # Route endpoints for auth & notification services
│   └── views.py                       # Business logic for auth, registration, dashboards, and alerts
│
├── students/                          # App: Student registry, profiles, and data import logic
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                       # Forms for student entries
│   ├── models.py                      # Student database schema (`Student` model)
│   └── views.py                       # Student data listing views
│
├── finance/                           # App: Tuition management and payment verification
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                       # Forms for payment proof upload
│   ├── models.py                      # SPP invoice schema (`Payment` model)
│   └── views.py                       # SPP status verification controller views
│
├── permits/                           # App: Leave request generation & approval system
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                       # Request and approval workflows forms
│   ├── models.py                      # Leave permission schema (`LeavePermit` model)
│   └── views.py                       # Leave workflow processing view actions
│
├── behavior/                          # App: Student conduct tracking & behavioral scoring
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                       # Forms for conduct record inputs
│   ├── models.py                      # Conduct record schema (`Behavior` model)
│   └── views.py                       # Conduct record views
│
├── static/                            # Shared static resource assets
│   ├── css/
│   │   └── simapon.css                # Custom site styling definitions
│   ├── js/
│   │   └── simapon.js                 # Dynamic DOM manipulation scripts
│   ├── logo-simapon.png               # Official application brand emblem logo
│   └── screenshots/                   # System UI view representations
│       ├── HalamanUtama.jpeg
│       ├── HalamanLogin.png
│       ├── HalamanRegister.png
│       ├── DashboardAdmin.jpeg
│       ├── DashboardGuru.jpeg
│       └── DashboardWali.png
│
└── templates/                         # HTML structure templates
    ├── base.html                      # Main HTML scaffold, notification dropdown, and toast script
    ├── index.html                     # Root portal redirect view
    ├── landing.html                   # Interactive home interface
    ├── dashboards/                    # Customized role-based dashboards
    │   ├── admin_base.html            # Main base dashboard scaffold for administrators
    │   ├── admin.html                 # Admin center home overview
    │   ├── admin_santri.html          # Admin view for student database
    │   ├── admin_guru.html            # Admin view for teacher registry
    │   ├── admin_parent.html          # Admin view for parents registry
    │   ├── admin_finance.html         # Admin view for tuition dashboard
    │   ├── admin_permit.html          # Admin view for student permit review
    │   ├── admin_behavior.html        # Admin view for student conduct log
    │   ├── edit_*.html                # Target record update views
    │   ├── guru.html                  # Dashboard view tailored for teachers
    │   └── parent.html                # Parent student monitoring dashboard
    └── registration/
        ├── login.html                 # Custom user auth login screen
        └── register.html              # Dynamic multi-role registration form
```

---

## 🛠️ System Requirements

Ensure the following development dependencies are installed on your environment:

- **Python 3.12+**
- **pip** (Python package installer)
- **Git**

---

## 🚀 Installation & Setup

Follow these steps to run the application locally on your machine:

### 1. Clone the Repository

```bash
git clone https://github.com/VICKYFIRNANSYAH/SIMAPON-ParentMonitoringSystem.git
cd SIMAPON-ParentMonitoringSystem
```

### 2. Configure Virtual Environment

Set up a virtual environment to manage dependencies securely without conflicts:

**For Windows:**

```cmd
python -m venv venv_windows
venv_windows\Scripts\activate
```

**For Linux / macOS:**

```bash
python3 -m venv venv_linux
source venv_linux/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup & Migrations

Create the SQLite database schema structures:

```bash
python manage.py migrate
```

_(Optional)_ Create an initial administrative superuser profile:

```bash
python manage.py createsuperuser
```

### 5. Start the Development Server

Launch the Django server:

```bash
python manage.py runserver 0.0.0.0:8000
```

Open your browser and navigate to: **[http://localhost:8000](http://localhost:8000)** or **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🌐 Public Tunneling (Optional Dev Feature)

To share the application over the public internet (for demos, evaluations, or external parent testing) without deployment hosting:

1. Ensure the development server is active.
2. Open a new terminal session, and execute Cloudflared:

```bash
cloudflared tunnel --url http://localhost:8000
```

---

## 📄 License & Credits

- **Source Code**: Licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
- **UNESA Logo**: Sourced from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:State_University_of_Surabaya_logo.png) (**CC BY-SA 4.0**). Trademarks belong to the Universitas Negeri Surabaya.
- **Technologies**: Powered by the Django web framework, openpyxl for Excel sheet parsing, and Pillow for image uploading validation.

---

## 👥 Authors & Team Members

This project was developed by:

| Avatar | Member | Role / Responsibilities | GitHub Profile |
| :---: | :--- | :--- | :--- |
| <img src="https://github.com/VICKYFIRNANSYAH.png" width="48" style="border-radius:50%;" /> | **Muhammad Vicky Firnansyah**<br />`25051204089` | Group Lead, Architecture, Multi-role Dashboards | [@VICKYFIRNANSYAH](https://github.com/VICKYFIRNANSYAH) |
| <img src="https://github.com/24wahyus-creator.png" width="48" style="border-radius:50%;" /> | **M. Wahyu Setya Agung**<br />`25051204095` | Financial System & Excel Parser Integration | [@24wahyus-creator](https://github.com/24wahyus-creator) |
| <img src="https://github.com/aldiokhasy.png" width="48" style="border-radius:50%;" /> | **Aldio Khasy Shiham**<br />`25051204238` | Permits Workflow & Character Score Logs | [@aldiokhasy](https://github.com/aldiokhasy) |
| <img src="https://github.com/ahmadsyaifulloh274-ai.png" width="48" style="border-radius:50%;" /> | **Ahmad Syaifulloh**<br />`25051204385` | Database Optimization & Technical Documentation | [@el-mas-dev](https://github.com/el-mas-dev) |

---

<a id="readme-id"></a>

## Bahasa Indonesia

<p align="center">
  <a href="#readme-en">↑ Kembali ke Bahasa Inggris</a>
</p>

**SIMAPON** (Sistem Monitoring Pondok) adalah aplikasi pemantauan santri berbasis web yang dibangun dengan framework Django. Sistem ini dirancang untuk mempermudah komunikasi serta pemantauan akademik, kehadiran, perizinan, riwayat keuangan (SPP), dan catatan perkembangan perilaku santri secara langsung oleh para orang tua/wali murid, guru, dan administrator pondok pesantren.

---

## 📸 Pratinjau & Tangkapan Layar

Berikut adalah tampilan antarmuka dan fitur-fitur utama dari sistem **SIMAPON**:

### 1. Halaman Utama (Landing Page)

Pintu masuk yang ramah dengan branding modern, memperkenalkan lingkungan pondok pesantren dan poin-poin utama platform.

<p align="center">
  <img src="static/screenshots/HalamanUtama.jpeg" alt="SIMAPON Landing Page" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 2. Autentikasi Multi-Role

Halaman registrasi dan login yang aman untuk memungkinkan administrator, guru, dan wali murid mengakses dasbor sistem masing-masing.

<p align="center">
  <img src="static/screenshots/HalamanLogin.png" alt="SIMAPON Login Page" width="48%" style="border-radius: 8px; margin-right: 2%; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
  <img src="static/screenshots/HalamanRegister.png" alt="SIMAPON Registration Page" width="48%" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 3. Dashboard Administrator (Dashboard Admin)

Pusat kendali admin untuk melihat metrik utama, data registrasi wali/guru terbaru, persetujuan izin keluar santri, serta verifikasi bukti SPP.

<p align="center">
  <img src="static/screenshots/DashboardAdmin.jpeg" alt="SIMAPON Admin Dashboard" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 4. Dashboard Guru (Dashboard Guru)

Dasbor bagi guru pengajar untuk mengevaluasi skor kedisiplinan/perilaku santri, merekomendasikan izin keluar, dan memantau status murid.

<p align="center">
  <img src="static/screenshots/DashboardGuru.jpeg" alt="SIMAPON Teacher Dashboard" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

### 5. Dashboard Wali Murid (Dashboard Wali)

Tampilan khusus yang kaya informasi bagi wali murid untuk melacak pembayaran SPP, status perizinan aktif, dan catatan perilaku secara real-time.

<p align="center">
  <img src="static/screenshots/DashboardWali.png" alt="SIMAPON Parent Dashboard" width="720" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.15);" />
</p>

---

## ✨ Fitur Utama

- 🔐 **Registrasi & Login Multi-role**: Sistem login dan dasbor kustom berdasarkan peran untuk Admin, Guru, dan Wali Murid.
- 📊 **Dasbor Dinamis**: Metrik interaktif yang menampilkan status perizinan aktif, riwayat pembayaran, dan catatan perilaku terbaru.
- 👨‍🎓 **Manajemen Santri Komprehensif**: Entri data dinamis, profil registrasi santri, dan pengindeksan basis data terpusat.
- 📝 **Sistem Perizinan Keluar (Leave Permits)**: Pengajuan izin keluar santri secara digital oleh wali/guru dengan alur persetujuan waktu nyata (real-time) oleh administrator.
- 📈 **Catatan Perilaku (Behavior Tracking)**: Log sikap santri yang mencakup tindakan positif dan pelanggaran untuk mengevaluasi perkembangan karakter santri.
- 💳 **Keuangan & SPP**: Kemudahan unggah bukti pembayaran untuk verifikasi admin, daftar jadwal tagihan SPP, dan pembaruan status transaksi secara dinamis.
- 📥 **Impor Massal via Excel**: Fitur impor massal data santri dan registrasi pengguna secara cepat menggunakan pengolah Excel berbasis `openpyxl`.
- 🔔 **Sistem Notifikasi Real-Time**: Alur notifikasi interaktif dalam aplikasi untuk menyampaikan pembaruan persetujuan izin, pembayaran SPP, dan catatan kedisiplinan secara langsung bagi seluruh pengguna melalui pop-up toast dan menu dropdown lonceng di navbar.

---

## 🏗️ Implementasi Object-Oriented Programming (OOP)

Aplikasi **SIMAPON** dirancang dengan menerapkan pilar utama konsep pemrograman berorientasi objek (OOP) di dalam arsitektur Django:

- **🧬 Inheritance (Pewarisan)**
  - Kelas `User` mewarisi dari `django.contrib.auth.models.AbstractUser` untuk membangun otentikasi multi-role.
  - Kelas data model (`Student`, `Payment`, `LeavePermit`, `BehaviorRecord`) mewarisi fungsionalitas ORM dari `models.Model`.
  - Struktur form validasi (contoh: `StudentForm`, `PaymentForm`) mewarisi kelas bawaan Django `forms.ModelForm`.
- **🔒 Encapsulation (Enkapsulasi)**
  - Representasi data dan logika transaksi dibungkus dengan aman di dalam kelas model, menyembunyikan detail implementasi dari template.
  - Controller (Django Views) mengenkapsulasi rutinitas penanganan permintaan, memproses payload input, dan mengembalikan respons tertentu sembari melindungi status data internal.
- **👁️ Abstraction (Abstraksi)**
  - Django ORM mengabstraksi query SQL mentah yang kompleks menjadi objek Python yang bersih, melindungi lapisan aplikasi dari perubahan pada mesin basis data.
  - Formulir Django mengabstraksi pembuatan komponen HTML mentah serta rutinitas validasi klien/server ke dalam logika deklaratif tingkat tinggi.
- **🎭 Polymorphism (Polimorfisme)**
  - Metode standar seperti `is_valid()` dan `save()` menjalankan perilaku polimorfik di berbagai jenis formulir yang berbeda.
  - Melakukan override pada metode standar Django Admin (misalnya, `ModelAdmin`) untuk menyusun pola akses, tampilan formulir, dan opsi tata letak secara dinamis berdasarkan peran pengguna.

---

## 📂 Struktur Proyek

Detail struktur file dan direktori sama seperti yang tertera pada bagian [**Project Structure**](#-project-structure) di atas.

---

## 🛠️ Persyaratan Sistem

Pastikan perangkat Anda memiliki dependensi berikut:

- **Python 3.12+**
- **pip** (Penginstal pustaka Python)
- **Git**

---

## 🚀 Instalasi & Menjalankan Program

Ikuti langkah-langkah di bawah ini untuk menjalankan SIMAPON di komputer Anda:

### 1. Klon Repositori

```bash
git clone https://github.com/VICKYFIRNANSYAH/SIMAPON-ParentMonitoringSystem.git
cd SIMAPON-ParentMonitoringSystem
```

### 2. Konfigurasi Virtual Environment

Siapkan virtual environment untuk mengelola dependensi dengan aman tanpa konflik:

**Di Windows:**

```cmd
python -m venv venv_windows
venv_windows\Scripts\activate
```

**Di Linux / macOS:**

```bash
python3 -m venv venv_linux
source venv_linux/bin/activate
```

### 3. Pasang Dependensi

```bash
pip install -r requirements.txt
```

### 4. Setup Database & Migrasi

Buat struktur skema basis data SQLite:

```bash
python manage.py migrate
```

_(Opsional)_ Buat akun superuser sebagai akses administrator:

```bash
python manage.py createsuperuser
```

### 5. Jalankan Server Aplikasi

Jalankan server Django:

```bash
python manage.py runserver 0.0.0.0:8000
```

Buka browser Anda dan navigasikan ke: **[http://localhost:8000](http://localhost:8000)** atau **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🌐 Publikasi Sementara (Tunneling Cloudflared)

Untuk membagikan aplikasi melalui internet publik (untuk demo, evaluasi, atau pengujian luar oleh wali murid) tanpa hosting deployment:

1. Pastikan server pengembangan aktif.
2. Buka sesi terminal baru, dan jalankan Cloudflared:

```bash
cloudflared tunnel --url http://localhost:8000
```

---

## 📄 Lisensi & Kredit

- **Kode Sumber**: Berlisensi di bawah **MIT License** — lihat [LICENSE](LICENSE) untuk detailnya.
- **Logo UNESA**: Diambil dari [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:State_University_of_Surabaya_logo.png) (**CC BY-SA 4.0**). Merek dagang milik Universitas Negeri Surabaya.
- **Teknologi**: Didukung oleh framework web Django, `openpyxl` untuk parsing lembar kerja Excel, dan `Pillow` untuk validasi pengunggahan gambar.

---

## 👥 Tim Pengembang

Proyek ini dibangun dan dikembangkan oleh:

| Avatar | Anggota | Peran / Tanggung Jawab | Profil GitHub |
| :---: | :--- | :--- | :--- |
| <img src="https://github.com/VICKYFIRNANSYAH.png" width="48" style="border-radius:50%;" /> | **Muhammad Vicky Firnansyah**<br />`25051204089` | Arsitektur Sistem, Desain Dashboard Multi-role | [@VICKYFIRNANSYAH](https://github.com/VICKYFIRNANSYAH) |
| <img src="https://github.com/24wahyus-creator.png" width="48" style="border-radius:50%;" /> | **M. Wahyu Setya Agung**<br />`25051204095` | Integrasi Pembayaran & Parser Impor Excel | [@24wahyus-creator](https://github.com/24wahyus-creator) |
| <img src="https://github.com/aldiokhasy.png" width="48" style="border-radius:50%;" /> | **Aldio Khasy Shiham**<br />`25051204238` | Sistem Alur Perizinan & Rekap Sikap Santri | [@aldiokhasy](https://github.com/aldiokhasy) |
| <img src="https://github.com/ahmadsyaifulloh274-ai.png" width="48" style="border-radius:50%;" /> | **Ahmad Syaifulloh**<br />`25051204385` | Pengelolaan Database & Dokumentasi Teknis | [@ahmadsyaifulloh274-ai](https://github.com/ahmadsyaifulloh274-ai) |

---

> Dibuat untuk project akhir mata kuliah Pemrograman Berorientasi Objek (PBO) menggunakan Django di Universitas Negeri Surabaya.
