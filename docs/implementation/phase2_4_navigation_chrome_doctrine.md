# Phase 2.4 — Navigation Chrome Doctrine

Status: Doctrine capture (decisions only). No implementation in this phase.
Scope: Navigation chrome and top-level page surfaces. This document does NOT
redesign Profile blocks or any existing prototype structures.

---

## 0. Context

- The storage foundation is complete, and the profile-library aggregate endpoint
  is committed.
- The existing profile prototype already provides useful chart, table, favorites,
  and comparison structures. Those remain the reference.
- This phase only records navigation/surface decisions so future work has a
  stable, agreed starting point.

---

## 1. No Dashboard

- There is **no dashboard**.
- The app exposes **direct primary surfaces** — the user lands in and moves
  between real working surfaces (Map, Profile, Comparison, etc.), not a
  summarizing landing hub.

---

## 2. Current Primary Chrome (near-term)

The near-term primary navigation chrome consists of:

- Logo
- Map
- Profile
- Comparison
- Help
- Settings
- Account owner / account menu

This is the committed near-term set. Anything not in this list is not primary
chrome right now.

---

## 3. Future Chrome Candidates (not immediate)

These are acknowledged as likely future surfaces, but they are **not** part of
the immediate primary chrome:

- Store
- City Intelligence
- Transit Lab
- AI Home / AI Intake

They are parked candidates, to be promoted deliberately when their time comes.

---

## 4. City Intelligence — Status

- **Not** in primary chrome for now.
- **Subordinate to Comparison** for now.
- Its purpose is to support **final decision-making after astrology has narrowed
  the candidates** — i.e., it acts on a short list, not on the open world.
- Guardrail: avoid letting City Intelligence drift into becoming a casual
  travel-advisory replacement. It is a decision-support layer downstream of the
  astrological narrowing, not a general "where should I travel" tool.

---

## 5. Profile Page — Status

- **Do not redesign Profile blocks now.**
- The existing collapsible / profile prototype **remains the reference**.
- Possible future table order (TBD, not decided):
  1. Angle in Sign
  2. Planet in House
  3. Aspect to Angle
- It remains **TBD** whether the Profile page shows a single chart only, or also
  includes Current Location alongside the natal chart.

---

## 6. Active Profile

- The active profile / client selector remains a **Tier 1 global context**.
- The active profile should be **visible across major surfaces**, so the user
  always knows whose chart/context they are working in.

---

## 7. Comparison

- Comparison is **profile-bound** (it belongs to and is scoped by the active
  profile).
- **Profile switching during comparison** should either:
  - clear / restart the comparison context, or
  - be blocked while a comparison is active.
- The intent: a comparison must never silently mix data across profiles.

---

## Out of Scope / Do Not Touch (this phase)

- `main_centerline_FIXER.py`
- Repositories
- Schema
- Prototype HTML

This document is decisions-only and introduces no code or UI changes.
