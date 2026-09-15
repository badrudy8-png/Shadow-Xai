# Status Fitur

Implementasi ini menyediakan fondasi yang dapat dijalankan tanpa API key. Status berikut membedakan fitur yang sudah aktif dari extension point yang belum mengklaim implementasi penuh.

| Area | Sudah aktif | Extension point / pekerjaan lanjutan |
|---|---|---|
| LLM | Echo lokal, OpenAI-compatible adapter, local command adapter, model config | model selection cerdas, fallback, reasoning/verifier, token streaming provider-native |
| Memory | SQLite persistence, recent/search, export, deletion | summarization berbasis token, embeddings, multi-user encryption |
| Tools | registry, calculator, allowlist, timeout, audit | web search, Python sandbox, file/data tools, approval UI |
| RAG | ingestion, chunking, lexical retrieval, source citations | parser format, embeddings, vector DB, RAG benchmark |
| Agent | plan, bounded loop, retries, completion result | planner berbasis model, subtask queue, durable state |
| Advanced AI | summarizer, lexical fact checker, intelligent router, parallel executor, in-process jobs, knowledge graph, multimodal file fingerprint boundary | trusted fact checker, durable queue, real image/audio decoding, voice synthesis, codebase indexer |
| Behavior | system prompt, personality setting, instruction boundary | policy compiler dan persona profiles |
| Security | input/output limits, secret redaction, tool permission | prompt injection classifier, secret manager, formal security eval |
| Evaluation | case scoring dan regression tests | hallucination judge, benchmark corpus, quality dashboards |
| API | local JSON HTTP `/health` dan `POST /chat` | WebSocket/streaming, auth, accounts, sessions, multi-user isolation |
| Project management | issue templates, PR template, roadmap, ADR, changelog, milestones, MIT license, dependency policy | release automation dan governance review |
| Infrastructure | GitHub Actions, pytest, compile check, Docker | lint/type/coverage gates, monitoring |
| Training | dokumentasi extension point saja | dataset pipeline, training/fine-tuning, LoRA/PEFT, checkpoint conversion |

Fitur eksternal yang membutuhkan kredensial atau infrastruktur tidak diaktifkan secara default. Ini disengaja untuk mencegah kebocoran secret, eksekusi kode berbahaya, dan pengiriman data tanpa persetujuan.
