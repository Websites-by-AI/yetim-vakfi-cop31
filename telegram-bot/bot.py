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
 "startups": "🚀 20 Startup", "su_title": "🚀 20 Startup — kategori seçin:",
 "su_climate": "🌱 İklim (10)", "su_social": "💛 Sosyal (10)",
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
 "b_wnews": "📰 Son haberler:\n🎨 Filistinli Çocuklar İçin Çiz — 3 Ekim, 81 il\n🎒 20.000+ çocuğa çanta + kırtasiye (19 ülke)\n🎓 YKS 74.sü 100 bin ₺ ödülünü bağışladı\n🎪 Aksa Kahramanları Çocuk Şenliği\n\n🔗 Tümü: " + P_NEWS,
 "b_wmag": "📖 Elimsende Dergisi (2. sayı yayında!)\nVakfın süreli yayını — hikayeler ve projeler.\n\n🔗 " + P_MAG,
 "b_wgift": "🎁 Hediye Bağışı — bir çocuğu sevindirin!\nSevdikleriniz adına bağış hediye edin.\n\n🔗 " + P_GIFT,
 "b_wpay": "📲 SMS Bağışı: " + P_SMS + "\n(örn. YETİM → 9868: 50 ₺ • EĞİTİM → 8868: 240 ₺)\n🏦 Havale/EFT hesap numaraları:\n" + P_BANK,
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
 "startups": "🚀 20 Startups", "su_title": "🚀 20 Startups — pick a category:",
 "su_climate": "🌱 Climate (10)", "su_social": "💛 Social (10)",
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
 "b_wnews": "📰 Latest news:\n🎨 Draw for Palestinian Children — Oct 3, 81 provinces\n🎒 20,000+ kids got bags + stationery (19 countries)\n🎓 YKS #74 donated his ₺100K prize\n🎪 Aksa Heroes Kids Festival\n\n🔗 All: " + P_NEWS,
 "b_wmag": "📖 Elimsende Magazine (issue #2 out!)\nThe foundation's periodical — stories & projects.\n\n🔗 " + P_MAG,
 "b_wgift": "🎁 Gift Donation — make a kid happy!\nDonate a gift in a loved one's name.\n\n🔗 " + P_GIFT,
 "b_wpay": "📲 SMS Donation: " + P_SMS + "\n(e.g. YETİM → 9868: 50 ₺ • EĞİTİM → 8868: 240 ₺)\n🏦 Wire transfer account numbers:\n" + P_BANK,
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
 "startups": "🚀 ۲۰ استارتاپ", "su_title": "🚀 ۲۰ استارتاپ — دسته را انتخاب کنید:",
 "su_climate": "🌱 اقلیمی (۱۰)", "su_social": "💛 اجتماعی (۱۰)",
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
 "b_wnews": "📰 آخرین اخبار:\n🎨 نقاشی برای کودکان فلسطین — ۳ اکتبر، ۸۱ استان\n🎒 کیف + لوازم‌التحریر برای +۲۰٬۰۰۰ کودک (۱۹ کشور)\n🎓 رتبه ۷۴ کنکور جایزه ۱۰۰ هزار لیری را بخشید\n🎪 جشنواره کودکان قهرمانان اقصی\n\n🔗 همه: " + P_NEWS,
 "b_wmag": "📖 مجله الیم‌سنده (شماره ۲ منتشر شد!)\nنشریه موسسه — داستان‌ها و پروژه‌ها.\n\n🔗 " + P_MAG,
 "b_wgift": "🎁 هدیه دادن — یک کودک را خوشحال کنید!\nبه نام عزیزانتان کمک هدیه بدهید.\n\n🔗 " + P_GIFT,
 "b_wpay": "📲 کمک پیامکی: " + P_SMS + "\n(مثلاً YETİM به 9868: ۵۰ لیر • EĞİTİM به 8868: ۲۴۰ لیر)\n🏦 شماره حساب‌های بانکی:\n" + P_BANK,
 "b_wvol": "🙋 داوطلب شوید!\nفرم: " + P_VOL + "\n☎️ 0212 970 60 60",
 "ask_hint": "روش استفاده: /ask سؤال شما (مثلاً: /ask هزینه حمایت چقدر است؟)",
 "ask_no": "🌙 جواب مطمئنی ندارم. تماس: 0212 970 60 60",
},
}
user_lang = {}
user_page = {}
user_su = {}
PER_PAGE = 7
LI = {"tr": 0, "en": 1, "fa": 2}
SU_STAGE = {
 "tr": ["Fikir", "Prototip", "Ön Tohum", "Tohum"],
 "en": ["Idea", "Prototype", "Pre-seed", "Seed"],
 "fa": ["ایده", "نمونه اولیه", "پیش‌بذری", "بذری"],
}
SU_BADGE = {
 "tr": ("✅ Startup Zone adayı", "💛 Vakıf modeli"),
 "en": ("✅ Startup Zone fit", "💛 Foundation model"),
 "fa": ("✅ مناسب Startup Zone", "💛 مدل خیریه"),
}
STARTUPS = [
 {"e": "☀️", "n": "SolarSack", "c": "Türkiye", "k": "c", "st": 1, "sec": ("Enerji", "Energy", "انرژی"), "d": ("Öğrenciler için güneş panelli sırt çantası: gündüz şarj olur, gece ışık ve telefon şarjı verir.", "Solar-panel backpack for students: charges by day, gives light + phone charge at night.", "کوله‌پشتی خورشیدی برای دانش‌آموزان: روز شارژ می‌شود، شب نور و شارژ موبایل می‌دهد.")},
 {"e": "💧", "n": "DropLoop", "c": "Türkiye", "k": "c", "st": 2, "sec": ("Su", "Water", "آب"), "d": ("Evler için gri su geri dönüşüm kiti — duş suyunu bahçe ve sifon için arıtır.", "Greywater recycling kit for homes — cleans shower water for garden + toilet use.", "کیت بازیافت آب خاکستری خانه — آب حمام را برای باغ و سرویس بهداشتی تصفیه می‌کند.")},
 {"e": "🧱", "n": "RePlast", "c": "Türkiye", "k": "c", "st": 3, "sec": ("Atık", "Waste", "پسماند"), "d": ("Plastik atıkları yapı tuğlasına çevirir — 1 ton plastik = 800 tuğla.", "Turns plastic waste into building bricks — 1 ton of plastic = 800 bricks.", "پسماند پلاستیک را به آجر ساختمانی تبدیل می‌کند — ۱ تن پلاستیک = ۸۰۰ آجر.")},
 {"e": "🌾", "n": "AgroSense", "c": "Kenya", "k": "c", "st": 2, "sec": ("Tarım Teknolojisi", "AgriTech", "فناوری کشاورزی"), "d": ("Küçük çiftçiler için toprak sensörü — sulamayı %40 azaltır, SMS ile uyarır.", "Soil sensor for small farmers — cuts irrigation 40%, alerts by SMS.", "سنسور خاک برای کشاورزان خرد — آبیاری را ۴۰٪ کم می‌کند، با پیامک هشدار می‌دهد.")},
 {"e": "🔋", "n": "VoltVault", "c": "Germany", "k": "c", "st": 1, "sec": ("Enerji", "Energy", "انرژی"), "d": ("Eski elektrikli araç bataryalarından köy mikro-şebekeleri kurar.", "Builds village micro-grids from second-life EV batteries.", "از باتری‌های دست‌دوم خودروی برقی، ریزشبکه برق روستایی می‌سازد.")},
 {"e": "🌊", "n": "AquaHarvest", "c": "UAE", "k": "c", "st": 3, "sec": ("Su", "Water", "آب"), "d": ("Havadan su üreten cihaz — günde 50 litre, güneş enerjisiyle çalışır.", "Atmospheric water generator — 50 liters/day, solar-powered.", "دستگاه تولید آب از هوا — روزی ۵۰ لیتر، با انرژی خورشیدی کار می‌کند.")},
 {"e": "🍞", "n": "CrumbCycle", "c": "France", "k": "c", "st": 2, "sec": ("Gıda", "Food", "غذا"), "d": ("Fırın fazlası ekmeği hayvan yemine çeviren toplama ağı.", "Collection network turning surplus bakery bread into animal feed.", "شبکه جمع‌آوری نان اضافه نانوایی‌ها و تبدیل آن به خوراک دام.")},
 {"e": "🚲", "n": "CargoBee", "c": "Netherlands", "k": "c", "st": 3, "sec": ("Ulaşım", "Mobility", "حمل‌ونقل"), "d": ("Son kilometre teslimat için e-kargo bisiklet filosu — sıfır emisyon.", "E-cargo bike fleet for last-mile delivery — zero emission.", "ناوگان دوچرخه باربری برقی برای تحویل آخر مسیر — بدون آلایندگی.")},
 {"e": "🏠", "n": "ThermoBrick", "c": "Egypt", "k": "c", "st": 1, "sec": ("Yapı", "Buildings", "ساختمان"), "d": ("Tarımsal atıktan yalıtımlı tuğla — evleri yazın serin, kışın sıcak tutar.", "Insulating bricks from farm waste — homes stay cool in summer, warm in winter.", "آجر عایق از ضایعات کشاورزی — خانه را تابستان خنک و زمستان گرم نگه می‌دارد.")},
 {"e": "🌳", "n": "CarbonGarden", "c": "UK", "k": "c", "st": 0, "sec": ("Karbon", "Carbon", "کربن"), "d": ("Şehirlere mikro-ormanlar kurar, KOBİ'lere karbon kredisi sunar.", "Plants urban micro-forests and offers carbon credits to small businesses.", "در شهرها ریزجنگل می‌کارد و به کسب‌وکارهای کوچک اعتبار کربن می‌دهد.")},
 {"e": "🧸", "n": "YetimTech", "c": "Türkiye", "k": "s", "st": 3, "sec": ("Yetim Bakımı", "Orphan Care", "مراقبت از ایتام"), "d": ("Şeffaf yetim sponsorluk platformu — aylık bağış, fotoğraf ve mektup takibi.", "Transparent orphan sponsorship platform — monthly giving with photo + letter updates.", "پلتفرم شفاف حمایت از ایتام — کمک ماهانه با عکس و نامه کودک.")},
 {"e": "🎒", "n": "SchoolKit", "c": "Pakistan", "k": "s", "st": 2, "sec": ("Eğitim", "Education", "آموزش"), "d": ("Köy çocuklarına çanta ve kırtasiye aboneliği — her dönem otomatik ulaşır.", "Bag + stationery subscription for village kids — auto-delivered each term.", "اشتراک کیف و لوازم‌التحریر برای کودکان روستایی — هر ترم خودکار می‌رسد.")},
 {"e": "🍲", "n": "WarmPlate", "c": "Jordan", "k": "s", "st": 1, "sec": ("Gıda", "Food", "غذا"), "d": ("Kriz bölgelerine franchising aşevleri — günde 5.000 sıcak yemek.", "Franchise soup kitchens for crisis zones — 5,000 hot meals a day.", "آشپزخانه‌های زنجیره‌ای برای مناطق بحرانی — روزی ۵٬۰۰۰ غذای گرم.")},
 {"e": "👩‍⚕️", "n": "MobileClinic", "c": "Bangladesh", "k": "s", "st": 3, "sec": ("Sağlık", "Health", "سلامت"), "d": ("Kırsal anneler için mobil sağlık minibüsleri — aşı ve doğum öncesi bakım.", "Mobile health vans for rural mothers — vaccines + prenatal care.", "ون‌های سلامت سیار برای مادران روستایی — واکسن و مراقبت بارداری.")},
 {"e": "📚", "n": "ReadBridge", "c": "Germany", "k": "s", "st": 2, "sec": ("Eğitim", "Education", "آموزش"), "d": ("Mülteci çocuklara ana dilde hikâye kitapları — 12 dilde basıldı.", "Mother-tongue storybooks for refugee children — printed in 12 languages.", "کتاب داستان به زبان مادری برای کودکان پناهنده — چاپ به ۱۲ زبان.")},
 {"e": "🧵", "n": "LoomHope", "c": "Burkina Faso", "k": "s", "st": 1, "sec": ("Geçim", "Livelihood", "معیشت"), "d": ("Dul anneler için dokuma kooperatifleri — tezgâh ve pazar erişimi sağlar.", "Weaving cooperatives for widowed mothers — looms + market access.", "تعاونی‌های بافندگی برای مادران بیوه — دستگاه بافندگی و دسترسی به بازار.")},
 {"e": "❄️", "n": "WinterShield", "c": "Türkiye", "k": "s", "st": 2, "sec": ("Yardım", "Relief", "امداد"), "d": ("Kış yardım kiti kitlesel fonlaması — mont, bot ve ısıtıcı.", "Crowdfunded winter aid kits — coat, boots + heater.", "تأمین جمعی کیت زمستانی — کاپشن، چکمه و بخاری.")},
 {"e": "💧", "n": "WellDrop", "c": "Mali", "k": "s", "st": 3, "sec": ("Su", "Water", "آب"), "d": ("Canlı GPS takipli güneş enerjili su kuyuları — bağışçı kuyusunu izler.", "Solar water wells with live GPS tracking — donors watch their well.", "چاه آب خورشیدی با ردیابی زنده GPS — خیر چاهش را دنبال می‌کند.")},
 {"e": "🎓", "n": "SkillSprout", "c": "Türkiye", "k": "s", "st": 2, "sec": ("Geçim", "Livelihood", "معیشت"), "d": ("Yetim gençlere meslek kursları — dikiş, kodlama, tasarım.", "Vocational courses for orphan youth — sewing, coding, design.", "دوره‌های مهارتی برای جوانان یتیم — خیاطی، برنامه‌نویسی، طراحی.")},
 {"e": "🤝", "n": "KinLink", "c": "UK", "k": "s", "st": 0, "sec": ("Yetim Bakımı", "Orphan Care", "مراقبت از ایتام"), "d": ("Aileleri yetim aileleriyle eşleştiren platform — aylık destek ve ziyaret.", "Platform pairing families with orphan families — monthly support + visits.", "پلتفرم پیوند خانواده‌ها با خانواده‌های دارای یتیم — حمایت ماهانه و دیدار.")},
]

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
        [InlineKeyboardButton(s["startups"], callback_data="m:startups")],
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

