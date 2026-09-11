# Portofolio Glenn Josia Devano

Website portofolio pribadi dengan halaman Profile, Experience, dan Achievements. Proyek ini dibuat dengan Django, HTML5, dan CSS3 sebagai pengembangan Tutorial 02 dan Tugas 2 PBP.

## Identitas

- Nama: Glenn Josia Devano
- NPM: 2506614712
- Kelas: PBP F

## Fitur

- Bagian profil yang berisi perkenalan, identitas, foto, dan tautan media sosial.
- Timeline Experience yang mengambil tiga pengalaman dari database, dengan status Ongoing atau Completed.
- Halaman Achievements berisi lima hasil kompetisi CTF dari database dan bukti masing-masing.
- Halaman utama memuat preview Experience dan Achievement dengan tautan menuju halaman lengkap.
- Navbar transparan dengan blur, tetap di atas saat di-scroll, dan penanda halaman aktif.
- Navbar dan footer bersama melalui template inheritance Django.
- Tampilan responsif untuk layar desktop, tablet, dan perangkat seluler.

## Teknologi

- Django untuk model, database, routing, unit test, dan merender template.
- HTML5 untuk struktur dan semantik halaman.
- CSS3 untuk layout, timeline, navbar sticky, dan tampilan responsif tanpa JavaScript.

## Cara Menjalankan Proyek

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

Untuk mengelola data tanpa mengedit HTML, jalankan `python manage.py createsuperuser`, lalu masuk ke `/admin/`. Model Achievement dan Experience sudah terdaftar. Pada deskripsi Experience, satu baris teks akan ditampilkan sebagai satu poin. Field `logo` menyimpan path static untuk logo COMPFEST, RISTEK, dan Open House Fasilkom UI 2025. Jangan bagikan kredensial admin atau berkas `.env`.

Untuk database di PWS, migrasi dan pengisian data perlu dijalankan di lingkungan PWS juga; isi SQLite lokal tidak ikut terkirim melalui Git. Pengembangan ini belum di-deploy ulang.

## Alur Sederhana Aplikasi

1. `portofolio/urls.py` menerima pola URL dan meneruskannya ke `main/urls.py` melalui `include`.
2. `/` memanggil `show_main`, `/experience/` memanggil `show_experience`, dan `/achievements/` memanggil `show_achievements`.
3. View menyiapkan context. View Experience dan Achievements mengambil QuerySet dari model masing-masing.
4. Template halaman mengisi blok pada `templates/base.html`. Daftar data ditampilkan melalui `{% for %}`, dengan `{% empty %}` untuk database kosong.
5. Browser menerima HTML dan memuat stylesheet serta foto dari static files.

Bagian yang perlu dikenali untuk melanjutkan proyek:

| Perubahan yang ingin dilakukan | Lokasi |
| --- | --- |
| Menambah atau mengubah isi prestasi/pengalaman | Django Admin, bukan template |
| Menambah field prestasi | `main/models.py`, kemudian `makemigrations` dan `migrate` |
| Mengubah urutan daftar | `order_by()` di `main/views.py` |
| Mengubah susunan hasil, judul, penyelenggara, tahun, dan bukti | model/data Achievement dan `templates/achievements.html` |
| Menambah tautan navbar atau mengubah footer | `templates/base.html` |
| Mengubah warna, jarak, dan layout mobile | `static/css/style.css` |

Warna bersama ada pada `:root`. Palet navy dan teal digunakan konsisten pada seluruh halaman agar berbeda dari referensi teman. Navbar diatur oleh `.site-header`: `position: sticky`, `top: 0`, dan `z-index` membuatnya tetap terlihat; latar `rgba` dan `backdrop-filter` memberi efek transparan. Titik timeline dibuat oleh `.experience-item::before`, sedangkan garis hanya dibuat oleh `:not(:last-child)::after`. Keduanya memakai `left: 0` dan `translateX(-50%)` agar pusatnya sama. Bila hanya ada satu pengalaman, tidak ada garis penghubung. Grid Achievement berubah dari tiga kolom di desktop menjadi dua kolom di tablet dan satu kolom di mobile.

