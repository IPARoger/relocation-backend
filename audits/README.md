# audits/ — read-only inventory outputs

## Purpose

This folder holds read-only inventory / audit outputs (ownership maps, workflow
truth audits, dishonest-workflow inventories, feasibility studies). Audits never
modify runtime code, backend, schema, or data — they only describe current
truth.

See `docs/architecture/TWO_AGENT_RELAY_GOVERNANCE.md` for the binding rules.

## Contract

- An audit is diagnosis only. Producing an audit must result in zero code,
  backend, schema, or data changes.
- File naming: `audits/<NN>_<short-slug>.md`.
- Either agent may produce an audit when explicitly assigned, but the audit must
  be honest about evidence vs inference and must not self-select follow-up work.
- Use `audits/TEMPLATE.md` as the starting point.

## Lane rules (summary)

- Audits are read-only. No self-selecting the next task from an audit's findings.
- Findings are observations, not authorization. New work begins only when a human
  explicitly assigns it as a task in `tasks/`.
