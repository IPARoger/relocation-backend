# Layer 2 Authoring Platform Architecture

**Status:** Canonical architecture doctrine — not active Beta implementation
**Date:** 2026-06-27
**Mode:** Architecture and product design only — no interpretive content, no Layer 2 entries, no migrations, no production code
**Authority:** Subordinate to [FOUNDATIONAL_CONSTITUTION.md](../constitutional/FOUNDATIONAL_CONSTITUTION.md)
**Companions:** [AI_CONSULTATION_ARCHITECTURE.md](AI_CONSULTATION_ARCHITECTURE.md) · [INTENT_TRANSLATION_ENGINE.md](INTENT_TRANSLATION_ENGINE.md) · [AI_COMMUNICATION_DOCTRINE.md](AI_COMMUNICATION_DOCTRINE.md)

> **Promotion rule:** This document describes future platform capability. Nothing here becomes active until explicitly promoted into an implementation plan with scope, migration plan, validation gate, and rollback path. The Beta ships with exactly one default model. This architecture exists so that decision does not have to be revisited when the second author arrives.

> **Design ethic (FOUNDATIONAL_CONSTITUTION.md §0.2):** Reveal, don't impose. The authoring platform reveals an astrologer's own method back to them as structure they can inspect, version, and own. It never imposes a method, and it never silently rewrites one.

---

## 0. Framing: a knowledge platform, not a content store

The objective is **not** to store interpretations. The objective is to let astrologers build, review, revise, version, audit, and publish their own interpretive models over a span of years — the way a writer builds a body of work, not the way a form collects answers.

The architectural reference points are **WordPress, Notion, and Obsidian**, not an astrology textbook:

| Reference | Lesson borrowed |
|-----------|-----------------|
| WordPress | Every unit of content is an addressable object with a stable permalink, revision history, and a publish/draft lifecycle |
| Notion | Content is structured data with typed properties, not freeform prose; the same data renders many ways |
| Obsidian | Entries link to one another; the value is in the graph of relationships, not the individual note |

The single most important architectural commitment follows from this framing:

> **Every Layer 2 entry is an addressable, identity-bearing object — not a paragraph inside a file.**

Everything else in this document is a consequence of that commitment.

---

## 1. The entry is the atomic unit

A Layer 2 model is not a document. It is a **collection of independently addressable entries**. The entry — not the model, not the file — is the unit of authorship, review, versioning, inheritance, and reuse.

This is the difference between "page 187 of a markdown file" and "find the Saturn-in-12th entry." When an astrologer thinks *I want to revisit Saturn in the 12th* six months from now, the platform resolves that thought to **one object**, not a scroll position.

### 1.1 Entry identity

Every entry carries a **stable canonical ID** that never changes once assigned, even as the entry's content is revised across years.

```
L2-PIH-SUN-10
│  │   │   └── qualifier (house 10)
│  │   └────── subject (Sun)
│  └────────── entry type (Planet-In-House)
└───────────── Layer 2 namespace
```

The ID is **content-independent and version-independent**. Revising the prose for `L2-PIH-SUN-10` a hundred times never changes its ID. This stability is what makes long-term addressing, cross-references, and review queues possible.

### 1.2 Entry type registry

Entry types are a closed, versioned vocabulary (extensible by platform release, not by individual authors). Illustrative types:

| Type code | Meaning | Example ID |
|-----------|---------|------------|
| `PIH` | Planet in house | `L2-PIH-SAT-12` |
| `PIS` | Planet in sign | `L2-PIS-VEN-LIB` |
| `ASP` | Aspect between bodies/points | `L2-ASP-SUN-MC-TRINE` |
| `DIG` | Dignity rule | `L2-DIG-MAR-DOMICILE` |
| `ORB` | Orb configuration | `L2-ORB-MAJOR-DEFAULT` |
| `HEM` | House emphasis / weighting | `L2-HEM-ANGULAR` |
| `CLU` | Archetype cluster (feeds Translation Engine §2) | `L2-CLU-CAREER-RECOGNITION` |
| `REC` | Search recipe / cookbook entry | `L2-REC-CAREER-EXPRESSIVE` |
| `TRD` | Tradeoff preference | `L2-TRD-DIGNITY-OVER-EXACTNESS` |
| `SUB` | Substitution strategy | `L2-SUB-SUN-1ST` |
| `LNG` | Explanatory language / terminology | `L2-LNG-DETRIMENT` |

