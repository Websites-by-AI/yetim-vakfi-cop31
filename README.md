# Yetim Vakfı × COP31 — Open Project 💛🌍

Fundraising tracker + COP31 Green Zone registration site, Telegram bot, and
HuggingFace RAG module for Yetim Vakfı (Orphan Foundation, Istanbul).

## Structure
```
site/            Static website (trackers, reports, Excel) — just open the .html files
telegram-bot/    Trilingual Telegram bot (TR/EN/FA) — needs TELEGRAM_BOT_TOKEN
hf-rag/          Dependency-free Q&A module (works with no token)
```

## Quick start
- **Site:** open `site/yetim-vakfi-fundraising-tracker.html` in any browser (offline OK).
- **Bot:** see `telegram-bot/README.md` (get token from @BotFather).
- **RAG:** `cd hf-rag && python rag.py "What is the sponsorship fee?"`

## Push to GitHub (Websites-by-AI org)
```bash
# 1. Create an EMPTY repo on github.com in the Websites-by-AI org (web UI, no README)
# 2. Then:
git remote add origin https://github.com/Websites-by-AI/REPO-NAME.git
git branch -M main
git push -u origin main
# Use a FRESH token with minimal scope. Never reuse exposed tokens.
```

## 🔐 Security rules
- **Never commit tokens** (`.env` is git-ignored). Tokens live only in environment variables.
- If a token was ever pasted in chat/email, **revoke it immediately** and create a new one.
