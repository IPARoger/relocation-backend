# CITY SEARCH PRODUCTION REQUIREMENTS

**Status:** Requirements document — not an implementation plan  
**Last updated:** 2026-06-14  
**Purpose:** Define the production standard that any city search implementation must satisfy. This document is technology-agnostic. Any vendor, library, or custom solution must be evaluated against these requirements before adoption.  
**Current state:** GeoNames `ILIKE display_name%` prefix search. Functional but not production-ready.

---

## 1. USER EXPECTATIONS

Users searching for a birth city, current location, or comparison city expect the following:

### 1.1 They will type what they know, not what the database says

Users do not know canonical city names. They type:
- Nicknames: NYC, LA, SF, Chi, Philly, The Big Apple
- Abbreviations: St. Louis, Ft. Worth, Mt. Pleasant, Pt. Barrow
- Historical names: Bombay, Saigon, Peking, Calcutta, Bangalore
- Transliterated forms: Moskva / Moscow, München / Munich, Praha / Prague
- Alternate scripts: Users on non-Latin keyboards may type in their native script
- Misspellings: Chcago, Melbounre, Buenas Aries, Stockhol
- Partial names: "San Fran", "New Yor", "Los Ang"

### 1.2 They expect disambiguation when a name is ambiguous

- "Portland" → Portland OR vs Portland ME vs Portland UK
- "Springfield" → which of ~40 US cities
- "Newcastle" → New South Wales vs Tyne and Wear
- "San José" → California vs Costa Rica vs Spain
- "Victoria" → British Columbia vs Hong Kong vs Australia

### 1.3 They expect results immediately

- First result must appear within 300ms of keystroke (debounced)
- Results must degrade gracefully with imperfect queries
- A completely blank result for a known city is unacceptable

### 1.4 They expect the most relevant result first

- "New York" → New York City (pop 8.8M), not New York Mills MN (pop 1,000)
- "Paris" → Paris France (pop 2.1M) before Paris Texas (pop 26,000), unless user is in US context
- "London" → London UK before London Ontario

### 1.5 They expect context-appropriate disambiguation

- Results must show enough information to distinguish cities with the same name: country, region/state, population hint
- Display format: `City, Region, Country` or `City, Country` when unambiguous

---

## 2. GLOBAL NAME VARIANTS

This is the core challenge. Any production system must handle:

### 2.1 Abbreviations (English, common)

| Input | Expected match |
|---|---|
| NYC | New York City |
| LA | Los Angeles |
| SF | San Francisco |
| DC | Washington D.C. |
| St Louis | Saint Louis |
| St. Louis | Saint Louis |
| Ft Worth | Fort Worth |
| Ft. Worth | Fort Worth |
| Mt Fuji | Mount Fuji |
| Pt. Barrow | Point Barrow |
| N. Orleans | New Orleans |

Rule: `St.` ↔ `Saint`, `Ft.` ↔ `Fort`, `Mt.` ↔ `Mount`, `Pt.` ↔ `Point`, `N.` ↔ `North`, `S.` ↔ `South`, `E.` ↔ `East`, `W.` ↔ `West`.

### 2.2 Historical names (must map to current canonical name)

| Historical name | Canonical name | Country |
|---|---|---|
| Bombay | Mumbai | India |
| Calcutta | Kolkata | India |
| Madras | Chennai | India |
| Bangalore | Bengaluru | India |
| Saigon | Ho Chi Minh City | Vietnam |
| Peking | Beijing | China |
| Canton | Guangzhou | China |
| Nanking | Nanjing | China |
| Formosa | Taiwan (island — no single city) | — |
| Leopoldville | Kinshasa | DR Congo |
| Salisbury | Harare | Zimbabwe |
| Stalingrad | Volgograd | Russia |
| Leningrad | Saint Petersburg | Russia |
| Königsberg | Kaliningrad | Russia |
| Christiania | Oslo | Norway |
| Pressburg | Bratislava | Slovakia |
| Adrianople | Edirne | Turkey |
| Constantinople | Istanbul | Turkey |

