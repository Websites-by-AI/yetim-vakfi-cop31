# Deploy Guide — Bot Token + GitHub Upload + Run 🚀

## Part A — Get Telegram bot token (5 min, free)
1. Open Telegram, search **@BotFather**, press Start.
2. Send `/newbot`, choose a name (e.g. `Yetim Vakfi COP31`) and a username
   (must end in `bot`, e.g. `yetim_cop31_bot`).
3. BotFather replies with a **token** like `123456:ABC-DEF...` — copy it.
4. ⚠️ Keep this token secret. Never post it in chat or in the repo.

## Part B — Upload code to GitHub (no token needed!)
1. Go to **github.com/Websites-by-AI** → **Repositories** → **New**.
2. Name it e.g. `yetim-vakfi-cop31`, set Public or Private, **do NOT add README** → **Create**.
3. On the repo page click **uploading an existing file** (or Add file → Upload files).
4. Download `yetim-vakfi-cop31.zip` from your workspace, **unzip it**,
   then **drag ALL files/folders** (`site/`, `telegram-bot/`, `hf-rag/`, `README.md`…)
   into the GitHub page → **Commit changes**. Done! 🎉

> Alternative (git): `git remote add origin https://github.com/Websites-by-AI/REPO.git`
> then `git push -u origin main` (needs a fresh token — create at
> GitHub → Settings → Developer settings → Personal access tokens).

## Part C — Run the bot (on your computer or a server)
```bash
cd telegram-bot
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="PASTE_TOKEN_HERE"   # Windows: set TELEGRAM_BOT_TOKEN=...
python bot.py
```
Then open your bot in Telegram → `/start`. Keep it running 24/7 with a VPS
(Hetzner/DigitalOcean ~€4/mo) using `nohup python bot.py &` or systemd.

## 🔐 Rules
- Token lives ONLY in `.env` / environment — never in code or chat.
- If a token leaks, revoke it and make a new one.