## Progres Mingguan

Catatan Tugas 1 di bawah menjelaskan kondisi proyek saat minggu tersebut, bukan struktur setelah Tugas 2.

### Tutorial 0

- Membuat proyek Django dan repository Git.
- Menambahkan halaman awal serta konfigurasi dasar proyek.

### Tutorial 1

- Membuat bagian profil menggunakan HTML5 dan CSS3.
- Menambahkan foto, informasi diri, dan tautan media sosial.
- Mengatur static files dan deployment menggunakan WhiteNoise.

### Tugas 1

- Menambahkan section Experience dengan tiga pengalaman organisasi.
- Menggunakan konsep timeline vertikal dengan titik dan garis yang dibuat melalui CSS.
- Mengubah isi pengalaman menjadi daftar poin agar lebih mudah dibaca.
- Menyesuaikan layout untuk desktop dan perangkat seluler.
- Memeriksa kembali struktur HTML, duplikasi CSS, dan dokumentasi proyek.

#### 1. Elemen semantic HTML apa saja yang digunakan dan bagaimana elemen tersebut membantu struktur serta aksesibilitas website?

Saya menggunakan `<header>` untuk bagian navigasi, `<nav>` untuk kumpulan tautan, `<main>` untuk isi utama, `<section>` untuk memisahkan Profile dan Experience, serta `<footer>` untuk penutup halaman. Pada Experience, saya memakai `<ol>` karena pengalaman ditampilkan sebagai urutan timeline. Setiap pengalaman menjadi satu `<li>`, sedangkan rincian kegiatannya memakai `<ul>` dan `<li>`.

Struktur tersebut membuat fungsi setiap bagian lebih jelas daripada jika seluruh halaman hanya memakai `<div>`. Browser dan pembaca layar juga lebih mudah mengenali navigasi, konten utama, serta batas antarseksi. Saya tidak menambahkan `<article>` atau `<aside>` karena belum ada konten mandiri maupun informasi sampingan yang membutuhkannya.

#### 2. Apa tantangan utama saat membuat layout responsif? Bagaimana pendekatan dan hasil evaluasi ketika tampilan berpindah dari desktop ke mobile?

Tantangan utama saya adalah bagian Profile yang menggunakan beberapa kolom pada desktop menjadi terlalu sempit ketika langsung dipakai di layar kecil. Foto, nama, dan detail profil juga perlu tetap memiliki urutan baca yang jelas. Saya mengatasinya dengan CSS Grid: desktop memakai area `identity`, `photo`, dan `details`, kemudian media query di bawah 600 piksel mengubahnya menjadi satu kolom dengan urutan nama, foto, lalu detail. Ukuran foto dibatasi agar tidak memenuhi layar, sementara tautan sosial dapat berpindah baris dengan `flex-wrap`.

Pada timeline, kesulitannya adalah menjaga titik tepat di tengah garis dan menghentikan garis agar tidak melewati pengalaman terakhir. Titik dan garis dibuat relatif terhadap setiap `experience-card`; garis hanya diberikan pada item yang bukan item terakhir. Evaluasinya dilakukan dengan membandingkan tampilan desktop dan mobile, melihat apakah teks masih nyaman dibaca, urutan konten tetap masuk akal, serta memastikan tidak muncul scroll horizontal.

#### 3. Apa keterbatasan website statis yang dibuat? Fitur dinamis apa yang ingin dikembangkan selanjutnya?

Saat ini data profil dan pengalaman masih ditulis langsung di template. Akibatnya, setiap perubahan harus dilakukan dengan membuka HTML, dan pemilik website belum dapat menambah pengalaman melalui halaman khusus. Website juga belum memiliki penyimpanan data, autentikasi, maupun formulir yang benar-benar diproses oleh server.

