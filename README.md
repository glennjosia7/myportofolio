# Portofolio Glenn Josia Devano

Website portofolio pribadi untuk menampilkan profil dan pengalaman organisasi. Proyek ini dibuat dengan Django, HTML5, dan CSS3 sebagai pengembangan dari Tutorial 01 PBP.

## Identitas

- Nama: Glenn Josia Devano
- NPM: 2506614712
- Kelas: PBP F

## Fitur

- Bagian profil yang berisi perkenalan, identitas, foto, dan tautan media sosial.
- Timeline pengalaman yang memuat COMPFEST 18, RISTEK, dan Open House Fasilkom UI 2025.
- Animasi masuk pada bagian profil dan efek hover pada tautan sosial.
- Tampilan responsif untuk layar desktop dan perangkat seluler.

## Teknologi

- Django untuk routing dan merender template.
- HTML5 untuk struktur dan semantik halaman.
- CSS3 untuk layout, timeline, animasi, dan tampilan responsif.

## Cara Menjalankan Proyek

```powershell
git clone https://github.com/glennjosia7/myportolio.git
cd myportolio
python -m venv env
env\Scripts\activate
python -m pip install -r requirements.txt
python manage.py runserver
```

Buka `http://127.0.0.1:8000/` pada browser setelah server berjalan.

## Alur Sederhana Aplikasi

1. Browser mengakses alamat `/`.
2. `portofolio/urls.py` meneruskan permintaan tersebut ke fungsi `landing_page`.
3. Fungsi di `portofolio/views.py` merender `templates/index.html`.
4. Template memuat foto dan `static/css/style.css` melalui tag `{% static %}`.
5. Browser menampilkan halaman portofolio beserta layout responsifnya.

Bagian yang paling sering diubah adalah `templates/index.html` untuk isi halaman dan `static/css/style.css` untuk tampilannya. Jika ingin menambah pengalaman, cukup salin satu elemen `<li class="experience-card">`, ganti isinya, lalu letakkan di dalam `<ol class="experience-list">`. Warna utama tersimpan sebagai variabel pada bagian `:root`, sedangkan aturan layar kecil berada di dalam `@media (max-width: 600px)`.

## Progres Mingguan

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

## Dokumentasi Penggunaan AI

Saya menggunakan AI Web ChatGPT untuk memeriksa pemahaman, bukan untuk meminta hasil website siap pakai. Percakapan difokuskan pada alur kerja Django, rencana pengembangan data Experience, dan cara menunjukkan bukti implementasi berdasarkan rubrik.

Tautan percakapan: [AI Web ChatGPT - Analisis Struktur Semantik](https://chatgpt.com/share/6a9ae1a1-4fe8-83ec-8d60-b252bab78aec)

### Ringkasan Penggunaan AI

1. Saya menjelaskan pemahaman saya bahwa request ke `/` diarahkan oleh `urls.py` menuju `landing_page`, lalu view merender `index.html` dan browser meminta static files. ChatGPT membantu mengoreksi batas tanggung jawab URL, view, template, dan static files.
2. Saya mendiskusikan kemungkinan memindahkan data Experience yang masih hardcode ke model Django. Hasil percakapan membantu saya memahami urutan belajar dari mengirim data melalui view, melakukan perulangan di template, menggunakan model dan database, hingga mengelola data melalui Django Admin.
3. Saya membandingkan sekadar memenuhi checklist dengan memberikan bukti implementasi yang dapat dinilai. Dari pembahasan tersebut, saya memahami bahwa struktur `<section>`, `<ol>`, dan `<li>`, pseudo-element pada timeline, selector `:not(:last-child)`, media query, serta penjelasan proses pada README dapat menjadi bukti keputusan teknis.

AI membantu menjelaskan konsep dan memberi contoh umum, tetapi contoh tersebut tidak selalu sama dengan struktur proyek saya. Karena itu, saya tidak langsung menyalinnya. Saya tetap memeriksa file yang digunakan, menyesuaikan penjelasan dengan implementasi yang benar-benar ada, serta menguji tampilan desktop dan mobile secara manual.
