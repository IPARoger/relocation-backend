# Geocoder and City Strategy (From Archaeology)

---

## Why cities are core (not decoration)

Relocation decisions happen at **named places**; the map must connect semantically rich astrology overlays to **human geography**.

## Readability and density

- Problems cited: “millions of dots,” uneven clutter, ocean contrast issues for lines, labels obscured under overlays.
- Philosophy appears: optimize **cities per square inch / screen area**, not population alone.
- Zoom-threshold approaches and bounding-box rendering recur as prototypes.

---

## Search and disambiguation

- First-match jumps fail for duplicate names (Springfield, Portland, etc.).
- Need structured results: city + region/state + country + coordinates + optional population; **ranking by human relevance**, not only database order.

---

## Internationalization

- Non-Latin labels and mixed scripts complicated manual validation.
- Need transliteration, alternate spellings, historical names (Bombay/Mumbai), and “Astro.com naming alignment” for repeatable validation sessions.

---

## Provider strategy tension (open)

- Leaflet/OSM friction: labels, wrapping, performance, aesthetic “boutique map” goals.
- Google/Mapbox/MapLibre each offers different tradeoffs: licensing, vector picking, custom styling, offline potential.

**Archaeology consensus:** do not migrate prematurely; separate canonical geometry from display; reassess after display adapter maturity.

---

## Dataset anecdotes (process lessons)

GeoNames-style parsing mistakes (wrong column for population → empty city lists) show **schema verification** must be part of ingestion—not assumed.

---

## UX details that affect trust

“Undefined” country fields were **metadata display** bugs, not necessarily failed search—diagnostic categories matter.