The type registry is the schema contract between Layer 2 and its consumers (Engine, Navigator, Guardian, Translation Engine). A new entry type is a platform-level change with its own consumer-compatibility review.

### 1.3 The entry object

Each entry separates a **content payload** from a **metadata envelope**. Consumers read the payload; the platform manages the envelope.

```
Entry
├── id                 L2-PIH-SAT-12              (immutable canonical ID)
├── type               PIH                         (from the type registry)
├── subject            { planet: SAT, house: 12 }  (structured, machine-usable)
├── content            { ... typed fields ... }    (the interpretive payload — see §1.4)
└── envelope
    ├── status         Approved                    (lifecycle state — §4)
    ├── version        7                           (current version number — §3)
    ├── last_reviewed  2026-06-20
    ├── reviewer       <author identity>
    ├── source         { kind, ref }               (provenance — §5)
    ├── confidence     high | medium | low | unset
    ├── notes          (author-private working notes)
    ├── overrides      L2-PIH-SAT-12@default        (what this entry overrides — §2)
    ├── dependencies   [ L2-DIG-SAT-FALL, ... ]     (entries this one relies on — §1.5)
    └── related        [ L2-PIH-SAT-1, ... ]        (soft links — §1.5)
```

The metadata envelope is what makes the entry feel like a managed object rather than a block of text. It is the WordPress revision bar, the Notion property panel, and the Obsidian backlink pane, unified onto one object.

### 1.4 Content payload is typed, never raw markdown

The content payload is a set of **typed fields**, not a freeform blob. The exact field set is defined per entry type (a `PIH` entry and an `ORB` entry have different fields). The platform never asks an author to edit raw markdown or JSON; the Wizard (§9) renders typed fields as a writing studio.

Typing the payload serves three architectural goals:

1. **Multi-surface rendering** — the same entry feeds a Navigator explanation, an inline citation, a Cookbook recipe, and a Translation Engine cluster without per-surface authoring.
2. **Partial completeness** — an author can fill the short consumer-facing line and leave the deep teaching paragraph blank; blank fields fall back (§6) rather than breaking.
3. **Validation** — the platform can check that an `ORB` entry contains a number, that an `ASP` entry references valid bodies, etc.

### 1.5 The entry graph

`dependencies` and `related` turn the model from a list into a graph (the Obsidian lesson).

- **Dependencies** are hard: if `L2-PIH-SAT-12` is written in terms of Saturn's dignity, it depends on `L2-DIG-SAT-FALL`. Changing a dependency flags dependents for re-review (§4.3).
- **Related** are soft: navigational links the Wizard uses for "walk me through every Saturn placement" without implying a logical dependency.

The graph is what lets the platform answer "what else is affected if I change this?" — a question a pile of text cannot answer.

---

## 2. Inheritance: Default → Professional Override

### 2.1 Models are layered namespaces

A **Model** is a named namespace of entries owned by an author. There is always exactly one **Default Model** (platform-owned, ships with Beta). Professional models are **overlays** on top of the Default Model.

```
Resolved Model (what a consumer actually sees)
        ▲
        │  per-entry resolution
        │
┌───────┴────────┐
│ Professional   │   sparse: contains only the entries the author chose to override
│ Override Model │
└───────┬────────┘
        │ falls through to
┌───────┴────────┐
│ Default Model  │   complete: contains an entry for every required key
└────────────────┘
```

### 2.2 Per-entry resolution (copy-on-write)

Resolution is computed **per entry ID**, not per model:

> For entry key `K`, the resolved entry is the override model's entry for `K` if one exists and is active; otherwise the Default Model's entry for `K`.

This is copy-on-write inheritance. A professional model is **sparse** — it stores only the entries the author has actually touched. An author who loves everything except the Venus material **forks only the Venus entries**; the other several hundred entries continue to resolve to the Default Model automatically.

This directly answers the modularity requirement (§11): overriding one entry never duplicates the rest.

### 2.3 Forking an entry

"Fork" = copy-on-write of a single entry from a parent model into the author's override model.

```
L2-PIS-VEN-LIB@default  ──fork──►  L2-PIS-VEN-LIB@author
                                   envelope.overrides = L2-PIS-VEN-LIB@default
                                   envelope.source    = { kind: forked, ref: default@v3 }
```

