# AI Operator Constitution

Status: Required reading for AI-assisted project work.

Purpose: Keep AI sessions small, truthful, reversible, and budget-aware.

## First Law

Reveal structure. Preserve judgment.

The software reveals chart/geography structure. The human user preserves judgment.

## Budget-Aware Reading Rule

Do not read large doctrine files automatically.

Before reading large files, identify the task type and propose the smallest relevant reading set.

Ask the operator to approve the reading set.

Use this default menu:

- FOUNDATIONAL_CONSTITUTION.md — always relevant for major product decisions.
- TRUE_MASTER_PROJECT_PROFILE.md — project orientation.
- ARCHITECTURE_AND_BACKEND_CANON.md — backend, endpoints, data, persistence, calculations.
- BACKEND_ENGINE_ARCHITECTURE.md — engine-specific architecture.
- CORE_CONCEPTS_AND_LAYERS.md — product layers, ontology, intent, AI boundaries.
- INTERFACE_AND_DESIGN_CANON.md — UI, UX, map, profile, comparison, visual systems.
- AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md — AI behavior, prompts, Cursor discipline.
- FUTURE_FEATURES_ROADMAP.md — future features, roadmap quarantine.
- SYSTEM_BOUNDARIES_AND_CANONS.md — hard boundaries and non-goals.
- CODEBASE_DICTIONARY.md — exact live-code endpoints, schemas, constants.

## Task Routing

If touching UI, request permission to read INTERFACE_AND_DESIGN_CANON.md.

If touching backend, request permission to read ARCHITECTURE_AND_BACKEND_CANON.md and/or BACKEND_ENGINE_ARCHITECTURE.md.

If touching AI behavior, request permission to read AI_SYSTEMS_AND_PROMPT_PROTOCOLS.md.

If planning future features, request permission to read FUTURE_FEATURES_ROADMAP.md.

If changing schemas, endpoints, or contracts, request permission to read CODEBASE_DICTIONARY.md.

If unsure, ask before reading.

## Required Workflow

Do not code immediately.

1. Inspect only.
2. Plan only.
3. Wait for approval.
4. Implement the smallest coherent change.
5. Smoke test.
6. Report honestly.

## Versioning Rule

Do not overwrite prototypes unless explicitly instructed.

Prefer versioned files:

- prototype_settings_v1.html → prototype_settings_v2.html
- prototype_comparison_v1.html → prototype_comparison_v2.html
- continue v3, v4, etc.

Preserve old prototypes.

## Git Discipline

Before implementation:

- run git status
- identify uncommitted changes
- do not proceed if unexpected changes exist

Use local commits at stable plateaus.

Do not push to GitHub unless explicitly instructed.

## Required Closeout

Every implementation closeout must include:

1. Files created.
2. Files edited.
3. Files intentionally not touched.
4. Validation run.
5. Validation not run.
6. Browser checks if UI changed.
7. Rollback path.
8. Rejected scope.
9. Known uncertainty.
10. Next smallest safe step.

## Forbidden Behavior

Do not:

- claim success without validation
- invent endpoints, schemas, or files
- mix backend math with UI styling
- change multiple instability sources at once
- rewrite stable files for aesthetics
- silently drop saved-object semantics
- treat future roadmap as active implementation
- expose debug internals in commercial UI
- flatten human judgment into ranking or oracle language

