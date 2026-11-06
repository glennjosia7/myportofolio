# myportofolio

# Project Description

Website portofolio pribadi berbasis Django milik Glenn Josia Devano. Project ini menampilkan Profile, Experience, Achievements, Projects, dan Certifications, serta menyediakan operasi Create, Update, Delete, dan JSON Data Delivery untuk bagian data pilihan (Certifications dan Projects).

Situs juga dilengkapi autentikasi (register, login, logout), session dan cookie `last_login`, otorisasi berbasis peran (pengunjung, pengguna biasa, Editor, dan pemilik), serta fitur star pada Projects dan Certifications.

Project ini merupakan hasil pengerjaan Tutorial 0 sampai Tutorial 7 serta Tugas 1 sampai Tugas 6 pada mata kuliah Pemrograman Berbasis Platform (CSGE602022), Program Studi S1 Sistem Informasi, Universitas Indonesia.

| Identitas | |
| --- | --- |
| Nama | Glenn Josia Devano |
| NPM | 2506614712 |
| Kelas | PBP F |
| Repository | https://github.com/glennjosia7/myportofolio |

# Features

- Bagian profil berisi perkenalan, identitas, foto, dan tautan media sosial.
- Timeline Experience yang mengambil data dari database, dengan status Ongoing atau Completed.
- Halaman Achievements berisi lima hasil kompetisi CTF dari database beserta buktinya.
- Halaman utama memuat preview Experience dan Achievement dengan tautan menuju halaman lengkap.
- Halaman Projects dengan Create, Update, Delete, pencarian berdasarkan judul, dan endpoint JSON.
- Halaman Certifications memuat data lewat AJAX (`fetch()`) dari endpoint JSON dengan kondisi loading, kosong, dan error, pencarian debounced tanpa reload, modal tambah data, serta notifikasi toast.
- Halaman Certifications tetap menyediakan Create, Update, Delete, dan endpoint JSON.
- Registrasi, login, dan logout memakai sistem autentikasi bawaan Django, serta status login pada navbar.
- Session dan cookie `last_login` yang di-set saat login dan dihapus saat logout.
- Otorisasi berbasis peran: pengunjung (baca), pengguna biasa (baca + star), Editor (update), dan pemilik/superuser (create, update, delete).
- Fitur star pada Projects dan Certifications (maksimal satu star per pengguna) dengan jumlah star dan status pengguna.
- API utama Projects dan Certifications kini memakai Django REST Framework melalui `/api/v1/`. Endpoint JSON manual berbasis `JsonResponse` dari tugas sebelumnya tetap dipertahankan untuk kompatibilitas; jumlah dan status star ditampilkan tanpa mengekspos data akun sensitif.
- Navbar transparan dengan blur, tetap di atas saat di-scroll, dan penanda halaman aktif.
- Navbar dan footer bersama melalui template inheritance Django (`base.html`).
- Form berbasis ModelForm dengan validasi Django dan proteksi CSRF pada setiap request POST.
- Unit test otomatis untuk model, view, form, routing, serialization, dan tampilan halaman.
- Tampilan responsif untuk desktop, tablet, dan perangkat seluler.
- Perlindungan XSS dua lapis pada Certifications: `strip_tags` di `clean_<field>` sisi server dan `escapeHtml` untuk setiap nilai yang disisipkan ke HTML lewat JavaScript.

# Technology Stack

- Django 5.2.18 untuk model, database, routing, form, serialization, unit test, dan rendering template.
- Django REST Framework 3.18.3 untuk serializer, API view berbasis fungsi, permission class, dan Browsable API.
- Python 3.11+ (proyek diuji pada Python 3.14.8) sebagai bahasa utama.
- HTML5 untuk struktur dan semantik halaman.
- CSS3 untuk layout, timeline, navbar sticky, modal popover, dan tampilan responsif.
- JavaScript (fetch, AbortController, popover API) untuk interaksi AJAX tanpa framework frontend.
- SQLite untuk database pengembangan lokal.
- PostgreSQL (melalui `psycopg2-binary`) untuk database pada lingkungan PWS.
- WhiteNoise untuk penyajian static files pada deployment.
- python-dotenv untuk membaca konfigurasi dari berkas `.env`.

Versi dependency minimum ada pada `requirements.txt`.

# Setup Instruction

```bash
git clone https://github.com/glennjosia7/myportofolio.git
cd myportofolio
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata experiences achievements
python manage.py test main
python manage.py runserver
```

