# Individual Assignment 6 — Progress 2

**Tanggal:** 5 November 2026
**Status:** COMPLETE

## 1. Ringkasan Progress 1

Progress 1 di-commit oleh pengguna sebagai `6870f53 feat(certifications): add DRF-based edit modal for assignment 6`.

Hasil Progress 1 yang diverifikasi ulang:

- Modal edit Certifications memakai `GET` detail API dan `PATCH` ke `/api/v1/certifications/<int>/`.
- Modal hanya tersedia untuk pemilik izin `main.change_certification` (Editor dan superuser).
- Baseline test: 31 API test, 97 total test.
- Working tree bersih sebelum Progress 2.

## 2. Baseline Awal Progress 2

- **Branch:** `main`
- **Commit:** `6870f53` (Progress 1), `e4e1ae8` (Tutorial 07)
- **Python:** 3.14.8 (`.venv`)
- **Django:** 5.2.18
- **DRF:** 3.18.3
- **`manage.py check`:** PASS
- **`manage.py migrate --check`:** PASS (exit 0)
- **`manage.py test main.tests_api`:** 31 test, OK
- **`manage.py test main`:** 97 test, OK

## 3. Audit Permission Empat Peran

Kebijakan diverifikasi di `main/permissions.py`, bukan hanya di template:

| Peran | Read | Create | PUT/PATCH | Delete | Star |
|---|---|---|---|---|---|
| Anonymous | 200 | 403 | 403 | 403 | 403 |
| Pengguna biasa | 200 | 403 | 403 | 403 | 200 |
| Editor | 200 | 403 | 200 | 403 | 200 |
| Superuser | 200 | 201 | 200 | 204 | 200 |

Bukti:

- Anonymous dan pengguna biasa ditolak pada POST/PUT/PATCH/DELETE, dan database tidak berubah.
- Editor hanya lolos jika memiliki Django permission `main.change_certification`; bukan berdasarkan nama grup.
- Superuser lolos seluruh operasi.
- Star selalu memakai `request.user`; status star pengguna lain tidak bocor (`is_starred` dihitung per request).
- Endpoint star memakai `IsAuthenticated`.

## 4. Audit Legacy Views

Route legacy yang diperiksa:

- `main:create_certification` — `login_required` + `has_perm("main.add_certification")`.
- `main:create_certification_ajax` — `has_perm("main.add_certification")`, anonymous ditolak 403.
- `main:update_certification` — `login_required` + `has_perm("main.change_certification")`.
- `main:delete_certification` — `login_required` + `has_perm("main.delete_certification")`.
- `main:toggle_star_certification` — `login_required`, semua pengguna login boleh star.

Tidak ditemukan route legacy yang memberi hak lebih luas. Pengujian POST langsung oleh pengguna biasa dan Editor menghasilkan 403, dengan jumlah dan isi database tetap. Halaman edit legacy tetap memakai form POST dan masih kompatibel, tetapi bukan lagi jalur edit utama di halaman Certifications.

## 5. Verifikasi Session dan CSRF

- Tidak ada `csrf_exempt` di `main/` maupun `portofolio/`.
- `SessionAuthentication` terpasang eksplisit pada seluruh API view Certifications.
- Test yang sudah ada dan tetap lulus:
  - `test_session_write_without_csrf_is_rejected` — login sesi nyata, PATCH tanpa token → 403, database tidak berubah.
  - `test_session_write_with_csrf_succeeds` — login sesi nyata + token valid → 200, data berubah.
- Browser test membuktikan setiap PATCH/POST/DELETE mengirim `X-CSRFToken`; tidak ada respons sukses palsu saat permintaan ditolak.
- Star pengguna biasa berhasil lewat sesi browser dan kembali ke keadaan semula setelah unstar.

## 6. Pengujian Frontend Certifications

Browser: Playwright + Chromium headless, server lokal port 8012, data sementara.

| Peran | Hasil |
|---|---|
| Pengguna biasa | 2 kartu terlihat; tombol Add/Edit/Delete = 0; tombol Star = 2; star 0 → 1 → 0; PATCH/POST/DELETE langsung = 403; tidak ada navigasi tak terduga |
| Anonymous | 2 kartu terlihat; seluruh tombol tulis = 0; 2 tautan "Login to star"; PATCH langsung = 403 |
| Editor | Add = 0, Delete = 0, Edit = 2; prefill nama/organisasi/URL benar; PATCH = 200; toast sukses; POST/DELETE langsung = 403 |
| Superuser | Create = 201; Edit = 200; Delete = 204; validasi nama kosong = 400 + toast error; search debounce bekerja |

Respons jaringan yang tercatat:

```text
POST /api/v1/certifications/13/star/ -> 200
POST /api/v1/certifications/13/star/ -> 200
PATCH /api/v1/certifications/12/ -> 403   (pengguna biasa)
POST /api/v1/certifications/ -> 403       (pengguna biasa)
DELETE /api/v1/certifications/12/ -> 403  (pengguna biasa)
POST /api/v1/certifications/ -> 403       (Editor)
DELETE /api/v1/certifications/12/ -> 403  (Editor)
PATCH /api/v1/certifications/12/ -> 200   (Editor)
POST /api/v1/certifications/ -> 400       (validasi)
POST /api/v1/certifications/ -> 201       (superuser)
PATCH /api/v1/certifications/14/ -> 200   (superuser)
DELETE /api/v1/certifications/14/ -> 204  (superuser)
```

Setelah pengujian, database development kembali berisi 1 akun asli dan 0 certification. Tidak ada data pengguna permanen yang diubah.

## 7. Pengujian Modal dan Aksesibilitas

Modal edit:

- Terbuka dengan data Certification yang dipilih.
- Tidak menampilkan data basi saat berpindah dari Alpha Cert ke Beta Cert.
- Tanggal kedaluwarsa terisi `2028-02-02` dan dapat dikosongkan lewat PATCH (`null`).
- Tertutup lewat Escape, tombol Batal, dan ikon close.
- Fokus awal berada di dalam dialog (tombol Batal).
- Tombol submit dinonaktifkan saat proses; modal tetap terbuka dan nilai input dipertahankan saat error 400.
- Modal Add dan Edit tidak saling mengganggu.

Kontras terukur (WCAG AA minimum 4.5:1 untuk teks normal):

```text
Heading            17.27:1
Label              17.27:1
Input text         15.19:1
Placeholder         8.20:1
Primary button      8.30:1
Secondary button   17.27:1
Close icon          9.32:1
Focus outline      15.19:1 (2 px)
```

Responsif:

```text
390 px  : overflow 0; submit terlihat; konten modal dapat di-scroll
768 px  : overflow 0 setelah perbaikan; actions terlihat; date field terlihat
1440 px : overflow 0; actions terlihat
```

Ditemukan overflow horizontal 7 px pada 768 px akibat navbar horizontal. Diperbaiki dengan `flex-wrap: wrap` dan perataan kanan pada `.site-header nav`.

Perbaikan kecil aksesibilitas: label backdrop modal Add/Edit dibedakan dari tombol close agar nama aksesibel tidak duplikat.

## 8. Perubahan Kode

Kode aplikasi:

- `static/css/style.css` — navbar dapat wrap agar tidak overflow di 768 px.
- `templates/components/certification_form_modal.html` — `aria-label` backdrop dibedakan.
- `templates/components/certification_edit_modal.html` — `aria-label` backdrop dibedakan.

Test:

- `main/tests_api.py` — 3 test baru:
  - pengguna biasa tidak boleh create/delete;
  - method tidak didukung → 405 dan ID tidak valid → 404;
  - star terikat pada `request.user`.
- `main/tests.py` — 1 test baru: percobaan POST langsung ke route legacy oleh pengguna biasa dan Editor ditolak, database tidak berubah.

Dokumentasi:

- `docs/tugas-6/PROGRESS_2.md` (file ini).

Tidak ada perubahan model, migrasi, serializer, permission class, API view, dependency, atau data permanen.

## 9. Hasil Pengujian Otomatis

```text
python manage.py check
-> System check identified no issues (0 silenced).

python manage.py migrate --check
-> PASS, tidak ada migrasi tertunda.

python manage.py test main.tests_api --verbosity 2
-> Ran 34 tests, OK (baseline 31).

python manage.py test main
-> Ran 101 tests, OK (baseline 97).
```

Tidak ada test yang dihapus atau dilemahkan.

## 10. Hasil Browser QA

Semua skenario pada bagian 6 dan 7 dijalankan dengan browser sungguhan. Screenshot desktop disimpan sementara di luar repository (`progress2-certifications.png`) dan tidak di-commit.

Yang belum diverifikasi di browser:

- Pengguna biasa menekan tombol Edit secara visual — tombol memang tidak dirender; percobaan langsung lewat API diuji terpisah.
- Focus trap penuh di dalam modal — popover native tidak mengunci fokus; fokus awal berada di dalam dialog dan Escape menutup modal.

## 11. Kesenjangan yang Tersisa

Tidak ada gap fungsional atau otorisasi yang ditemukan pada lingkup Tugas 6.

Sisa pekerjaan bersifat dokumentasi dan finalisasi:

- Bagian `### Tugas 6` dan empat jawaban reflektif di README.
- AI disclosure final dan referensi percakapan ChatGPT Website dari pengguna.
- Review diff akhir dan verifikasi end-to-end penuh.
- Persiapan submisi berupa tautan commit.

## 12. Rencana Finalisasi

Jumat, 6 November 2026:

1. Tulis empat jawaban reflektif Tugas 6 di README.
2. Tulis AI disclosure faktual: ChatGPT Website (jika pengguna menyediakan referensi) dan OpenCode/DeepSeek V4.1 Flash.
3. Verifikasi akhir `manage.py check`, `migrate --check`, dan seluruh test.
4. Review diff, pastikan tidak ada file sensitif atau artefak test.
5. Siapkan tautan commit untuk SCELE.

## 13. Rekomendasi Commit Manual

File yang berubah:

```text
static/css/style.css
templates/components/certification_form_modal.html
templates/components/certification_edit_modal.html
main/tests_api.py
main/tests.py
docs/tugas-6/PROGRESS_2.md   (baru)
```

Pesan commit:

```text
test(certifications): strengthen role, legacy, and responsive regression coverage
```

Perintah (dijalankan manual oleh pengguna, bukan agen):

```bash
git diff --check
git status --short
git add static/css/style.css \
        templates/components/certification_form_modal.html \
        templates/components/certification_edit_modal.html \
        main/tests_api.py main/tests.py \
        docs/tugas-6/PROGRESS_2.md
git diff --cached --check
git diff --cached --stat
git commit -m "test(certifications): strengthen role, legacy, and responsive regression coverage"
git push origin main
```

## 14. Catatan Penggunaan AI

- **Interface:** OpenCode.
- **Model:** DeepSeek V4.1 Flash.
- **Dibantu AI:** audit izin, penulisan test, browser QA, pengukuran kontras/responsif, dan dokumentasi.
- **Verifikasi manusia:** keputusan lingkup, persetujuan perubahan, dan seluruh operasi Git.
- **Batasan:** referensi percakapan ChatGPT Website belum tersedia dan tidak dicantumkan; tidak ada hasil test yang dikarang.
