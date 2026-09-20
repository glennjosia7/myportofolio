# myportofolio

# Project Description

Website portofolio pribadi berbasis Django milik Glenn Josia Devano. Project ini menampilkan Profile, Experience, Achievements, Projects, dan Certifications, serta menyediakan operasi Create, Update, Delete, dan JSON Data Delivery untuk bagian data pilihan (Certifications dan Projects).

Project ini merupakan hasil pengerjaan Tutorial 0 sampai Tutorial 3 serta Tugas 1, Tugas 2, dan Tugas 3 pada mata kuliah Pemrograman Berbasis Platform (CSGE602022), Program Studi S1 Sistem Informasi, Universitas Indonesia.

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
- Halaman Certifications dengan Create, Update, Delete, dan endpoint JSON.
- JSON Data Delivery melalui `django.core.serializers`, lalu deserialisasi sebelum dirender ke template.
- Navbar transparan dengan blur, tetap di atas saat di-scroll, dan penanda halaman aktif.
- Navbar dan footer bersama melalui template inheritance Django (`base.html`).
- Form berbasis ModelForm dengan validasi Django dan proteksi CSRF pada setiap request POST.
- Unit test otomatis untuk model, view, form, routing, serialization, dan tampilan halaman.
- Tampilan responsif untuk desktop, tablet, dan perangkat seluler tanpa JavaScript.

# Technology Stack

- Django 5.2 untuk model, database, routing, form, serialization, unit test, dan rendering template.
- Python 3.11 sebagai bahasa utama.
- HTML5 untuk struktur dan semantik halaman.
- CSS3 untuk layout, timeline, navbar sticky, modal popover, dan tampilan responsif.
- SQLite untuk database pengembangan lokal.
- PostgreSQL (melalui `psycopg2-binary`) untuk database pada lingkungan PWS.
- WhiteNoise untuk penyajian static files pada deployment.
- python-dotenv untuk membaca konfigurasi dari berkas `.env`.

Versi dependency minimum ada pada `requirements.txt`.

# Setup Instruction

```powershell
git clone https://github.com/glennjosia7/myportofolio.git
cd myportofolio
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata experiences achievements
python manage.py test
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` pada browser setelah server berjalan.

Perintah `loaddata experiences achievements` mengisi tiga pengalaman dan lima prestasi dari fixture JSON. Jalankan saat pertama menyiapkan database. Menjalankannya ulang akan mengembalikan objek dengan ID yang sama ke isi fixture, termasuk menimpa perubahan pada objek tersebut.

Untuk mengelola data tanpa mengedit HTML, jalankan `python manage.py createsuperuser`, lalu masuk ke `/admin/`. Model Achievement, Experience, Project, dan Certification sudah terdaftar. Pada deskripsi Experience, satu baris teks akan ditampilkan sebagai satu poin. Field `logo` menyimpan path static untuk logo COMPFEST, RISTEK, dan Open House Fasilkom UI 2025. Data Project dapat ditambah melalui `/projects/add/` dan diubah melalui `/projects/<id>/update/`, sedangkan Certification dapat ditambah atau diubah melalui `/certifications/`. Jangan bagikan kredensial admin atau berkas `.env`.

# Database Migration

Database proyek dikelola melalui sistem migrasi Django.

- `python manage.py makemigrations` membandingkan definisi model dengan riwayat migrasi dan membuat berkas instruksi perubahan skema (misalnya `main/migrations/0006_project.py` dan `0007_certification.py`). Pada tahap ini tabel belum dibuat.
- `python manage.py migrate` menjalankan migrasi yang belum diterapkan sehingga tabel dan kolom benar-benar tersedia di database.
- Riwayat migrasi proyek: `0001_initial` sampai `0007_certification`. Berkas migrasi ikut masuk Git agar struktur database dapat dibuat ulang pada lingkungan lain.
- `python manage.py makemigrations --check --dry-run` memastikan tidak ada perubahan model yang belum memiliki migrasi.
- `python manage.py loaddata experiences achievements` memuat data awal dari `main/fixtures/` (fixture JSON).

Untuk database di PWS, migrasi dan pengisian data perlu dijalankan di lingkungan PWS juga; isi SQLite lokal tidak ikut terkirim melalui Git. Pengembangan ini belum di-deploy ulang.

# Alur Sederhana Aplikasi