Pada Windows, gunakan `py -m venv .venv` lalu `.venv\Scripts\activate` sebagai pengganti dua perintah venv di atas. Nama folder virtual environment bebas; `.venv` dan `env` sama-sama diabaikan Git.

Buka `http://127.0.0.1:8000/` pada browser setelah server berjalan.

Perintah `loaddata experiences achievements` mengisi tiga pengalaman dan lima prestasi dari fixture JSON. Jalankan saat pertama menyiapkan database. Menjalankannya ulang akan mengembalikan objek dengan ID yang sama ke isi fixture, termasuk menimpa perubahan pada objek tersebut.

Untuk mengelola data tanpa mengedit HTML, jalankan `python manage.py createsuperuser`, lalu masuk ke `/admin/`. Model Achievement, Experience, Project, dan Certification sudah terdaftar. Pada deskripsi Experience, satu baris teks akan ditampilkan sebagai satu poin. Field `logo` menyimpan path static untuk logo COMPFEST, RISTEK, dan Open House Fasilkom UI 2025. Data Project dapat ditambah melalui `/projects/add/` dan diubah melalui `/projects/<id>/update/`, sedangkan Certification dapat ditambah atau diubah melalui `/certifications/`. Jangan bagikan kredensial admin atau berkas `.env`.

# Database Migration

Database proyek dikelola melalui sistem migrasi Django.

- `python manage.py makemigrations` membandingkan definisi model dengan riwayat migrasi dan membuat berkas instruksi perubahan skema (misalnya `main/migrations/0006_project.py` dan `0007_certification.py`). Pada tahap ini tabel belum dibuat.
- `python manage.py migrate` menjalankan migrasi yang belum diterapkan sehingga tabel dan kolom benar-benar tersedia di database.
- Riwayat migrasi proyek: `0001_initial` sampai `0009_certification_starred_by`. Berkas migrasi ikut masuk Git agar struktur database dapat dibuat ulang pada lingkungan lain.
- `python manage.py makemigrations --check --dry-run` memastikan tidak ada perubahan model yang belum memiliki migrasi.
- `python manage.py loaddata experiences achievements` memuat data awal dari `main/fixtures/` (fixture JSON).

Untuk database di PWS, migrasi dan pengisian data perlu dijalankan di lingkungan PWS juga; isi SQLite lokal tidak ikut terkirim melalui Git. Pengembangan ini belum di-deploy ulang.

# Alur Sederhana Aplikasi

1. `portofolio/urls.py` menerima pola URL dan meneruskannya ke `main/urls.py` melalui `include`.
2. `/` memanggil `show_main`, `/experience/` memanggil `show_experience`, `/achievements/` memanggil `show_achievements`, `/projects/` memanggil `show_projects`, dan `/certifications/` memanggil `show_certifications`.
3. View Experience dan Achievements mengambil QuerySet untuk template. Halaman Projects dan Certifications menyiapkan kerangka HTML; JavaScript mengambil daftar dari endpoint DRF `/api/v1/` melalui `fetch()`.
4. Template halaman mewarisi `templates/base.html`. Experience dan Achievements menggunakan rendering template, sedangkan kartu Projects dan Certifications dirakit dari JSON DRF dengan escaping. Form HTML tetap ada untuk rendering input, dan aksi AJAX mengirim method HTTP yang sesuai (POST/PATCH/DELETE) dengan token CSRF.
5. Browser menerima HTML dan memuat stylesheet serta foto dari static files.

Bagian yang perlu dikenali untuk melanjutkan proyek:

| Perubahan yang ingin dilakukan | Lokasi |
| --- | --- |
| Menambah atau mengubah isi prestasi/pengalaman | Django Admin, bukan template |
| Menambah field prestasi | `main/models.py`, kemudian `makemigrations` dan `migrate` |
| Mengubah urutan daftar | `order_by()` di `main/views.py` |
| Mengubah susunan hasil, judul, penyelenggara, tahun, dan bukti | model/data Achievement dan `templates/achievements.html` |
| Menambah atau mengubah field Certification | `main/models.py`, `main/forms.py`, dan `templates/certifications.html` |
| Menambah atau mengubah field Project | `main/models.py`, `main/forms.py`, dan `templates/project.html` |
| Menambah tautan navbar atau mengubah footer | `templates/base.html` |
| Mengubah warna, jarak, dan layout mobile | `static/css/style.css` |

