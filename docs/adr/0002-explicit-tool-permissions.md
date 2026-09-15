# ADR 0002: Explicit tool permissions

- Status: accepted
- Date: 2026-09-15

## Context

Agent yang dapat menjalankan tool memiliki risiko kebocoran data dan perubahan eksternal tanpa sengaja.

## Decision

Tool harus terdaftar, di-allowlist, memiliki timeout, dicatat dalam audit, dan tidak aktif secara default jika berdampak eksternal. Tindakan berisiko membutuhkan approval layer.

## Consequences

Integrasi menjadi sedikit lebih verbose, tetapi perilaku dapat diaudit dan diuji. Web search, code execution, dan file mutation tidak boleh ditambahkan sebagai shortcut tanpa sandbox dan permission model.
