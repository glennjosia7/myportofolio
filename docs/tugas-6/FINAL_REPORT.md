# Individual Assignment 6 — Final Report

**Tanggal finalisasi:** 5 November 2026
**Batas akhir:** Senin, 9 November 2026, 23:59 WIB
**Status:** READY WITH LIMITATIONS

## 1. Executive Summary

Individual Assignment 6 selesai secara fungsional. Bagian **Certifications** memiliki API DRF lengkap (list, detail, create, update, delete, star), empat peran diterapkan di server, halaman memakai AJAX untuk seluruh operasi, dan edit memakai PATCH ke API. Empat pertanyaan reflektif serta AI disclosure sudah ditulis di README.

Verifikasi terakhir:

```text
Django check          : PASS
Migration check       : PASS
API tests             : 34 test, OK
Seluruh test main     : 101 test, OK
Browser QA            : PASS (4 peran, modal, responsif)
Browsable API         : PASS
```

Repository siap untuk commit final manual. Tidak ada commit, push, deployment, atau submisi SCELE yang dilakukan agen.

## 2. Development Timeline

| Tahap | Tanggal | Commit | Isi |
|---|---|---|---|
| Tutorial 07 | 2 November 2026 | `e4e1ae8` | API Projects, permission, test dasar |
| Progress 1 | 4 November 2026 | `6870f53` | Modal edit Certifications via PATCH |
| Progress 2 | 5 November 2026 | `fc1959f` | Audit peran, CSRF, legacy, browser QA, fix navbar |
| Finalisasi | 5 November 2026 | belum di-commit | README, refleksi, AI disclosure, focus modal, laporan |

Tanggal implementasi dan tanggal commit sesuai riwayat Git. Finalisasi dijalankan lebih awal dari target 6 November; tidak ada tanggal yang dimundurkan atau dimanipulasi.

## 3. Repository Baseline

- Repository: `myportofolio`
- Branch: `main`
- Commit terakhir sebelum finalisasi: `fc1959f`
- Python: 3.14.8 (`.venv`)
- Django: 5.2.18
- DRF: 3.18.3
- Database development: SQLite, tidak di-track Git
- Test sebelum perubahan finalisasi: 34 API, 101 total, semuanya lulus

## 4. Complete Assignment Compliance Matrix

| Requirement | Sumber | Implementasi | Bukti | Status |
|---|---|---|---|---|
| ModelSerializer untuk model sendiri | PDF hal. 1-2 | `CertificationSerializer` | `main/serializers.py` | PASS |
| Field eksplisit, bukan `__all__` | PDF hal. 1 | 10 field ditulis eksplisit | `main/serializers.py:52-59` | PASS |
| Star count read-only | PDF hal. 1 | `SerializerMethodField` | `get_star_count` | PASS |
| Status star pengguna read-only | PDF hal. 1 | `get_is_starred` memakai `request.user` | test read-only | PASS |
| Tidak ada data akun sensitif | PDF hal. 1 | Hanya username pada `starred_by_names` | response API | PASS |
| Validasi teks + `strip_tags` | PDF hal. 1 | `validate_name`, `validate_issuing_organization`, `validate_credential_id` | test validasi | PASS |
| Permission empat peran | PDF hal. 1-2 | `IsPortfolioOwnerOrEditorOrReadOnly` | test + browser | PASS |
| Star memakai `IsAuthenticated` + `request.user` | PDF hal. 2 | `certification_star` | test star | PASS |
| API list GET/POST | PDF hal. 2 | `certification_list` | 200/201 | PASS |
| API detail GET/PUT/PATCH/DELETE | PDF hal. 2 | `certification_detail` | test + browser | PASS |
| API star POST | PDF hal. 2 | `certification_star` | 200 | PASS |
| `@api_view` + SessionAuthentication | PDF hal. 2 | seluruh view Certifications | `main/api_views.py` | PASS |
| Pencarian lewat query parameter | PDF hal. 2 | `?name=` nama/organisasi | test search | PASS |
| Status 201/400/403/404/204 | PDF hal. 2 | sesuai operasi | test API | PASS |
| Routing `<int:>` + nama unik | PDF hal. 2 | `api:certification-*` | `main/api_urls.py` | PASS |
| Halaman memakai API untuk list/search/create/star/delete | PDF hal. 2 | fetch + render kartu | browser + kode | PASS |
| Edit lewat PUT/PATCH | PDF hal. 2 | modal edit PATCH | browser PATCH 200 | PASS |
| Toast error 400/403 | PDF hal. 2 | `writeCertification` + `showToast` | browser validasi 400 | PASS |
| `X-CSRFToken` | PDF hal. 2 | header pada semua request tulis | test + browser | PASS |
| Escaping teks dan URL | PDF hal. 2 | `escapeHtml`, `safeHttpUrl` | kode + test | PASS |
| Test per peran + cek database | PDF hal. 2-3 | 34 API test | `main/tests_api.py` | PASS |
| Test CSRF sesi nyata | PDF hal. 3 | `enforce_csrf_checks=True` + `.login()` | test lulus | PASS |
| `test main` lulus | PDF hal. 3 | 101 test | output test | PASS |
| Halaman Tutorial 07 tetap berfungsi | PDF hal. 3 | Projects API + halaman | browser | PASS |
| Empat jawaban reflektif | PDF hal. 3-4 | `### Tugas 6` | README | PASS |
| AI disclosure transparan | Rubrik | tools, strategi, batasan | README | PASS |

