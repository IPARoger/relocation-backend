# Web2 Backend — Executive Summary (1 page)

**For:** Second opinions, advisors, non-dev founder  
**Full detail:** `WEB2_BACKEND_DECISIONS_FOR_REVIEW_v1_2026-06-12.md`  
**City/geo detail:** `CITY_SEARCH_AND_GEOCODING_STRATEGY.md`  
**Date:** 2026-06-12

---

## What we're building

A **complete Web2 relocation astrology instrument** — maps, birth charts, city comparison, notes, settings, accounts — **before any AI**.

## Ground truth (verified live 2026-06-12)

The old "schema sandbox / not applied" docs are **out of date**. The Supabase project is **live with real data and a working schema**:

- **Live tables w/ data:** `profiles`, `places` (21), `favorite_places` (18), `birth_records` (3), `saved_searches`, `comparison_sets`, `comparison_set_places`, `notes`, `visited_places`, `share_links`, `user_settings`, + `intention_profiles`, `current_location_history`, `location_events`, `profile_relationships`.
- **Model:** `Supabase Auth user → account_user_id → profiles → {birth_records, favorites, searches, comparisons, notes, …}`.
- **The `repositories/` Python layer matches the live schema.** The old `00001–00006` migrations are **superseded/dead** (different table names like `professional_accounts`); the applied schema is `2026_06_08_schema_v1.sql`.
- **`user_settings` already supports account-level (profile_id null) + optional per-profile** rows. Existing rows hold `theme`, `orb_defaults`, `zodiac`.
- **`places` already has `language_code` + `alternate_names_json`** — built for multilingual.

**What's genuinely missing:** (1) real **auth** — rows currently use a placeholder `00000000-…` dev account; (2) **RLS** enforcement; (3) frontend **wired to Supabase** (Settings still uses browser `localStorage`).

---

## Decisions now made (founder, 2026-06-12)

Founder preference: **"use maintained plugins like Supabase that handle security so we don't have to."** That resolves two of the three big forks:

### 1. How the website saves data → ✅ **Direct to Supabase + RLS** (DECIDED)

The web page talks straight to Supabase; security enforced by database rules (RLS) + Supabase Auth — a maintained, security-handled service. No custom Python API server to run. Python `repositories/` retained for backend/admin/AI jobs only.

### 2. How users log in → ✅ **Supabase Auth: Email + Google + Apple** (DECIDED)

All native to Supabase Auth. **Instagram login is not possible** (Meta retired it); Facebook is the Meta alternative if wanted. Founder must register developer apps on Google/Apple consoles to get keys (~10 min each; Apple needs $99/yr developer account).

### 3. Static HTML vs framework → ⚠️ **STILL OPEN** (for second opinion)

Prototypes stay as HTML sandboxes. The shipping product (Settings, Notes, auth, shared nav) likely wants **SvelteKit or Next.js** to avoid copy-pasting across dozens of files. Confirm framework choice with reviewers.

## Multilingual (founder direction)

Fully multilingual product. Two distinct mechanisms:

- **Map labels → single native language per view.** The user's chosen language is applied to the *whole* map (e.g. all-English or all-Japanese), **not** mixed local scripts (raw OSM shows Tokyo in Japanese, Cairo in Arabic, Paris in French — we do **not** want that). This requires a vector-tile provider with a `language` setting (**MapTiler** or **Mapbox**). `places.language_code` + `alternate_names_json` already support storing localized names.
- **Dynamic text (AI interpretations, UI strings, possibly overlay text & notes) → DeepL.** [DeepL API](https://www.deepl.com/pro-api) for high-quality translation. Note: DeepL does **not** translate map labels (that's the tile provider's job); it translates app/AI text.

---

## City & map stack (four separate things)

| Need | Solution | Cost |
|------|----------|------|
| City list with countries | **GeoNames** — fixed today (`build_cities.py`) | Free |
| Type-ahead city search | **Geoapify** subscription (storage allowed) | ~$ |
| Map with language labels | **MapTiler** + **MapLibre** | ~$ |
| Birth-time → UTC (historical DST) | **timezonefinder** + IANA (offline code) | Free |

**Do not use Google Places** for stored birth cities — their license forbids permanent storage.

---

## Build sequence (founder's plan)

1. **Decide** the three forks above (get second opinions).
2. **Apply database schema** + fix schema/code mismatch.
3. **Auth** (login) + security rules (RLS).
4. **Settings** pages — many — wired to real database.
5. **Notes** page.
6. **City search plugin** + map density + initial chart-adding flow.
7. **Full Web2 version** — tie everything together.
8. *Then* AI.

---

## Shopping list (short)

| Service | Why | Link |
|---------|-----|------|
| Supabase | Database + login | [supabase.com](https://supabase.com/) |
| Geoapify | City autocomplete | [geoapify.com](https://www.geoapify.com/) |
| MapTiler | Map tiles + languages | [maptiler.com](https://www.maptiler.com/) |
| Google Cloud Console | Google login keys | [console.cloud.google.com](https://console.cloud.google.com/) |
| Apple Developer | Apple login keys | [developer.apple.com](https://developer.apple.com/) |
| GeoNames admin file | Full region names (free) | [download.geonames.org](https://download.geonames.org/export/dump/admin1CodesASCII.txt) |

Full checklist with pricing links: `CITY_SEARCH_AND_GEOCODING_STRATEGY.md` §7.

---

## What to ask reviewers (narrowed — the genuinely open items)

1. **Frontend framework:** SvelteKit vs Next.js vs stay static-HTML longer? (Map-heavy UI + Supabase.)
2. **Any forced server-side work?** The astrology/chart computation and **historical-timezone** math may need to run server-side (Supabase **Edge Functions**, a maintained option) rather than in the browser. Where's the line?
3. **Map provider for single-language labels:** MapTiler vs Mapbox — which better delivers "whole map in one chosen language"?
4. **Translation:** DeepL for AI/UI/notes — pre-translate and store, or translate on-demand and cache? Any better managed option?
5. **Geoapify** the right storage-friendly autocomplete choice long-term?
6. **RLS** policy design for the `account_user_id → profiles → children` tree — any gotchas?

### Already resolved (no longer open)
- ~~A vs B~~ → **Direct to Supabase + RLS** (founder: prefer managed/secure plugins).
- ~~Auth method~~ → **Supabase Auth: Email + Google + Apple**.
- ~~Schema/repo mismatch~~ → **Resolved:** live DB matches `repositories/`; old `00001–06` migrations superseded.
- ~~Account vs per-profile settings~~ → **Both already supported** (account-level default + optional per-profile).

---

## Documents in this package

| File | Audience |
|------|----------|
| `WEB2_BACKEND_EXEC_SUMMARY.md` | This page — fast read |
| `WEB2_BACKEND_DECISIONS_FOR_REVIEW_v1_2026-06-12.md` | Full decision doc for AI/engineer review |
| `CITY_SEARCH_AND_GEOCODING_STRATEGY.md` | City/map/timezone canon + shopping list |