The fork records **what it overrode and at what version**. This is what lets the platform later say "the default Venus-in-Libra entry has been updated since you forked it — would you like to review the differences?"

### 2.4 Multi-level inheritance (future)

The architecture permits more than two layers (e.g., Default → Institutional/School model → Individual professional). Resolution remains the same fall-through algorithm applied down an ordered chain. Beta assumes two layers; the algorithm does not need to change to support more.

---

## 3. Versioning

Two independent versioning planes, because authors revise entries continuously but consume models as coherent snapshots.

### 3.1 Entry version history (append-only)

Each entry has an **append-only version log**. Saving a change creates a new immutable version record; prior versions are never mutated or deleted.

```
L2-PIH-SAT-12
├── v1  draft        2025-11-02  source: manual
├── v2  ai_suggested 2025-11-04  source: reading-upload R-014
├── v3  approved     2025-11-09  reviewer: <author>
├── ...
└── v7  approved     2026-06-20  reviewer: <author>   ← current
```

Append-only history gives the WordPress revision bar: diff any two versions, roll back to a prior version (which creates a *new* version equal to the old content — history is never rewritten), and audit who changed what when.

### 3.2 Model manifest version (a snapshot)

A **Model Manifest** pins a specific entry version for every key the model resolves. Publishing a model produces an immutable manifest:

```
Model "Author-X Method" — Manifest v12
├── L2-PIH-SUN-10  → author@v4
├── L2-PIH-SAT-12  → author@v7
├── L2-PIS-VEN-LIB → author@v2
├── L2-DIG-MAR-...  → default@v3      (inherited; pinned to the default version in force)
└── ... (every required key resolved and pinned)
```

A manifest is a **reproducible compilation** of the model at a moment in time. It is what consultations pin (§7) and what consumers load (§8). Editing entries after publishing does not alter an existing manifest; it produces a *new* manifest when the author next publishes.

### 3.3 Why two planes

| Plane | Granularity | Mutability | Purpose |
|-------|-------------|------------|---------|
| Entry version log | One entry | Append-only | Authorship, diff, rollback, audit |
| Model manifest | Whole model | Immutable once published | Reproducibility, consumption, consultation pinning |

Authors live in the entry plane. Consumers live in the manifest plane. The platform translates between them.

---

## 4. Approval lifecycle

### 4.1 States

Every entry version carries one lifecycle state:

| State | Meaning | Consumed by Engine/Navigator? |
|-------|---------|-------------------------------|
| **Draft** | Author is actively writing; incomplete | No |
| **AI Suggested** | Drafted by AI (reading upload or assistance); awaiting human attention | No |
| **Needs Review** | Flagged for human review (new, changed dependency, or conflict) | No |
| **Approved** | Human-approved; eligible for publication and consumption | Yes (when published in a manifest) |
| **Deprecated** | Superseded but retained; resolves only if nothing newer is approved | Conditionally |
| **Archived** | Removed from active resolution; retained for history | No |

### 4.2 State machine

Transitions are explicit and audited. Illustrative allowed transitions:

```
Draft ──────────────► Needs Review ──────────► Approved
  ▲                        ▲                      │
  │                        │                      ▼
AI Suggested ──────────────┘                  Deprecated ──► Archived
                                                   ▲             │
                                                   └─────────────┘
```

**Constitutional invariant:** nothing reaches **Approved** without an explicit human action. AI may move an entry *into* `AI Suggested` or `Needs Review`; only a human moves it to `Approved` (§12).

### 4.3 Review triggers

An entry is moved to **Needs Review** automatically when:

- It is newly created by AI (`AI Suggested` → surfaced in the review queue)
- A **dependency** (§1.5) changes version after this entry was approved
- A **conflict** is detected (e.g., an uploaded reading contradicts the approved content — §5)
- The **parent default entry** changes after this entry was forked (§2.3)

These triggers are how the platform protects an author from silent drift: approved content can become *stale*, but it is flagged, never quietly altered.

---

## 5. Reading upload → candidate entries

Reading upload is a **pre-population pipeline**, not an import. The Ontology Assistant (an AI role, never user-facing as an authority) reads anonymized professional readings and proposes entries.

### 5.1 Pipeline