## 5. Serializer Implementation

- `CertificationSerializer` mewarisi `ModelSerializer`.
- Field: `id`, `name`, `issuing_organization`, `issue_date`, `expiration_date`, `credential_id`, `credential_url`, `star_count`, `is_starred`, `starred_by_names`.
- `id` read-only; field bintang memakai `SerializerMethodField` sehingga tidak dapat dipalsukan client.
- `expiration_date` opsional dan menerima `null`.
- Teks dibersihkan dengan `strip_tags`; nama yang hanya berisi tag atau spasi ditolak.
- URL dan tanggal divalidasi oleh field DRF.
- Client yang mengirim `star_count`, `is_starred`, atau `starred_by_names` tidak dapat mengubah nilai tersimpan; test membuktikannya.

## 6. Authentication and Authorization

| Peran | Read | Create | PUT/PATCH | Delete | Star |
|---|---|---|---|---|---|
| Anonymous | ya | 403 | 403 | 403 | 403 |
| Pengguna biasa | ya | 403 | 403 | 403 | ya |
| Editor | ya | 403 | ya | 403 | ya |
| Superuser | ya | 201 | ya | 204 | ya |

- Editor memakai Django permission `main.change_certification`, bukan nama grup saja.
- Permission diperiksa di server melalui permission class.
- Template hanya menyembunyikan kontrol; request langsung tetap ditolak.
- Route legacy memakai `has_perm` yang sama dan diuji tidak dapat dipakai untuk bypass.

## 7. REST API and Routing

```text
GET/POST        /api/v1/certifications/
GET/PUT/PATCH/DELETE /api/v1/certifications/<int:id>/
POST            /api/v1/certifications/<int:id>/star/
```

- Function-based view dengan `@api_view`.
- `SessionAuthentication`.
- `get_object_or_404` untuk ID tidak ditemukan.
- Method tidak didukung menghasilkan `405`; route non-integer menghasilkan `404`.
- Browsable API diuji lewat server lokal: `Accept: text/html` merender DRF, `Accept: application/json` mengembalikan `application/json`.

## 8. Frontend AJAX Integration

- List dan pencarian memakai `fetch` + debounce 300 ms + `AbortController`.
- Create, edit, delete, dan star memakai endpoint DRF.
- Tidak ada reload halaman untuk operasi tersebut.
- `X-CSRFToken` dikirim dari cookie `csrftoken`.
- `escapeHtml` dipakai untuk seluruh nilai teks; `safeHttpUrl` membatasi tautan ke `http`/`https`.
- Toast menampilkan sukses, validasi 400, penolakan 403, dan kegagalan jaringan.
- Tombol submit dinonaktifkan saat request berjalan untuk mencegah duplikasi.

## 9. Certification Edit Flow

```text
Edit → GET /api/v1/certifications/<id>/
     → isi modal
     → ubah field
     → PATCH /api/v1/certifications/<id>/
     → validasi serializer + permission + CSRF
     → 200
     → refresh kartu + toast
```