Pengembangan berikutnya yang paling relevan adalah memindahkan data Experience ke model Django. Data tersebut kemudian dapat dikelola melalui Django Admin, diambil oleh view, dan ditampilkan dengan perulangan pada template. Dengan begitu, pengalaman baru dapat ditambahkan tanpa mengubah struktur HTML satu per satu. Fitur ini juga menjadi langkah yang masuk akal untuk mempelajari alur Model-View-Template tanpa menambah kompleksitas yang belum diperlukan.

### Tutorial 2

- Memisahkan Profile dan Experience menjadi dua halaman sesuai pengerjaan Tutorial 02.
- Mengambil Experience dari model melalui view dan context, lalu menampilkannya dengan Django Template Language.
- Mempertahankan struktur model Experience hasil tutorial dan menambahkan pilihan kategori Organization serta Committee. Fixture Experience mengisi COMPFEST 18, RISTEK Fasilkom UI, dan Open House Fasilkom UI 2025.

### Tugas 2

1. **Bagaimana alur permintaan sampai halaman baru ditampilkan?**

   Saat pengguna membuka `/achievements/`, Django memeriksa `portofolio/urls.py`. Pola `path("", include("main.urls"))` meneruskan pencocokan URL ke aplikasi `main`. Di `main/urls.py`, pola `achievements/` mengarah ke fungsi `show_achievements`. Fungsi tersebut menyiapkan `Achievement.objects.order_by("pk")` dan menyimpannya dalam context dengan nama `achievement_list`.

   Model Achievement mendefinisikan struktur data yang disimpan di database. QuerySet dari view dievaluasi ketika datanya dibutuhkan saat rendering. Template `achievements.html` melakukan perulangan untuk menampilkan hasil kompetisi, judul, penyelenggara, dan tahun jika tersedia. Jika tidak ada objek, blok `{% empty %}` menampilkan pesan kosong. Template ini mewarisi navbar dan footer dari `base.html`. Hasil akhirnya adalah respons HTML; browser tidak menerima kode Python atau tag template Django.

2. **Mengapa data prestasi disimpan pada model, bukan langsung di template?**

   Isi prestasi bisa berubah tanpa perubahan desain. Misalnya, menambahkan hasil kompetisi baru cukup dengan membuat objek Achievement melalui admin; struktur HTML tidak perlu disalin. Field `title`, `result`, `organizer`, dan `evidence_image` berupa teks, sedangkan `year` berupa bilangan bulat positif yang boleh kosong. Tahun WreckIT! 7.0 diverifikasi dari sertifikat bertanggal 5 Agustus 2026. Jika suatu data memang tidak memiliki tahun atau bukti, field tersebut dapat dibiarkan kosong daripada ditebak.

   Pemisahan ini juga memudahkan pengembangan: data yang sama nantinya bisa diurutkan atau digunakan oleh halaman lain tanpa membuat salinan isi di HTML. Template hanya mengatur tampilan. Fixture JSON dipakai untuk mengisi data awal, bukan dibaca langsung oleh template; setelah dimuat, view tetap mengambil data dari database.

3. **Apa perbedaan `makemigrations` dan `migrate`?**

   `makemigrations` membandingkan definisi model dengan riwayat migrasi dan membuat berkas instruksi perubahan skema. Menambahkan model Achievement menghasilkan `main/migrations/0002_achievement.py`. Pada tahap itu, tabelnya belum otomatis dibuat dalam database. `migrate` kemudian menjalankan migrasi yang belum diterapkan sehingga tabel dan kolomnya benar-benar tersedia.

   Sebagai contoh, jika nanti model ditambah field `certificate_url = models.URLField(blank=True)`, jalankan `python manage.py makemigrations main` untuk membuat migrasi, lalu `python manage.py migrate` untuk menambahkan kolomnya. Sebaliknya, mengganti teks judul prestasi melalui admin hanya mengubah satu record, sehingga tidak memerlukan migrasi. Berkas migrasi perlu ikut masuk Git agar struktur database dapat dibuat ulang pada lingkungan lain.