```
Anonymized readings
      │
      ▼
Ontology Assistant extraction
      │
      ├── candidate content payloads (typed, per entry type)
      ├── provenance: which reading(s) suggested this  → envelope.source
      ├── confidence: how consistently it appeared      → envelope.confidence
      └── conflict flags: contradicts an approved entry?
      │
      ▼
Entries created in state = AI Suggested
      │
      ▼
Surfaced in the Wizard review queue (§9) — never auto-approved
```

### 5.2 Provenance and confidence are first-class

Every AI-suggested entry records:

- **Source**: the reading(s) it was derived from (`envelope.source.kind = reading-upload`, `ref = R-014`)
- **Confidence**: derived from consistency across readings (`high` if the theme recurred across many readings; `low` if it appeared once)

This lets the Wizard offer "review only AI-generated entries, highest-confidence first" and lets the author trust or distrust a suggestion with its evidence attached.

### 5.3 Conflict handling is non-confrontational

If an upload contradicts an existing **Approved** entry, the platform does **not** overwrite. It creates a *new* `AI Suggested` version and flags a conflict for review, framed as opportunity, not correction (per AI_CONSULTATION_ARCHITECTURE.md §14 and AI_COMMUNICATION_DOCTRINE.md). The approved version remains in force until a human decides.

### 5.4 Style is extracted separately

Communication style (warmth, density, caution, directness) is extracted into a **separate Style profile**, never mixed into ontology entries (per AI_CONSULTATION_ARCHITECTURE.md §14). Style governs *how* AI speaks; ontology governs *what the symbols mean*. They are different objects with different lifecycles.

---

## 6. Fallback

Fallback is the safety net that makes partial authorship viable.

### 6.1 Three states of an entry key in an override model

| State | Meaning | Resolves to |
|-------|---------|-------------|
| **Overridden** | Author has an active approved entry for this key | The author's entry |
| **Absent** | Author has no entry for this key | The Default Model entry (automatic) |
| **Intentionally blank** | Author created an entry but left fields empty | Field-level fallback to Default (§6.2) |

### 6.2 Field-level fallback

Fallback operates at the **field** level, not just the entry level. If an author overrides the short consumer line of `L2-PIH-SUN-10` but leaves the deep teaching paragraph blank, the resolved entry uses the author's short line and the Default Model's teaching paragraph. This lets authors override surgically — a sentence, not a whole entry.

### 6.3 Fallback is always to the Default Model

There is always a complete Default Model beneath every override model, so resolution can never fail to produce a usable entry. A required key can never be unresolvable. This is an architectural guarantee, not a runtime hope.

---

## 7. Consultation model pinning

A saved consultation must be **reproducible years later**. To achieve this it pins the exact model state it was conducted under.

### 7.1 What a consultation stores

```
Saved Consultation
├── ...consultation canon...
└── model_binding
    ├── model_id          "Author-X Method"
    ├── manifest_version  12
    └── resolved_digest   <hash of the full entry-version map>
```

Because a manifest (§3.2) is immutable and pins every entry to a specific version, storing `model_id + manifest_version` is sufficient to reconstruct exactly what every symbol meant during that consultation — even if the author has since revised hundreds of entries.

### 7.2 Re-running an old consultation

When an old consultation is reopened, the platform loads its pinned manifest, not the author's current model. The Navigator may *offer* to re-run under the current model and show what changed, but the historical consultation is never silently reinterpreted under newer content. (Reveal the change; don't impose it.)

---

## 8. Consumption: how Engine, Navigator, and Guardian read Layer 2

Layer 2 is **read-only** to all three AI roles. None of them writes to it. They consume a **resolved manifest** (§3.2), each using different facets of the entry payload.

| Consumer | Reads | Does not read |
|----------|-------|---------------|
| **Engine** (deterministic search/optimization) | Structured `subject`, `ORB`, `DIG`, `HEM`, `REC`, `CLU`, `SUB` fields — the machine-usable parameters | Prose teaching fields |
| **Navigator** (user-facing voice) | `LNG`, consumer-facing lines, teaching paragraphs, citations | Author-private `notes` |
| **Guardian** (audit) | The *resolved manifest version* itself, plus provenance | — |

### 8.1 The resolved-manifest contract

Consumers never resolve inheritance themselves. The platform compiles a manifest into a flat **Resolved Model** (every key → one entry payload at one version) and hands that to consumers. This keeps inheritance/versioning logic in one place and gives consumers a stable, flat read model.

### 8.2 Guardian's special role