1. `portofolio/urls.py` menerima pola URL dan meneruskannya ke `main/urls.py` melalui `include`.
2. `/` memanggil `show_main`, `/experience/` memanggil `show_experience`, `/achievements/` memanggil `show_achievements`, `/projects/` memanggil `show_projects`, dan `/certifications/` memanggil `show_certifications`.
3. View menyiapkan context. View Experience dan Achievements mengambil QuerySet, sedangkan View Projects dan Certifications mengambil response JSON lalu melakukan deserialize.
4. Template halaman mengisi blok pada `templates/base.html`. Daftar data ditampilkan melalui `{% for %}`, dengan `{% empty %}` untuk database kosong. Form Project memakai `ProjectForm`, sedangkan form Certification memakai `CertificationForm`. Perubahan dan penghapusan data menggunakan request `POST` dengan CSRF token.
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

# Tugas 3 Implementation

Tugas 3 berfokus pada Form dan Data Delivery. Fitur utama yang dikembangkan adalah halaman Certifications lengkap (Create, Update, Delete, JSON), dan halaman Projects dilengkapi Update agar kedua bagian data pilihan memiliki alur CRUD yang konsisten.

## Form implementation

- `ProjectForm` dan `CertificationForm` merupakan `ModelForm` yang menghubungkan field form langsung ke field model.
- `CertificationForm` memiliki enam field dengan tipe data bervariasi yang semuanya dapat diinput user:
  - `name` (`CharField` / `TextInput`)
  - `issuing_organization` (`CharField` / `TextInput`)
  - `issue_date` (`DateField` / `DateInput` tipe `date`)
  - `expiration_date` (`DateField`, opsional / `DateInput` tipe `date`)
  - `credential_id` (`CharField` / `TextInput`)
  - `credential_url` (`URLField` / `URLInput`)
- `ProjectForm` memiliki lima field: `title`, `description`, `tech_stack`, `project_url`, dan `project_image_url`.
- Setiap form dirender dengan `{% csrf_token %}` dan menampilkan `field.errors` agar validasi Django terlihat. Label dan placeholder disesuaikan melalui `labels` dan `widgets`.

## CRUD flow

| Operasi | URL | View | Template |
| --- | --- | --- | --- |
| Create Certification | `certifications/add/` | `create_certification` | `certification_form.html` |
| Update Certification | `certifications/<id>/update/` | `update_certification` | `certification_form.html` |
| Delete Certification | `certifications/<id>/delete/` | `delete_certification` | `certifications.html` (POST + CSRF) |
| Create Project | `projects/add/` | `create_project` | `projects_form.html` |
| Update Project | `projects/<uuid>/update/` | `update_project` | `projects_form.html` |
| Delete Project | `projects/<uuid>/delete/` | `delete_project` | `components/project_delete_modal.html` |

- **Create**: view membuat form dari `request.POST or None`; jika valid, `form.save()` menyimpan objek baru dan redirect dengan pesan sukses.
- **Update**: view mengambil objek dengan `get_object_or_404`, lalu membuat form dengan `instance=objek`. `form.save()` memperbarui record yang sama, bukan membuat record baru.
- **Delete**: hanya menerima request `POST` melalui form berisi `{% csrf_token %}`. Request `GET` tidak menghapus data (hanya redirect), sehingga penghapusan tidak bisa dipicu oleh tautan biasa.

## JSON delivery flow

- Endpoint `/api/projects/` (`get_projects_json`) dan `/certifications/json/` (`get_certifications_json`) mengembalikan data dalam format JSON.
- Data diambil dari QuerySet (misalnya `Project.objects.all()` atau `Certification.objects.order_by("-issue_date", "name")`), difilter bila ada parameter pencarian, lalu diubah dengan `serializers.serialize("json", queryset)`.
- Hasilnya dikirim sebagai `HttpResponse(..., content_type="application/json")`.
- Endpoint JSON dapat diperiksa langsung di browser, misalnya `http://127.0.0.1:8000/certifications/json/`.

## Serialization/deserialization

1. View `show_certifications` memanggil `get_certifications_json` untuk mendapatkan response JSON.
2. Isi response dibaca dengan `json_response.content.decode("utf-8")`.
3. `serializers.deserialize("json", ...)` mengubah JSON kembali menjadi objek Python (DeserializedObject). Setiap `.object` dikumpulkan ke dalam list.
4. List tersebut dimasukkan ke context dan dirender oleh template dengan `{% for %}`.

