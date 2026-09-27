# HF RAG module (Yetim Vakfı × COP31) 📚

Lightweight Q&A over verified facts. **No downloads, no token needed** for retrieval.

## Use
```bash
cd hf-rag
python rag.py "What is the sponsorship fee?"
python rag.py "sponsorluk ücreti ne kadar?" --lang tr
python rag.py "هزینه حمایت چقدر است؟" --lang fa
```

## How it works
- `knowledge.json` — 16 verified facts (EN/TR/FA)
- `rag.py` — pure-Python TF-IDF + cosine retrieval; `ask(q, lang)` returns best answer
- Optional: set `HF_TOKEN` + `pip install huggingface_hub` for generative answers (`--generate`)

## Telegram bot
`../telegram-bot/bot.py` imports this module for the `/ask` command automatically.