The Guardian (AI_CONSULTATION_ARCHITECTURE.md §2) audits that:

- The manifest version a consultation used is recorded and traceable
- No consumer output cites content that isn't in the resolved manifest (no fabricated ontology)
- AI-suggested or draft content never leaked into a user-facing surface (only Approved-and-published content is consumed)

Guardian enforces the boundary between *authored truth* and *AI invention* at consumption time.

---

## 9. The Wizard: workflow, not UI

This section designs the **underlying workflow** the future Wizard sits on. It does not design the UI. The Wizard should feel like a welcoming writing studio; architecturally, that feeling is produced by three capabilities: **addressing, work queues, and sessions.**

### 9.1 Addressing (query over entries)

Because every entry is an identity-bearing object with a typed envelope, the platform supports queries the Wizard turns into natural actions:

| Author intent | Underlying query |
|---------------|------------------|
| "Search by placement" | entries WHERE subject matches |
| "Walk me through every Saturn placement" | entries WHERE subject.planet = SAT, ordered |
| "Review all relationship placements" | entries WHERE related ∋ relationship-domain OR type ∈ {7th-house, Venus, …} |
| "Show entries needing review" | entries WHERE status = Needs Review |
| "Review only AI-generated entries" | entries WHERE source.kind = reading-upload OR ai-assist |
| "Continue where I left off" | resume the author's open review session (§9.3) |
| "Resume unfinished review" | the work queue with unreviewed items remaining |

None of these are possible against a markdown file. All of them are trivial against addressable entries.

### 9.2 Work queues

A **work queue** is a persisted, ordered set of entry references with progress state — the backbone of "review all X." A queue is generated from a query (§9.1) and remembers which items are done.

```
Review Queue "Saturn placements"
├── generated from: subject.planet = SAT
├── L2-PIH-SAT-1   ✓ reviewed
├── L2-PIH-SAT-12  ◻ pending   ← cursor
└── ...
```

Queues are what make a multi-hundred-entry model feel walkable rather than overwhelming.

### 9.3 Review sessions

A **session** binds an author to a queue with a cursor and timestamps, so "continue where I left off" resolves to an exact entry. Sessions are durable across days and devices. This is the Notion lesson: the work has state, and the platform remembers it.

### 9.4 The Wizard never exposes raw markdown

The Wizard reads and writes **typed fields** on entry objects (§1.4). Serialization (markdown, JSON, database rows) is an implementation detail beneath the Wizard. An author edits "the short line" and "the teaching paragraph," not a file.

---

## 10. Review and export

Authors must always be able to **export, review, approve, revise, and replace** without editing raw files.

| Operation | Architecture |
|-----------|--------------|
| **Export** | Render a model manifest (or any entry subset) to a portable, human-readable package. Export is a *projection* of typed entries, not the source of truth. |
| **Review** | Open entries via queues/sessions (§9); diff versions (§3.1) |
| **Approve** | Human state transition to Approved (§4.2) |
| **Revise** | Create a new entry version (append-only, §3.1) |
| **Replace** | Deprecate the old version, approve a new one; history retained (§4) |

### 10.1 Export is a projection, never the master

Critically, **the database of entries is the source of truth; an exported file is a snapshot.** This inverts the Obsidian default (files-as-truth) deliberately: identity, versioning, inheritance, and review state cannot live in flat files. Export exists for portability, backup, and human reading — re-import is a *reconciliation* against entry IDs, not a wholesale overwrite.

### 10.2 Round-trip safety

Because every entry has a stable ID, an exported-then-edited-then-reimported entry reconciles to the *same object* (a new version of `L2-PIH-SAT-12`), not a duplicate. IDs make round-tripping safe.

---

## 11. Modularity (restated as a guarantee)

The copy-on-write override model (§2.2) yields the modularity guarantee directly:

> A professional may override any single entry without duplicating any other entry.

- Fork one entry → that one entry lives in the override model; the rest inherit.
- "I love everything except your Venus material" → fork the Venus entries only.
- Default Model improvements continue to flow to every non-overridden entry automatically (with review flags where a forked parent changed, §4.3).

Sparse override models are the architectural expression of "build on the shoulders of the default without inheriting its maintenance."

---

## 12. Future AI assistance boundary

AI participation in authoring is governed by a single hard rule:

> **AI may draft. Humans approve. AI never silently edits approved content.**