Serialization diperlukan karena objek model Django tidak dapat dikirim langsung sebagai data JSON melalui HTTP. Objek harus diubah lebih dulu menjadi format data yang dapat dipahami client, lalu dideserialisasi bila backend ingin memakainya kembali sebagai objek. Pola yang sama dipakai untuk Projects pada `show_projects` dan `get_projects_json`.

# Testing

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Test mencakup URL dan template, pengambilan data dari database, kondisi kosong, tahun opsional, escaping teks HTML, keberadaan file bukti, kesesuaian fixture, konsistensi navigasi, serta seluruh alur Tugas 3:

- create, update, dan delete Project maupun Certification;
- penolakan form tidak valid;
- delete hanya berjalan pada request POST;
- endpoint JSON mengembalikan `Content-Type: application/json` dan field yang benar;
- halaman daftar menggunakan data hasil deserialisasi JSON.

Pemeriksaan lokal terakhir pada 20 September 2026: 30 test lulus, `check` tidak menemukan masalah, dan tidak ada perubahan model yang belum memiliki migrasi. Test berjalan di database test terpisah sehingga tidak menghapus data portofolio lokal.

# Reflection Questions

## 1. Mengapa menggunakan ModelForm dibanding membuat form HTML secara manual? Mengapa `csrf_token` wajib?

ModelForm menghubungkan field pada form dengan field pada model. Django dapat membuat input, melakukan validasi dasar, dan menyimpan data melalui `form.save()`. Dengan form HTML manual, saya perlu menulis ulang setiap field, membaca nilainya dari `request.POST`, melakukan validasi, lalu membuat atau memperbarui object sendiri. ModelForm mempersingkat alur tersebut dan menjaga aturan form tetap mengikuti model, sehingga perbedaan antara model dan form lebih kecil kemungkinannya.

`csrf_token` diperlukan pada form yang mengirim request `POST`. Token ini dibuat oleh server dan disertakan pada form. Django memeriksa token tersebut sebelum menerima perubahan, sehingga website lain tidak dapat dengan mudah membuat browser pengguna mengirim request perubahan tanpa persetujuan yang sah. Tanpa token, Django menolak request dengan status `403 Forbidden`.

## 2. Mengapa JSON lebih banyak digunakan dibanding XML pada aplikasi web modern?

JSON memiliki bentuk yang lebih ringkas dan langsung cocok dengan object serta array yang digunakan JavaScript. Parser JSON tersedia di banyak bahasa pemrograman, sehingga pertukaran data antara backend dan frontend lebih sederhana dan payload lebih kecil. XML tetap berguna pada sistem tertentu, tetapi biasanya membutuhkan tag pembuka dan penutup sehingga payload menjadi lebih panjang untuk data yang sama.

## 3. Bagaimana alur view mengembalikan data JSON, dan mengapa serialization diperlukan?

Saat `/certifications/` dibuka, routing proyek meneruskan request ke `main/urls.py`, lalu route tersebut memanggil `show_certifications`. View memanggil endpoint `get_certifications_json`, mengambil seluruh object Certification, dan mengubahnya menjadi JSON dengan `serializers.serialize()`. JSON dikembalikan sebagai `HttpResponse` dengan `content_type="application/json"`.

Setelah itu, `show_certifications` membaca isi response JSON dan menggunakan `serializers.deserialize()` untuk mengubahnya kembali menjadi object Python. Object tersebut dimasukkan ke context dan dirender oleh `certifications.html`. Serialization diperlukan karena object model Django tidak dapat dikirim langsung sebagai data JSON melalui HTTP; object harus diubah lebih dulu menjadi format data yang dapat dipahami client.

# AI Disclosure

Pengembangan project ini mendapatkan bantuan dari **AI ChatGPT Web** untuk proses brainstorming, review struktur kode, debugging error, dan mendapatkan rekomendasi improvement. Seluruh implementasi akhir tetap melalui proses pemahaman, pengecekan, dan perubahan manual oleh developer.

Dalam pengerjaan Tugas 3, bantuan AI ChatGPT Web digunakan untuk:

- membantu memahami implementasi Django ModelForm;
- membantu menyusun alur CRUD Certification dan menyelaraskan alur CRUD Project;
- membantu memeriksa hubungan antara model, form, view, URL, dan template;
- membantu debugging error saat menjalankan test dan server;
- memberikan masukan terhadap struktur kode, README, dan dokumentasi.

