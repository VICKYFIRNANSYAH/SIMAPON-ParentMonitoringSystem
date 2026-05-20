# Format Data XLSX untuk Import

Dokumen ini menjelaskan format yang diperlukan untuk mengimpor data Santri dan Guru ke dalam sistem SIMAPON.

## 1. Format Import Data Santri

Gunakan file dengan format `.xlsx` atau `.csv` dengan kolom-kolom berikut:

### Kolom yang Diperlukan:

| Kolom             | Alias Alternatif  | Tipe Data | Wajib | Keterangan                                 |
| ----------------- | ----------------- | --------- | ----- | ------------------------------------------ |
| `nis`             | `NIS`             | Text      | ✓     | Nomor Induk Santri (unik, max 20 karakter) |
| `name`            | `Name`            | Text      | ✓     | Nama lengkap santri (max 100 karakter)     |
| `grade`           | `Grade`           | Text      | ✓     | Kelas santri (max 50 karakter)             |
| `birth_date`      | `Birth Date`      | Date      | ✓     | Tanggal lahir                              |
| `parent_username` | `Parent Username` | Text      | ✗     | Username wali murid yang sudah terdaftar   |
| `parent_email`    | `Parent Email`    | Text      | ✗     | Email wali murid (jika tidak ada username) |

**Catatan**: Parent bersifat opsional. Jika kosong, santri akan dibuat tanpa wali murid.

### Format Tanggal yang Didukung:

Sistem secara otomatis memahami berbagai format tanggal:

- `DD/MM/YYYY` (contoh: 15/05/2010)
- `YYYY-MM-DD` (contoh: 2010-05-15)
- `DD-MM-YYYY` (contoh: 15-05-2010)
- `MM/DD/YYYY` (contoh: 05/15/2010)

### Contoh Data Santri (XLSX):

```
nis      | name            | grade | birth_date | parent_username
======== | =============== | ===== | ========== | ================
001001   | Ahmad Rizki     | 1A    | 15/05/2010 | ibu_ani
001002   | Nur Azizah      | 1A    | 22/08/2010 | ibu_ani
001003   | Muhammad Fauzi  | 1B    | 10/03/2011 |
```

**Catatan**: Row ketiga tidak punya parent (opsional).

### Contoh Data Santri (CSV):

```csv
nis,name,grade,birth_date,parent_username
001001,Ahmad Rizki,1A,15/05/2010,ibu_ani
001002,Nur Azizah,1A,22/08/2010,ibu_ani
001003,Muhammad Fauzi,1B,10/03/2011,
```

### Catatan Import Santri:

- **NIS** harus unik (tidak boleh duplikat dengan data yang sudah ada)
- **Tanggal lahir** wajib diisi dan akan otomatis dikonversi ke format yang valid
- **Parent** opsional - jika kosong maka santri dibuat tanpa wali murid
- Jika parent_username tidak ditemukan, baris akan dilewatkan
- Sistem secara otomatis memahami berbagai format input (text, number, date)
- Baris yang tidak valid akan dilewatkan dengan notifikasi di akhir import

---

## 2. Format Import Data Guru

Gunakan file dengan format `.xlsx` atau `.csv` dengan kolom-kolom berikut:

### Kolom yang Diperlukan:

| Kolom          | Alias Alternatif | Tipe Data | Keterangan                                       |
| -------------- | ---------------- | --------- | ------------------------------------------------ |
| `username`     | `Username`       | Text      | Username guru (unik, max 150 karakter)           |
| `email`        | `Email`          | Text      | Email guru (unik, format email valid)            |
| `phone_number` | `Phone`, `phone` | Text      | Nomor telepon (opsional, max 15 karakter)        |
| `password`     | `Password`       | Text      | Password guru (opsional, default: 'password123') |

### Contoh Data Guru (XLSX):

```
username    | email              | phone_number | password
=========== | ================== | ============ | ========
pak_ahmad   | ahmad@sekolah.com  | 081234567890 | Guru@2024
ibu_sarah   | sarah@sekolah.com  | 082345678901 |
pak_budi    | budi@sekolah.com   | 083456789012 | Budi@2024
```

### Contoh Data Guru (CSV):

```csv
username,email,phone_number,password
pak_ahmad,ahmad@sekolah.com,081234567890,Guru@2024
ibu_sarah,sarah@sekolah.com,082345678901,
pak_budi,budi@sekolah.com,083456789012,Budi@2024
```

### Catatan Import Guru:

- **Username** dan **Email** wajib diisi dan harus unik
- Password bersifat opsional; jika kosong maka akan menggunakan default: `password123`
- Phone number bersifat opsional
- Baris yang tidak valid akan dilewatkan
- Kolom nama tidak ada pada import (nama akan menggunakan username)

---

## 3. Panduan Membuat File XLSX

### Menggunakan Microsoft Excel / LibreOffice Calc:

1. Buat spreadsheet baru
2. Tambahkan header di baris pertama sesuai dengan tabel di atas
3. Isi data mulai dari baris kedua
4. Simpan dengan format `.xlsx` (Excel 2007 dan lebih baru)

### Tips:

- **Sistem otomatis**: Tidak perlu khawatir tentang format - sistem akan otomatis mengenali berbagai tipe input (text, number, date, float)
- **Tanggal fleksibel**: Format tanggal bisa DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY, atau MM/DD/YYYY
- **Alias kolom**: Gunakan salah satu dari alias yang tersedia (case-insensitive)
- **Spasi otomatis**: Spasi di awal/akhir sel akan otomatis dihapus
- **Angka otomatis**: Angka akan otomatis dikonversi ke text jika diperlukan
- **Excel & LibreOffice**: Kompatibel dengan Excel dan LibreOffice Calc

---

## 4. Error Handling

### Pesan Error Umum:

- **"NIS sudah terdaftar"** → NIS sudah ada di database, gunakan NIS baru
- **"Baris dilewatkan"** → Ada kolom wajib yang kosong atau tanggal tidak valid
- **"Username/Email sudah terdaftar"** → Username atau email guru sudah ada
- **"Error saat import: ..."** → Error spesifik akan ditampilkan di pesan

### Fitur Otomatis Sistem:

- **Konversi tipe data**: Otomatis mengkonversi float, int, date ke string format yang valid
- **Format tanggal**: Otomatis mendeteksi dan mengonversi berbagai format tanggal ke DD/MM/YYYY
- **Alias kolom**: Case-insensitive, mendukung berbagai variasi nama kolom (nis/NIS, name/Name, dll)
- **Whitespace**: Otomatis menghapus spasi di awal dan akhir setiap cell
- **Nullable fields**: Untuk field opsional (parent, password), kosong diizinkan

### Rekomendasi:

- **Preview data**: Buka file di Excel/Calc untuk verifikasi sebelum upload
- **Test import**: Lakukan test dengan beberapa baris dulu
- **Error checking**: Perhatikan pesan di akhir import (berapa yang berhasil, berapa dilewati)
- **Kolom header**: Pastikan header row ada (baris pertama)
- **Format konsisten**: Gunakan format yang sama untuk semua baris di kolom yang sama
