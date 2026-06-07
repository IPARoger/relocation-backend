# AI Work Protocol

## Context Discipline

The AI must not proactively ingest project files.

The AI must only read:

1. Files explicitly referenced by the operator.
2. Files required to complete the current task.
3. Files directly referenced by an already-authorized document.

Do not recursively explore the repository.

Do not scan folders looking for additional context.

Do not ingest archaeology, historical documents,
old onboarding material, validation archives,
transfer documents, abandoned experiments,
or superseded doctrine unless explicitly requested.

When additional context appears useful,
ask for permission before expanding scope.

Repository size is not a license to read everything.

Context discipline is mandatory.

## Reading Priority

Before beginning work:

1. Read AI_WORK_PROTOCOL.md
2. Read AI_OPERATOR_CONSTITUTION.md
3. Determine which doctrine category applies:

   * UI work → UI/Product canon
   * Backend work → Architecture canon
   * AI work → AI canon
   * Planning work → Roadmap
4. Read only the minimum files required.

If uncertain, ask before expanding scope.

## Workflow Discipline

Before coding:

1. Inspect current files.
2. Propose plan.
3. Wait for approval.
4. Implement.
5. Run smoke tests.
6. Run browser verification if UI changed.
7. Report results.
8. Report uncertainty.
9. Report rollback path.
10. Report next smallest safe step.

## Versioning Discipline

Do not overwrite working prototypes.

Prefer:

prototype_x_v2.html
prototype_x_v3.html
prototype_x_v4.html

Preserve history unless explicitly instructed otherwise.

## Commit Discipline

Do not commit everything.

Use narrowly scoped commits.

Before committing:

* Show staged files.
* Show staged diff summary.
* Wait for approval.

Do not push unless explicitly instructed.

## Browser Verification

Any UI work requires browser verification.

Do not claim success until:

* page loads
* controls render
* interactions work
* console shows no blocking errors

Report browser findings explicitly.

## Constitution Relationship

AI_OPERATOR_CONSTITUTION.md is the primary entry point.

Before any task:

1. Read AI_OPERATOR_CONSTITUTION.md
2. Read AI_WORK_PROTOCOL.md
3. Follow all requirements in both documents
4. Determine the minimum doctrine required for the task
5. Read only those additional documents

AI_WORK_PROTOCOL.md governs:

- repository reading behavior
- scope expansion
- workflow discipline
- browser verification
- versioning discipline
- commit discipline

Its requirements are mandatory.

Task-specific doctrine is read only after these documents.

Required reading chain:

AI_OPERATOR_CONSTITUTION.md
        ↓
AI_WORK_PROTOCOL.md
        ↓
Task-specific doctrine