Pengembang tetap membaca ketentuan tugas, memeriksa struktur repository, menyesuaikan kode dengan pola Project yang sudah ada, dan menjalankan test secara manual. Kode tidak langsung diterima sebagai hasil otomatis; setiap bagian diperiksa kembali agar sesuai dengan fitur yang benar-benar digunakan.

## Riwayat dan strategi prompting

- Percakapan Tugas 1 (AI ChatGPT Web): https://chatgpt.com/share/6a9ae1a1-4fe8-83ec-8d60-b252bab78aec
- Percakapan Tugas 2 (AI ChatGPT Web): https://chatgpt.com/share/6aa3d20a-9c40-83ec-b83c-6f973f820a62
- Percakapan Tugas 3 (AI ChatGPT Web): https://chatgpt.com/share/6aaf89fc-ef68-83ec-b16a-6a1e73766bed

# Progres Mingguan

Catatan di bawah menjelaskan kondisi proyek pada minggu terkait, bukan struktur akhir setelah Tugas 3.

## Tutorial 0

- Membuat proyek Django dan repository Git.
- Menambahkan halaman awal serta konfigurasi dasar proyek.

## Tutorial 1

- Membuat bagian profil menggunakan HTML5 dan CSS3.
- Menambahkan foto, informasi diri, dan tautan media sosial.
- Mengatur static files dan deployment menggunakan WhiteNoise.

## Tugas 1

- Menambahkan section Experience dengan tiga pengalaman organisasi.
- Menggunakan konsep timeline vertikal dengan titik dan garis yang dibuat melalui CSS.
- Mengubah isi pengalaman menjadi daftar poin agar lebih mudah dibaca.
- Menyesuaikan layout untuk desktop dan perangkat seluler.
- Memeriksa kembali struktur HTML, duplikasi CSS, dan dokumentasi proyek.

### 1. Elemen semantic HTML apa saja yang digunakan dan bagaimana elemen tersebut membantu struktur serta aksesibilitas website?

Saya menggunakan `<header>` untuk bagian navigasi, `<nav>` untuk kumpulan tautan, `<main>` untuk isi utama, `<section>` untuk memisahkan Profile dan Experience, serta `<footer>` untuk penutup halaman. Pada Experience, saya memakai `<ol>` karena pengalaman ditampilkan sebagai urutan timeline. Setiap pengalaman menjadi satu `<li>`, sedangkan rincian kegiatannya memakai `<ul>` dan `<li>`.

Struktur tersebut membuat fungsi setiap bagian lebih jelas daripada jika seluruh halaman hanya memakai `<div>`. Browser dan pembaca layar juga lebih mudah mengenali navigasi, konten utama, serta batas antarseksi. Saya tidak menambahkan `<article>` atau `<aside>` karena belum ada konten mandiri maupun informasi sampingan yang membutuhkannya.

### 2. Apa tantangan utama saat membuat layout responsif? Bagaimana pendekatan dan hasil evaluasi ketika tampilan berpindah dari desktop ke mobile?

Tantangan utama saya adalah bagian Profile yang menggunakan beberapa kolom pada desktop menjadi terlalu sempit ketika langsung dipakai di layar kecil. Foto, nama, dan detail profil juga perlu tetap memiliki urutan baca yang jelas. Saya mengatasinya dengan CSS Grid: desktop memakai area `identity`, `photo`, dan `details`, kemudian media query di bawah 600 piksel mengubahnya menjadi satu kolom dengan urutan nama, foto, lalu detail. Ukuran foto dibatasi agar tidak memenuhi layar, sementara tautan sosial dapat berpindah baris dengan `flex-wrap`.

Pada timeline, kesulitannya adalah menjaga titik tepat di tengah garis dan menghentikan garis agar tidak melewati pengalaman terakhir. Titik dan garis dibuat relatif terhadap setiap `experience-card`; garis hanya diberikan pada item yang bukan item terakhir. Evaluasinya dilakukan dengan membandingkan tampilan desktop dan mobile, melihat apakah teks masih nyaman dibaca, urutan konten tetap masuk akal, serta memastikan tidak muncul scroll horizontal.

### 3. Apa keterbatasan website statis yang dibuat? Fitur dinamis apa yang ingin dikembangkan selanjutnya?