### 2.3 Transliterations (same city, different romanization)

| Transliteration | Canonical |
|---|---|
| Moskva / Moscow | Moscow, Russia |
| München / Munchen | Munich, Germany |
| Praha / Prag | Prague, Czechia |
| Firenze / Florenz | Florence, Italy |
| Venezia / Venecia | Venice, Italy |
| Köln / Koeln / Cologne | Cologne, Germany |
| Wien / Vienne | Vienna, Austria |
| Warszawa / Varsovie | Warsaw, Poland |
| Beograd / Belgrade | Belgrade, Serbia |
| Kyiv / Kiev / Kyyiv | Kyiv, Ukraine |
| Tbilisi / Tiflis | Tbilisi, Georgia |
| Yerevan / Erevan | Yerevan, Armenia |
| Almaty / Alma-Ata | Almaty, Kazakhstan |
| Ulaanbaatar / Ulan Bator | Ulaanbaatar, Mongolia |
| Dhaka / Dacca | Dhaka, Bangladesh |
| Colombo / Kolombo | Colombo, Sri Lanka |

### 2.4 Native script input

Users may type in non-Latin scripts and expect results:
- Arabic: مكة → Mecca; بيروت → Beirut; القاهرة → Cairo
- Hebrew: ירושלים → Jerusalem
- Cyrillic: Москва → Moscow; Київ → Kyiv
- Chinese: 北京 → Beijing; 上海 → Shanghai; 香港 → Hong Kong
- Japanese: 東京 → Tokyo; 大阪 → Osaka
- Korean: 서울 → Seoul
- Hindi: मुंबई → Mumbai; दिल्ली → Delhi
- Thai: กรุงเทพ → Bangkok

This requires Unicode-aware matching against an `alternate_names` field that contains native-script variants.

### 2.5 Diacritic tolerance

Users on English keyboards typically omit diacritics:
- `Sao Paulo` → São Paulo
- `Bogota` → Bogotá
- `Zurich` → Zürich
- `Dusseldorf` → Düsseldorf
- `Malmo` → Malmö
- `Gothenburg` → Göteborg
- `Reykjavik` → Reykjavík
- `Bratislava` (no diacritics issue here, but `Banska Bystrica` → Banská Bystrica)

The system must match input without diacritics to records with diacritics.

---

## 3. TRANSLITERATION CHALLENGES

### 3.1 No single standard

Multiple romanization systems exist for the same language:
- **Chinese:** Pinyin (official), Wade-Giles (older English), Postal romanization (historical)
  - Beijing (Pinyin) = Peking (Postal) = Pei-ching (Wade-Giles)
  - Guangzhou = Canton
  - Chongqing = Chungking
- **Russian:** ISO 9, BGN/PCGN, scholarly transliteration
  - Kyiv (BGN) = Kiev (older BGN) = Kyyiv (ISO)
  - Tbilisi = Tiflis
- **Arabic:** Many competing standards, plus regional pronunciation differences
  - Jeddah / Jedda / Jidda / Jeddah (all valid)
  - Riyadh / Riyad / ar-Riyad
- **Japanese:** Hepburn (most common for English users), Nihon-shiki, Kunrei-shiki
  - Tokyo = Tōkyō
  - Osaka = Ōsaka

### 3.2 Soft rules for the production system

1. The database `alternate_names_json` column must store all known romanization variants.
2. The search layer must match user input against both `display_name` (canonical) and all entries in `alternate_names_json`.
3. The canonical name returned to the user should be the internationally recognized English name (e.g., "Beijing" not "Peking"), but either input must find it.
4. The `canonical_name` field stores the primary English romanization.

### 3.3 Ambiguous transliterations

Some transliterations are shared by multiple cities:
- "Chengdu" is unambiguous; "Changsha" vs "Changchun" vs "Changde" require disambiguation
- "Al-Khobar" / "Al Khobar" / "Alkhobar" must all match the same city

