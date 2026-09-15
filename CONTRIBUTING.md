# Panduan Kontribusi

Terima kasih telah berkontribusi pada Shadow-Xai. Proyek ini masih berada pada tahap fondasi, sehingga diskusi desain dan dokumentasi sama pentingnya dengan kode.

## Alur perubahan

1. Buka issue untuk perubahan arsitektur atau fitur besar.
2. Buat branch pendek dari `main`.
3. Tambahkan implementasi, pengujian, dan dokumentasi yang relevan.
4. Jalankan `python -m pytest` dan `python -m compileall src`.
5. Buat pull request dengan ringkasan, pengujian, serta dampak keamanan dan privasi.

## Standar kontribusi

Jangan menyertakan token, API key, data pribadi, prompt privat, atau checkpoint model berukuran besar. Perubahan terhadap alat atau tindakan agen harus menjelaskan permission, validasi input, timeout, logging, dan mekanisme persetujuan pengguna.

## Commit

Gunakan pesan commit yang singkat dan deskriptif, misalnya `feat: add provider adapter` atau `docs: explain tool safety`.