Saat itu data profil dan pengalaman masih ditulis langsung di template. Akibatnya, setiap perubahan harus dilakukan dengan membuka HTML, dan pemilik website belum dapat menambah pengalaman melalui halaman khusus. Website juga belum memiliki penyimpanan data, autentikasi, maupun formulir yang benar-benar diproses oleh server.

Pengembangan berikutnya yang paling relevan adalah memindahkan data Experience ke model Django. Data tersebut kemudian dapat dikelola melalui Django Admin, diambil oleh view, dan ditampilkan dengan perulangan pada template. Dengan begitu, pengalaman baru dapat ditambahkan tanpa mengubah struktur HTML satu per satu.

## Tutorial 2

- Memisahkan Profile dan Experience menjadi dua halaman sesuai pengerjaan Tutorial 02.
- Mengambil Experience dari model melalui view dan context, lalu menampilkannya dengan Django Template Language.
- Mempertahankan struktur model Experience hasil tutorial dan menambahkan pilihan kategori Organization serta Committee. Fixture Experience mengisi COMPFEST 18, RISTEK Fasilkom UI, dan Open House Fasilkom UI 2025.

## Tugas 2

### 1. Bagaimana alur permintaan sampai halaman baru ditampilkan?

Saat pengguna membuka `/achievements/`, Django memeriksa `portofolio/urls.py`. Pola `path("", include("main.urls"))` meneruskan pencocokan URL ke aplikasi `main`. Di `main/urls.py`, pola `achievements/` mengarah ke fungsi `show_achievements`. Fungsi tersebut menyiapkan `Achievement.objects.order_by("pk")` dan menyimpannya dalam context dengan nama `achievement_list`.

Model Achievement mendefinisikan struktur data yang disimpan di database. QuerySet dari view dievaluasi ketika datanya dibutuhkan saat rendering. Template `achievements.html` melakukan perulangan untuk menampilkan hasil kompetisi, judul, penyelenggara, dan tahun jika tersedia. Jika tidak ada objek, blok `{% empty %}` menampilkan pesan kosong. Template ini mewarisi navbar dan footer dari `base.html`. Hasil akhirnya adalah respons HTML; browser tidak menerima kode Python atau tag template Django.

### 2. Mengapa data prestasi disimpan pada model, bukan langsung di template?

Isi prestasi bisa berubah tanpa perubahan desain. Misalnya, menambahkan hasil kompetisi baru cukup dengan membuat objek Achievement melalui admin; struktur HTML tidak perlu disalin. Field `title`, `result`, `organizer`, dan `evidence_image` berupa teks, sedangkan `year` berupa bilangan bulat positif yang boleh kosong. Tahun WreckIT! 7.0 diverifikasi dari sertifikat bertanggal 5 Agustus 2026. Jika suatu data memang tidak memiliki tahun atau bukti, field tersebut dapat dibiarkan kosong daripada ditebak.

Pemisahan ini juga memudahkan pengembangan: data yang sama nantinya bisa diurutkan atau digunakan oleh halaman lain tanpa membuat salinan isi di HTML. Template hanya mengatur tampilan. Fixture JSON dipakai untuk mengisi data awal, bukan dibaca langsung oleh template; setelah dimuat, view tetap mengambil data dari database.

### 3. Apa perbedaan `makemigrations` dan `migrate`?

`makemigrations` membandingkan definisi model dengan riwayat migrasi dan membuat berkas instruksi perubahan skema. Menambahkan model Achievement menghasilkan `main/migrations/0002_achievement.py`. Pada tahap itu, tabelnya belum otomatis dibuat dalam database. `migrate` kemudian menjalankan migrasi yang belum diterapkan sehingga tabel dan kolomnya benar-benar tersedia.

Sebagai contoh, jika nanti model ditambah field `certificate_url = models.URLField(blank=True)`, jalankan `python manage.py makemigrations main` untuk membuat migrasi, lalu `python manage.py migrate` untuk menambahkan kolomnya. Sebaliknya, mengganti teks judul prestasi melalui admin hanya mengubah satu record, sehingga tidak memerlukan migrasi. Berkas migrasi perlu ikut masuk Git agar struktur database dapat dibuat ulang pada lingkungan lain.

### Implementasi dan pemeriksaan Tugas 2

