# Beta Reference Ontology v1

**Model ID:** `beta_reference_ontology_v1`
**Version:** 1.0.0
**Status:** Draft — all entries require Wizard review before production use
**Created:** 2026-06-27
**Total Entries:** 224

---

## Purpose

This is the application's first seed ontology.

It provides a conservative, modular symbolic grammar that makes the consultation system operational at beta.

It is not the permanent ontology. Every entry in this model is independently reviewable, revisable, and replaceable.

---

## What this model contains

| File | Category | Type | Entries |
|---|---|---|---|
| `01_planet_in_house.json` | Planet in House | PIH | 120 |
| `02_chiron_in_house.json` | Chiron in House | PIH | 12 |
| `03_aspect_grammar.json` | Major Aspect Grammar | ASP | 6 |
| `04_planet_angle_contacts.json` | Planet-Angle Contacts (A*C*G) | ASP | 40 |
| `05_dignity_summaries.json` | Hybrid Dignity Summaries | DIG | 36 |
| `06_orb_doctrine.json` | Default Orb Doctrine | ORB | 7 |
| `07_late_house_guidance.json` | Late-House Guidance | HEM | 3 |

---

## What this model does NOT contain

The following entry types belong to Layer 3 or Layer 4 and must not be embedded in Layer 2:

- **SUB** -- Substitution hints (Layer 4 operation)
- **REC** -- Consultation recommendations (Layer 3/4)
- **TRD** -- Tradeoff notes (Layer 3/4)
- **CLU** -- Cluster patterns (Layer 4)

---

## Entry anatomy

Each entry includes:

  "id":       "L2-PIH-SUN-10",
  "type":     "PIH",
  "subject":  { "planet": "SUN", "house": 10 },
  "content":  {
    "short_line":               "...",
    "symbolic_themes":          "...",
    "practical_tendencies":     "...",
    "traditional_associations": "...",
    "source_context":           "..."  (optional)
  },
  "envelope": {
    "status":        "Draft",
    "version":       1,
    "reviewer":      null,
    "last_reviewed": null,
    "source":        { "kind": "initial_generation", "ref": "beta_v1_2026-06-27" },
    "confidence":    "medium",
    "notes":         "...",
    "overrides":     null,
    "dependencies":  [],
    "related":       []
  }

---

## ID conventions

| Entry Type | ID Pattern | Example |
|---|---|---|
| Planet in House | L2-PIH-{PLANET}-{HH} | L2-PIH-SUN-10 |
| Chiron in House | L2-PIH-CHI-{HH} | L2-PIH-CHI-04 |
| Aspect Grammar | L2-ASP-GRAM-{ASPECT} | L2-ASP-GRAM-TRI |
| Planet-Angle Contact | L2-ASP-{PLANET}-{ANGLE}-CONJ | L2-ASP-SUN-MC-CONJ |
| Dignity Summary | L2-DIG-{PLANET}-{TYPE} | L2-DIG-SUN-DOM |
| Orb Doctrine | L2-ORB-{ASPECT} | L2-ORB-CONJ |
| Late-House Guidance | L2-HEM-{SLUG} | L2-HEM-LATE-DEG |

---

## Constitutional alignment

This ontology was generated in compliance with:

- FOUNDATIONAL_CONSTITUTION.md ss0 -- Constitutional chain (First Law, Design Spirit, Operational Test)
- FOUNDATIONAL_CONSTITUTION.md ss7.6-7.9 -- AI Constitutional Limits
- LAYER_2_AUTHORING_ARCHITECTURE.md ss0.1 -- Layer 1 / Layer 2 boundary doctrine
- AI_COMMUNICATION_DOCTRINE.md -- Content is symbolic grammar only, not consultation, prediction, or psychological profile
- PATTERN_RECOGNITION_AND_MEANING_DOCTRINE.md -- Astrology provides structure; the AI reveals patterns; the user discovers meaning

Each entry provides symbolic vocabulary, not finished narrative. Every entry leaves room for professional revision, cultural context, and user participation in meaning.

---

## Confidence levels

| Level | Meaning |
|---|---|
| high | Widely accepted across classical and modern traditions |
| medium | Common in mainstream practice; some variation exists |
| low | Contested or tradition-specific; requires specialist review |

Modern outer planet dignity assignments (Uranus/Neptune/Pluto) are medium. Some pre-modern traditional domicile assignments (Mars/SCO, Jupiter/PIS, Saturn/AQU) are marked medium as they differ from modern standard practice.

---

## Review status

All 224 entries are in Draft status.

No entry has been reviewed or approved by a professional astrologer.

This model must not be used in production consultations without Wizard review.

---

## Next steps

1. Wizard review pass -- all entries need human approval before use
2. AI-L2-2 -- Freeze entry type registry and typed field schemas
3. Founder review -- the founder's professional ontology may override any individual entry
4. Professional authors -- specialists may provide override models for specific entry sets
5. L2-P0 through L2-P8 -- full Layer 2 platform implementation

---

## Archival note

Consultations generated during beta will be pinned to this manifest version for long-term reproducibility. See MANIFEST.json for the full entry inventory.
