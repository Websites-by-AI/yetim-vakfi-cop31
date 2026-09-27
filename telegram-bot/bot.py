#!/usr/bin/env python3
"""
Aya - Yetim Vakfi x COP31 Telegram Bot (TR / EN / FA)

Friendly assistant with 20 skills + Foundation site sections (projects, news,
magazine, gift, SMS/bank, volunteer), COP31 info + /ask (local RAG).

Token is read ONLY from TELEGRAM_BOT_TOKEN env var. Never hard-code tokens.
"""
import os
import sys
from pathlib import Path

RAG_DIR = Path(__file__).resolve().parent.parent / "hf-rag"
sys.path.insert(0, str(RAG_DIR))
try:
    import rag as local_rag
    HAS_RAG = True
    SKILLS = local_rag.entries()
except Exception:
    local_rag = None
    HAS_RAG = False
    SKILLS = []

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
except ImportError:
    print("Missing dependency. Run: pip install -r requirements.txt")
    sys.exit(2)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not TOKEN or TOKEN == "PUT_YOUR_TOKEN_HERE":
    print("ERROR: TELEGRAM_BOT_TOKEN is not set.")
    sys.exit(1)

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
# Main-site sections (from sitemap)
P_PROJECTS = "https://yetimvakfi.org.tr/en/project"
P_NEWS = "https://yetimvakfi.org.tr/haber"
P_MAG = "https://yetimvakfi.org.tr/yayin"
P_GIFT = "https://yetimvakfi.org.tr/gift-donate"
P_SMS = "https://yetimvakfi.org.tr/sms"
P_BANK = "https://yetimvakfi.org.tr/hesap-numaralari"
P_VOL = "https://yetimvakfi.org.tr/basvuru/gonullu-formu"

