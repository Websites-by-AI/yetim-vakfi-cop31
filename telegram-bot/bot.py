#!/usr/bin/env python3
"""
Yetim Vakfi x COP31 Telegram Bot (TR / EN / FA)

Features: campaigns, donate links, sponsorship info (900 TL/mo),
COP31 Green Zone info, Startup Zone rules, FAQ, contact, and /ask (local RAG).

Token is read ONLY from the TELEGRAM_BOT_TOKEN environment variable.
Never hard-code tokens in this file.

Run:
    export TELEGRAM_BOT_TOKEN="123456:ABC..."   # from @BotFather
    pip install -r requirements.txt
    python bot.py
"""
import os
import sys
from pathlib import Path

# Optional local RAG module (../hf-rag/rag.py) - works without any token.
RAG_DIR = Path(__file__).resolve().parent.parent / "hf-rag"
sys.path.insert(0, str(RAG_DIR))
try:
    import rag as local_rag
    HAS_RAG = True
except Exception:
    local_rag = None
    HAS_RAG = False

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(2)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not TOKEN or TOKEN == "PUT_YOUR_TOKEN_HERE":
    print("ERROR: TELEGRAM_BOT_TOKEN is not set.")
    print("Get a token from @BotFather, then run:")
    print('  export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"')
    print("  python bot.py")
    sys.exit(1)

# ---------------- Links (verified) ----------------
DONATE = "https://bagis.yetimvakfi.org.tr/en/donate"
SITE = "https://yetimvakfi.org.tr/en"
SPONSOR = "https://yetimvakfi.org.tr/en/yetim-sponsorluk"
APPLE = "https://apps.apple.com/app/yetim-vakf%C4%B1/id6745053470"
PLAY = "https://play.google.com/store/apps/details?id=tr.org.yetimvakfi"
CONTACT_PAGE = "https://yetimvakfi.org.tr/iletisim"
MAPS = "https://maps.app.goo.gl/G7xEt7ZmWxuf5hQf9"
GZ = "https://cop31.tr/green-zone"
GZ_VISIT = "https://cop31.tr/register-to-visit"
STARTUP = "https://startupzone.cop31.center/"
UNFCCC = "https://unfccc.int/cop31"