Warna bersama ada pada `:root`. Palet navy dan teal digunakan konsisten pada seluruh halaman. Navbar diatur oleh `.site-header`: `position: sticky`, `top: 0`, dan `z-index` membuatnya tetap terlihat; latar `rgba` dan `backdrop-filter` memberi efek transparan. Titik timeline dibuat oleh `.experience-item::before`, sedangkan garis hanya dibuat oleh `:not(:last-child)::after`. Grid Achievement berubah dari tiga kolom di desktop menjadi dua kolom di tablet dan satu kolom di mobile.

# Tugas 6 Implementation

Tugas 6 menerapkan Django REST Framework pada bagian **Certifications**, mengikuti pola yang sudah dibuat untuk Projects pada Tutorial 07. Implementasi berada di `main/serializers.py`, `main/permissions.py`, `main/api_views.py`, dan `main/api_urls.py`.

## Endpoint API

| Method | URL | Hak akses | Status sukses |
| --- | --- | --- | --- |
| GET | `/api/v1/certifications/` | semua peran | 200 |
| POST | `/api/v1/certifications/` | superuser | 201 |
| GET | `/api/v1/certifications/<int:id>/` | semua peran | 200 |
| PUT | `/api/v1/certifications/<int:id>/` | Editor, superuser | 200 |
| PATCH | `/api/v1/certifications/<int:id>/` | Editor, superuser | 200 |
| DELETE | `/api/v1/certifications/<int:id>/` | superuser | 204 |
| POST | `/api/v1/certifications/<int:id>/star/` | pengguna login | 200 |

Pencarian memakai query parameter `name` dan mencocokkan nama atau organisasi penerbit. Endpoint lama `get_certifications_json` dan halaman edit legacy tetap tersedia untuk kompatibilitas, tetapi halaman Certifications sekarang memakai API DRF.

## Serializer, permission, dan frontend

- `CertificationSerializer` adalah `ModelSerializer` dengan daftar field eksplisit. `star_count`, `is_starred`, dan `starred_by_names` adalah `SerializerMethodField` yang read-only; data akun seperti email dan password hash tidak ikut dikirim.
- `validate_name`, `validate_issuing_organization`, dan `validate_credential_id` memakai `strip_tags`, sehingga tag HTML dibersihkan dan input yang hanya berisi tag ditolak.
- `IsPortfolioOwnerOrEditorOrReadOnly` membaca `request.user.is_superuser` dan Django permission `main.change_certification`. Endpoint star memakai `IsAuthenticated` dan selalu memakai `request.user`, bukan ID dari client.
- Halaman Certifications memakai `fetch()` untuk list, pencarian debounced 300 ms, create, edit melalui PATCH, delete, dan star. Setiap request tulis mengirim `X-CSRFToken`; nilai teks di-escape dengan `escapeHtml`, dan URL kredensial diperiksa `safeHttpUrl` sebelum dirender.
- Modal edit memuat detail dari API, mengisi field yang ada, lalu mengirim PATCH. Error validasi `400`, penolakan `403`, dan kegagalan jaringan ditampilkan lewat toast tanpa menutup form.

