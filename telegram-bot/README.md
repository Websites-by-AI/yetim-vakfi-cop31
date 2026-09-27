# Yetim Vakfı × COP31 Telegram Bot 🤖

Trilingual (TR/EN/FA) info bot: campaigns, donations, sponsorship (900 TL/mo),
COP31 Green Zone info, Startup Zone rules, FAQ, contact + `/ask` (local RAG).

## 1. Get a bot token (2 min)
1. Open Telegram → talk to **@BotFather** → `/newbot` → name it.
2. Copy the token (looks like `123456:ABC-DEF...`).
3. ⚠️ **Never share this token in chat or commit it to git.**

## 2. Run
```bash
cd telegram-bot
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"   # Windows: set TELEGRAM_BOT_TOKEN=...
python bot.py
```
Open your bot in Telegram → `/start`.

## 3. /ask (RAG)
Works offline with zero setup using `../hf-rag/knowledge.json`.
For generative answers, also set `HF_TOKEN` (needs `huggingface_hub`).

## Deploy (VPS, simple)
```bash
nohup python bot.py > bot.log 2>&1 &
# or use systemd / docker for production
```