T = {
"tr": {
 "welcome": "Merhaba! Ben Aya 🌙🧸\nYetim Vakfı × COP31 asistanınızım. Size nasıl yardımcı olabilirim?",
 "campaigns": "💛 Kampanyalar", "donate": "🤲 Bağış", "sponsor": "🧸 Sponsorluk",
 "cop31": "🌍 COP31 Yeşil Alan", "startup": "🚀 Startup Kuralları", "faq": "❓ SSS",
 "contact": "📞 İletişim", "lang": "🌐 Dil", "back": "⬅️ Geri",
 "skills": "🌟 20 Yetenek", "skills_title": "🌟 20 yeteneğim — birine dokunun:",
 "site": "🏛️ Vakıf Sitesi", "site_title": "🏛️ Vakıf sitesi bölümleri:",
 "wprojects": "🏠 Projeler", "wnews": "📰 Haberler", "wmag": "📖 Dergi",
 "wgift": "🎁 Hediye", "wpay": "📲 SMS & Banka", "wvol": "🙋 Gönüllü",
 "b_campaigns": "💛 8 Kampanya:\n🧸 Yetim Sponsorluğu (aylık 900 ₺)\n🍲 Gazze Sıcak Yemek\n🎒 İyilik Çantası – Kırtasiye (1.500 ₺/set)\n🐑 Adak–Akika–Şükür Kurbanı\n🤲 Zekât & Sadaka\n🏠 Yetimhane & Yerleşkeler\n🧺 Gıda Paketi\n🎓 Eğitim & Burs\n\nBağış: " + DONATE,
 "b_donate": "🤲 Bağış Yolları:\n🌐 Online: " + DONATE + "\n🍎 App Store: " + APPLE + "\n📱 Google Play: " + PLAY + "\n📲 SMS: EĞİTİM yazıp 9868'e gönderin (50 ₺, kırtasiye)",
 "b_sponsor": "🧸 Yetim Sponsorluğu:\n• Ayda 900 ₺, yılda 10.800 ₺\n• 21 ülkede 26.490 yetim (Eyl 2026)\n• En az 1 yıl sponsorluk\n\nBaşvuru: " + SPONSOR,
 "b_cop31": "🌍 COP31 Green Zone:\n📅 9–20 Kasım 2026 (11–12: Liderler Zirvesi)\n📍 Antalya EXPO Center, Aksu–Antalya\n🎟️ Ücretsiz + QR ile giriş\n\n🔗 Ziyaret kaydı: " + GZ_VISIT + "\n🔗 Green Zone: " + GZ + "\n🔗 UNFCCC: " + UNFCCC + "\n\nNGO'lar için doğru yol: Climate Supporter (greenzone@cop31.tr)",
 "b_startup": "🚀 Startup Zone Kuralları:\n✅ Sadece iklim startup'ları (şirket)\n✅ Desk stand: 0–3 yaş şirketler\n✅ Exhibitor (masa/5/15 m²) veya Sponsor\n📝 Sonuç: startup@cop31.tr\n❌ NGO'lar giremez → Climate Supporter yolunu kullanın\n\n🔗 " + STARTUP,
 "b_faq": "❓ SSS:\n• Yetim Vakfı nerede? → Fatih/İstanbul (iletişim menüsü)\n• Sponsorluk ne kadar? → Ayda 900 ₺\n• COP31'e nasıl katılırım? → cop31.tr/register-to-visit\n• Startup mıyız? → Hayır; NGO'lar Climate Supporter'a başvurur",
 "b_contact": "📞 İletişim:\n☎️ 0212 970 60 60\n✉️ info@yetimvakfi.org.tr\n📍 Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/İstanbul\n🗺️ " + MAPS + "\n🌐 " + CONTACT_PAGE,
 "b_wprojects": "🏠 Projeler:\n🍲 Gazze Sıcak Yemek • ❄️ Kış Yardımı • 🏦 Gıda Bankacılığı\n🧵 Kalkınma: dikiş, dokuma, tarım, hayvancılık\n🏠 Yetimhaneler • 🕊️ Esenlik Durakları\n\n🔗 Tümü: " + P_PROJECTS,
 "b_wnews": "📰 Son haberler:\n🎒 20.000+ çocuğa kırtasiye sevinci\n🐑 2026 Kurban bereketi sınırları aştı\n📖 Elimsende 2. sayı yayında\n☀️ Yaz molası etkinlikleri\n\n🔗 Tümü: " + P_NEWS,
 "b_wmag": "📖 Elimsende Dergisi (2. sayı yayında!)\nVakfın süreli yayını — hikayeler ve projeler.\n\n🔗 " + P_MAG,
 "b_wgift": "🎁 Hediye Bağışı — bir çocuğu sevindirin!\nSevdikleriniz adına bağış hediye edin.\n\n🔗 " + P_GIFT,
 "b_wpay": "📲 SMS Bağışı: " + P_SMS + "\n(örn. EĞİTİM → 9868, 50 ₺ kırtasiye)\n🏦 Havale/EFT hesap numaraları:\n" + P_BANK,
 "b_wvol": "🙋 Gönüllü olun!\nBaşvuru formu: " + P_VOL + "\n☎️ 0212 970 60 60",
 "ask_hint": "Kullanım: /ask sorunuz (örn: /ask sponsorluk ücreti ne kadar?)",
 "ask_no": "🌙 Bu konuda emin bir cevabım yok. İletişim: 0212 970 60 60",
},
"en": {
 "welcome": "Hello! I'm Aya 🌙🧸\nYour Yetim Vakfı × COP31 assistant. How can I help you?",
 "campaigns": "💛 Campaigns", "donate": "🤲 Donate", "sponsor": "🧸 Sponsorship",
 "cop31": "🌍 COP31 Green Zone", "startup": "🚀 Startup Rules", "faq": "❓ FAQ",
 "contact": "📞 Contact", "lang": "🌐 Lang", "back": "⬅️ Back",
 "skills": "🌟 20 Skills", "skills_title": "🌟 My 20 skills — tap one:",
 "site": "🏛️ Foundation Site", "site_title": "🏛️ Foundation site sections:",
 "wprojects": "🏠 Projects", "wnews": "📰 News", "wmag": "📖 Magazine",
 "wgift": "🎁 Gift", "wpay": "📲 SMS & Bank", "wvol": "🙋 Volunteer",
 "b_campaigns": "💛 8 Campaigns:\n🧸 Orphan Sponsorship (900 ₺/mo)\n🍲 Gaza Hot Meals\n🎒 School Bag – Stationery (1,500 ₺/set)\n🐑 Vow–Aqiqah–Thanksgiving Qurbani\n🤲 Zakat & Sadaqah\n🏠 Orphanages & Settlements\n🧺 Food Parcel\n🎓 Education & Scholarship\n\nDonate: " + DONATE,
 "b_donate": "🤲 Ways to donate:\n🌐 Online: " + DONATE + "\n🍎 App Store: " + APPLE + "\n📱 Google Play: " + PLAY + "\n📲 SMS: text EĞİTİM to 9868 (50 ₺, stationery)",
 "b_sponsor": "🧸 Orphan Sponsorship:\n• 900 ₺/month, 10,800 ₺/year\n• 26,490 orphans in 21 countries (Sep 2026)\n• Minimum 1 year\n\nApply: " + SPONSOR,
 "b_cop31": "🌍 COP31 Green Zone:\n📅 9–20 Nov 2026 (11–12: Leaders Summit)\n📍 Antalya EXPO Center, Aksu–Antalya\n🎟️ Free entry with QR\n\n🔗 Visit registration: " + GZ_VISIT + "\n🔗 Green Zone: " + GZ + "\n🔗 UNFCCC: " + UNFCCC + "\n\nRight lane for NGOs: Climate Supporter (greenzone@cop31.tr)",
 "b_startup": "🚀 Startup Zone Rules:\n✅ Climate startups (companies) only\n✅ Desk stand: companies 0–3 years old\n✅ Exhibitor (desk/5/15 m²) or Sponsor\n📝 Decisions via: startup@cop31.tr\n❌ NGOs cannot enter → use Climate Supporter lane\n\n🔗 " + STARTUP,
 "b_faq": "❓ FAQ:\n• Where is Yetim Vakfı? → Fatih/Istanbul (contact menu)\n• Sponsorship fee? → 900 ₺/month\n• How to join COP31? → cop31.tr/register-to-visit\n• Are we a startup? → No; NGOs apply as Climate Supporter",
 "b_contact": "📞 Contact:\n☎️ +90 212 970 60 60\n✉️ info@yetimvakfi.org.tr\n📍 Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/Istanbul\n🗺️ " + MAPS + "\n🌐 " + CONTACT_PAGE,
 "b_wprojects": "🏠 Projects:\n🍲 Gaza Hot Meal • ❄️ Winter Aid • 🏦 Food Banking\n🧵 Development: sewing, weaving, farming, livestock\n🏠 Orphanages • 🕊️ Stations of Peace\n\n🔗 All: " + P_PROJECTS,
 "b_wnews": "📰 Latest news:\n🎒 Stationery joy for 20,000+ children\n🐑 2026 Qurbani beyond borders\n📖 Elimsende issue #2 out\n☀️ Summer break activities\n\n🔗 All: " + P_NEWS,
 "b_wmag": "📖 Elimsende Magazine (issue #2 out!)\nThe foundation's periodical — stories & projects.\n\n🔗 " + P_MAG,
 "b_wgift": "🎁 Gift Donation — make a kid happy!\nDonate a gift in a loved one's name.\n\n🔗 " + P_GIFT,
 "b_wpay": "📲 SMS Donation: " + P_SMS + "\n(e.g. EĞİTİM → 9868, 50 ₺ stationery)\n🏦 Wire transfer account numbers:\n" + P_BANK,
 "b_wvol": "🙋 Become a volunteer!\nForm: " + P_VOL + "\n☎️ +90 212 970 60 60",
 "ask_hint": "Usage: /ask your question (e.g. /ask what is the sponsorship fee?)",
 "ask_no": "🌙 I have no confident answer. Contact: +90 212 970 60 60",
},
"fa": {
 "welcome": "سلام! من آیا هستم 🌙🧸\nدستیار یتیم‌وکفی × COP31 شما. چطور کمکتان کنم؟",
 "campaigns": "💛 کمپین‌ها", "donate": "🤲 کمک مالی", "sponsor": "🧸 حمایت از یتیم",
 "cop31": "🌍 گرین‌زون COP31", "startup": "🚀 قوانین استارتاپ", "faq": "❓ سؤالات",
 "contact": "📞 تماس", "lang": "🌐 زبان", "back": "⬅️ بازگشت",
 "skills": "🌟 ۲۰ مهارت", "skills_title": "🌟 ۲۰ مهارت من — یکی را بزنید:",
 "site": "🏛️ سایت موسسه", "site_title": "🏛️ بخش‌های سایت موسسه:",
 "wprojects": "🏠 پروژه‌ها", "wnews": "📰 اخبار", "wmag": "📖 مجله",
 "wgift": "🎁 هدیه", "wpay": "📲 پیامک و بانک", "wvol": "🙋 داوطلب",
 "b_campaigns": "💛 ۸ کمپین:\n🧸 حمایت از یتیم (ماهانه ۹۰۰ لیر)\n🍲 غذای گرم غزه\n🎒 کیف مهربانی – لوازم‌التحریر (۱۵۰۰ لیر)\n🐑 قربانی نذر/عقیقه/شکر\n🤲 زکات و صدقه\n🏠 یتیم‌خانه‌ها\n🧺 بسته غذایی\n🎓 آموزش و بورسیه\n\nکمک: " + DONATE,
 "b_donate": "🤲 راه‌های کمک:\n🌐 آنلاین: " + DONATE + "\n🍎 اپ‌استور: " + APPLE + "\n📱 گوگل‌پلی: " + PLAY + "\n📲 پیامک: EĞİTİM به 9868 (۵۰ لیر، لوازم‌التحریر)",
 "b_sponsor": "🧸 حمایت از یتیم:\n• ماهانه ۹۰۰ لیر، سالانه ۱۰٬۸۰۰ لیر\n• ۲۶٬۴۹۰ یتیم در ۲۱ کشور\n• حداقل ۱ سال\n\nثبت: " + SPONSOR,
 "b_cop31": "🌍 گرین‌زون COP31:\n📅 ۹ تا ۲۰ نوامبر ۲۰۲۶ (۱۱–۱۲: اجلاس رهبران)\n📍 آنتالیا EXPO Center\n🎟️ ورود رایگان با QR\n\n🔗 ثبت بازدید: " + GZ_VISIT + "\n🔗 گرین‌زون: " + GZ + "\n🔗 UNFCCC: " + UNFCCC + "\n\nمسیر درست NGOها: Climate Supporter",
 "b_startup": "🚀 قوانین Startup Zone:\n✅ فقط استارتاپ‌های اقلیمی (شرکت)\n✅ میز: شرکت ۰ تا ۳ ساله\n✅ غرفه‌دار یا حامی\n📝 نتیجه: startup@cop31.tr\n❌ NGO پذیرفته نمی‌شود → مسیر Climate Supporter\n\n🔗 " + STARTUP,
 "b_faq": "❓ سؤالات:\n• یتیم‌وکفی کجاست؟ → فاتح/استانبول (منوی تماس)\n• هزینه حمایت؟ → ماهانه ۹۰۰ لیر\n• شرکت در COP31؟ → cop31.tr/register-to-visit\n• آیا استارتاپیم؟ → نه؛ NGOها Climate Supporter می‌شوند",
 "b_contact": "📞 تماس:\n☎️ 0212 970 60 60\n✉️ info@yetimvakfi.org.tr\n📍 Dervişali, Kariye Cami Sk. No:6, Fatih/İstanbul\n🗺️ " + MAPS,
 "b_wprojects": "🏠 پروژه‌ها:\n🍲 غذای گرم غزه • ❄️ کمک زمستانی • 🏦 بانک غذا\n🧵 توسعه: خیاطی، بافندگی، کشاورزی، دامداری\n🏠 یتیم‌خانه‌ها • 🕊️ ایستگاه‌های آرامش\n\n🔗 همه: " + P_PROJECTS,
 "b_wnews": "📰 آخرین اخبار:\n🎒 شادی لوازم‌التحریر برای +۲۰٬۰۰۰ کودک\n🐑 قربانی ۲۰۲۶ فراتر از مرزها\n📖 شماره ۲ مجله الیم‌سنده\n☀️ فعالیت‌های تابستانی\n\n🔗 همه: " + P_NEWS,
 "b_wmag": "📖 مجله الیم‌سنده (شماره ۲ منتشر شد!)\nنشریه موسسه — داستان‌ها و پروژه‌ها.\n\n🔗 " + P_MAG,
 "b_wgift": "🎁 هدیه دادن — یک کودک را خوشحال کنید!\nبه نام عزیزانتان کمک هدیه بدهید.\n\n🔗 " + P_GIFT,
 "b_wpay": "📲 کمک پیامکی: " + P_SMS + "\n(مثلاً EĞİTİM به 9868، ۵۰ لیر لوازم‌التحریر)\n🏦 شماره حساب‌های بانکی:\n" + P_BANK,
 "b_wvol": "🙋 داوطلب شوید!\nفرم: " + P_VOL + "\n☎️ 0212 970 60 60",
 "ask_hint": "روش استفاده: /ask سؤال شما (مثلاً: /ask هزینه حمایت چقدر است؟)",
 "ask_no": "🌙 جواب مطمئنی ندارم. تماس: 0212 970 60 60",
},
}
user_lang = {}
user_page = {}
PER_PAGE = 7

