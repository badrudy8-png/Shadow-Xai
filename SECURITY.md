# Kebijakan Keamanan

## Pelaporan

Jangan membuka kerentanan keamanan yang belum diperbaiki sebagai issue publik. Untuk saat ini, hubungi pemilik repositori melalui kanal privat GitHub dan sertakan langkah reproduksi minimal, dampak, versi yang terdampak, serta bukti konsep yang tidak merusak data.

## Ruang lingkup perhatian

Laporkan kebocoran kredensial, bypass permission alat, eksekusi kode tanpa persetujuan, prompt injection yang mengubah tindakan eksternal, paparan data pengguna, dan masalah yang dapat menyebabkan model bertindak di luar batas yang dikonfigurasi.

## Praktik pengembangan

Kredensial harus disimpan di environment atau secret manager, bukan di source code. Integrasi jaringan harus memiliki timeout dan validasi. Tindakan yang mengubah data, mengirim pesan, atau memengaruhi sistem eksternal harus dapat diaudit dan membutuhkan persetujuan sesuai tingkat risikonya.