def su_kb(lg):
    s = T[lg]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(s["su_climate"], callback_data="su:c:0"),
         InlineKeyboardButton(s["su_social"], callback_data="su:s:0")],
        [InlineKeyboardButton(s["back"], callback_data="m:menu")],
    ])

async def show_su_list(q, lg, cat, pg, uid):
    idxs = [i for i, s in enumerate(STARTUPS) if s["k"] == cat]
    total = max(1, (len(idxs) + PER_PAGE - 1) // PER_PAGE)
    pg = max(0, min(pg, total - 1))
    user_su[uid] = (cat, pg)
    rows = []
    for i in idxs[pg * PER_PAGE:(pg + 1) * PER_PAGE]:
        s = STARTUPS[i]
        rows.append([InlineKeyboardButton(f"{s['e']} {s['n']}", callback_data=f"st:{i}")])
    nav = []
    if pg > 0:
        nav.append(InlineKeyboardButton("◀", callback_data=f"su:{cat}:{pg - 1}"))
    nav.append(InlineKeyboardButton(T[lg]["back"], callback_data="m:startups"))
    if pg < total - 1:
        nav.append(InlineKeyboardButton("▶", callback_data=f"su:{cat}:{pg + 1}"))
    rows.append(nav)
    await q.edit_message_text(f"{T[lg]['su_title']} ({pg + 1}/{total})",
                              reply_markup=InlineKeyboardMarkup(rows))

async def show_su_detail(q, lg, idx, uid):
    s = STARTUPS[idx]
    li = LI[lg]
    badge = SU_BADGE[lg][0 if s["k"] == "c" else 1]
    cat, pg = user_su.get(uid, (s["k"], 0))
    kb = InlineKeyboardMarkup([[InlineKeyboardButton(T[lg]["back"], callback_data=f"su:{cat}:{pg}")]])
    await q.edit_message_text(
        f"{s['e']} {s['n']}\n📍 {s['c']} • {SU_STAGE[lg][s['st']]}\n🏷️ {s['sec'][li]}\n\n{s['d'][li]}\n\n{badge}",
        reply_markup=kb, disable_web_page_preview=True)

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
    elif data == "m:startups":
        await q.edit_message_text(T[lg]["su_title"], reply_markup=su_kb(lg))
    elif data.startswith("su:"):
        parts = data.split(":")
        await show_su_list(q, lg, parts[1], int(parts[2]) if len(parts) > 2 else 0, uid)
    elif data.startswith("st:"):
        await show_su_detail(q, lg, int(data.split(":")[1]), uid)
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
