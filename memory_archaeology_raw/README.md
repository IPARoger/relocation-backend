# Memory Archaeology Raw Intake

This folder is a low-friction intake area for raw archaeology outputs from old chats and external review sessions.

Do not process, summarize, deduplicate, or classify material at paste time. The first goal is traceability.

## Workflow

1. Raw archaeology outputs from old chats are pasted directly into files under `pending_imports/`.
2. Raw outputs should remain unedited initially.
3. Cursor later:
   - classifies the material,
   - deduplicates it,
   - extracts durable truths,
   - updates permanent docs.
4. Original raw outputs are preserved for traceability.
5. Repetitions are valuable signals and should not be aggressively removed during intake.

## Folder Roles

- `pending_imports/`: raw incoming archaeology dumps that have not been processed yet.
- `processed/`: raw files that have already been reviewed and mined for durable memory.
- `consolidated_notes/`: intermediate organized notes created during processing.
- `rejected_or_duplicate/`: material that was reviewed and intentionally not promoted, usually because it was duplicate, obsolete, or not durable.

## Naming Conventions

Use stable semantic names when pasting known chat outputs (examples in `pending_imports/`):

- `chat_01_early_architecture_and_contours.md`
- `chat_02_truth_grid_and_validation.md`
- `chat_03_ux_overlay_and_map_design.md`
- `chat_04_ai_strategy_and_professional_workflows.md`
- `chat_05_travel_transits_and_future_modes.md`
- `chat_06_memory_and_workflow_infrastructure.md`
- `chat_07_additional_archaeology_and_overflow.md`
- `current_chat_truth_grid_memory_and_infrastructure.md`
- `deepseek_chat_01_strategic_and_philosophical.md`
- `deepseek_chat_02_additional_strategy.md`

For additional imports, use:

- `chat_08_topic_short_name.md`, etc.
- `source_name_YYYYMMDD.md` for named external sources.
- `topic_short_name.md` only when the source is not chronological.

Avoid names with secrets, client names, or private identifying information.

## Recommended Paste Format

At the top of each raw file, optionally add a short source note:

```markdown
# Source

- Origin: old Cursor chat / ChatGPT chat / DeepSeek chat / manual notes
- Approximate date:
- Scope:
- Privacy notes:

# Raw Extraction

Paste the raw output below this line without editing.
```

If adding a header slows intake down, skip it and paste the raw output directly.

## Memory Types

### Raw Extraction

Raw extraction is the unedited source material pasted into `pending_imports/`. It may be repetitive, messy, chronological, or speculative.

Raw extraction is evidence, not canonical truth.

### Durable Memory

Durable memory is curated, compact, and stable. It belongs in `ai_context/` or long-lived docs after review.

Examples:

- `ai_context/core_product_truths.md`
- `ai_context/decisions.md`
- `ai_context/product_brief.md`

### Current Implementation State

Current implementation state describes what is true in the code now. It should change as features, bugs, and validation status change.

Example:

- `ai_context/current_state.md`

### Future Speculative Ideas

Future speculative ideas are possible directions, not commitments. They may belong in a roadmap after review, but should not be promoted into core truths unless they become durable principles.

Examples:

- Later AI workflows.
- Map library migration.
- Marketplace or certification ideas.
- Travel mode.

## Processing Rule

Processing happens later. During intake, preserve the raw material as-is.