Verifikasi browser:

- Prefill nama, organisasi, dan URL benar.
- Tidak ada data basi saat berpindah certification.
- PATCH Editor dan superuser `200`.
- Escape, tombol Batal, dan ikon close menutup modal.
- Error 400 mempertahankan isi form dan modal tetap terbuka.
- Fokus berpindah ke field pertama saat modal terbuka, Tab/Shift+Tab berputar di dalam dialog, dan fokus kembali ke tombol Edit setelah modal ditutup.

## 10. Testing Results

```text
python manage.py check
-> System check identified no issues (0 silenced).

python manage.py migrate --check
-> PASS (exit 0)

python manage.py test main.tests_api
-> Ran 34 tests, OK

python manage.py test main
-> Ran 101 tests, OK
```

Cakupan API mencakup empat peran, penolakan tulis dengan pengecekan database, validasi input, field read-only, star, CSRF negatif/positif, method `405`, ID `404`, dan route legacy. Tidak ada test yang dihapus atau dilemahkan pada finalisasi.

## 11. Browser Verification

Playwright + Chromium headless, server lokal, data sementara:

```text
Anonymous : 2 kartu, 0 kontrol tulis, 2 tautan login-to-star
User      : 0 edit/delete, star 0→1→0
Editor    : add 0, edit 2, delete 0, PATCH 200, fokus masuk modal
Superuser : create 201, edit 200, delete 204, search 1 hasil
Responsif : overflow 0 pada 390/768/1440; submit terlihat
Console   : tidak ada error JavaScript
```

Halaman `/`, `/experience/`, `/achievements/`, `/projects/`, `/certifications/`, `/login/`, `/register/` semuanya `200`. Data uji dihapus setelah verifikasi; database development kembali ke 1 akun asli dan 0 certification.

## 12. UI/UX and Accessibility

Kontras terukur pada Progress 2 (WCAG AA minimum 4.5:1 untuk teks normal):

```text
Heading 17.27:1 | Label 17.27:1 | Input 15.19:1 | Placeholder 8.20:1
Primary 8.30:1  | Secondary 17.27:1 | Close 9.32:1 | Focus 15.19:1
```

Finalisasi menambahkan pengelolaan fokus modal:

- fokus awal ke field pertama (bukan tombol close/backdrop),
- Tab dan Shift+Tab berputar di dalam dialog,
- fokus kembali ke tombol pemicu setelah modal ditutup,
- backdrop tidak ikut dalam urutan fokus.

Navbar tidak overflow pada 390/768/1440 px setelah perbaikan Progress 2.

## 13. Security Review

**Temuan yang sudah dikendalikan:**

- CSRF aktif; tidak ada `csrf_exempt`; request tulis tanpa token ditolak.
- Permission server-side untuk seluruh operasi tulis.
- Escaping teks dan validasi URL mencegah XSS dari data tersimpan.
- Field bintang read-only; identitas star dari `request.user`.
- `.env`, `db.sqlite3`, `.venv`, dan `__pycache__` tidak di-track Git.
- `ALLOWED_HOSTS` tidak memakai wildcard.

**Risiko yang tersisa:**

1. `SECRET_KEY` memiliki nilai fallback hardcoded di `portofolio/settings.py`. Nilai tidak dicetak di laporan. Jika environment produksi tidak menyetel `SECRET_KEY`, fallback yang dapat diketahui publik membuat sesi/CSRF tidak aman. Rekomendasi: set `SECRET_KEY` acak di environment PWS dan rotasi jika pernah dipakai produksi.
2. `DEBUG` default `True` saat `PRODUCTION` tidak diset. Pastikan environment PWS menyetel `PRODUCTION=true`/`DEBUG=false`.
3. `SESSION_COOKIE_SECURE` dan `CSRF_COOKIE_SECURE` belum diset. Perilaku HTTPS di balik proxy PWS belum diverifikasi; jangan aktifkan tanpa memastikan proxy meneruskan skema dengan benar.
4. Test lokal dan browser tidak membuktikan keamanan seluruh konfigurasi produksi.

