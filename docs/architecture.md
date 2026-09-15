# Arsitektur Shadow-Xai

## Lapisan utama

| Lapisan | Modul | Tanggung jawab |
|---|---|---|
| Interface | `cli.py`, `api.py` | CLI interaktif dan JSON HTTP lokal. |
| Orchestrator | `engine.py`, `agent.py` | Konteks, planning terbatas, retry, dan verifikasi hasil. |
| Model adapter | `llm.py` | Echo lokal, command model, dan endpoint OpenAI-compatible. |
| Memory | `memory.py` | SQLite persistence, retrieval, export, dan deletion. |
| Knowledge | `rag.py` | Ingestion, chunking, lexical retrieval, dan source tracking. |
| Tools | `tools.py` | Registry allowlist, timeout, kalkulator aman, dan audit. |
| Safety | `security.py` | Batas input/output, validasi, dan redaction secret. |
| Quality | `evaluation.py`, `tests/` | Case-based evaluation dan regression checks. |

## Jalur percakapan

1. Input divalidasi oleh `SecurityPolicy`.
2. Pesan disimpan di history lokal dan, jika diaktifkan, `MemoryStore`.
3. Konteks RAG yang relevan dapat disisipkan dengan source marker.
4. `LLMAdapter` menghasilkan respons; default-nya tidak menggunakan jaringan.
5. Output divalidasi dan dicatat kembali ke history/memory.

## Batas keamanan

Tidak ada tool eksternal yang aktif secara default. Calculator menggunakan AST allowlist, bukan `eval`. API hanya bind ke localhost jika dijalankan tanpa flag host. API key hanya dibaca dari environment dan tidak pernah ditampilkan oleh `config` command.
