# Tutorial 10 — Laporan Backend Django

Baseline `bfddf57` pada `main` yang melacak `origin/main`. Implementasi
mengacu pada Tutorial 10 halaman 2–4 dan kontrak `ProjectSerializer` dari
Tutorial 07. Perubahan ditinjau dan diuji di salinan kerja terisolasi.

## Perubahan

- Daftarkan `rest_framework.authtoken` dan `django-cors-headers`.
- Aktifkan TokenAuthentication dan SessionAuthentication. `project_list`
  menerima token karena sebelumnya menetapkan autentikasi sesi secara eksplisit.
- Pertahankan kode 403 untuk penulisan anonim seperti sebelumnya. Header
  `Token` yang tidak valid menghasilkan 401, agar klien dapat meminta login ulang.
- Tambah `POST /api/v1/auth/token/` dan `POST /api/v1/auth/logout/`. Logout
  menghapus token yang dipakai permintaan dan mempertahankan sesi web Django.
- CORS lokal dibatasi ke origin loopback pada mode pengembangan. Produksi
  memakai daftar origin eksplisit dan middleware hanya melayani `/api/v1/`.
- Project GET tetap publik. POST tetap hanya untuk superuser. Endpoint
  Certification, star, permission Editor, serta CSRF tetap mengikuti kode lama.

## Bukti

| Pemeriksaan | Hasil |
|---|---|
| Baseline `check`, migrasi SQLite, `migrate --check`, `test main` | Lulus, 101 test |
| `check`, migrasi authtoken 0001–0004, `migrate --check`, `makemigrations --check --dry-run` | Lulus dengan settings uji yang mengecualikan middleware CORS |
| Regresi lama dan lima uji token baru | 106 test lulus pada settings uji tersebut |
| CORS preflight dan penolakan origin lainnya | Terblokir karena `django-cors-headers` belum terpasang |
| Migrasi dan server pada repo Django asli | Belum dijalankan. Patch menunggu penerapan pada workspace yang dapat menulis ke repo. |

Pengujian memakai akun fixture dan SQLite sementara. Status CORS perlu
verifikasi dengan `python manage.py test main` setelah dependensi terpasang.
Tidak ada deployment, perubahan database asli, staging, commit, atau push.