### 12.1 What AI may do

- Create entries in `AI Suggested` (reading upload, §5)
- Propose a *new version* of an existing entry into a review state (never overwriting the approved version)
- Generate draft language for empty fields, left in `Draft`/`AI Suggested`
- Flag conflicts and staleness for human attention

### 12.2 What AI may never do

- Move any entry to `Approved`
- Mutate an `Approved` entry version in place
- Publish a manifest
- Consume its own unapproved suggestions in a user-facing surface

### 12.3 How AI proposes a change to approved content

```
Approved L2-PIH-SAT-12@v7
        │
   AI proposes change
        ▼
New version v8 created in state = AI Suggested / Needs Review
        │
   surfaced in review queue
        ▼
Human approves → v8 becomes Approved (v7 retained in history)
   or rejects  → v8 archived, v7 remains current
```

The approved version `v7` stays in force the entire time. There is no window in which AI-authored content is live without human approval. This is the Layer 2 expression of the constitutional boundary (FOUNDATIONAL_CONSTITUTION.md §7.6–7.9): the AI reveals a candidate; the human keeps judgment.

---

## 13. How the twelve design questions resolve

| # | Question | Resolved by |
|---|----------|-------------|
| 1 | Model representation | §1 entries-as-objects; §1.4 typed payloads |
| 2 | Inheritance | §2 Default→Override per-entry copy-on-write |
| 3 | Versioning | §3 two planes: entry log + model manifest |
| 4 | Approval states | §4 six-state lifecycle + state machine |
| 5 | Reading upload pre-population | §5 candidate pipeline → AI Suggested |
| 6 | Fallback | §6 entry- and field-level fallback to Default |
| 7 | Consultation pinning | §7 manifest binding + resolved digest |
| 8 | Engine/Navigator/Guardian consumption | §8 read-only resolved manifest |
| 9 | Wizard editing | §9 addressing + queues + sessions; no raw markdown |
| 10 | Review/export | §10 export-as-projection; DB is source of truth |
| 11 | Modularity | §2.2 + §11 sparse override models |
| 12 | Future AI assistance | §12 draft/approve boundary |

---

## 14. Recommended implementation phases

The Beta does not build any of this. These phases describe how the architecture is **promoted** into reality after Beta, smallest safe step first.

| Phase | Scope | Precondition |
|-------|-------|--------------|
| **L2-P0 — Default Model formalization** | Represent the single Beta default model as addressable, typed entries with stable IDs (no override, no versioning UI yet). Internal only. | Entry type registry (§1.2) frozen |
| **L2-P1 — Entry identity + version log** | Append-only entry versioning and stable IDs persisted. Still single-author (platform). | L2-P0 |
| **L2-P2 — Manifest + consumption contract** | Resolved-manifest compilation; Engine/Navigator/Guardian read manifests; consultations pin manifests (§7). | L2-P1 |
| **L2-P3 — Override models + inheritance** | Second model on top of Default; per-entry copy-on-write fork; field-level fallback (§2, §6). | L2-P2 |
| **L2-P4 — Approval lifecycle + review triggers** | Six-state machine, dependency/stale/fork-drift review flags (§4). | L2-P3 |
| **L2-P5 — Wizard workflow core** | Addressing, work queues, review sessions (§9). No content authoring AI yet. | L2-P4 |
| **L2-P6 — Reading upload pipeline** | Ontology Assistant extraction → AI Suggested entries with provenance/confidence/conflict (§5). | L2-P5 |
| **L2-P7 — AI assistance + style extraction** | AI drafting within the §12 boundary; separate Style profile (§5.4). | L2-P6 |
| **L2-P8 — Export/import projection** | Portable export as projection; ID-reconciled round-trip (§10). | L2-P5 |

Each phase requires its own implementation document, migration plan, validation gate, and rollback path before becoming active work.

---

## 15. Explicitly out of scope for this document

- Interpretive content of any kind (no Layer 2 entries written)
- Database schema / table definitions / migrations
- UI design (only the workflow beneath it)
- Pricing/packaging of professional authoring (see AI_CONSULTATION_ARCHITECTURE.md §17)
- The specific extraction model used by the Ontology Assistant
- Field-set definitions per entry type (a downstream schema task)

---

*AI-L2-1 complete. Architecture and product design only. No interpretive content. No migrations. No production code.*
