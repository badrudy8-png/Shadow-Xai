# Changelog

Semua perubahan penting dicatat di sini.

## [0.3.0] - 2026-09-15

### Added

- Quality profile `fast`, `balanced`, `quality`, dan `reasoning` dengan model selection yang dapat dioverride.
- Parameter reasoning family-aware untuk model GPT, Claude, dan Gemini pada gateway OpenAI-compatible.
- Retry terbatas dengan exponential backoff, response metadata, validasi payload, dan fallback provider yang eksplisit.
- System prompt profesional untuk respons natural, terstruktur, jujur, aman, dan tanpa chain-of-thought internal.
- Dokumentasi integrasi lengkap di `docs/llm.md` serta 17 regression tests.

## [0.2.0] - 2026-09-15

### Added

- Engine lokal dan CLI interaktif.
- LLM adapter abstraction.
- SQLite memory, tool registry, safe calculator, lexical RAG, agent loop.
- Security policy, evaluation helpers, local HTTP API, CI, dan Docker.
- Issue template, PR template, roadmap, ADR, serta feature status.

## [0.1.0] - 2026-09-15

### Added

- Struktur paket awal dan kontrak `ChatEngine`.
