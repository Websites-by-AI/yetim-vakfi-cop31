/* Aya - on-site assistant (TR/EN/FA). Offline: TF-IDF over 20 skills. No server, no token.
   Optional: set window.AYA_HF_URL to a Worker proxy for generative answers. */
(function(){
"use strict";
const KB=[
["sponsor-en","en","Orphan sponsorship fee","Orphan sponsorship costs 900 TL per month (10,800 TL per year), minimum 1 year. 26,490 orphans in 21 countries are sponsored (Sep 2026). Apply: https://yetimvakfi.org.tr/en/yetim-sponsorluk"],
["sponsor-tr","tr","Yetim sponsorluk ücreti","Yetim sponsorluğu ayda 900 TL, yılda 10.800 TL'dir; en az 1 yıl. 21 ülkede 26.490 yetim destekleniyor (Eyl 2026). Başvuru: https://yetimvakfi.org.tr/en/yetim-sponsorluk"],
["sponsor-fa","fa","هزینه حمایت از یتیم","حمایت از هر یتیم ماهانه ۹۰۰ لیر (سالانه ۱۰٬۸۰۰ لیر) است، حداقل ۱ سال. ۲۶٬۴۹۰ یتیم در ۲۱ کشور حمایت می‌شوند."],
["contact-en","en","Yetim Vakfi contact","Phone +90 212 970 60 60, email info@yetimvakfi.org.tr, address Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/Istanbul. Map: https://maps.app.goo.gl/G7xEt7ZmWxuf5hQf9"],
["contact-tr","tr","Yetim Vakfı iletişim","Telefon 0212 970 60 60, e-posta info@yetimvakfi.org.tr, adres Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/İstanbul. https://yetimvakfi.org.tr/iletisim"],
["contact-fa","fa","تماس با یتیم‌وکفی","تلفن 0212 970 60 60، ایمیل info@yetimvakfi.org.tr، نشانی: فاتح/استانبول، ترکیه."],
["donate-en","en","How to donate","Donate online at https://bagis.yetimvakfi.org.tr/en/donate or via the app (App Store id6745053470, Google Play tr.org.yetimvakfi). SMS: text EĞİTİM to 9868 for 50 TL stationery donation."],
["donate-tr","tr","Nasıl bağış yapılır","Online bağış: https://bagis.yetimvakfi.org.tr/en/donate veya mobil uygulama (App Store / Google Play). SMS: 9868'e EĞİTİM yazın (50 TL kırtasiye bağışı)."],
["cop31-en","en","COP31 Green Zone basics","COP31 runs 9-20 Nov 2026 at Antalya EXPO Center, Aksu-Antalya. Green Zone is free with visitor QR from https://cop31.tr/register-to-visit. World Leaders Summit: 11-12 Nov."],
["cop31-tr","tr","COP31 Yeşil Alan bilgileri","COP31, 9-20 Kasım 2026'da Antalya EXPO Center'da. Yeşil Alan ücretsizdir, QR için: https://cop31.tr/register-to-visit. Liderler Zirvesi: 11-12 Kasım."],
["cop31-fa","fa","اطلاعات گرین‌زون COP31","کاپ ۳۱ از ۹ تا ۲۰ نوامبر ۲۰۲۶ در آنتالیا EXPO Center برگزار می‌شود. ورود به گرین‌زون رایگان با QR است. اجلاس رهبران: ۱۱–۱۲ نوامبر."],
["lanes-en","en","Green Zone participation lanes","NGOs join as Climate Supporter via greenzone@cop31.tr. Startups use the Startup Zone (startupzone.cop31.center). Visitors register at cop31.tr/register-to-visit."],
["startup-en","en","Startup Zone rules","Startup Zone is only for climate startups (companies). Desk stands are for companies 0-3 years old. Routes: Exhibitor (desk/5/15 sqm) or Sponsor. Decisions via startup@cop31.tr. NGOs cannot enter; they must use the Climate Supporter lane."],
["startup-tr","tr","Startup Zone kuralları","Startup Zone sadece iklim startup'larına (şirket) açıktır. Desk stand 0-3 yaş şirketler içindir. Sonuçlar startup@cop31.tr ile bildirilir. NGO'lar giremez; Climate Supporter yolunu kullanmalıdır."],
["stationery-en","en","Stationery campaign","With 1,500 TL you cover one child's full stationery set. 2026 target: 20,000 children."],
["stationery-tr","tr","Kırtasiye kampanyası","1.500 TL ile bir çocuğun tüm kırtasiye ihtiyacı karşılanır. 2026 hedefi: 20.000 çocuk."],
["app-en","en","Mobile app","Free Yetim Vakfi app: donate, manage sponsorships, track projects, receipts. App Store id6745053470, Google Play tr.org.yetimvakfi."],
["volunteer-en","en","Become a volunteer","Join as a volunteer via the form at https://yetimvakfi.org.tr/basvuru/gonullu-formu or contact +90 212 970 60 60."],
["ramadan-en","en","Ramadan campaign","Ramadan 2026 goal: reach 543,096 people in 30 countries with iftars, food parcels, zakat and fitrah."],
["gaza-en","en","Gaza Hot Meal Project","Gaza Hot Meal Project delivers hot meals in Gaza; donations are zakat-eligible. Info: https://yetimvakfi.org.tr/en/project/filistin-sicak-yemek"]
];
const UI={
 tr:{hello:"Merhaba! Ben Aya 🌙 Size nasıl yardımcı olabilirim?",ph:"Sorunuzu yazın...",send:"➤",no:"Bu konuda emin bir cevabım yok 🌙 İletişim: 0212 970 60 60",skills:"20 yetenek:",you:"Siz"},
 en:{hello:"Hello! I'm Aya 🌙 How can I help you?",ph:"Type your question...",send:"➤",no:"I have no confident answer 🌙 Contact: +90 212 970 60 60",skills:"20 skills:",you:"You"},
 fa:{hello:"سلام! من آیا هستم 🌙 چطور کمکتان کنم؟",ph:"سؤالتان را بنویسید...",send:"➤",no:"جواب مطمئنی ندارم 🌙 تماس: 0212 970 60 60",skills:"۲۰ مهارت:",you:"شما"}
};
let LANG="tr";
try{ LANG=localStorage.getItem("aya_lang")||"tr"; if(!UI[LANG]) LANG="tr"; }catch(e){}
function saveLang(){ try{localStorage.setItem("aya_lang",LANG);}catch(e){} }
// TF-IDF
function tok(s){ try{ return (s.toLowerCase().match(/[\p{L}\p{N}]+/gu)||[]); }catch(e){ return (s.toLowerCase().match(/[a-z0-9_]+/g)||[]); } }
const DF={}, TF=KB.map(e=>{ const c={}, seen={}; tok(e[2]+" "+e[3]).forEach(t=>{c[t]=(c[t]||0)+1; if(!seen[t]){DF[t]=(DF[t]||0)+1; seen[t]=1;}}); return c; });
const IDF={}; Object.keys(DF).forEach(t=>{ IDF[t]=Math.log((1+KB.length)/(1+DF[t]))+1; });
function vec(c){ const v={}; for(const t in c) v[t]=c[t]*(IDF[t]||0); return v; }
function cos(a,b){ let d=0,na=0,nb=0; for(const t in a){d+=a[t]*(b[t]||0); na+=a[t]*a[t];} for(const t in b) nb+=b[t]*b[t]; return d/((Math.sqrt(na)||1)*(Math.sqrt(nb)||1)); }
function search(q){
  const qv=vec(tok(q).reduce((m,t)=>(m[t]=(m[t]||0)+1,m),{}));
  let best=null,bs=-1;
  const pool=KB.map((e,i)=>[e,i]).filter(([e])=>e[1]===LANG);
  (pool.length?pool:KB.map((e,i)=>[e,i])).forEach(([e,i])=>{ const s=cos(qv,vec(TF[i])); if(s>bs){bs=s;best=e;} });
  if(bs<0.12){ KB.forEach(e=>{ const i=KB.indexOf(e); const s=cos(qv,vec(TF[i])); if(s>bs){bs=s;best=e;} }); }
  return {e:best,s:bs};
}
function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function linkify(s){ return esc(s).replace(/(https?:\/\/[^\s<]+)/g,'<a href="$1" target="_blank" rel="noopener">$1</a>'); }
// UI
const css=`#aya-fab{position:fixed;bottom:20px;right:20px;width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#095c5f,#059669);color:#fff;font-size:30px;border:none;cursor:pointer;box-shadow:0 8px 24px rgba(0,0,0,.3);z-index:9998}
#aya-panel{position:fixed;bottom:88px;right:20px;width:min(360px,92vw);height:min(520px,70vh);background:#fff;border-radius:18px;box-shadow:0 16px 50px rgba(0,0,0,.3);display:none;flex-direction:column;overflow:hidden;z-index:9999;font-family:inherit}
#aya-panel.open{display:flex}
#aya-head{background:linear-gradient(135deg,#095c5f,#059669);color:#fff;padding:12px 14px;display:flex;align-items:center;gap:8px}
#aya-head b{flex:1;font-size:15px}
#aya-head button{background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.4);color:#fff;border-radius:8px;padding:3px 8px;font-size:11px;cursor:pointer;font-weight:700}
#aya-head button.on{background:#fff;color:#065f46}
#aya-msgs{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px;background:#f8faf8;font-size:13.5px}
.aya-m{max-width:88%;padding:9px 12px;border-radius:14px;line-height:1.55;word-wrap:break-word}
.aya-m.bot{background:#fff;border:1px solid #d1fae5;border-bottom-left-radius:4px;align-self:flex-start}
.aya-m.me{background:#0d7377;color:#fff;border-bottom-right-radius:4px;align-self:flex-end}
.aya-m small{display:block;margin-top:4px;opacity:.65;font-size:11px}
.aya-m a{color:#059669;word-break:break-all}.aya-m.me a{color:#fef08a}
#aya-chips{display:flex;gap:6px;overflow-x:auto;padding:8px 10px;border-top:1px solid #e5e7eb;background:#fff}
#aya-chips button{flex-shrink:0;background:#f0fdfa;border:1.5px solid #99f6e4;border-radius:999px;padding:5px 11px;font-size:11.5px;cursor:pointer;font-family:inherit;white-space:nowrap}
#aya-form{display:flex;gap:6px;padding:10px;border-top:1px solid #e5e7eb;background:#fff}
#aya-in{flex:1;border:1.5px solid #d1d5db;border-radius:10px;padding:9px 11px;font-size:13.5px;font-family:inherit}
#aya-form button{background:#059669;color:#fff;border:none;border-radius:10px;padding:0 14px;font-size:16px;cursor:pointer}`;
const st=document.createElement("style"); st.textContent=css; document.head.appendChild(st);
const fab=document.createElement("button"); fab.id="aya-fab"; fab.textContent="🌙"; fab.title="Aya";
const panel=document.createElement("div"); panel.id="aya-panel";
panel.innerHTML=`<div id="aya-head"><span style="font-size:22px">🌙</span><b>Aya • Yetim Vakfı × COP31</b><button data-l="tr">TR</button><button data-l="en">EN</button><button data-l="fa">FA</button></div><div id="aya-msgs"></div><div id="aya-chips"></div><form id="aya-form"><input id="aya-in" autocomplete="off"><button type="submit">➤</button></form>`;
document.body.appendChild(fab); document.body.appendChild(panel);
const msgs=panel.querySelector("#aya-msgs"), chips=panel.querySelector("#aya-chips"),
      form=panel.querySelector("#aya-form"), inp=panel.querySelector("#aya-in");
fab.onclick=()=>{ panel.classList.toggle("open"); if(panel.classList.contains("open")&&!msgs.children.length) botSay(UI[LANG].hello); };
panel.querySelectorAll("#aya-head button").forEach(b=>{ b.onclick=()=>{ LANG=b.dataset.l; saveLang(); paintLang(); }; });
function paintLang(){
  panel.querySelectorAll("#aya-head button").forEach(b=>b.classList.toggle("on",b.dataset.l===LANG));
  inp.placeholder=UI[LANG].ph;
  const list=KB.filter(e=>e[1]===LANG).concat(KB.filter(e=>e[1]!==LANG)).slice(0,20);
  chips.innerHTML="";
  list.forEach(e=>{ const c=document.createElement("button"); c.textContent=e[2].slice(0,26); c.title=e[2]; c.onclick=()=>userSay(e[2]); chips.appendChild(c); });
}
function addMsg(html,me){ const d=document.createElement("div"); d.className="aya-m "+(me?"me":"bot"); d.innerHTML=html; msgs.appendChild(d); msgs.scrollTop=msgs.scrollHeight; }
function botSay(t){ addMsg(linkify(t),false); }
function userSay(t){
  t=(t||"").trim(); if(!t) return;
  addMsg(esc(t),true); inp.value="";
  const r=search(t);
  setTimeout(()=>{
    if(r.s<0.12||!r.e) botSay(UI[LANG].no);
    else addMsg(linkify(r.e[3])+`<small>📌 ${esc(r.e[2])}</small>`,false);
  },350);
}
form.onsubmit=e=>{ e.preventDefault(); userSay(inp.value); };
paintLang();
})();