def menu_kb(lg):
    s = T[lg]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["campaigns"], callback_data="m:campaigns"),
         InlineKeyboardButton(s["donate"], callback_data="m:donate")],
        [InlineKeyboardButton(s["sponsor"], callback_data="m:sponsor"),
         InlineKeyboardButton(s["cop31"], callback_data="m:cop31")],
        [InlineKeyboardButton(s["startup"], callback_data="m:startup"),
         InlineKeyboardButton(s["skills"], callback_data="m:skills")],
        [InlineKeyboardButton(s["faq"], callback_data="m:faq"),
         InlineKeyboardButton(s["contact"], callback_data="m:contact")],
        [InlineKeyboardButton(s["site"], callback_data="m:site"),
         InlineKeyboardButton(s["lang"], callback_data="m:lang")],
    ])

def site_kb(lg):
    s = T[lg]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["wprojects"], callback_data="w:projects"),
         InlineKeyboardButton(s["wnews"], callback_data="w:news")],
        [InlineKeyboardButton(s["wmag"], callback_data="w:mag"),
         InlineKeyboardButton(s["wgift"], callback_data="w:gift")],
        [InlineKeyboardButton(s["wpay"], callback_data="w:pay"),
         InlineKeyboardButton(s["wvol"], callback_data="w:vol")],
        [InlineKeyboardButton(s["back"], callback_data="m:menu")],
    ])

