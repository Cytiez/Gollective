Nama: Raqilla Al-Abrar
NPM: 2406496025
Kelas: A

Link PWS: https://raqilla-alabrar-gollective.pbp.cs.ui.ac.id/

##TUGAS1##
Step by step implementasi checklist:
    1. Inisiasi pembuatan projek Django
       Membuat project baru bernama 'gollective' menggunakan 'django-admin startproject gollective .'
    2. Membuat aplikasi main
       Menggunakan perintah 'python manage.py startapp main', lalu menambahkan 'main' ke INSTALLED_APPS yang berada di settings.py
    3. Membuat model Products
       Pada main/models.py saya membuat model Product dengan field wajib (name, price, description, thumbnail, category, is_featured). Selain itu saya juga menambahkan field tambahan
       club_name -> nama club dari jersey (CharField)
       season -> musim jersey (CharField)
       release_year -> tahun rolis jersey (IntegerField)
       condition -> kondisi jersey (CharField, dengan default = mint)
       authenticity -> status keaslian dari jersey (BooleanField, dengan default = true)

       setelah itu saya menjalankan migration dengan menjalankan:
       python manage.py makemigrations
       python manage.py migrate
    4. Membuat view dan template:
       views.py: membuat fungsi show_main untuk mengirim context
       templates/main.html: menampilkan context yang sudah dibuat pada views.py
    5. Routing url
       main/urls.py: menambahkan path untuk fungsi show_main.
       gollective/urls.py: menambahkan include('main.urls') agar root URL diarahkan ke app main.
    6. Testing lokal dan deploy ke pws
       Setelah melakukan semua pembuatan diatas saya melakukan testing pada lokal server terlebih dahulu untuk cek apakah ada kesalahan menggunakan python manage.py runserver. Lalu jika tidak terjadi kesalahn baru saya deploy ke pws.

Bagan request client ke web aplikasi berbasis Django:
    <img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/70602f2c-3dfc-4eae-8031-23e5531478a6" />
    1. Client
        User membuka url di browser. Request dari client tersebut akan dikirim ke server Django
    2. urls.py (Project -> app)
        Pertama Django akan cek urls.py pada gollective/urls.py, lalu request akan diarahkan ke main/urls.py, urls.py berfungsi untuk memetakan URL ke view yang sesuai.
    3. views.py
        Setelah URL dicocokan, fungsi apda views.py akan dijalankan. Views berperan sebagai jembatan antara data (model) dan tampilan (template).
    4. models.py <-> databse
        models.py adalah representasi data dalam bentuk Python class. Model akan berkomunikasi dengan database untuk mengambil atau menyimpan data.
    5. templates (HTML)
        Setelah model mendapatkan data, view akan mengirim data tersebut dalam bentuk context ke file template. Template akan mengatur bagaimana data akan ditampilkan ke user.
    6. Response kembali ke client
        Template dirender menjadi HTML. Django mengirim HTML tersebut sebagai response ke browser. Browser akan menampilkan tampilan halaman web yang sudah berisi beragam data dari database.

Peran settings.py
    settings.py adalah ousat konfigurasi dari Django
    INSTALLED_APPS: daftar aplikasi yang digunakan
    DATABASES: konfigurasi database
    MIDDLEWARE: middleware untuk request atau response
    TEMPLATE: pengaturan engine template Django
    ALLOWED HOST: untuk keamanan dan deployment aplikasi
    STATICFILES: konfugrasi file statis seperti CSS, JS, gambar

Cara kerja migrasi
    python manage.py makemigrations → membuat file migrasi dari perubahan model.
    python manage.py migrate → mengeksekusi file migrasi tersebut agar database sinkron dengan model.
    Migrasi memastikan struktur database selalu sesuai dengan definisi model di Python.

Django dipilih sebagai framework awal karena beberapa alasan berikut:
    1. Konsep MVT yabg mudah dipahami untuk belajar alur web app
    2. Fitur bawaan lengkap seperti ORM, auth, admin, form, dan lain-lain
    3. Dokumentasi Django sudah sangat baik sehingga memudahkan mahasiswa untuk belajar mandiri

Feedback: Sejauh ini sudah sangat baik, asdosnya juga keren banget, sangat amat membantu.

##TUGAS2##
Mengapa perlu data delivery?
    Data delivery dibutuhkan supaya aplikasi bisa saling bertukar data, baik antar sistem maupun antar platform. Misalnya backend Django bisa memberikan data JSON ke aplikasi mobile, atau menyediakan XML untuk integrasi dengan sistem lain. Tanpa data delivery, aplikasi hanya bisa menampilkan HTML ke user dan sulit diintegrasikan.
Mana yang lebih baik JSON atau XML? Kenapa JSON lebih populer
    Secara umum JSON lebih baik untuk kebutuhan modern karena lebih ringan, mudah dibaca manusia, dan lebih efisien diproses komputer. XML cenderung verbose dengan banyak tag pembuka/penutup. JSON lebih populer karena sudah jadi standar di web API, didukung langsung oleh JavaScript, dan lebih gampang diolah di berbagai bahasa pemrograman.
Method is_valid()
    is_valid() digunakan untuk memeriksa apakah data yang di-submit melalui form sudah sesuai dengan aturan model dan field validasi. Method ini juga otomatis membersihkan data (cleaned_data). Kita butuh ini supaya data yang masuk ke database tidak rusak atau tidak sesuai format.
Kenapa butuh csrf_token untuk bikin form? Bahaya jika tidak menggunakan, bagaimana penyerang dapat memanfaatkannya?
    csrf_token mencegah serangan CSRF (Cross-Site Request Forgery), yaitu serangan di mana attacker membuat user tanpa sadar mengirim request berbahaya. Kalau token ini tidak ada, attacker bisa memanfaatkan session user yang sedang login untuk melakukan aksi seperti mengubah data atau mengirim form tanpa izin.
Implementasi checklist
    1. Tambah view data delivery
        Pada views.py ditambahkan fungsi show_xml, show_json, show_xml_by_id, dan show_json_by_id untuk mengembalikan data produk dalam format XML/JSON.
        Menggunakan serializers.serialize() dari Django untuk mengubah queryset menjadi XML/JSON.
    2. Routing URL
        Di main/urls.py ditambahkan path untuk masing-masing fungsi: /xml/, /json/, /xml/<id>/, /json/<id>/.
    3. Buat halaman utama dengan tombol add
        Pada main.html ditambahkan tombol Add Product untuk redirect ke form input.
        Data produk ditampilkan dalam bentuk list, setiap produk punya tombol Detail untuk melihat detail produk.
    4. Form input produk
        Membuat forms.py dengan ProductForm berbasis ModelForm.
        Membuat view add_product yang menampilkan form dan menyimpan data baru ketika di-submit.
        Template add_product.html berisi form dengan {% csrf_token %} untuk keamanan.
    5. Halaman detail produk
        Membuat view show_product yang menampilkan detail produk berdasarkan id.
        Template product_detail.html menampilkan informasi lengkap produk.
    6. Testing lokal dan deploy pws
        Menjalankan server lokal dengan python manage.py runserver untuk cek error.
        Push ke GitHub dan PWS, lalu cek di URL deployment.