# ---------------- Texts (TR / EN / FA) ----------------
T = {
"tr": {
 "welcome": "🧸 Yetim Vakfı × 🌍 COP31 botuna hoş geldiniz!\nNe yapmak istersiniz?",
 "campaigns": "💛 Kampanyalar", "donate": "🤲 Bağış", "sponsor": "🧸 Sponsorluk",
 "cop31": "🌍 COP31 Yeşil Alan", "startup": "🚀 Startup Kuralları", "faq": "❓ SSS",
 "contact": "📞 İletişim", "lang": "🌐 Dil / Language / زبان", "back": "⬅️ Geri",
 "b_campaigns": "💛 8 Kampanya:\n🧸 Yetim Sponsorluğu (aylık 900 ₺)\n🍲 Gazze Sıcak Yemek\n🎒 İyilik Çantası – Kırtasiye (1.500 ₺/set)\n🐑 Adak–Akika–Şükür Kurbanı\n🤲 Zekât & Sadaka\n🏠 Yetimhane & Yerleşkeler\n🧺 Gıda Paketi\n🎓 Eğitim & Burs\n\nBağış: " + DONATE,
 "b_donate": "🤲 Bağış Yolları:\n🌐 Online: " + DONATE + "\n🍎 App Store: " + APPLE + "\n📱 Google Play: " + PLAY + "\n📲 SMS: EĞİTİM yazıp 9868'e gönderin (50 ₺, kırtasiye)",
 "b_sponsor": "🧸 Yetim Sponsorluğu:\n• Ayda 900 ₺, yılda 10.800 ₺\n• 21 ülkede 26.490 yetim (Eyl 2026)\n• En az 1 yıl sponsorluk\n\nBaşvuru: " + SPONSOR,
 "b_cop31": "🌍 COP31 Green Zone:\n📅 9–20 Kasım 2026 (11–12: Liderler Zirvesi)\n📍 Antalya EXPO Center, Aksu–Antalya\n🎟️ Ücretsiz + QR ile giriş\n\n🔗 Ziyaret kaydı: " + GZ_VISIT + "\n🔗 Green Zone: " + GZ + "\n🔗 UNFCCC: " + UNFCCC + "\n\nNGO'lar için doğru yol: Climate Supporter (greenzone@cop31.tr)",
 "b_startup": "🚀 Startup Zone Kuralları:\n✅ Sadece iklim startup'ları (şirket)\n✅ Desk stand: 0–3 yaş şirketler\n✅ Exhibitor (masa/5/15 m²) veya Sponsor\n📝 Sonuç: startup@cop31.tr\n❌ NGO'lar giremez → Climate Supporter yolunu kullanın\n\n🔗 " + STARTUP,
 "b_faq": "❓ SSS:\n• Yetim Vakfı nerede? → Fatih/İstanbul (iletişim menüsü)\n• Sponsorluk ne kadar? → Ayda 900 ₺\n• COP31'e nasıl katılırım? → cop31.tr/register-to-visit\n• Startup mıyız? → Hayır; NGO'lar Climate Supporter'a başvurur",
 "b_contact": "📞 İletişim:\n☎️ 0212 970 60 60\n✉️ info@yetimvakfi.org.tr\n📍 Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/İstanbul\n🗺️ " + MAPS + "\n🌐 " + CONTACT_PAGE,
 "ask_hint": "Kullanım: /ask sorunuz (örn: /ask sponsorluk ücreti ne kadar?)",
 "ask_no": "Bu konuda emin bir cevabım yok. İletişim: 0212 970 60 60",
},
"en": {
 "welcome": "🧸 Yetim Vakfı × 🌍 COP31 bot — welcome!\nWhat would you like to do?",
 "campaigns": "💛 Campaigns", "donate": "🤲 Donate", "sponsor": "🧸 Sponsorship",
 "cop31": "🌍 COP31 Green Zone", "startup": "🚀 Startup Rules", "faq": "❓ FAQ",
 "contact": "📞 Contact", "lang": "🌐 Dil / Language / زبان", "back": "⬅️ Back",
 "b_campaigns": "💛 8 Campaigns:\n🧸 Orphan Sponsorship (900 ₺/mo)\n🍲 Gaza Hot Meals\n🎒 School Bag – Stationery (1,500 ₺/set)\n🐑 Vow–Aqiqah–Thanksgiving Qurbani\n🤲 Zakat & Sadaqah\n🏠 Orphanages & Settlements\n🧺 Food Parcel\n🎓 Education & Scholarship\n\nDonate: " + DONATE,
 "b_donate": "🤲 Ways to donate:\n🌐 Online: " + DONATE + "\n🍎 App Store: " + APPLE + "\n📱 Google Play: " + PLAY + "\n📲 SMS: text EĞİTİM to 9868 (50 ₺, stationery)",
 "b_sponsor": "🧸 Orphan Sponsorship:\n• 900 ₺/month, 10,800 ₺/year\n• 26,490 orphans in 21 countries (Sep 2026)\n• Minimum 1 year\n\nApply: " + SPONSOR,
 "b_cop31": "🌍 COP31 Green Zone:\n📅 9–20 Nov 2026 (11–12: Leaders Summit)\n📍 Antalya EXPO Center, Aksu–Antalya\n🎟️ Free entry with QR\n\n🔗 Visit registration: " + GZ_VISIT + "\n🔗 Green Zone: " + GZ + "\n🔗 UNFCCC: " + UNFCCC + "\n\nRight lane for NGOs: Climate Supporter (greenzone@cop31.tr)",
 "b_startup": "🚀 Startup Zone Rules:\n✅ Climate startups (companies) only\n✅ Desk stand: companies 0–3 years old\n✅ Exhibitor (desk/5/15 m²) or Sponsor\n📝 Decisions via: startup@cop31.tr\n❌ NGOs cannot enter → use Climate Supporter lane\n\n🔗 " + STARTUP,
 "b_faq": "❓ FAQ:\n• Where is Yetim Vakfı? → Fatih/Istanbul (contact menu)\n• Sponsorship fee? → 900 ₺/month\n• How to join COP31? → cop31.tr/register-to-visit\n• Are we a startup? → No; NGOs apply as Climate Supporter",
 "b_contact": "📞 Contact:\n☎️ +90 212 970 60 60\n✉️ info@yetimvakfi.org.tr\n📍 Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/Istanbul\n🗺️ " + MAPS + "\n🌐 " + CONTACT_PAGE,
 "ask_hint": "Usage: /ask your question (e.g. /ask what is the sponsorship fee?)",
 "ask_no": "I have no confident answer. Contact: +90 212 970 60 60",
},
"fa": {
 "welcome": "🧸 به ربات یتیم‌وکفی × COP31 🌍 خوش آمدید!\nچه کاری می‌خواهید بکنید؟",
 "campaigns": "💛 کمپین‌ها", "donate": "🤲 کمک مالی", "sponsor": "🧸 حمایت از یتیم",
 "cop31": "🌍 گرین‌زون COP31", "startup": "🚀 قوانین استارتاپ", "faq": "❓ سؤالات",
 "contact": "📞 تماس", "lang": "🌐 Dil / Language / زبان", "back": "⬅️ بازگشت",
 "b_campaigns": "💛 ۸ کمپین:\n🧸 حمایت از یتیم (ماهانه ۹۰۰ لیر)\n🍲 غذای گرم غزه\n🎒 کیف مهربانی – لوازم‌التحریر (۱۵۰۰ لیر)\n🐑 قربانی نذر/عقیقه/شکر\n🤲 زکات و صدقه\n🏠 یتیم‌خانه‌ها\n🧺 بسته غذایی\n🎓 آموزش و بورسیه\n\nکمک: " + DONATE,
 "b_donate": "🤲 راه‌های کمک:\n🌐 آنلاین: " + DONATE + "\n🍎 اپ‌استور: " + APPLE + "\n📱 گوگل‌پلی: " + PLAY + "\n📲 پیامک: EĞİTİM به 9868 (۵۰ لیر، لوازم‌التحریر)",
 "b_sponsor": "🧸 حمایت از یتیم:\n• ماهانه ۹۰۰ لیر، سالانه ۱۰٬۸۰۰ لیر\n• ۲۶٬۴۹۰ یتیم در ۲۱ کشور\n• حداقل ۱ سال\n\nثبت: " + SPONSOR,
 "b_cop31": "🌍 گرین‌زون COP31:\n📅 ۹ تا ۲۰ نوامبر ۲۰۲۶ (۱۱–۱۲: اجلاس رهبران)\n📍 آنتالیا EXPO Center\n🎟️ ورود رایگان با QR\n\n🔗 ثبت بازدید: " + GZ_VISIT + "\n🔗 گرین‌زون: " + GZ + "\n🔗 UNFCCC: " + UNFCCC + "\n\nمسیر درست NGOها: Climate Supporter",
 "b_startup": "🚀 قوانین Startup Zone:\n✅ فقط استارتاپ‌های اقلیمی (شرکت)\n✅ میز: شرکت ۰ تا ۳ ساله\n✅ غرفه‌دار یا حامی\n📝 نتیجه: startup@cop31.tr\n❌ NGO پذیرفته نمی‌شود → مسیر Climate Supporter\n\n🔗 " + STARTUP,
 "b_faq": "❓ سؤالات:\n• یتیم‌وکفی کجاست؟ → فاتح/استانبول (منوی تماس)\n• هزینه حمایت؟ → ماهانه ۹۰۰ لیر\n• شرکت در COP31؟ → cop31.tr/register-to-visit\n• آیا استارتاپیم؟ → نه؛ NGOها Climate Supporter می‌شوند",
 "b_contact": "📞 تماس:\n☎️ 0212 970 60 60\n✉️ info@yetimvakfi.org.tr\n📍 Dervişali, Kariye Cami Sk. No:6, Fatih/İstanbul\n🗺️ " + MAPS,
 "ask_hint": "روش استفاده: /ask سؤال شما (مثلاً: /ask هزینه حمایت چقدر است؟)",
 "ask_no": "جواب مطمئنی ندارم. تماس: 0212 970 60 60",
},
}
user_lang = {}