# Testing

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
python manage.py test main.tests_api
python manage.py test main
```

Test API berada di `main/tests_api.py` dan memakai `APITestCase`. Cakupannya:

- create, update, dan delete Project maupun Certification;
- penolakan form tidak valid;
- delete hanya berjalan pada request POST;
- endpoint JSON mengembalikan `Content-Type: application/json` dan field yang benar;
- halaman Certifications merender kerangka AJAX dan mengambil data dari endpoint JSON;
- endpoint JSON Certifications mengirim `star_count`, `is_starred`, dan `starred_by_names`, serta filter nama/organisasi;
- view AJAX `create_certification_ajax`: `201` berhasil, `400` pada input tidak valid, `403` tanpa permission, dan `strip_tags` membersihkan tag HTML;
- autentikasi: register, login (cookie `last_login`), logout, dan tampilan navbar;
- otorisasi Certification: pengunjung dialihkan ke login, pengguna biasa `403`, Editor boleh update tetapi `403` untuk create/delete, pemilik boleh semuanya;
- penyembunyian tombol aksi dan flag permission pada template;
- star pada Project dan Certification (tambah, batalkan, maksimal satu per pengguna) serta username pada JSON;
- empat peran pada API Certifications, termasuk penolakan `403` dan pengecekan isi database setelah request ditolak;
- validasi serializer: nama kosong, tag HTML, URL tidak valid, dan tanggal tidak valid;
- CSRF dengan sesi nyata: request tanpa token ditolak `403`, request dengan token berhasil;
- method yang tidak didukung (`405`), ID yang tidak ada (`404`), serta field star yang read-only.

Pemeriksaan final pada 5 November 2026: `check` bersih, tidak ada migrasi tertunda, 34 API test lulus, dan 101 total test `main` lulus. Alur empat peran, modal edit, pencarian, dan tampilan responsif juga diperiksa dengan browser. Test berjalan di database test terpisah sehingga tidak menghapus data portofolio lokal.

# Tugas 6 Reflection

### Tugas 6

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan.** REST (Representational State Transfer) adalah gaya arsitektur API yang memakai resource sebagai objek utama, URL sebagai penanda resource, method HTTP sebagai aksi, dan pertukaran representasi data yang tidak menyimpan state sesi di server. Pada proyek ini, `/api/v1/certifications/` adalah koleksi resource dan `/api/v1/certifications/5/` adalah satu certification. `GET` membaca, `POST` membuat, `PUT`/`PATCH` mengubah, dan `DELETE` menghapus. Mengembalikan JSON saja tidak otomatis membuat API RESTful: endpoint yang memakai satu URL untuk semua aksi, menyimpan state percakapan di server, atau tidak konsisten memakai method dan status HTTP tetap bukan REST. Yang dinilai adalah keseluruhan kontrak resource, method, status, dan representasi, bukan format payload semata.

   `PUT` berarti mengganti representasi resource secara keseluruhan, sedangkan `PATCH` mengubah sebagian field. Pada `CertificationSerializer`, field `name`, `issuing_organization`, `issue_date`, `credential_id`, dan `credential_url` wajib diisi, sehingga `PUT /api/v1/certifications/5/` tanpa salah satunya menghasilkan `400`. Field `expiration_date` opsional; bila dihilangkan dari PUT, nilai lama tidak otomatis terhapus karena serializer hanya memperbarui atribut yang dikirim. Untuk mengosongkannya, kirim `null`. `PATCH` cocok untuk modal edit yang hanya mengirim field yang berubah, misalnya `{"name": "Cloud Practitioner"}`; `PUT` cocok ketika client memang mengirim seluruh data certification, misalnya dari form yang memuat semua field.

2. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05?** Serializer adalah lapisan yang mengubah objek model menjadi representasi data (serialization) dan sebaliknya mengubah data input menjadi objek Python yang tervalidasi (deserialization). `CertificationSerializer` menentukan field yang boleh keluar, menambahkan field hasil perhitungan seperti `star_count` dan `is_starred`, serta menjalankan validasi field dan objek sebelum data disimpan. Saat `POST` atau `PATCH`, `serializer.is_valid()` memeriksa tipe data, field wajib, format tanggal dan URL, lalu memanggil `validate_<field>` untuk membersihkan teks dengan `strip_tags`. Jika valid, `serializer.save()` membuat atau memperbarui instance.

   Dengan `JsonResponse` manual, saya harus mengambil setiap atribut model, menghitung star sendiri, menentukan field mana yang boleh keluar, dan menulis validasi secara terpisah. Cara itu mudah menghasilkan inkonsistensi ketika model berubah dan rawan membocorkan field yang tidak disengaja. Serializer memusatkan kontrak representasi dan validasi di satu tempat, sehingga API view cukup menangani request, permission, dan status HTTP. Serializer juga bukan renderer: setelah data tervalidasi, renderer DRF yang mengubahnya menjadi JSON (atau HTML pada Browsable API).

3. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?** Autentikasi menjawab siapa pengguna yang mengirim request; otorisasi menjawab tindakan apa yang boleh dilakukan pengguna tersebut. Di proyek ini, `SessionAuthentication` membaca sesi Django dan mengisi `request.user`. Permission class kemudian memakai identitas itu: `IsPortfolioOwnerOrEditorOrReadOnly` mengizinkan semua orang membaca, pengguna login memberi star lewat `IsAuthenticated`, Editor boleh `PUT`/`PATCH` jika memiliki permission `main.change_certification`, dan hanya superuser yang boleh membuat atau menghapus. Jadi autentikasi saja tidak cukup: pengguna biasa sudah terautentikasi, tetapi tetap tidak boleh mengubah certification.

   Menyembunyikan tombol Edit atau Delete di template hanya mengatur tampilan. Penyerang dapat mengirim `PATCH` atau `DELETE` langsung dengan `curl`, `fetch`, atau alat HTTP lain tanpa melewati UI. Karena itu keputusan akhir harus ada di server, pada permission class dan pengecekan Django permission. Template hanya membantu pengalaman pengguna; server tetap menolak request yang tidak berhak dengan `403`. Pengujian pada proyek ini membuktikan keduanya: tombol tidak muncul untuk pengguna biasa, dan request langsung ke endpoint tetap ditolak tanpa mengubah database.

4. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai `force_authenticate` tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?** Dengan `SessionAuthentication`, browser mengirim cookie sesi secara otomatis pada setiap request ke domain yang sama. Situs lain dapat memancing browser korban mengirim `POST`, `PUT`, `PATCH`, atau `DELETE` ke aplikasi; browser tetap menyertakan cookie sesi, sehingga server dapat mengira request itu berasal dari pengguna yang sah. Token CSRF mencegahnya karena token tidak dapat dibaca situs lain dan harus dikirim eksplisit, di proyek ini lewat header `X-CSRFToken` yang nilainya diambil dari cookie `csrftoken`. Server membandingkan token header dengan token sesi; request tanpa token atau dengan token salah ditolak `403`.

   `force_authenticate()` hanya menempelkan objek user ke request di test client. Ia melewati proses login sesi, cookie, dan pemeriksaan CSRF, sehingga test tetap lolos meskipun perlindungan CSRF sebenarnya rusak. Karena itu test CSRF memakai `APIClient(enforce_csrf_checks=True)` dan `.login()` dengan kredensial nyata. Test negatif membuktikan `PATCH` tanpa token ditolak `403` dan database tidak berubah; test positif membuktikan `PATCH` dengan sesi dan token valid berhasil `200`. Keduanya bersama-sama menunjukkan bahwa SessionAuthentication dan CSRF benar-benar aktif, bukan hanya diasumsikan dari kode.

# AI Disclosure

### Penggunaan AI pada Tugas 6

Pada Tugas 6, **ChatGPT Website** digunakan sebagai pendamping belajar untuk membahas perbedaan REST dan JSON, peran `ModelSerializer`, semantik PUT/PATCH, permission empat peran, `SessionAuthentication` dan CSRF, serta pengujian API. Diskusi diarahkan pada pemahaman alasan teknis, contoh konseptual, dan cara memeriksa hasil, bukan meminta jawaban reflektif atau potongan kode lengkap untuk langsung disalin. ChatGPT juga membantu menyusun pembagian pekerjaan ke tiga checkpoint dan meninjau laporan progres.

Pengerjaan berlangsung bertahap: Progress 1 untuk edit Certifications melalui API, Progress 2 untuk pemeriksaan permission, CSRF, dan responsivitas, lalu finalisasi untuk dokumentasi dan aksesibilitas modal. Pengguna menentukan ruang lingkup dan melakukan operasi Git (`add`, `commit`, `push`) secara manual. Kelulusan test atau laporan agen tidak dengan sendirinya membuktikan seluruh kondisi aplikasi; verifikasi hanya mencakup skenario yang benar-benar diuji.

Strategi penggunaan AI adalah memahami konsep dan ketentuan terlebih dahulu, membandingkannya dengan struktur aplikasi, lalu menilai hasil melalui pengujian Django dan perilaku browser. 

Keterbatasan yang tetap diperhatikan: penjelasan AI dapat keliru, test otomatis tidak meliputi semua kombinasi kasus, browser QA tidak setara dengan audit aksesibilitas menyeluruh, dan pengujian lokal belum membuktikan konfigurasi PWS/HTTPS produksi.

### Riwayat Chat

- Percakapan Tugas 1 (AI ChatGPT Web): https://chatgpt.com/share/6a9ae1a1-4fe8-83ec-8d60-b252bab78aec
- Percakapan Tugas 2 (AI ChatGPT Web): https://chatgpt.com/share/6aa3d20a-9c40-83ec-b83c-6f973f820a62
- Percakapan Tugas 3 (AI ChatGPT Web): https://chatgpt.com/share/6aaf89fc-ef68-83ec-b16a-6a1e73766bed
- Percakapan Tugas 4 (AI ChatGPT Web): https://chatgpt.com/share/6ab9d9ae-0eac-83ec-8fcf-61b219ed6618
- Percakapan Tugas 5 (AI ChatGPT Web): https://chatgpt.com/share/6ac28198-0f0c-83ec-abeb-4ea8b4cc989b
- Percakapan Tugas 6 (AI ChatGPT Web): https://chatgpt.com/share/6aeda796-a468-83ec-a834-3cdf379434aa