---

## 4. RANKING REQUIREMENTS

Results must be ranked by relevance, not alphabetically. The ranking function must balance:

### 4.1 Match quality (highest priority)

| Match type | Rank weight |
|---|---|
| Exact canonical name match | 1.0 |
| Exact alternate name match | 0.95 |
| Prefix canonical name match | 0.85 |
| Prefix alternate name match | 0.75 |
| Contains canonical name | 0.60 |
| Fuzzy / diacritic-stripped match | 0.50 |
| Phonetic match | 0.40 |

### 4.2 Population weight

Population is the strongest signal for disambiguation when match quality is equal:
- New York City (8.8M) must rank above New York Mills MN (1,000)
- Paris France (2.1M) must rank above Paris Texas (26,000) for equal query quality
- Weight function: `log10(max(population, 1000))` normalized to 0–1

### 4.3 User geography context (when available)

- If user's locale or IP suggests a country, apply a moderate boost to cities in that country
- This is a signal, not a hard filter — Paris France must still be findable from the US
- Boost factor: ×1.2 for same country, ×1.1 for same region

### 4.4 Result limit

- Return at most 10 results
- For common city names (Portland, Springfield, Richmond), 10 results must include both the most populous and the most likely intended matches from different countries

---

## 5. DISAMBIGUATION REQUIREMENTS

### 5.1 Required fields for disambiguation display

Every result shown to the user must include sufficient context to distinguish it:

**Minimum display set:**
- `display_name` (e.g., "Portland")
- `admin1` (region/state/province — e.g., "Oregon")
- `country_name` (e.g., "United States")
- `population` (used for UI sorting, may be shown as relative hint)

**UI format:**
```
Portland, Oregon, United States          (pop 650K)
Portland, Maine, United States           (pop 68K)
Portland, Dorset, United Kingdom         (pop 12K)
```

### 5.2 Same-name disambiguation rules

When multiple cities share a name:
1. Sort by `population DESC`
2. Always show country for all ambiguous results
3. Show admin1 (state/province) when country is not sufficient (e.g., multiple US cities named Springfield)
4. Never truncate the country field when ambiguity exists

### 5.3 Historical name disambiguation

When user types a historical name:
- Show the current canonical name as the primary result
- Include a sub-label indicating the historical name was used: e.g., "Mumbai (formerly Bombay)"
- Do not silently change what the user typed without acknowledging the mapping

---

## 6. POPULATION WEIGHTING

### 6.1 Why population matters

Population is the most reliable proxy for "how many users will search for this city." A city of 5M will be searched by vastly more users than a city of 5,000 with the same name.

### 6.2 Population data source

GeoNames `cities500.txt` includes population from GeoNames database, sourced from national censuses and Wikipedia. Accuracy varies by country. Last update varies by city.

### 6.3 Population tiers

| Tier | Population range | Examples |
|---|---|---|
| Megacity | > 10M | Tokyo, Delhi, Shanghai, São Paulo, Cairo |
| Major city | 1M – 10M | Chicago, Sydney, Toronto, Berlin |
| Large city | 200K – 1M | Denver, Cape Town, Kyoto, Lyon |
| Medium city | 50K – 200K | Ann Arbor, Galway, Chiang Mai |
| Small city | 5K – 50K | Sedona, Glastonbury, Davos |
| Town | < 5K | Include only if explicitly searched |

### 6.4 Population for ranking formula

```
population_score = log10(max(population, 100)) / log10(25_000_000)
# Normalizes to 0–1 where Shanghai (~25M) = 1.0
```

This is already implemented in `scripts/ingest_cities_to_places.py` as `importance_rank`.

### 6.5 Population data limitations

- GeoNames population data for many African, Central Asian, and Pacific cities is stale (pre-2015)
- City administrative boundaries differ by country; "city" population vs metro population varies wildly
- Historical names may have population data for the wrong time period
- No production system should rely on population alone; it is a ranking signal, not a filter