def back_site_kb(lg):
    return InlineKeyboardMarkup([[InlineKeyboardButton(T[lg]["back"], callback_data="m:site")]])

def lang_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang:tr"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang:en"),
        InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang:fa"),
    ]])

def back_kb(lg):
    return InlineKeyboardMarkup([[InlineKeyboardButton(T[lg]["back"], callback_data="m:menu")]])

async def show_skills(q, lg, pg):
    total = max(1, (len(SKILLS) + PER_PAGE - 1) // PER_PAGE)
    pg = max(0, min(pg, total - 1))
    rows = []
    for e in SKILLS[pg * PER_PAGE:(pg + 1) * PER_PAGE]:
        rows.append([InlineKeyboardButton(f"· {e['title'][:30]}", callback_data=f"sk:{e['id']}")])
    nav = []
    if pg > 0:
        nav.append(InlineKeyboardButton("◀", callback_data=f"skp:{pg - 1}"))
    nav.append(InlineKeyboardButton(T[lg]["back"], callback_data="m:menu"))
    if pg < total - 1:
        nav.append(InlineKeyboardButton("▶", callback_data=f"skp:{pg + 1}"))
    rows.append(nav)
    await q.edit_message_text(f"{T[lg]['skills_title']} ({pg + 1}/{total})",
                              reply_markup=InlineKeyboardMarkup(rows))

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_lang[update.effective_user.id] = "en"
    await update.message.reply_text("🌐 Choose language / Dil seç / زبان:", reply_markup=lang_kb())

async def ask_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lg = user_lang.get(update.effective_user.id, "en")
    question = " ".join(ctx.args).strip()
    if not question:
        await update.message.reply_text(T[lg]["ask_hint"])
        return
    if not HAS_RAG:
        await update.message.reply_text(T[lg]["ask_no"])
        return
    try:
        res = local_rag.ask(question)
    except Exception:
        await update.message.reply_text(T[lg]["ask_no"])
        return
    if res.get("score", 0) < 0.12:
        await update.message.reply_text(T[lg]["ask_no"])
    else:
        await update.message.reply_text(f"🌙 Aya:\n{res['answer']}\n\n📌 {res.get('title', '')}",
                                        disable_web_page_preview=True)

async def on_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    try:
        await q.answer()
    except Exception:
        pass  # stale button taps from old queue can't be answered - ignore
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
    elif data == "m:site":
        await q.edit_message_text(T[lg]["site_title"], reply_markup=site_kb(lg))
    elif data.startswith("w:"):
        key = "b_w" + data.split(":")[1]
        await q.edit_message_text(T[lg].get(key, "..."), reply_markup=back_site_kb(lg),
                                  disable_web_page_preview=True)
    elif data == "m:skills":
        user_page[uid] = 0
        await show_skills(q, lg, 0)
    elif data.startswith("skp:"):
        pg = int(data.split(":")[1])
        user_page[uid] = pg
        await show_skills(q, lg, pg)
    elif data.startswith("sk:"):
        sid = data.split(":", 1)[1]
        e = next((x for x in SKILLS if x["id"] == sid), None)
        pg = user_page.get(uid, 0)
        if e:
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(T[lg]["back"], callback_data=f"skp:{pg}")]])
            await q.edit_message_text(f"🌟 {e['title']}\n\n{e['text']}", reply_markup=kb,
                                      disable_web_page_preview=True)
        else:
            await show_skills(q, lg, pg)
    elif data.startswith("m:"):
        key = "b_" + data.split(":")[1]
        await q.edit_message_text(T[lg].get(key, "..."), reply_markup=back_kb(lg),
                                  disable_web_page_preview=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask_cmd))
    app.add_handler(CallbackQueryHandler(on_button))
    print("Aya is running. Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
