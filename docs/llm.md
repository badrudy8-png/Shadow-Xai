# LLM Integration Guide

## Tujuan desain

Modul LLM Shadow-Xai memisahkan orkestrasi percakapan dari transport provider. Mode `echo` tetap menjadi default agar instalasi baru dapat dijalankan tanpa jaringan, API key, atau biaya. Ketika provider eksternal diaktifkan, engine memakai adapter OpenAI-compatible yang sama untuk gateway komersial, proxy internal, dan server model lokal.

Shadow-Xai tidak menjanjikan kesetaraan persis dengan model tertentu seperti GPT-4.5. Kualitas akhir dipengaruhi oleh model yang tersedia, system prompt, konteks, retrieval, parameter reasoning, batas output, dan kualitas instruksi pengguna. Profil `quality` dan `reasoning` dirancang untuk mengarahkan konfigurasi ke model yang lebih kuat, tetapi benchmark aplikasi tetap diperlukan.

## Konfigurasi kualitas

| Profil | Tujuan | Contoh model default pada katalog saat ini |
|---|---|---|
| `fast` | Latensi dan biaya rendah | `gpt-5-mini` |
| `balanced` | Kualitas umum, coding, dan analisis | `gpt-5` |
| `quality` | Generasi dan reasoning yang lebih kuat | `gpt-5.5` |
| `reasoning` | Masalah multi-langkah dan analisis mendalam | `claude-opus-4-7` |

Model ID hanya contoh. Provider atau gateway adalah sumber kebenaran; gunakan `SHADOW_MODEL_NAME` untuk memaksa model tertentu. Jangan menyimpan API key dalam repository.

## Provider OpenAI-compatible

```bash
export SHADOW_MODEL_PROVIDER=openai-compatible
export SHADOW_MODEL_BASE_URL=https://api.openai.com/v1
export SHADOW_MODEL_API_KEY='secret-di-environment'
export SHADOW_MODEL_NAME=gpt-5
export SHADOW_QUALITY_PROFILE=quality
export SHADOW_REASONING_EFFORT=high
export SHADOW_MAX_OUTPUT_TOKENS=2400
export SHADOW_MODEL_RETRIES=2
shadow-xai chat "Analisis trade-off arsitektur event-driven untuk aplikasi multi-tenant."
```

Adapter membentuk parameter sesuai keluarga model. GPT memakai `max_completion_tokens` dan `reasoning`; Claude memakai `max_tokens` yang lebih besar daripada budget thinking; Gemini memakai `max_tokens` dan tidak menggunakan `max_completion_tokens`. Perbedaan ini mencegah respons kosong atau terpotong karena kontrak token yang salah.

## Respons natural dan profesional

`Settings.system_prompt` bawaan mengarahkan model untuk memahami intent, menjawab dalam bahasa pengguna, menyatakan asumsi, membedakan fakta dan ketidakpastian, memakai struktur yang mudah dipindai, serta tidak menampilkan chain-of-thought internal. Engine menyimpan hingga `SHADOW_MAX_HISTORY_MESSAGES` pesan terakhir dan dapat menyisipkan konteks RAG yang memiliki sumber.

Pedoman kualitas yang disarankan:

1. Mulai dengan jawaban atau keputusan utama.
2. Jelaskan alasan yang dapat diverifikasi, bukan proses berpikir internal.
3. Gunakan contoh konkret, batasan, dan langkah verifikasi.
4. Saat permintaan ambigu, ajukan satu pertanyaan klarifikasi yang paling menentukan.
5. Jangan mengklaim browsing, eksekusi tool, atau tindakan eksternal tanpa bukti.

## Retry dan fallback

Transport melakukan retry terbatas dengan exponential backoff untuk error jaringan atau provider. Jika provider utama tetap gagal dan `SHADOW_FALLBACK_PROVIDER` berbeda, engine beralih ke fallback dan menandai `ChatResponse.used_fallback=True`. Default fallback adalah `echo`, sehingga kegagalan jaringan tidak membuat aplikasi diam-diam mengarang jawaban.

## Contoh API Python

```python
from shadow_xai import ChatEngine
from shadow_xai.config import Settings

settings = Settings.from_env()
engine = ChatEngine(settings=settings)
response = engine.respond("Buat rencana migrasi database yang aman.")
print(response.text)
print(response.model, response.provider, response.used_fallback)
```

## Verifikasi

```bash
python -m pytest -q
python -m compileall -q src
shadow-xai config
```

Gunakan test provider palsu untuk regression test payload dan response parsing. Smoke test provider nyata harus dijalankan secara manual dengan API key yang tidak pernah dicommit.
