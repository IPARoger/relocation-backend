# Memory Maintenance Workflow

This document explains how project memory should be maintained without turning old chats, reports, and speculative ideas into an unstructured pile.

## Purpose

The goal is durable continuity. Cursor and external reviewers should be able to understand the product direction, current state, and important constraints without rereading every past chat.

This workflow is not an autonomous agent system. The user remains the final editor and approver.

**Institutional map (broader pipeline):** `docs/process/archaeology_and_synthesis_workflow.md` — raw → synthesis → doctrine → review bundle → rehydration. **Cadence:** `docs/process/doctrine_review_cycle.md`.

## Sources

Useful memory can come from:

- Cursor task reports in `cursor_latest_report.md`.
- AI reviews in `review_latest.md`.
- Proposed memory updates in `proposed_updates/`.
- Validation reports and narratives under `validation/`.
- Roadmap and design docs under `docs/`.
- Old chat transcripts or manual extraction documents.
- Consolidated archaeology synthesis notes in `memory_archaeology_raw/consolidated_notes/` (distilled from raw pending imports; preserves themes and rejected paths without replacing raw evidence).

## Mining Old Chats

When mining old chats, extract only material that changes future decisions:

- Durable product principles.
- Architectural decisions and rejected approaches.
- Validated behavior and known caveats.
- Unresolved questions.
- Edge cases and validation lessons.
- UX philosophy and design constraints.

Do not preserve every tactical debugging detail. Keep raw quotes only when wording matters or when they explain a decision that might otherwise be misunderstood.

## Processing Extraction Docs

Use extraction docs as raw input, not as final memory. A good extraction pass should:

1. Group items by taxonomy, not by chat chronology.
2. Separate confirmed facts from hypotheses.
3. Remove duplicate phrasing.
4. Promote stable principles into durable memory.
5. Move speculative or later-stage ideas into roadmap sections.
6. Keep implementation details in current state only while they remain true.

## Consolidating Raw Archaeology (optional phase)

After `pending_imports/` accrues structured extractions:

1. Read raw files **as-is** (repetition is signal).
2. Write or update themed synthesis notes under `memory_archaeology_raw/consolidated_notes/`.
3. Promote only stable principles into `ai_context/` and `docs/` with explicit **Implemented / Roadmap / Speculative** labeling.
4. Preserve raw files for traceability even when synthesis exists.

## Updating Durable Memory

Durable memory files should be edited deliberately:

- `core_product_truths.md` holds stable non-ephemeral principles.
- `decisions.md` holds decisions that should steer future implementation.
- `current_state.md` holds what is true now.
- `open_questions.md` holds unresolved issues and prompts for future judgment.
- `product_brief.md` holds the high-level product identity and philosophy.

The reviewer script may generate suggestions under `proposed_updates/`, but it should not overwrite these files automatically. The user or Cursor should review suggested updates, accept useful changes, and discard the rest.

## Memory Types

### Raw Extraction

Raw extraction is source material mined from chats, notes, transcripts, validation logs, or external reviews. It can be redundant, chronological, messy, and partially speculative.

Use it as input. Do not treat it as canonical.

### Durable Memory

Durable memory is compact, stable, and actively curated. It should be safe to hand to a future reviewer as context.

Examples:

- `core_product_truths.md`
- `product_brief.md`
- `decisions.md`

### Roadmap

The roadmap describes desired future direction and implementation sequence. It can include features that are not built yet, but should distinguish near-term from later-stage ideas.

Example:

- `docs/relocation_app_product_roadmap.md`

### Current Implementation State

Current state describes what is working, what remains caveated, and which files currently matter. It should change as implementation changes.

Example:

- `current_state.md`

### Speculative Future Ideas

Speculative ideas are possible directions, not commitments. Keep them out of core truths unless they become stable product principles.

Examples:

- Future map library migration.
- AI intake workflows.
- Marketplace or certification ecosystem.
- Advanced travel/road-trip mode.

## Merging raw archaeology (chronology and buckets)

Raw chat extracts in `memory_archaeology_raw/pending_imports/` are **chronological evidence**, not a single voice. When consolidating:

- **Prefer later evolved positions** for *current* architecture and UX doctrine when earlier and later extracts conflict (e.g. **truth_grid** over contour-first complacency; **staged ASC** over blocking full-stack overlays)—unless the question is explicitly still **open** in `open_questions.md` or `memory_archaeology_raw/consolidated_notes/open_questions_and_unresolved_areas.md`.
- **DeepSeek**-style extracts: useful for **strategy and philosophy**; treat implementation claims as **unverified** until checked against the repo.
- **Never delete** contradictory older takes from raw files; **do** reconcile before promoting into `ai_context/` (durable “current truth” is curated, not a transcript).

Keep **four buckets** separate when writing synthesis (see also `docs/institutional_memory_synthesis.md`):

1. **Implemented reality** — matches code and `current_state.md`.
2. **Durable philosophy** — principles that should survive refactors (truth, inspectability, tone).
3. **Speculative roadmap** — vision not shipped.
4. **Workflow infrastructure** — how the team runs AI, reviews, and archaeology (process, not the app’s features).

### Project memory vs chat memory

**Chat memory** dies with the session. **Project memory** is what makes collaboration **persistent**: themed notes under `memory_archaeology_raw/consolidated_notes/`, then promotion into `ai_context/` and `docs/` after human review. Treating the latest reply as authoritative without that step is the main **vibe-chaos** failure mode archaeology documents.

## Review Rhythm

After a meaningful task:

1. Cursor writes `cursor_latest_report.md`.
2. Run `scripts/ai_review_cursor_report.py`.
3. Read `review_latest.md`.
4. Read files in `proposed_updates/`.
5. Manually accept, edit, or reject proposed durable memory changes.
6. Commit only reviewed memory updates.

## Anti-Chaos Rules

- Do not let every interesting sentence become durable memory.
- Do not mix current facts with future hopes.
- Do not mix rejected approaches with recommended architecture.
- Do not overwrite curated docs from an AI proposal without human review.
- Do not preserve local secrets, private client notes, or API keys in durable memory.