Tidak ada temuan kritis yang menghalangi pemenuhan tugas secara lokal.

## 14. README and Reflective Answers

README sekarang memuat:

- Technology stack termasuk Django REST Framework.
- Setup lintas platform (macOS/Linux + catatan Windows).
- Riwayat migrasi sampai `0009_certification_starred_by`.
- `# Tugas 6 Implementation` dengan tabel endpoint dan ringkasan serializer/permission/frontend.
- `# Tugas 6 Reflection` dengan heading `### Tugas 6` dan empat jawaban.
- Perintah test yang benar (`test main`, bukan seluruh test yang mungkin menjalankan e2e).
- Hasil test terbaru (34 API, 101 total).
- AI disclosure Tugas 6.

Empat jawaban membahas REST/JSON/PUT/PATCH, serializer, autentikasi vs otorisasi, dan CSRF. Contoh memakai endpoint serta perilaku serializer proyek ini, termasuk catatan bahwa `expiration_date` opsional tidak otomatis terhapus oleh PUT.

## 15. AI Disclosure

Disclosure membedakan:

- **ChatGPT Website:** pemahaman ketentuan, perencanaan checkpoint, penyusunan prompt, dan review.
- **OpenCode + DeepSeek V4.1 Flash:** audit repository, implementasi modal, test, browser QA, dan dokumentasi.
- **Developer:** keputusan lingkup, persetujuan perubahan, verifikasi, dan seluruh operasi Git.

Disclosure juga memuat strategi prompting, enam contoh prompt, batasan AI, dan pernyataan bahwa tautan percakapan ChatGPT Tugas 6 belum tersedia sehingga tidak dicantumkan. Tidak ada tautan atau ID percakapan yang dikarang.

## 16. Git and Repository Hygiene

File finalisasi:

```text
M  README.md
M  templates/certifications.html
?? docs/tugas-6/FINAL_REPORT.md
```

- `git diff --check`: bersih.
- Tidak ada file `.env`, database, cache, screenshot, atau kredensial di diff.
- Tidak ada migrasi baru.
- Tidak ada perubahan dependency.
- Progress 1 dan Progress 2 tetap sebagai commit terpisah; laporan lama tidak ditimpa.

## 17. Remaining Risks or Limitations

- Tautan percakapan ChatGPT Website Tugas 6 belum tersedia; user dapat menambahkannya sebelum submisi.
- Deployment PWS dan konfigurasi produksi tidak diverifikasi.
- Fallback `SECRET_KEY` masih ada; aman untuk lokal, berisiko jika dipakai produksi.
- Test dan browser QA hanya membuktikan skenario yang diuji, bukan jaminan bebas celah.
- Focus trap diuji di Chromium; perilaku browser lain tidak diuji.

## 18. Final Readiness

**READY WITH LIMITATIONS.**

Seluruh kebutuhan fungsional, dokumentasi, dan test Assignment 6 terpenuhi. Limitasi yang tersisa adalah tautan ChatGPT Tugas 6, verifikasi produksi, dan pengelolaan `SECRET_KEY`—tidak menghalangi penilaian lokal, tetapi perlu diperhatikan sebelum deployment.

## 19. Manual Commit Recommendation

```bash
git diff --check
git status --short

git add README.md \
        templates/certifications.html \
        docs/tugas-6/FINAL_REPORT.md

git diff --cached --check
git diff --cached --stat
git commit -m "fix(certifications): trap modal focus and finalize assignment 6 documentation"
git push origin main
```

Jalankan manual. Agen tidak mengeksekusi perintah Git.

## 20. SCELE Submission Checklist

- [ ] Commit final dibuat dan di-push ke GitHub.
- [ ] Repository GitHub publik dan dapat diakses asisten dosen.
- [ ] Tautan yang dikumpulkan adalah tautan **commit**, bukan hanya URL repository.
- [ ] Tautan percakapan ChatGPT Tugas 6 ditambahkan jika tersedia.
- [ ] Jalankan `python manage.py test main` sekali lagi dari commit final.
- [ ] Pastikan tidak ada file `.env` atau kredensial yang ikut ter-push.
- [ ] Submit melalui SCELE sebelum Senin, 9 November 2026, 23:59 WIB.