---

## 7. COUNTRY WEIGHTING

### 7.1 The "Paris problem"

"Paris" returns 12 cities in GeoNames. Paris France (2.1M) must always rank first globally. Paris Texas (26K) must rank second for US users. Paris Ontario (12K) may rank second for Canadian users.

### 7.2 Country weighting rules

1. **Absolute rule:** World population centers are not suppressed by locale. Tokyo, Mumbai, Cairo, São Paulo must always be in top results when queried by name, regardless of user country.

2. **Boost, don't filter:** User locale applies a moderate boost to same-country results, never a filter. A user in Germany must still find Seoul, Nairobi, and Buenos Aires.

3. **Country name in query:** "Paris France" must immediately return Paris France only. The country term in the query is a hard filter that overrides all weighting.

4. **Country code disambiguation:** If `country_code` is included in the query string (e.g., "London UK"), use it as a hard filter.

### 7.3 Country boosting formula

```
country_boost = 1.2 if city.country_code == user_locale_country else 1.0
final_score = match_score × population_score × country_boost
```

---

## 8. STATE/PROVINCE WEIGHTING

### 8.1 When state/province matters

State/province context is most important for:
- United States (50 states; dozens of cities share names across states)
- Canada (10 provinces; e.g., "London" → London ON vs London UK)
- Australia (6 states; "Melbourne" is unambiguous, but "Richmond" is not)
- Brazil (26 states; "São Paulo" the city vs São Paulo the state)
- India (28 states; "Agra" is in Uttar Pradesh)
- Germany (16 Länder; multiple cities share names)

### 8.2 State/province in query input

Users frequently include state/province in their query:
- "Austin TX" → Austin, Texas
- "Austin MN" → Austin, Minnesota
- "Portland ME" → Portland, Maine
- "Portland OR" → Portland, Oregon
- "London Ontario" → London, Canada

The system must parse trailing state abbreviations and postal codes as filters.

### 8.3 State abbreviation normalization

US postal codes (2-letter abbreviations) must map to full state names for display but be recognized as search filters:
- `NY` → New York state
- `CA` → California
- `TX` → Texas
- `FL` → Florida

Canadian provinces: `ON`, `BC`, `QC`, `AB`, etc.
Australian states: `NSW`, `VIC`, `QLD`, `SA`, `WA`, `TAS`, `NT`, `ACT`

---

## 9. SEARCH QUALITY METRICS

Production readiness must be verified with quantitative metrics before launch.

### 9.1 Recall@1 (most critical metric)

The percentage of queries where the correct city appears as the first result.

**Minimum required:** 85% Recall@1 on the test set below  
**Target:** 95% Recall@1

### 9.2 Recall@5

The percentage of queries where the correct city appears in the top 5 results.

**Minimum required:** 97% Recall@5

### 9.3 Required test set

The following queries must pass Recall@1 before any city search solution is considered production-ready:

```
QUERY               EXPECTED FIRST RESULT
────────────────    ────────────────────────────────────
"New York"          New York City, NY, United States
"NYC"               New York City, NY, United States
"LA"                Los Angeles, CA, United States
"SF"                San Francisco, CA, United States
"St Louis"          St. Louis, MO, United States
"Saint Louis"       St. Louis, MO, United States
"Ft Worth"          Fort Worth, TX, United States
"Fort Worth"        Fort Worth, TX, United States
"Bombay"            Mumbai, Maharashtra, India
"Mumbai"            Mumbai, Maharashtra, India
"Calcutta"          Kolkata, West Bengal, India
"Kolkata"           Kolkata, West Bengal, India
"Madras"            Chennai, Tamil Nadu, India
"Bangalore"         Bengaluru, Karnataka, India
"Bengaluru"         Bengaluru, Karnataka, India
"Saigon"            Ho Chi Minh City, Vietnam
"Ho Chi Minh"       Ho Chi Minh City, Vietnam
"Peking"            Beijing, China
"Beijing"           Beijing, China
"Canton"            Guangzhou, Guangdong, China
"Guangzhou"         Guangzhou, Guangdong, China
"Leningrad"         Saint Petersburg, Russia
"Moscow"            Moscow, Russia
"Moskva"            Moscow, Russia
"Munich"            Munich, Bavaria, Germany
"München"           Munich, Bavaria, Germany
"Vienna"            Vienna, Austria
"Wien"              Vienna, Austria
"Prague"            Prague, Czechia
"Praha"             Prague, Czechia
"Florence"          Florence, Tuscany, Italy
"Firenze"           Florence, Tuscany, Italy
"Venice"            Venice, Veneto, Italy
"Venezia"           Venice, Veneto, Italy
"Warsaw"            Warsaw, Masovian, Poland
"Warszawa"          Warsaw, Masovian, Poland
"Cologne"           Cologne, North Rhine-Westphalia, Germany
"Köln"              Cologne, North Rhine-Westphalia, Germany
"Kyiv"              Kyiv, Ukraine
"Kiev"              Kyiv, Ukraine
"Istanbul"          Istanbul, Turkey
"Constantinople"    Istanbul, Turkey
"Tehran"            Tehran, Iran
"Teheran"           Tehran, Iran
"Bangalore"         Bengaluru, Karnataka, India
"Bangkok"           Bangkok, Thailand
"Krung Thep"        Bangkok, Thailand
"Chiang Mai"        Chiang Mai, Thailand
"Podgorica"         Podgorica, Montenegro
"Reykjavik"         Reykjavík, Iceland
"Reykjavík"         Reykjavík, Iceland
"São Paulo"         São Paulo, Brazil
"Sao Paulo"         São Paulo, Brazil
"Buenos Aires"      Buenos Aires, Argentina
"Cape Town"         Cape Town, Western Cape, South Africa
"Nairobi"           Nairobi, Kenya
"Addis Ababa"       Addis Ababa, Ethiopia
"Lagos"             Lagos, Lagos State, Nigeria
"Accra"             Accra, Greater Accra, Ghana
"Kinshasa"          Kinshasa, DR Congo
"Harare"            Harare, Zimbabwe
"Salisbury"         Harare, Zimbabwe (historical)
"Taipei"            Taipei, Taiwan
"Seoul"             Seoul, South Korea
"Tokyo"             Tokyo, Japan
"Osaka"             Osaka, Japan
"Hong Kong"         Hong Kong, China
"Singapore"         Singapore, Singapore
"Kuala Lumpur"      Kuala Lumpur, Malaysia
"Jakarta"           Jakarta, Indonesia
"Manila"            Manila, Philippines
"Karachi"           Karachi, Pakistan
"Lahore"            Lahore, Pakistan
"Dhaka"             Dhaka, Bangladesh
"Colombo"           Colombo, Sri Lanka
"Kabul"             Kabul, Afghanistan
"Tashkent"          Tashkent, Uzbekistan
"Almaty"            Almaty, Kazakhstan
"Alma-Ata"          Almaty, Kazakhstan
"Ulaanbaatar"       Ulaanbaatar, Mongolia
"Ulan Bator"        Ulaanbaatar, Mongolia
```

### 9.4 Typo tolerance test set

```
QUERY               EXPECTED FIRST RESULT
────────────────    ────────────────────────────────────
"Chcago"            Chicago, IL, United States
"Melbounre"         Melbourne, Victoria, Australia
"Stockhol"          Stockholm, Sweden
"Buenas Aries"      Buenos Aires, Argentina
"Copenhagan"        Copenhagen, Denmark
"Amsterdm"          Amsterdam, Netherlands
"Lisbn"             Lisbon, Portugal
"Barcleona"         Barcelona, Spain
"Sevila"            Seville, Spain
"Napels"            Naples, Campania, Italy
```

### 9.5 Disambiguation test set