#### Implementasi dan pemeriksaan Tugas 2

Model baru memiliki lima field selain primary key otomatis. Halaman `/achievements/` memakai named route `main:show_achievements`. Data awalnya memuat POLRI CTF, WreckIT! 7.0, FINDIT! CTF, DSG Zero Day CTF Open Arena, dan Hack The Box Global Cyber Skills Benchmark 2026 berdasarkan CV serta bukti yang tersedia.

Bukti visual yang digunakan adalah foto penghargaan POLRI CTF, sertifikat finalis WreckIT! 7.0, sertifikat finalis FINDIT! 2026, sertifikat Open Arena DSG Zero Day, dan sertifikat partisipasi Hack The Box. Kelimanya disimpan sebagai static image dan dapat dibuka dari kartu. Sertifikat HTB mencatat peringkat tim 62 dari 589 tim; angka tersebut dipakai sebagai hasil pada kartu tanpa mengubah status sertifikatnya.

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Test mencakup URL dan template baru, tiga Experience dan lima Achievement pada dashboard, beberapa objek yang muncul dari database, kondisi kosong, tahun opsional, escaping teks, keberadaan file bukti, kesesuaian fixture, serta konsistensi navigasi ketiga halaman. Test Experience juga memeriksa kategori Organization, status selesai/berlangsung, dan deskripsi dengan beberapa poin. Semua perubahan diuji di database test terpisah, bukan dengan menghapus data portofolio lokal.

Pemeriksaan lokal pada 9 September 2026: 17 test lulus, `check` tidak menemukan masalah, dan tidak ada perubahan model yang belum memiliki migrasi. Dashboard, Experience, dan Achievements diperiksa pada lebar 320, 390, 768, dan 1440 piksel. Tidak ada scroll horizontal; grid Achievement berubah menjadi 3–2 pada desktop, dua kolom pada tablet, dan satu kolom pada mobile. Semua gambar bukti dan dua logo organisasi berhasil dimuat, navbar tetap sticky, serta garis timeline berhenti pada item terakhir. Pemeriksaan ini tidak membuktikan deployment PWS sudah berhasil.

Test lokal masih mengeluarkan peringatan WhiteNoise karena folder hasil `collectstatic` belum ada; ini tidak menggagalkan test. Pemeriksaan ini tidak membuktikan deployment PWS sudah berhasil.

