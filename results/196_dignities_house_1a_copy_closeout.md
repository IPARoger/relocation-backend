# DIGNITIES-HOUSE-1A Closeout — Help & Settings Copy Alignment

**Date:** 2026-06-21  
**Scope:** Copy-only alignment for PIH dignity disclosure. No behavior, color, persistence, or lookup changes.

**Builds on:** `results/195_dignities_house_1_closeout.md`, `results/194_dignities_house_doctrine_1.md`

---

## Summary

Aligns user-facing dignity doctrine across the PIH `?` help and Settings surfaces. Documents the intentional two-color simplification (Rulership+Exaltation vs Detriment+Fall), ontology preset options (Modern / Ancient / Hybrid default / Advanced custom), and Appearance links for optional Exaltation/Fall colors — all as disclosure only; no new wiring.

---

## Copy surfaces updated

| Surface | Location | What changed |
|---------|----------|--------------|
| **PIH `?` help** | `PIH_DIGNITIES_HELP_COPY` + `pihDignitiesHelpHtml()` | Two-color simplification in main paragraph; ontology preset paragraph with link to Astrology settings; Exaltation/Fall color paragraph with link to Appearance settings |
| **Settings → Astrology → Dignities** | `dignitiesDisplayHtml()` | Two-color doctrine; Appearance link for optional Exaltation/Fall colors; ontology preset list (Modern, Ancient, Hybrid default, Advanced) with Coming soon badge |
| **Settings → Appearance → Dignity colors** | `dignityAppearanceHtml()` + `settingsDisplayBodyHtml()` | New stub section: two-color default explanation; Exaltation color / Fall color stub rows; Coming soon badge |

**Surfaces unchanged:** PIH toggle behavior, `lookupFamilyByHouse`, CSS colors (`#eef7f3` / `#faf3e8`), Diffs mode, Quick Share, map, P2P, wheel, settings persistence, `dignity_ontology.js`, smoke script.

---

## Exact copy additions (doctrine)

1. **Two colors, not four** — Rulership and Exaltation share one overlay (generally positive); Detriment and Fall share one (generally difficult).
2. **Ontology presets** — Modern, Ancient, Hybrid (default), or Advanced (custom system); configured in Astrology settings (Coming soon).
3. **Optional color customization** — Separate Exaltation and Fall colors under Appearance settings (Coming soon).

---

## Validation

| Script | Result |
|--------|--------|
| `python3 scripts/smoke_dignities_house.py` | **12/12 PASS** |

No smoke script changes required; existing static checks still pass.

---

## No behavior changes

- No dignity diffs
- No color CSS changes
- No settings save/load changes
- No ontology table or lookup changes
- No Quick Share, map, P2P, wheel, or Diffs changes

---

## Rollback scope

Revert DIGNITIES-HOUSE-1A commit. Restores prior help copy (single paragraph, no preset/color links) and removes Appearance Dignity colors stub section. DIGNITIES-HOUSE-1 house lookup and styling remain intact if only this commit is reverted.

---

## Commit

```
DIGNITIES-HOUSE-1A: align dignity help and settings copy
```
