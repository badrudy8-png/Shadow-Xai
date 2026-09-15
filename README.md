# Shadow-Xai

**Shadow-Xai** adalah fondasi chatbot AI open source yang dirancang untuk percakapan alami, penalaran, adaptasi konteks, penggunaan alat, bantuan pemrograman, analisis informasi, dan perilaku agen yang dapat dikendalikan.

> **Status:** tahap fondasi awal. Implementasi model, provider, memori, dan alat eksternal belum diaktifkan secara default.

## Tujuan

Proyek ini bertujuan menyediakan struktur yang jelas untuk membangun asisten AI yang modular, dapat diuji, aman, dan mudah dikembangkan. Kemampuan seperti belajar mandiri, penggunaan alat, dan tindakan agen harus selalu dilengkapi batasan keamanan, audit, dan persetujuan yang sesuai.

## Yang sudah tersedia

- Struktur paket Python minimal.
- Antarmuka `ChatEngine` yang dapat dikembangkan untuk provider model.
- CLI lokal untuk memeriksa instalasi dan menjalankan respons placeholder.
- Konfigurasi proyek melalui `pyproject.toml`.
- Pengujian dasar dengan `pytest`.
- Dokumentasi arsitektur dan panduan kontribusi.

## Instalasi untuk pengembangan

Gunakan Python 3.10 atau yang lebih baru.

```bash
git clone https://github.com/badrudy8-png/Shadow-Xai.git
cd Shadow-Xai
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Penggunaan saat ini

CLI berikut memverifikasi bahwa fondasi proyek terpasang:

```bash
shadow-xai --help
shadow-xai --version
shadow-xai chat "Halo, Shadow-Xai"
```

Pada tahap ini, perintah `chat` mengembalikan respons placeholder. Integrasi model nyata akan ditambahkan melalui adapter provider, bukan dengan menaruh API key di source code.

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
3. Menambahkan memori percakapan dengan kontrol privasi dan penghapusan data.
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