Model baru memiliki lima field selain primary key otomatis. Halaman `/achievements/` memakai named route `main:show_achievements`. Data awalnya memuat POLRI CTF, WreckIT! 7.0, FINDIT! CTF, DSG Zero Day CTF Open Arena, dan Hack The Box Global Cyber Skills Benchmark 2026 berdasarkan CV serta bukti yang tersedia.

Bukti visual yang digunakan adalah foto penghargaan POLRI CTF, sertifikat finalis WreckIT! 7.0, sertifikat finalis FINDIT! 2026, sertifikat Open Arena DSG Zero Day, dan sertifikat partisipasi Hack The Box. Kelimanya disimpan sebagai static image dan dapat dibuka dari kartu. Sertifikat HTB mencatat peringkat tim 62 dari 589 tim; angka tersebut dipakai sebagai hasil pada kartu tanpa mengubah status sertifikatnya.

Test mencakup URL dan template baru, tiga Experience dan lima Achievement pada dashboard, beberapa objek yang muncul dari database, kondisi kosong, tahun opsional, escaping teks, keberadaan file bukti, kesesuaian fixture, serta konsistensi navigasi ketiga halaman. Test Experience juga memeriksa kategori Organization, status selesai/berlangsung, dan deskripsi dengan beberapa poin.

Pemeriksaan lokal pada 9 September 2026: 17 test lulus, `check` tidak menemukan masalah, dan tidak ada perubahan model yang belum memiliki migrasi. Dashboard, Experience, dan Achievements diperiksa pada lebar 320, 390, 768, dan 1440 piksel. Tidak ada scroll horizontal; grid Achievement berubah menjadi 3–2 pada desktop, dua kolom pada tablet, dan satu kolom pada mobile.

Arah hero mempertahankan [portofolio sebelumnya](https://portofolio-website-sand.vercel.app/#experience): foto persegi dengan bidang putih offset, tombol sosial solid, dan latar navy. Timeline tetap ringkas, dengan logo persegi di sisi kiri seperti susunan Experience pada LinkedIn. Palet navy-teal dipakai secara konsisten agar tidak menyalin tampilan referensi teman. Kartu Achievement memakai thumbnail dengan konteks pendek. Implementasinya tetap HTML/CSS dan template Django, tanpa React, library UI, atau JavaScript. Referensi teknis: [fixture Django](https://docs.djangoproject.com/en/5.2/howto/initial-data/), [CSS position](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position), dan [backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter).

## Tutorial 3

- Membuat `base.html` sebagai template dasar untuk navbar, footer, metadata, dan content block.
- Menambahkan model `Project`, migration, `ProjectForm`, serta halaman `/projects/add/`.
- Menambahkan halaman `/projects/` yang dapat mencari project berdasarkan judul.
- Menambahkan endpoint `/api/projects/` yang mengirim data Project dalam format JSON.
- Mengubah `show_projects` agar membaca response JSON dan melakukan deserialize sebelum merender template.
- Menambahkan penghapusan Project melalui request `POST` dengan CSRF token dan konfirmasi popover.

## Tugas 3

Fitur baru yang dibuat adalah halaman Certification. Data Certification disimpan pada model Django dan dapat dikelola melalui halaman web dengan operasi create, update, dan delete. Halaman daftar menggunakan data dari endpoint JSON, kemudian melakukan deserialisasi sebelum data dikirim ke template. Halaman Project juga dilengkapi operasi update agar kedua bagian data pilihan memiliki alur CRUD lengkap.

- `main/models.py`: model `Certification` dengan enam field dan `Project` dengan lima field.
- `main/forms.py`: `CertificationForm` dan `ProjectForm` berbasis `ModelForm`.
- `main/views.py`: `create_`, `update_`, dan `delete_certification/project`, serta endpoint JSON dan deserialisasi.
- `main/urls.py`: routing CRUD dan JSON untuk Projects serta Certifications.
- `templates/`: `certification_form.html`, `certifications.html`, `projects_form.html`, `project.html`, dan `components/project_delete_modal.html`.

Pemeriksaan revisi Tugas 3 menjalankan `python manage.py check`, `python manage.py makemigrations --check --dry-run`, dan `python manage.py test`. Pemeriksaan ini menghasilkan 30 test lulus. Halaman `/projects/`, `/projects/add/`, `/projects/<id>/update/`, `/certifications/`, `/certifications/add/`, dan `/certifications/<id>/update/` juga diperiksa untuk memastikan title tidak ganda, input tanggal memakai tipe date, dan tidak ada scroll horizontal.
