# ADR 0001: Provider-neutral core

- Status: accepted
- Date: 2026-09-15

## Context

Shadow-Xai perlu mendukung provider lokal dan API eksternal tanpa mengikat engine inti pada satu vendor.

## Decision

Engine menggunakan kontrak `LLMAdapter` dengan implementasi echo lokal, local-command, dan OpenAI-compatible. Provider eksternal opt-in melalui environment.

## Consequences

Pengujian dapat berjalan tanpa jaringan atau secret. Streaming, fallback, dan provider-specific reasoning tetap menjadi extension point yang harus mematuhi kontrak yang sama.
