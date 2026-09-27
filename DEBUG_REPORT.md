# Debug Report — 26 Sept 2026

## Site files tested
1. `yetim-vakfi-fundraising-tracker.html` (main app: fundraising + COP31 Green Zone registration)
2. `cop31-startup-zone-rules-check.html` (FA rules checker)
3. `yetim-vakfi-cop31-swot-report.html` (SWOT report)

## A. Static analysis — ALL PASS ✅
| Check | Tracker | Rules Check | SWOT |
|---|---|---|---|
| HTML tags balanced | ✅ | ✅ | ✅ |
| Duplicate `id=` | none | none | none |
| JS `$('id')` refs resolve (76 total) | ✅ all | ✅ all | ✅ all |
| `onclick` handlers defined | ✅ all | ✅ all | ✅ all |
| `data-i18n` keys exist (93) | ✅ all | n/a (FA only) | n/a (EN only) |
| `t('key')` calls resolve (42) | ✅ all | n/a | n/a |
| `node --check` JS syntax | ✅ | ✅ | ✅ |

## B. Runtime simulation (Node + DOM stub) — ALL PASS ✅
Executed init + full user flows with zero errors:
- Tracker: `renderAll`, TR↔EN toggle, Green Zone view switch, add/edit/delete donation,
  add/edit/delete campaign, visitor registration + confirmation code, check-in/out,
  pledge → donation conversion, registration delete, CSV/JSON exports, rate change, full reset.
  Final state after reset: 24 donations, 3 registrations, 8 campaigns (correct sample data).
- Rules Check: answer all 7 questions, theme select, NGO demo auto-fill, reset, print path.
- SWOT: init + checklist listeners.

## C. Result
No bugs found. No fixes needed. Last verified: 2026-09-26.

## D. Fact check (info debugging) — 26 Sept 2026
Checked every name / address / phone / link / fee / date against official sources.
| # | Item | Was | Now (verified) | Source |
|---|---|---|---|---|
| 1 | Apple App Store link | ❌ WRONG — guessed ID `1569605623` | ✅ `apps.apple.com/app/yetim-vakfı/id6745053470` | App Store listing |
| 2 | Google Play link | developer page (weak) | ✅ direct app `details?id=tr.org.yetimvakfi` | Play listing |
| 3 | Sponsorship fee | ❌ WRONG — 600 TL/mo (old) | ✅ **900 TL/mo** → 10,800 TL/yr; impact calc, samples, xlsx all updated | yetimvakfi.org.tr/en/yetim-sponsorluk (table updated 04.09.2026) |
| 4 | Sponsored orphans stat | — | ✅ 26,490 orphans in 21 countries (Sept 2026) added | same page |
| 5 | Stationery set | 18,100 children (old news) | ✅ 1,500 TL confirmed; 2026 target 20,000 children | iyilik-cantasi-2026 page |
| 6 | Phone | missing | ✅ 0212 970 60 60 (header pills + footer + xlsx) | yetimvakfi.org.tr/iletisim |
| 7 | Email | missing | ✅ info@yetimvakfi.org.tr | same |
| 8 | Address | missing | ✅ Dervişali, Kariye Cami Sk. No:6, 34087 Fatih/İstanbul | same |
| 9 | COP31 venue | ✅ already correct | ✅ kept + full address: Solak Alanya Yolu Serik Cd., Aksu–Antalya | UNFCCC cop31/ifp |
| 10 | Leaders Summit 11–12 Nov | ✅ confirmed | ✅ kept dates; closure claim softened (unconfirmed) → "check official program" | cop31.tr thematic-days news |
| 11 | Org name | ✅ Yetim Vakfı / Orphan Foundation correct | no change | official site + app listings |

## E. Pending (needs user input)
- Telegram bot: no bot code exists in workspace — awaiting user code or build request.
- Unclear token "chenfnrla dn" in request — asked user for clarification.