def menu_kb(lg):
    s = T[lg]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["campaigns"], callback_data="m:campaigns"),
         InlineKeyboardButton(s["donate"], callback_data="m:donate")],
        [InlineKeyboardButton(s["sponsor"], callback_data="m:sponsor"),
         InlineKeyboardButton(s["cop31"], callback_data="m:cop31")],
        [InlineKeyboardButton(s["startup"], callback_data="m:startup"),
         InlineKeyboardButton(s["faq"], callback_data="m:faq")],
        [InlineKeyboardButton(s["contact"], callback_data="m:contact"),
         InlineKeyboardButton(s["lang"], callback_data="m:lang")],
    ])

def lang_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang:tr"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang:fa"),
    ]])

def back_kb(lg):
    return InlineKeyboardMarkup([[InlineKeyboardButton(T[lg]["back"], callback_data="m:menu")]])

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_lang[update.effective_user.id] = "en"
    await update.message.reply_text("🌐 Choose language / Dil seç / زبان:", reply_markup=lang_kb())

async def ask_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = user_lang.get(update.effective_user.id, "en")
    q = " ".join(ctx.args).strip()
    if not q:
        await update.message.reply_text(T[lg]["ask_hint"])
        return
    if not HAS_RAG:
        await update.message.reply_text(T[lg]["ask_no"])
        return
    try:
        res = local_rag.ask(q)
    except Exception:
        await update.message.reply_text(T[lg]["ask_no"])
        return
    if res.get("score", 0) < 0.12:
        await update.message.reply_text(T[lg]["ask_no"])
    else:
        await update.message.reply_text(f"💡 {res['answer']}\n\n📌 {res.get('title','')}")

async def on_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = update.effective_user.id
    lg = user_lang.get(uid, "en")
    data = q.data
    if data.startswith("lang:"):
        lg = data.split(":")[1]
        user_lang[uid] = lg
        await q.edit_message_text(T[lg]["welcome"], reply_markup=menu_kb(lg))
    elif data == "m:menu":
        await q.edit_message_text(T[lg]["welcome"], reply_markup=menu_kb(lg))
    elif data == "m:lang":
        await q.edit_message_text("🌐 Choose language / Dil seç / زبان:", reply_markup=lang_kb())
    elif data.startswith("m:"):
        key = "b_" + data.split(":")[1]
        await q.edit_message_text(T[lg].get(key, "..."), reply_markup=back_kb(lg),
                                  disable_web_page_preview=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask_cmd))
    app.add_handler(CallbackQueryHandler(on_button))
    print("Bot is running. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
