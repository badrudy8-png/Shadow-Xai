# Shadow-Xai

**Shadow-Xai** adalah fondasi chatbot AI open source modular untuk percakapan natural, reasoning, memory, tools, knowledge retrieval, dan agent orchestration yang aman.

> **Status:** fondasi aktif versi `0.2.0`. Engine lokal dapat dijalankan tanpa API key. Adapter model eksternal bersifat opt-in.

## Fitur yang sudah berjalan

- **LLM:** adapter echo lokal, OpenAI-compatible gateway, local-command adapter, model selection, quality profile, reasoning per keluarga model, retry, fallback, metadata penggunaan, dan system prompt profesional.
- **Memory:** SQLite persistence, recent retrieval, search, export, dan penghapusan data pengguna.
- **Tools:** registry, calculator berbasis AST, allowlist, timeout, dan audit log.
- **Knowledge/RAG:** document ingestion teks, chunking, lexical retrieval, dan source tracking.
- **Agent:** planning dasar, bounded multi-step loop, retry, state hasil, dan completion flag.
- **Security:** batas input/output, validasi, redaction secret, dan permission tools.
- **Evaluation:** evaluation case sederhana dan regression test suite.
- **API:** HTTP JSON lokal dengan `/health` dan `POST /chat`.
- **Infrastructure:** GitHub Actions CI, Python compile checks, pytest, Dockerfile, dan `.env.example`.
- **Project management:** issue templates, pull request template, roadmap, ADR, changelog, milestone plan, MIT license, dan dependency policy.
- **Advanced AI foundations:** summarizer, fact-check hook, intelligent routing, parallel tool executor, background job registry, knowledge graph, serta multimodal/file fingerprint gateway.

Lihat [status fitur lengkap](docs/feature-status.md) untuk membedakan implementasi aktif dan pekerjaan lanjutan.

## Instalasi dan penggunaan

```bash
git clone https://github.com/badrudy8-png/Shadow-Xai.git
cd Shadow-Xai
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
shadow-xai chat "Halo Shadow-Xai"
```

Mode interaktif:

```bash
shadow-xai chat
```

API lokal:

```bash
shadow-xai serve
curl http://127.0.0.1:8080/health
curl -X POST http://127.0.0.1:8080/chat \\
  -H 'Content-Type: application/json' \\
  -d '{"message":"Halo"}'
```

Konfigurasi publik:

```bash
shadow-xai config
```

## Provider model eksternal

Default tidak membutuhkan jaringan. Untuk endpoint OpenAI-compatible, salin `.env.example`, lalu set environment berikut tanpa memasukkan secret ke git:

```bash
export SHADOW_MODEL_PROVIDER=openai-compatible
export SHADOW_MODEL_BASE_URL=https://provider.example/v1
export SHADOW_MODEL_API_KEY='isi-di-environment-saja'
export SHADOW_MODEL_NAME=gpt-5
export SHADOW_QUALITY_PROFILE=balanced
export SHADOW_REASONING_EFFORT=medium
export SHADOW_MAX_OUTPUT_TOKENS=1800
export SHADOW_MODEL_RETRIES=2
shadow-xai chat "Jelaskan trade-off arsitektur ini secara profesional dan berikan rekomendasi."
```

Untuk respons yang lebih natural, gunakan model yang lebih kuat pada gateway Anda, `SHADOW_QUALITY_PROFILE=quality` atau `reasoning`, system prompt bawaan yang menjaga konteks dan ketidakpastian, serta riwayat yang cukup melalui `SHADOW_MAX_HISTORY_MESSAGES`. Shadow-Xai tidak mengklaim kesetaraan persis dengan GPT-4.5; kualitas ditentukan oleh model provider, konteks, prompt, dan evaluasi aplikasi. Lihat [panduan integrasi LLM](docs/llm.md) untuk parameter token, reasoning GPT/Claude/Gemini, retry, fallback, dan praktik keamanan.

## Pengembangan

```bash
python -m pytest -q
python -m compileall -q src
```

Struktur utama:

```text
src/shadow_xai/
├── engine.py       # orkestrasi percakapan
├── llm.py          # transport, model routing, reasoning, retry, fallback
├── memory.py       # SQLite memory
├── tools.py        # tool registry dan calculator
├── rag.py          # knowledge retrieval
├── agent.py        # agent loop
├── security.py     # policy dan validasi
├── evaluation.py   # evaluasi deterministik
└── api.py          # HTTP API
```

## Keamanan

Tool eksternal, eksekusi kode, web search, dan tindakan yang mengubah sistem **tidak aktif secara default**. Implementasi lanjutan wajib memakai sandbox, allowlist, timeout, audit, secret manager, dan persetujuan pengguna. Jangan commit API key, token, file `.env`, data privat, atau checkpoint model.

Baca [SECURITY.md](SECURITY.md), [arsitektur](docs/architecture.md), dan [status fitur](docs/feature-status.md).

## Project management

Permintaan bug dan fitur menggunakan template di `.github/ISSUE_TEMPLATE/`. Pull request mengikuti `.github/pull_request_template.md`. Arah pengembangan ada di [ROADMAP.md](ROADMAP.md), keputusan arsitektur di [docs/adr](docs/adr/), dan perubahan versi di [CHANGELOG.md](CHANGELOG.md). Kebijakan dependency tersedia di [docs/dependencies.md](docs/dependencies.md).

## Roadmap berikutnya

- Streaming native dan fallback provider.
- Embedding/vector database serta parser PDF/Office.
- WebSocket, autentikasi, session management, dan UI.
- Prompt-injection/security evaluation yang lebih kuat.
- Lint, type checking, coverage, monitoring, dan release automation.
- Dataset pipeline, LoRA/PEFT, checkpoint management, dan model evaluation.

Advanced AI yang aktif saat ini bersifat lokal dan deterministic. Riset otonom, automatic tool/model selection berbasis model, multimodal decoding, voice output, dan background jobs durable membutuhkan provider atau queue produksi yang belum diaktifkan.

## Lisensi

Proyek ini menggunakan [MIT License](LICENSE).
