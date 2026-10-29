# Digital Voting API

API pemilihan untuk latihan modularitas, prinsip SOLID, Git, dan unit testing. Server menggunakan FastAPI, validasi request menggunakan Pydantic, dan penyimpanan memakai struktur dictionary/list di memori. Tidak ada data yang bertahan setelah server dimatikan atau dimulai ulang.

> Proyek ini untuk pembelajaran. Endpoint validasi pemilih belum memakai autentikasi, jadi jangan digunakan untuk pemilihan nyata.

## Menjalankan proyek

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Buka dokumentasi interaktif FastAPI di `http://127.0.0.1:8000/docs`. Cek server melalui `GET /health`.

## Alur mencoba API

1. Daftarkan pemilih melalui `POST /voters` dengan `{"name":"Ayu","email":"ayu@example.com"}`. Pemilih baru belum tervalidasi.
2. Validasi pemilih dengan `PATCH /voters/{voter_id}/validate`.
3. Buat pemilihan dengan `POST /elections` dan body `{"title":"Ketua Kelas"}`.
4. Tambahkan kandidat melalui `POST /elections/{election_id}/candidates` dengan `{"name":"Budi","description":"Kandidat nomor satu"}`. Kandidat hanya dapat ditambahkan saat status masih `draft`.
5. Buka pemilihan lewat `POST /elections/{election_id}/open`. Pemilihan harus memiliki minimal satu kandidat.
6. Kirim suara lewat `POST /elections/{election_id}/votes` dengan `{"voter_id":"...","candidate_id":"..."}`.
7. Tutup pemilihan lewat `POST /elections/{election_id}/close`, lalu baca hasil melalui `GET /elections/{election_id}/results`.

Pemilih harus terdaftar dan tervalidasi, kandidat harus berasal dari pemilihan yang sama, dan pemilih hanya boleh memilih satu kali pada setiap pemilihan. Hasil hanya tersedia setelah pemilihan ditutup.

## Struktur penting

- `models/`: bentuk objek domain (`Voter`, `Election`, `Candidate`, `Vote`).
- `schemas/`: validasi request dan format response Pydantic.
- `repositories/`: kontrak repository (`Protocol`) serta implementasi dictionary/list in-memory.
- `services/`: aturan bisnis dan validasi alur pemilihan.
- `routes/`: endpoint HTTP; tiap modul meneruskan pekerjaan ke service.
- `tests/`: unit test untuk aturan pemilih, pemilihan, dan voting.

## Catatan desain

Service bergantung pada kontrak repository, bukan langsung pada detail dictionary. Jika kelak penyimpanan diganti, implementasi repository dapat diganti tanpa memindahkan aturan bisnis dari service. `create_app()` membuat penyimpanan baru sehingga setiap instance aplikasi mulai dengan data kosong.

## Menjalankan unit test

```powershell
pytest -q
```

Test mencakup jalur berhasil, email duplikat, pemilih belum tervalidasi, pemilih memilih dua kali, pemilihan tidak aktif, kandidat yang bukan bagian pemilihan, dan perhitungan hasil.

## Git: simpan progres belajar

```powershell
git init
git add .
git commit -m "Buat fondasi Digital Voting API"
```

Setelah mengerjakan satu bagian, periksa perubahan dengan `git status` dan `git diff`, lalu buat commit kecil dengan pesan yang menjelaskan perubahan. Remote GitHub dapat ditambahkan kemudian menggunakan `git remote add origin <URL-repository>`.
