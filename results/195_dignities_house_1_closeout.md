# DIGNITIES-HOUSE-1 Closeout

**Date:** 2026-06-21  
**Scope:** House-correspondence PIH dignity styling + `?` help. No dignity diffs, scoring, or chart math changes.

---

## Summary

PIH dignity cell backgrounds now use **`lookupFamilyByHouse(planet, house)`** — natural zodiac mapping (1=Aries … 12=Pisces) + existing `BY_PLANET` table. Relocated **house** drives styling, not birth **sign**. Collapsed families unchanged: rulership+exaltation → supportive; detriment+fall → challenging.

---

## Files changed

| File | Change |
|------|--------|
| `dignity_ontology.js` | `NATURAL_HOUSE_SIGNS`, `lookupFamilyByHouse()` |
| `app_shell.html` | PIH house lookup, `?` help, footer updates, settings copy |
| `scripts/smoke_dignities_house.py` | Unit + static validation (12 checks) |
| `scripts/smoke_comparison_sets.py` | `static_dignities_house_checks` (5) |

---

## Mapping behavior

```text
sign = NATURAL_HOUSE_SIGNS[house - 1]   // 1→Aries, 2→Taurus, … 12→Pisces
relationship = BY_PLANET[planet][sign]
family = supportive | challenging | null
```

| Example | House | Via sign | Family |
|---------|-------|----------|--------|
| Moon | 2 | Taurus (exaltation) | supportive |
| Sun | 7 | Libra (fall) | challenging |
| Sun | 1 | Aries (exaltation) | supportive |
| Uranus | any | — | null (unmapped) |

No visual split between rulership vs exaltation or detriment vs fall.

---

## Surfaces updated

| Surface | Dignities toggle | `?` help |
|---------|------------------|----------|
| **Relocated Profile page** PIH | Yes (default OFF) | Yes |
| **Comparisons page** columns PIH | Yes (persisted) | Yes |
| Map popup | No | No |
| Quick Share | No | No |
| Workbook PIH | No (placeholder) | No |

---

## Diffs interaction

Unchanged: Diffs fades identical **house numbers** only. Dignity tint follows house; not a separate diff category.

---

## Help copy (`?`)

Brief disclosure: traditional dignities apply to signs; relocation changes houses not signs; natural-zodiac house correspondence; Moon H2 / Sun H7 examples; subtle overlay not a score; default off for neutrality.

---

## Validation

| Script | Result |
|--------|--------|
| `python3 scripts/smoke_dignities_house.py` | **12/12 PASS** |
| `static_dignities_house_checks` | **5/5 PASS** |

Proved: Moon H2 supportive, Sun H7 challenging, PIH uses house lookup not sign, `?` help present, no dignity diff logic, no scoring language in help block.

---

## Known limits

1. Sun–Saturn only — outer planets / Chiron unmapped (no tint).
2. Green/amber CSS unchanged (blue/red Appearance slice deferred).
3. No per-relationship labels in cells or tooltips v1.
4. Workbook PIH section still placeholder.
5. `lookupFamily(planet, sign)` retained for non-PIH callers but PIH no longer uses sign path.

---

## Rollback scope

Revert DIGNITIES-HOUSE-1 commit. PIH reverts to sign-based `lookupFamily` (prior behavior). Remove `lookupFamilyByHouse` export and help UI.

---

## Commit

```
DIGNITIES-HOUSE-1: use house correspondence for PIH dignities
```
