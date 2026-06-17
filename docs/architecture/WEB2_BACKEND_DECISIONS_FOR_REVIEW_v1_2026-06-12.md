# Web2 Backend & Architecture — Decisions for Review

**Status:** Draft for second opinions. Nothing here is built yet.
**Date:** 2026-06-12
**Author context:** Prepared for a non-developer founder to circulate to other AIs/engineers for sanity-checking before implementation.

---

## 0. How to use this document

Each decision below is written as:

- **What it is** (plain language)
- **Why it matters**
- **Options**
- **Recommended default** (our current best guess)
- **Question for reviewers** (what we want a second opinion on)

If you are an AI/engineer reviewing this: please challenge the **Foundational Forks** (§2) hardest — everything else depends on them. Tell us where the recommended defaults are wrong, risky, or overcomplicated for a solo/small team shipping a **Web2 product before any AI features**.

---

## 1. Context & goal

- **Product:** a relocation **astrology instrument** (maps, birth charts, city comparison, notes, saved searches).
- **Current state:** mostly **static HTML prototypes** (no app framework). A **Supabase** project exists. A Python `repositories/` layer and a **draft (unapplied) database schema** exist but **do not match each other**. **No authentication. No live API.** Settings UI currently saves only to the browser's `localStorage`.
- **Near-term goal (founder's stated sequence):**
  1. Build out remaining **backend** + **Settings** pages (many).
  2. Build the **Notes** page.
  3. Tie everything together: **city search plugins**, **map density** handling, **initial chart-adding** flow.
  4. Ship a **complete, functional Web2 version**.
  5. *Only then* begin building/training the **AI** layer.

---

## 2. Foundational forks (decide these first)

### Decision A — Frontend approach: static HTML vs. a framework
**What it is:** Today the pages are hand-written HTML files. A "framework" (React/Next.js, SvelteKit, etc.) is a standard toolkit for building larger interactive apps with reusable components, routing, and login handling.

**Why it matters:** A full product with auth, many Settings screens, Notes, and shared navigation is painful to maintain as separate static HTML files (every change copy-pasted across pages). A framework pays for itself past a certain size — but adds a build step and a learning/tooling cost.

**Options:**
1. **Stay static HTML** + a little JavaScript. Lowest tooling, fastest for prototypes, gets unwieldy as features grow.
2. **Adopt a framework** (recommended: **SvelteKit** or **Next.js**). More upfront setup; far better for a real multi-page product with login and shared components.
3. **Hybrid:** keep the map/Genie sandbox as-is, build the "app shell" (auth, Settings, Notes, profile) in a framework.

**Recommended default:** Option 2/3 — move the *real app* to a framework, port the proven prototype UI into it. Doing auth + many Settings pages + Notes in raw HTML will become a maintenance trap.

**Question for reviewers:** For a solo founder shipping a Web2 product of this scope, is a framework worth it now, or should we ship static-HTML-first and migrate later? Which framework best fits Supabase + map-heavy UI?

---

### Decision B — How the browser talks to the database ("A vs B")
**What it is:** When a user changes a setting, *something* has to write it to the database. Two standard ways:

- **(A) Direct:** the web page talks **straight to Supabase** using a public "anon" key. Security is enforced by **Row-Level Security (RLS)** — database rules that guarantee users can only read/write *their own* rows. Login is handled by **Supabase Auth**.
- **(B) Middleman API:** the web page talks to **our own Python server** (FastAPI), which then talks to Supabase using a powerful "service-role" key. We write all the endpoints, login handling, and host the server ourselves.

**Plain analogy:** (A) is shopping with a smart keycard that only opens *your* locker (the building enforces the rules). (B) is hiring a clerk who holds the master key and fetches things for you — more control, but you employ and house the clerk.

**Why it matters:** This is the single biggest fork. It determines how much we build, what we host, and whether the existing Python `repositories/` stay relevant.

**Options / trade-offs:**
| | (A) Direct to Supabase | (B) Python API middleman |
|---|---|---|
| Build effort | Low | High (endpoints, auth, CORS, hosting) |
| Fits static/framework frontend | ✅ Yes | ✅ but heavier |
| Login (Google/Apple/email) | Built in | We build it |
| Servers to run 24/7 | None (Supabase only) | Supabase **+** our API host |
| Existing Python `repositories/` | Set aside for this slice (reusable later for admin/AI jobs) | Kept and central |
| Security model | RLS rules in the database | Our code in the API |

**Recommended default:** **(A) Direct to Supabase with RLS + Supabase Auth.** It matches a static/framework web app, gives social login almost for free, and avoids running a second server. The Python repos are not wasted — they remain useful for **batch/admin/AI backend jobs** later (where the service-role key is appropriate and there's no browser involved).

**Question for reviewers:** Is "Direct + RLS" the right call for this product, or are there workflows (heavy server-side astrology computation, third-party API keys that must stay secret, historical-timezone math) that *force* a backend API anyway? Where's the line between "do it in the browser" and "must be server-side"?

---

### Decision C — Authentication (login)
**What it is:** How users sign in and how we know "who" they are (the identity every saved row is attached to).

**Why it matters:** Everything user-owned (profiles, settings, favorites, notes) hangs off the logged-in identity. Auth choice also affects RLS (Decision B).

**Findings on providers (Supabase Auth):**
- ✅ **Email + password** — supported.
- ✅ **Google** — supported.
- ✅ **Apple** — supported (note: Apple requires a paid Apple Developer account + extra config).
- ❌ **Instagram** — **not** a supported login provider (Meta retired third-party Instagram login). The Meta option that works is **Facebook**.
- Each social provider requires us to **register a developer app** on that provider's site to get keys. **The founder must do this part** (it uses your accounts/billing); we wire up the rest.

**Recommended default:** Launch with **Email + Google + Apple**. Add **Facebook** only if a Meta login is desired. Drop Instagram.

**Question for reviewers:** Any reason to avoid Apple/Google at launch (cost, review friction)? Is email+Google enough for v1, deferring Apple/Facebook?

---

## 3. Data & schema decisions

### Decision D — Reconcile the schema/repository mismatch
**What it is:** The draft database migration defines `user_settings(account_id, settings, settings_version, ...)`. The Python repository writes a *different* shape: `user_settings(account_user_id, profile_id, settings_json, id)`. They disagree, and the schema is marked **"sandbox only — not applied."**

**Why it matters:** Nothing will work until the table definition and the code agree, and the schema is actually applied to the database.

**Open sub-questions:**
- Are settings **account-level** (one set per user) or **profile-level** (different defaults per chart/client)? The two sources disagree (migration = account-level; repo = allows profile-level).
- Confirm the canonical column names and JSON shape.

**Recommended default:** Pick **one** source of truth (lean toward account-level defaults with optional per-profile overrides), rewrite the other to match, then apply migrations cleanly.

**Question for reviewers:** Account-level vs per-profile settings — which is the right default for a tool where one professional manages many clients/charts?

---

### Decision E — Core data model (accounts → profiles → everything)
**What it is:** The relationships: an **account owner** (the logged-in human) owns multiple **profiles/clients**, each with **birth records**, and the account has **favorite places**, **saved searches**, **comparison sets**, and **notes**.

**Why it matters:** Getting this hierarchy right early prevents painful rewrites. Repositories already exist for: profiles, birth_records, favorite_places, saved_searches, comparison_sets, notes, places, visited_places, share_links, user_settings.

**Recommended default:** Keep the existing repository entities as the model; formalize the account → profile → records tree; make every user-owned row carry the owning account id (required for RLS).

**Question for reviewers:** Is anything missing from this entity list for a Web2 v1 (e.g., audit/history, soft-delete/archive, sharing)? Note `share_links` exists — is public sharing in scope for v1?

---

### Decision F — City search & geocoding stack
**What it is:** Four separate needs often confused as one:
1. **Canonical city+country dataset** — *(free, fixable now)* our current importer drops the country/region/timezone columns that **are already in the GeoNames file**. Re-parsing fixes "no countries" with no subscription.
2. **Interactive autocomplete subscription** — live "type a city, get ranked, disambiguated results." **Critical constraint: storage rights.** We save users' birth cities/favorites permanently, so we must use a provider that *allows storing results*.
   - ✅ **Geoapify** (already configured in `.env`), **Radar** — storage allowed, multilingual, country/region, predictable cost.
   - ⚠️ **Mapbox** — best autocomplete UX, but storing requires a pricier "Permanent" tier.
   - ❌ **Google Places** — best coverage, but forbids permanent storage of coordinates → disqualifying for our use.
3. **Map tiles + label language** *(this is "#3" the founder asked about)* — the actual map imagery. Raw OpenStreetMap tiles (current sandbox) can't show labels in different languages well. A keyed provider (**MapTiler** or **Mapbox**) rendered with **MapLibre** lets labels appear as "München" vs "Munich." This is purely about the **map picture and its text**, separate from search.
4. **Historical timezone** — converting a birth time to UTC needs the timezone *rules that were in effect at the birth date* (DST changes over decades). **No geocoding subscription solves this**; the correct approach is the offline IANA timezone database (already named in `.env` as `timezonefinder + zoneinfo`).

**Recommended default:** GeoNames (dataset, free) + **Geoapify** (autocomplete subscription, storage-friendly) + MapTiler/MapLibre (tiles + language) + offline IANA tz (historical). Avoid Google/Mapbox-temporary for anything we store.

**Question for reviewers:** Is Geoapify a sound long-term choice vs Radar for a storage-heavy astrology app? Any pitfalls with GeoNames freshness/quality? Better historical-timezone approach than timezonefinder+zoneinfo?

---

## 4. Security, hosting, operations

### Decision G — Row-Level Security (RLS)
**What it is:** Database rules ensuring user A can never read/write user B's data. Essential if we choose Direct-to-Supabase (Decision B-A).
**Why it matters:** Without it, the public anon key would expose everyone's data. RLS is currently only "stubs."
**Recommended default:** Write real RLS policies keyed to the logged-in account id for every user-owned table before launch.
**Question for reviewers:** Any gotchas writing RLS for a multi-profile (one account → many clients) model?

### Decision H — Hosting & environments
**What it is:** Where the website lives, and keeping **dev** (testing) separate from **prod** (real users).
**Recommended default:** Static/framework frontend on **Vercel/Netlify**; database on **Supabase hosted**; if we ever add a Python API (Decision B-B), host on **Fly.io/Render**. Maintain separate dev and prod Supabase projects.
**Question for reviewers:** Simplest reliable hosting for this stack for a solo founder?

### Decision I — Secrets & keys
**What it is:** Managing API keys safely. The **anon key** is safe in the browser (protected by RLS). The **service-role key** is all-powerful and must **never** ship to the browser. Geoapify/MapTiler keys need usage restrictions.
**Recommended default:** anon key in frontend (with RLS), service-role only in backend jobs, provider keys domain-restricted, secrets in host env vars (never committed).
**Question for reviewers:** Any exposure risks specific to a static frontend calling Supabase + Geoapify directly?

---

## 5. Product-build decisions (lower risk, still notable)

### Decision J — Settings: scope & migration off localStorage
Current Settings prototype saves to the browser only. Decide which settings are account-level vs profile-level (ties to Decision D) and migrate persistence to the database.
**Question for reviewers:** Common settings that *should* be device-local (e.g., UI theme) vs account-synced?

### Decision K — Notes architecture
A polymorphic `notes` table is drafted (notes attach to client/profile/chart/comparison/search). Decide rich-text storage format (HTML vs Markdown vs structured JSON) and whether notes are per-entity only or also a standalone notebook.
**Question for reviewers:** Best rich-text storage format for portability and future AI summarization?

### Decision L — Map density / readability
Known issue: "millions of dots," clutter, labels under overlays. Needs zoom-threshold / bounding-box rendering rules.
**Question for reviewers:** Proven techniques for legible city density on an interactive map at varying zooms?

### Decision M — Billing/subscriptions (parked?)
A commercial Web2 product may eventually need payments (e.g., Stripe). Likely out of scope for v1 but should be acknowledged.
**Question for reviewers:** Should v1 design leave room for paid tiers, or ignore for now?

---

## 6. Recommended default stack (one-line summary)

> **Framework frontend** (SvelteKit/Next) → **Direct to Supabase** (anon key + **RLS**) → **Supabase Auth** (Email + Google + Apple) → reconcile schema to **account-level settings w/ optional per-profile overrides** → **GeoNames + Geoapify + MapTiler/MapLibre + offline IANA timezone** → hosted on **Vercel/Netlify + Supabase**, dev/prod split. Python `repositories/` retained for **backend/admin/AI jobs**, not the browser path.

---

## 7. Build sequence (founder's plan, annotated)

1. **Foundational forks (§2)** — must be decided before coding.
2. **Schema reconciliation + apply migrations (D, E).**
3. **Auth (C) + RLS (G)** — establishes identity + isolation.
4. **Settings backend + pages (J).**
5. **Notes page (K).**
6. **City plugins + map density + initial chart-adding (F, L).**
7. **Tie-together / full Web2 version.**
8. *(Later)* AI layer — explicitly **after** Web2 is complete.

---

## 8. Glossary (for non-dev review)

- **Supabase:** a hosted database + login service.
- **Anon key / service-role key:** a public, RLS-limited key vs an all-powerful secret key.
- **RLS (Row-Level Security):** database rules so users only see their own data.
- **Framework (React/Svelte):** toolkit for building larger interactive apps.
- **API endpoint:** a URL our own server exposes for the app to call.
- **Geocoding:** turning a place name into coordinates + country/region/timezone.
- **Map tiles:** the actual map image squares; can show labels in different languages.
- **IANA timezone database:** the standard record of timezone/DST rules over history.
