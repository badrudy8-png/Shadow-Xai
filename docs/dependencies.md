# Dependency Management

Shadow-Xai meminimalkan dependency runtime dan menggunakan standard library untuk core, API, memory, dan tools dasar. Dependency development saat ini hanya `pytest`.

## Aturan

- Pin atau batasi versi dengan lower bound yang jelas.
- Tinjau changelog dan advisory sebelum upgrade.
- Jalankan test dan compile check setelah perubahan.
- Jangan menambahkan dependency hanya untuk fitur yang dapat ditulis dengan standard library.
- Gunakan lockfile atau SBOM saat deployment produksi.
- Audit dependency transitive sebelum mengaktifkan provider/model eksternal.

CI menjalankan matrix Python dan dapat diperluas dengan lint, type checking, coverage, serta dependency vulnerability scan.