```
QUERY               EXPECTED TOP 3 CONTAIN
────────────────    ────────────────────────────────────
"Portland"          Portland OR; Portland ME; Portland Dorset
"Springfield"       Springfield IL; Springfield MO; Springfield MA
"Richmond"          Richmond VA; Richmond BC; Richmond London
"Newcastle"         Newcastle NSW; Newcastle upon Tyne
"Birmingham"        Birmingham UK; Birmingham AL
"Victoria"          Victoria BC; Victoria Seychelles; Victoria Australia
"San Jose"          San José CA; San José Costa Rica
"London"            London UK; London Ontario; London OH
```

---

## 10. CANDIDATE VENDOR REVIEW

### 10.1 GeoNames (offline dataset — current implementation)

**Type:** Offline dataset (`cities500.txt`, `alternateNamesV2.zip`)

**Strengths:**
- Free, open license, storage-allowed
- 68,032 cities with population ≥5,000 in current ingest
- Includes `alternate_names` file with 13M+ name variants across 300+ languages and transliterations
- Historical names are included in alternate names
- No API key, no per-query cost, no rate limit

**Weaknesses:**
- Current implementation uses only `display_name ILIKE query%` — no alternate names, no typo tolerance, no transliteration
- `alternateNamesV2.zip` not yet loaded into `places.alternate_names_json`
- No phonetic matching
- No abbreviation normalization (NYC, LA, SF not recognized)
- Population data stale for many cities
- Admin1 codes display as numbers in current ingest (admin1CodesASCII.txt not loaded)
- No autocomplete ranking — results sorted alphabetically, not by relevance

**Gaps to close for production readiness:**
1. Load `alternateNamesV2.zip` into `alternate_names_json` column
2. Add full-text search index on `alternate_names_json`
3. Implement abbreviation normalization pre-processing
4. Switch from `ILIKE query%` to ranked full-text search using `tsvector`/`tsquery` with weights
5. Load `admin1CodesASCII.txt` to fix region name display

**License:** Creative Commons Attribution 4.0. Storage of results is explicitly permitted.

**Verdict:** Viable foundation, but requires significant search layer work to reach production quality. Zero ongoing cost.

---

### 10.2 Geoapify

**Type:** SaaS geocoding + autocomplete API

**Strengths:**
- Storage of results explicitly permitted (key differentiator vs Google)
- Good OSM-based coverage globally
- Supports autocomplete with language parameter
- Returns structured fields: name, country, state, city, postcode
- Already referenced in project `.env.example` (`GEOAPIFY_API_KEY`)
- Handles alternate names, diacritics, transliterations at the API level
- Response includes `rank.importance` (OSM-derived popularity)

**Weaknesses:**
- Per-request cost; pricing scales with usage
- API availability dependency (results degrade if API is down)
- Coverage in less-populated countries (Central Africa, Pacific islands) is weaker than GeoNames
- Rate limits on free tier (3,000 requests/day free)
- API key must never be exposed in browser; requires server-side proxy

**Required integration pattern:**
```
Browser → POST /places/autocomplete (8004 proxy) → Geoapify API → persist to places table → return place UUID
```

**License:** Results storage explicitly permitted per Geoapify ToS (unlike Google).

**Verdict:** Best balance of quality, storage rights, and cost for a subscription product. Recommended as Layer B autocomplete over the GeoNames Layer A dataset.

---

### 10.3 Mapbox (Geocoding API + Search Box API)

**Type:** SaaS geocoding API

**Strengths:**
- Industry-leading search quality; best handling of informal names, abbreviations
- Search Box API provides session-based autocomplete with excellent ranking
- Covers 200+ countries
- Excellent handling of transliterations and alternate names
- Returns `relevance` score per result
- Well-documented, stable API

**Weaknesses:**
- **Storage rights:** Standard tier prohibits permanent storage of results. "Permanent" storage requires the Enterprise/Permanent tier at significantly higher cost.
- Most expensive option among candidates
- Vendor lock-in risk: Mapbox proprietary data, not OSM-based
- API key must be server-side proxied (never in browser)

