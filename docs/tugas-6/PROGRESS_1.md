# Individual Assignment 6 — Progress 1

**Tanggal:** 4 November 2026
**Fokus:** Audit implementasi dan pengembangan awal Tugas 6
**Status:** IN PROGRESS

## 1. Kondisi Awal

- **Repository:** `/Users/devanmacbook/Documents/01_Kuliah/MAIN_KULIAH/Semester-3/PBP/Tugas-Individu/Tugas-Individu/myportofolio`
- **Branch aktif:** `main`
- **Commit baseline:** `e4e1ae8 Finish Tutorial 07: Django REST Framework Implementation`
- **Working tree awal:** bersih (tidak ada perubahan staged/unstaged/untracked)
- **Remote:** `origin` (GitHub `glennjosia7/myportofolio`), `pws` (PWS UI)
- **Python:** `.venv/bin/python` versi 3.14.8
- **Django:** 5.2.18
- **Django REST Framework:** 3.18.3

Hasil pemeriksaan awal:

```text
python manage.py check          -> System check identified no issues (0 silenced).
python manage.py migrate --check -> tidak ada migrasi tertunda (exit 0)
python manage.py test main.tests_api --verbosity 2 -> Ran 28 tests, OK
python manage.py test main      -> Ran 94 tests, OK
```

## 2. Analisis Kebutuhan Tugas 6

Sumber: `tugas-6.pdf` (5 halaman) dan `tutorial-7.pdf` sebagai prasyarat.

Kebutuhan utama:

1. **Serializer** — `ModelSerializer` untuk model bagian sendiri (Certifications), daftar `fields` eksplisit, field star hasil perhitungan read-only, data akun sensitif tidak tampil, validasi teks dengan `strip_tags`.
2. **Permission** — `IsPortfolioOwnerOrEditorOrReadOnly` (atau setara) pada list/detail, `IsAuthenticated` pada star, empat peran berlaku di server.
3. **API View dan URL** — function-based view dengan `@api_view` + `SessionAuthentication`, list (GET/POST), detail (GET/PUT/PATCH/DELETE), star (POST), pencarian lewat query parameter, status 200/201/204/400/403/404, path `<int:...>`.
4. **Integrasi halaman** — list, search, create, star, delete, dan **edit lewat PUT/PATCH API** tanpa reload; error 400/403 lewat toast; `X-CSRFToken`; escaping.
5. **Testing** — `APITestCase` per peran, cek isi database pada penolakan, validasi input, star, dan test CSRF dengan `APIClient(enforce_csrf_checks=True)` + `.login()`.
6. **Eksekusi** — `python manage.py test main` lulus, server berjalan, Browsable API dan halaman Tutorial 07 tetap berfungsi.
7. **Dokumentasi** — README dengan bagian `### Tugas 6`, empat pertanyaan reflektif, dan AI disclosure transparan.

## 3. Fitur yang Sudah Tersedia dari Tutorial 7

Semua klaim diperiksa langsung pada kode, bukan hanya dari laporan sebelumnya.

- **Model:** `Certification` dengan PK integer dan relasi `starred_by` ke `User` (`main/models.py`).
- **Serializer:** `CertificationSerializer` memakai `ModelSerializer`, daftar field eksplisit, `star_count`/`is_starred`/`starred_by_names` sebagai `SerializerMethodField` (read-only), `validate_name`/`validate_issuing_organization`/`validate_credential_id` memakai `strip_tags` (`main/serializers.py`).
- **Permission:** `IsPortfolioOwnerOrEditorOrReadOnly` mengizinkan GET untuk semua, PUT/PATCH hanya untuk superuser atau pemilik izin `main.change_certification`, POST/DELETE hanya superuser (`main/permissions.py`).
- **API view:** `certification_list`, `certification_detail`, `certification_star` memakai `@api_view` + `SessionAuthentication` (`main/api_views.py`).
- **Routing:** `/api/v1/certifications/`, `/api/v1/certifications/<int>/`, `/api/v1/certifications/<int>/star/` dengan nama URL unik `api:*` (`main/api_urls.py`).
- **Halaman:** list, search debounce, create modal, star, delete memakai fetch ke DRF; escaping HTML dan `safeHttpUrl` sudah ada (`templates/certifications.html`).
- **Test:** 15 test Certification API + 13 test Project API (`main/tests_api.py`).

## 4. Kesenjangan Implementasi

| Prioritas | Kesenjangan | Bukti |
|---|---|---|
| 1 | Tombol Edit mengarah ke halaman form HTML legacy (`main:update_certification`), bukan PUT/PATCH API | `templates/certifications.html` memakai `UPDATE_URL_TEMPLATE` dan `<a href=...>` |
| 2 | Belum ada test Editor PUT, test PATCH invalid yang memastikan database tidak berubah, dan test penolakan anonymous untuk seluruh method | `main/tests_api.py` |
| 3 | Bagian `### Tugas 6` beserta empat jawaban reflektif belum ada di README | `README.md` |
| 4 | AI disclosure Tugas 6 belum ditulis | `README.md` |

Catatan: view legacy `update_certification`, `create_certification`, dan `delete_certification` sudah memakai `has_perm` yang konsisten dengan aturan API. Tidak ditemukan view legacy yang memberi hak lebih luas.

## 5. Pekerjaan Progress 1

Perubahan yang dilakukan hari ini:

1. **Modal edit berbasis API**
   - File baru: `templates/components/certification_edit_modal.html`.
   - Berisi form edit dengan field yang sama seperti form tambah, ID unik, dan tombol simpan.
2. **Integrasi halaman Certifications**
   - File: `templates/certifications.html`.
   - Tombol Edit berubah dari link halaman legacy menjadi tombol `data-action="edit"`.
   - Klik Edit mengambil detail dari `GET /api/v1/certifications/<id>/`, mengisi form, lalu menampilkan modal.
   - Submit mengirim `PATCH /api/v1/certifications/<id>/` dengan JSON dan `X-CSRFToken`.
   - Modal hanya dirender untuk pengguna dengan `perms.main.change_certification` (Editor dan superuser).
   - Tanggal kedaluwarsa dikirim sebagai `null` agar bisa dikosongkan.
   - Error 400/403/network ditampilkan lewat toast; tombol submit dinonaktifkan saat proses.
3. **Penguatan test**
   - File: `main/tests_api.py`: test Editor PUT, test PATCH invalid tidak mengubah database, test anonymous ditolak untuk POST/PUT/PATCH/DELETE disertai pengecekan database.
   - File: `main/tests.py`: test halaman memastikan endpoint detail API dan modal edit tersedia untuk superuser/Editor, serta tidak tersedia untuk pengguna biasa.

## 6. Hasil Pengujian

```text
python manage.py check
-> System check identified no issues (0 silenced).

python manage.py migrate --check
-> lulus, tidak ada migrasi tertunda.

python manage.py test main.tests_api --verbosity 2
-> Ran 31 tests, OK (sebelum perubahan: 28 tests).

python manage.py test main
-> Ran 97 tests, OK (sebelum perubahan: 94 tests).
```

Regression API (setelah perubahan):

- `test_editor_can_put_full_update` — Editor PUT 200, data berubah.
- `test_editor_invalid_patch_does_not_change_database` — PATCH nama kosong 400, nama lama tetap.
- `test_anonymous_cannot_write` — POST/PUT/PATCH/DELETE 403, jumlah dan isi database tetap.

Verifikasi browser (Playwright + Chromium headless, server lokal port 8011, data sementara):

```text
Superuser:
LOADED_NAME Temp Browser Cert
RESPONSE PATCH /api/v1/certifications/7/ -> 200
MODAL_CLOSED true
WRITES ["PATCH /api/v1/certifications/7/"]

Editor:
ADD_BUTTON_COUNT 0
DELETE_BUTTON_COUNT 0
RESPONSE PATCH /api/v1/certifications/7/ -> 200
EDITOR_EDIT_OK true
```

Data sementara (1 certification, 1 superuser uji, 1 Editor uji) sudah dihapus setelah pengujian. Database development kembali berisi 1 akun asli dan 0 certification.

## 7. Pekerjaan Tersisa

### Progress 2 — Kamis, 5 November 2026

- Audit ulang seluruh matriks peran pada API dan halaman.
- Tambahan test bila masih ada celah (misalnya method tidak didukung pada collection/detail).
- Verifikasi browser untuk pengguna biasa (tombol edit/hapus tidak muncul) dan percobaan akses langsung.
- Pemeriksaan regresi UI/UX modal (kontras teks, fokus keyboard, toast error).
- Pemeriksaan konsistensi legacy view dan API.

### Finalisasi — Jumat, 6 November 2026

- Menulis bagian `### Tugas 6` berisi empat jawaban reflektif di README.
- Menulis AI disclosure Tugas 6 yang faktual.
- Menambahkan referensi percakapan ChatGPT Website dari pengguna (belum tersedia; jangan dibuat-buat).
- README setup/deskripsi final dan pemeriksaan keamanan dependensi.
- Verifikasi end-to-end final dan review diff.
- Persiapan submisi (tautan commit akhir).

## 8. Rekomendasi Commit Manual

File yang berubah:

```text
templates/certifications.html
templates/components/certification_edit_modal.html   (baru)
main/tests_api.py
main/tests.py
docs/tugas-6/PROGRESS_1.md                           (baru)
```

Pesan commit yang disarankan:

```text
feat(certifications): add DRF-based edit modal for assignment 6
```

Perintah (dijalankan manual oleh pengguna, bukan oleh agen):

```bash
git diff --check
git status --short

git add templates/certifications.html \
        templates/components/certification_edit_modal.html \
        main/tests_api.py main/tests.py \
        docs/tugas-6/PROGRESS_1.md

git diff --cached --check
git diff --cached --stat
git commit -m "feat(certifications): add DRF-based edit modal for assignment 6"
git push origin main
```

## 9. Catatan Penggunaan AI (bahan AI disclosure)

- **Interface:** OpenCode (model DeepSeek V4.1 Flash).
- **Tugas yang dibantu:** audit repository, pembacaan requirement, implementasi modal edit DRF, penulisan test, menjalankan test, verifikasi browser, dan penyusunan dokumen ini.
- **Strategi prompting:** meminta audit berbasis bukti terlebih dahulu, lalu satu irisan pekerjaan (edit via PATCH), kemudian verifikasi test dan browser.
- **Verifikasi manusia:** keputusan lingkup Progress 1, persetujuan perubahan, dan seluruh operasi Git dilakukan oleh pengguna.
- **Batasan:** hasil AI diverifikasi lewat test dan browser; tidak ada hasil test yang dikarang. Referensi percakapan ChatGPT Website untuk Tugas 6 belum tersedia dan tidak dicantumkan pada dokumen ini.
