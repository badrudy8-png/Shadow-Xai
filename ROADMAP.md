# Roadmap Shadow-Xai

## Milestone 0 — Fondasi (selesai)

- Engine lokal, CLI, tests, konfigurasi, security boundary, memory SQLite, tool registry, RAG lexical, agent loop, API lokal, CI, Docker.

## Milestone 1 — Model dan memory (berikutnya)

- Streaming provider-native dan fallback routing.
- Summarization conversation berbasis token budget.
- Embedding dan vector store pluggable.
- Enkripsi memory dan retention policy.

## Milestone 2 — Tools dan agent

- Tool approval API.
- Python sandbox terisolasi.
- Web search dengan source verification.
- Durable background queue dan progress events.

## Milestone 3 — Product interface

- Auth, user accounts, sessions, WebSocket/SSE, chat UI, file uploads.
- Monitoring, metrics, tracing, dan error tracking.

## Milestone 4 — Training dan multimodal

- Dataset/validation pipeline, LoRA/PEFT, checkpoint registry.
- Image/audio/file adapters dengan permission dan size limits.
- Benchmark dan regression dashboard.

Setiap milestone harus memiliki test, dokumentasi, threat model, dan rollback plan.