**License:** Permanent storage of results requires Enterprise tier. **Disqualified for birth city storage at standard pricing.**

**Verdict:** Best search quality but storage rights make it unsuitable for storing birth cities and favorites without Enterprise pricing. Evaluate only if Geoapify quality proves insufficient and budget permits.

---

### 10.4 Google Places API (Autocomplete + Geocoding)

**Type:** SaaS geocoding API

**Strengths:**
- Best global coverage; highest recall on obscure cities and neighborhoods
- Best handling of informal names, abbreviations, spelling variants
- Native-script search (Arabic, Chinese, Cyrillic, etc.) is best-in-class
- Extremely well-known developer API; extensive documentation

**Weaknesses:**
- **Storage rights: PROHIBITED.** Google Places ToS explicitly forbids storing autocomplete results or geocoding data in a database. Birth city storage, favorites, comparison cities — all would violate ToS.
- Highest per-request cost at scale
- Requires Google Cloud Console account, billing, OAuth setup
- API key exposure risk

**License:** Permanent storage of results is **prohibited** by Google Places ToS. **Disqualified for this product.** Birth cities, current locations, and favorites require permanent storage.

**Verdict:** Disqualified. Do not use for any flow that stores city data in the database.

---

### 10.5 Photon

**Type:** Open-source geocoder (OSM data); can be self-hosted

**Strengths:**
- Free, open source, no API key required
- OSM-based; global coverage
- Supports multiple languages for same-query results
- Can be self-hosted; no external dependency
- Storage explicitly permitted (OSM ODbL license)
- Handles diacritics, Unicode well
- Returns `osm_id` for deduplication

**Weaknesses:**
- Self-hosting requires infrastructure (Java, Elasticsearch, ~50GB data)
- Hosted instance (photon.komoot.io) has usage limits and no SLA
- Ranking is not as sophisticated as commercial vendors
- Alternate names coverage dependent on OSM contributor quality
- No abbreviation handling (NYC → New York City) — requires preprocessing layer
- Population ranking weaker than GeoNames

**License:** OSM ODbL — storage explicitly permitted.

**Verdict:** Excellent for self-hosted deployments where cost is paramount. Ranking and abbreviation handling require custom work. Viable if Geoapify proves too expensive at scale.

---

### 10.6 Pelias

**Type:** Open-source geocoder (multiple data sources); designed for self-hosting

**Strengths:**
- Modular: can ingest GeoNames + OSM + Who's on First + OpenAddresses simultaneously
- GeoNames alternate names support out-of-the-box
- REST API compatible with many clients
- Storage permitted (open data sources)
- Active community; used by transit agencies globally
- Supports fuzzy search, multilingual queries

**Weaknesses:**
- Self-hosting requires significant infrastructure (Elasticsearch, multiple Docker containers)
- Operational complexity: ingest pipeline, index rebuilds, monitoring
- Abbreviation handling requires custom configuration
- Cold start time for initial ingest is substantial (hours for global dataset)
- Engineering resources required to maintain

**License:** MIT (software); data licenses depend on sources ingested.

**Verdict:** Best self-hosted option for production-grade quality with full control. High operational cost. Recommended only if infrastructure investment is justified.

---

### 10.7 Nominatim (OpenStreetMap)

**Type:** Open-source geocoder (OSM data only); can be self-hosted

**Strengths:**
- OSM-based; global coverage; free
- Storage permitted (OSM ODbL)
- Handles many alternate names via OSM `name:XX` tags
- Well-understood, widely deployed

**Weaknesses:**
- **Not designed for autocomplete.** Nominatim is a structured search engine, not a typeahead system.
- Slow for prefix/partial queries without significant caching
- OSM data quality varies heavily by region (excellent in Europe, weaker in parts of Africa and Asia)
- No population-based ranking; results ordered by OSM relevance score only
- Abbreviation handling (NYC, LA) is poor without preprocessing
- Self-hosting requires PostgreSQL with OSM import (~1TB for full planet)
- Public instance (nominatim.openstreetmap.org) has strict usage limits (1 req/sec max, no production use)

