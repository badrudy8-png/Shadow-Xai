# Arsitektur Shadow-Xai

## Lapisan utama

Shadow-Xai dipisahkan menjadi beberapa lapisan agar model, memori, alat, dan antarmuka dapat berubah tanpa mengubah kontrak inti.

| Lapisan | Tanggung jawab |
|---|---|
| Interface | CLI, API, atau UI yang menerima permintaan pengguna. |
| Orchestrator | Mengelola konteks, pemilihan provider, batas waktu, dan alur respons. |
| Model adapter | Menyamakan antarmuka berbagai provider model. |
| Memory | Menyimpan konteks dengan retensi dan penghapusan yang dapat dikontrol. |
| Tool registry | Menyediakan alat yang di-allowlist dengan validasi dan audit. |
| Evaluation | Mengukur kualitas, keamanan, regresi, dan kepatuhan kebijakan. |

## Kontrak saat ini

`ChatEngine.respond(message)` adalah batas minimal yang menerima string non-kosong dan mengembalikan `ChatResponse`. Implementasi placeholder sengaja deterministik sehingga proyek dapat diuji sebelum provider model dipilih.

## Prinsip desain

- **Provider-agnostic:** kode inti tidak bergantung pada satu vendor model.
- **Least privilege:** alat hanya mendapat izin yang diperlukan.
- **Human control:** tindakan eksternal berisiko membutuhkan persetujuan pengguna.
- **Observable:** kegagalan, pemanggilan alat, dan keputusan penting dapat diaudit.
- **Testable:** komponen deterministik diuji tanpa jaringan atau kredensial nyata.

## Batas implementasi awal

Versi awal tidak mengirim data ke layanan eksternal, tidak menyimpan riwayat pengguna, tidak mengeksekusi kode, dan tidak melakukan tindakan agen. Semua fitur tersebut memerlukan desain ancaman, konfigurasi eksplisit, serta pengujian tambahan sebelum diaktifkan.
