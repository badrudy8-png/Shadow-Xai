# Shadow-Xai

**Shadow-Xai** adalah fondasi chatbot AI open source yang dirancang untuk percakapan alami, penalaran, adaptasi konteks, penggunaan alat, bantuan pemrograman, analisis informasi, dan perilaku agen yang dapat dikendalikan.

> **Status:** tahap fondasi aktif. Engine lokal sudah dapat dijalankan tanpa API key; adapter model eksternal dan alat agen masih menjadi pekerjaan lanjutan.

## Yang sudah tersedia

- Engine percakapan lokal yang dapat dijalankan langsung.
- Riwayat percakapan in-memory.
- Mode CLI satu pesan dan mode interaktif.
- Perintah `/help`, `/clear`, dan `/exit`.
- Antarmuka provider yang siap dikembangkan.
- Pengujian otomatis dan dokumentasi arsitektur.

## Instalasi

Gunakan Python 3.10 atau yang lebih baru.

```bash
git clone https://github.com/badrudy8-png/Shadow-Xai.git
cd Shadow-Xai
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Menjalankan engine

Kirim satu pesan:

```bash
shadow-xai chat "Halo, Shadow-Xai"
```

Atau jalankan mode interaktif:

```bash
shadow-xai chat
```

Contoh sesi:

```text
Shadow-Xai interactive mode. Ketik /help untuk bantuan.
Anda> Halo
Shadow-Xai> Shadow-Xai masih dalam tahap fondasi. Pesan diterima: Halo
Anda> /clear
Riwayat percakapan dihapus.
Anda> /exit
Sampai jumpa.
```

Engine saat ini bersifat lokal dan deterministik. Tidak ada data yang dikirim ke layanan eksternal dan tidak ada API key yang diperlukan. Respons placeholder akan diganti adapter model nyata pada tahap berikutnya.

## Struktur proyek

```text
.
├── docs/architecture.md
├── src/shadow_xai/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   └── engine.py
├── tests/test_engine.py
├── CONTRIBUTING.md
├── SECURITY.md
├── pyproject.toml
└── README.md
```

## Roadmap

1. Menambahkan adapter provider LLM dengan antarmuka yang konsisten.
2. Menambahkan konfigurasi environment yang tervalidasi.
3. Menambahkan memori persisten dengan kontrol privasi dan penghapusan data.
4. Menambahkan registry alat dengan allowlist, timeout, dan audit log.
5. Menambahkan evaluasi kualitas, keamanan, prompt injection, dan penggunaan alat.
6. Menambahkan antarmuka web atau API setelah kontrak inti stabil.

## Prinsip keamanan

Shadow-Xai tidak boleh mengeksekusi tindakan eksternal secara diam-diam. Integrasi alat harus menggunakan izin minimum, validasi input, timeout, pencatatan audit, dan persetujuan pengguna untuk tindakan yang berdampak. Jangan pernah melakukan commit terhadap API key, token, file `.env`, checkpoint model privat, atau data pengguna.

Lihat [SECURITY.md](SECURITY.md) untuk pelaporan kerentanan dan [docs/architecture.md](docs/architecture.md) untuk batas desain.

## Kontribusi

Baca [CONTRIBUTING.md](CONTRIBUTING.md) sebelum membuka pull request. Perubahan baru sebaiknya disertai pengujian, dokumentasi, dan penjelasan tentang dampak keamanan atau privasi.

## Lisensi

Lisensi proyek belum ditentukan oleh pemilik repositori. Jangan mengasumsikan kode ini bebas digunakan untuk distribusi atau produk komersial sampai file lisensi resmi ditambahkan.

## Tautan

- [Repositori GitHub](https://github.com/badrudy8-png/Shadow-Xai)
- [Dokumentasi arsitektur](docs/architecture.md)
- [Panduan kontribusi](CONTRIBUTING.md)
- [Kebijakan keamanan](SECURITY.md)