**License:** OSM ODbL — storage permitted.

**Verdict:** Not suitable as a primary autocomplete source. Acceptable as a geocoding validation tool or fallback for addresses.

---

## 11. PRODUCTION STANDARD SUMMARY

Any city search implementation must satisfy ALL of the following before being considered production-ready:

### 11.1 Functional requirements

| Requirement | Current GeoNames | Geoapify | Pelias |
|---|---|---|---|
| Prefix search | ✓ (ILIKE only) | ✓ | ✓ |
| Alternate name search | ✗ | ✓ | ✓ |
| Historical name search | ✗ | Partial | ✓ |
| Abbreviation normalization | ✗ | ✓ | Requires config |
| Diacritic-stripped match | ✗ | ✓ | ✓ |
| Native script input | ✗ | Partial | ✓ |
| Fuzzy/typo tolerance | ✗ | ✓ | ✓ |
| Population-based ranking | Partial (importance_rank) | ✓ | ✓ |
| Disambiguation display | Partial | ✓ | ✓ |
| Storage rights | ✓ | ✓ | ✓ |
| No per-query cost | ✓ | ✗ | ✓ (self-hosted) |

### 11.2 Data requirements

The `places` table must contain, for each city:

| Field | Current status | Required |
|---|---|---|
| `display_name` | ✓ | ✓ |
| `canonical_name` | ✓ | ✓ |
| `latitude` / `longitude` | ✓ | ✓ |
| `country_code` | ✓ | ✓ |
| `country_name` | ✓ | ✓ |
| `admin1` (full name) | Partial (codes only) | ✓ |
| `timezone_id` | ✓ | ✓ |
| `population` | ✓ | ✓ |
| `importance_rank` | ✓ | ✓ |
| `geonames_id` | ✓ | ✓ (for deduplication) |
| `alternate_names_json` | ✗ not loaded | ✓ required for production |
| Full-text search index | ✗ not created | ✓ required for production |

### 11.3 Minimum acceptance criteria

Before any city search solution is deployed to production users:

1. **Recall@1 ≥ 85%** on the required test set in §9.3
2. **Recall@5 ≥ 97%** on the required test set
3. **"Bombay" → Mumbai** must pass (top test for historical name support)
4. **"NYC" → New York City** must pass (top test for abbreviation support)
5. **"Praha" → Prague** must pass (top test for transliteration)
6. **Response time ≤ 300ms** at p95 (after 300ms debounce)
7. **Storage rights confirmed** in writing or ToS for all data sources used
8. **No Google Places API** used for any stored data
9. **Disambiguation display** includes at minimum: city, region, country
10. **Typo tolerance**: at least 1-character edit distance handled (drop/swap/insert)

---

## APPENDIX: GeoNames Alternate Names — Path to Production

The fastest path to production-quality search without a subscription API is loading `alternateNamesV2.txt` into the existing infrastructure.

**GeoNames file:** `alternateNamesV2.txt` — 13.4M rows covering 300+ languages, historical names, abbreviations, and transliterations.

**Implementation steps:**
1. Download `alternateNamesV2.zip` from `https://download.geonames.org/export/dump/`
2. For each `geoname_id` in `places`, collect all alternate name rows into a JSON array
3. Store in `places.alternate_names_json`
4. Create a PostgreSQL full-text search index using `tsvector` on `display_name || ' ' || canonical_name || ' ' || alternate_names_text`
5. Replace `ILIKE display_name%` with `to_tsquery` ranked search
6. Add client-side abbreviation pre-processing for `NYC→New York`, `St→Saint`, `Ft→Fort`, etc.
7. Re-run Recall@1 test suite to verify improvement

This approach requires no subscription, no new infrastructure, and no vendor dependency. It would bring the current GeoNames implementation from approximately 60% Recall@1 to an estimated 88–92% Recall@1 for the required test set.