Arah hero mempertahankan [portofolio sebelumnya](https://portofolio-website-sand.vercel.app/#experience): foto persegi dengan bidang putih offset, tombol sosial solid, dan latar navy. Timeline tetap ringkas, dengan logo persegi di sisi kiri seperti susunan Experience pada LinkedIn. Palet navy-teal dipakai secara konsisten agar tidak menyalin tampilan referensi teman. Kartu Achievement memakai thumbnail dengan konteks pendek. Implementasinya tetap HTML/CSS dan template Django, tanpa React, library UI, atau JavaScript. Referensi teknis: [fixture Django](https://docs.djangoproject.com/en/5.2/howto/initial-data/), [CSS position](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/position), dan [backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter).

## Dokumentasi Penggunaan AI

### Catatan Tugas 1

Saya menggunakan AI Web ChatGPT untuk memeriksa pemahaman, bukan untuk meminta hasil website siap pakai. Percakapan difokuskan pada alur kerja Django, rencana pengembangan data Experience, dan cara menunjukkan bukti implementasi berdasarkan rubrik.

Tautan percakapan: [AI Web ChatGPT - Tugas 1](https://chatgpt.com/share/6a9ae1a1-4fe8-83ec-8d60-b252bab78aec)

### Ringkasan Penggunaan AI

1. Saya menjelaskan pemahaman saya bahwa request ke `/` diarahkan oleh `urls.py` menuju `landing_page`, lalu view merender `index.html` dan browser meminta static files. ChatGPT membantu mengoreksi batas tanggung jawab URL, view, template, dan static files.
2. Saya mendiskusikan kemungkinan memindahkan data Experience yang masih hardcode ke model Django. Hasil percakapan membantu saya memahami urutan belajar dari mengirim data melalui view, melakukan perulangan di template, menggunakan model dan database, hingga mengelola data melalui Django Admin.
3. Saya membandingkan sekadar memenuhi checklist dengan memberikan bukti implementasi yang dapat dinilai. Dari pembahasan tersebut, saya memahami bahwa struktur `<section>`, `<ol>`, dan `<li>`, pseudo-element pada timeline, selector `:not(:last-child)`, media query, serta penjelasan proses pada README dapat menjadi bukti keputusan teknis.

AI membantu menjelaskan konsep dan memberi contoh umum, tetapi contoh tersebut tidak selalu sama dengan struktur proyek saya. Karena itu, saya tidak langsung menyalinnya. Saya tetap memeriksa file yang digunakan, menyesuaikan penjelasan dengan implementasi yang benar-benar ada, serta menguji tampilan desktop dan mobile secara manual.

### Catatan Tugas 2

Pengembangan Tugas 2 dibantu ChatGPT melalui Codex. Bantuan mencakup pembacaan checklist tugas dan CV, peninjauan portofolio lama, implementasi model/view/template/migrasi, penataan CSS, penulisan test, serta draf dokumentasi dan jawaban reflektif. Jadi, bantuan pada tahap ini bukan hanya diskusi konsep. Pembahasan kemudian dilanjutkan melalui AI Web ChatGPT untuk menguji pemahaman tentang alur MVT, rancangan model, routing, unit test, dan jawaban reflektif. Prompt diawali dengan analisis dan kesulitan yang saya alami, kemudian meminta kritik atau pertanyaan pemandu, bukan kode website siap pakai.

Tautan percakapan Tugas 2: [AI Web ChatGPT - Tugas 2](https://chatgpt.com/share/6aa3d34a-0698-83ec-85e1-739a8085dbfa)

Log ringkas permintaan dan keputusan sesi ini:

- Permintaan: mengembangkan Tugas 2 dengan bagian Prestasi berdasarkan CV, merapikan Experience, serta membuat navbar transparan yang tetap di atas ketika di-scroll. Portofolio lama diberikan sebagai referensi dan Ponytail diminta untuk menjaga kode sederhana.
- Hasil pembacaan sumber: lima hasil kompetisi CTF dipakai sebagai data awal. Tiga pengalaman organisasi dan kepanitiaan disesuaikan dengan CV.
- Implementasi: satu model Achievement dan halaman daftar; navbar/footer dibagikan lewat template inheritance. Dashboard menampilkan tiga Experience dan lima Achievement berbukti. Pengelolaan data menggunakan Django Admin bawaan, tanpa membuat formulir atau halaman detail tambahan.
- Revisi visual: konsep hero awal dipertahankan, kartu Experience diberi hover ringan serta identitas logo/badge, dan lima bukti pencapaian ditampilkan sebagai gambar yang dapat dibuka.
- Pemeriksaan: unit test dijalankan. Test awal menemukan sisa HTML lama pada Profile setelah pemisahan template; struktur tersebut dibersihkan dan seluruh test dijalankan ulang.

Jawaban reflektif di atas merupakan draf berbantuan AI yang perlu saya pelajari dan periksa sebelum pengumpulan. Untuk mengecek pemahaman secara mandiri, saya dapat menelusuri satu request `/achievements/`, menambahkan satu prestasi melalui admin, lalu menjelaskan mengapa tindakan itu tidak memerlukan migrasi. Menambah field baru adalah latihan berbeda karena melibatkan perubahan skema. Latihan ini belum dinyatakan sebagai kegiatan yang sudah saya lakukan.
