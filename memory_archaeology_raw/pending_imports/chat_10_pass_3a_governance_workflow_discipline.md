# Source

- Origin: ChatGPT Chat 10 archaeology export
- Part: 3 of 5
- Title: Pass 3A — Governance and Workflow Discipline
- Role: Raw archaeology extract (canonical evidence for this slice)
- Privacy: Remove secrets before promotion into durable memory

---

# CHAT_10_RAW_ARCHAEOLOGY_PASS_3A.md

## Scope

PASS 3A focuses only on governance and workflow evolution during Chat 10:

* governance evolution
* workflow discipline evolution
* AI review chain evolution
* approval chain evolution
* commit discipline evolution
* browser validation discipline evolution

This is archaeology, not a cleaned summary. It preserves the project’s operational learning during this chat, including friction, corrections, objections, doctrine formation, and unresolved process questions.

---

# 1. GOVERNANCE EVOLUTION DURING CHAT 10

## 1.1 Original state at the beginning of this phase

At the beginning of this chat phase, the project already had substantial governance doctrine from earlier work:

* small reversible changes
* avoid Cursor hallucination
* one instability source at a time
* smoke tests before acceptance
* Git checkpoints at plateaus
* never trust “done” without evidence
* do not let AI rewrite stable code casually
* preserve archaeology
* explicit rollback paths
* exact terminal commands for the non-developer operator

But the workflow had drifted during the rapid UI/design prototyping phase. The earlier backend/math period had strong validation discipline because geometry bugs were obvious trust risks. Once the work shifted into settings, comparison pages, city pages, color prototypes, and HTML mockups, it became less clear whether the same rigor should apply.

The user explicitly questioned this:

Was the smoke-test and Git discipline only for backend coding, or should it also apply to UI prototyping?

This became a major governance turning point.

The answer that emerged:

The discipline applies to UI too.

The risk is different, but still real. A UI prototype can still:

* overwrite useful work
* drift from doctrine
* introduce unstable assumptions
* waste money
* confuse the design direction
* accidentally stage/deleting unrelated files
* leave the repo dirty
* create false progress

Therefore governance is not only for math.

Governance is for any AI-assisted work that can create project state.

---

## 1.2 Cursor cost and trust pressure

The chat happened under strong emotional pressure from prior Cursor failures. The user had already experienced expensive AI loops where Cursor consumed money without producing useful work. This was especially acute after the Rain/Virga experiment, which had become a draining rabbit hole.

The user repeatedly emphasized:

* do not waste money
* do not let Cursor do broad speculative work
* do not let it code before planning
* do not accept claims without browser checks
* do not trust “it works” without proof
* do not let AI read everything and spend tokens unnecessarily

This context drove the creation of budget-aware governance.

The central insight:

AI governance is not only about correctness.

It is also about cost containment.

A tool can be wrong and expensive.

A tool can be “almost right” and still destructive because it creates repeated $3–$10 revision loops.

Thus the governance system needed to manage:

* correctness
* scope
* reading budget
* implementation budget
* approval gates
* repository hygiene

---

## 1.3 Repository reading discipline

One of the strongest governance developments in this chat was the formalization of reading discipline.

Earlier, the project had many doctrine documents, transfer docs, archaeology files, validation reports, design archives, screenshots, and onboarding documents. Cursor could theoretically read too much and burn money. The user worried that telling Cursor to “read current files” could become expensive if it scanned broad directories.

This led to a refined doctrine:

Cursor should not proactively ingest project files.

Cursor should only read:

1. Files explicitly referenced by the operator.
2. Files required to complete the current task.
3. Files directly referenced by an already-authorized document.

It should not:

* recursively explore the repository
* scan folders looking for context
* ingest archaeology unless asked
* read historical documents by default
* treat repository size as permission to read everything

When additional context appears useful, it must ask permission.

This became the AI Work Protocol.

---

## 1.4 Governance chain

A formal reading chain was created:

AI_OPERATOR_CONSTITUTION.md
↓
AI_WORK_PROTOCOL.md
↓
Task-specific doctrine

This chain was not merely symbolic. It was intended as the single entry point for Cursor and future AI sessions.

The logic:

* AI_OPERATOR_CONSTITUTION.md is the primary entry point.
* It tells Cursor to read AI_WORK_PROTOCOL.md.
* AI_WORK_PROTOCOL.md governs repository reading behavior, scope expansion, workflow discipline, browser verification, versioning discipline, and commit discipline.
* Only then does the AI read task-specific doctrine.

This reduced ambiguity. Cursor should not begin by scanning the repository. It should not decide to read 40 files because the project is complex. It should pass through the constitution and work protocol first.

The user asked whether this doctrine should also be preserved for future ChatGPT sessions. The answer was yes: the governance chain must be included in transfer documents and archaeology so new chats continue enforcing it.

---

## 1.5 `.cursorignore` and blue-dot accessible doctrine set

A major operational issue arose around Cursor access to the repository.

The user clarified that the project had been set up so Cursor should only have access to a limited directory or limited “blue dotted” files. The `.cursorignore` file excludes:

* generated exports
* transfer docs
* audits
* old onboarding
* visual design archives
* product training
* process docs
* future docs
* validation folders
* memory archaeology
* archives
* backups
* generated Python noise
* venv
* large raw consolidations

But it explicitly does not ignore active canon library folders:

* docs/bootstrap/
* docs/constitutional/
* docs/product/
* docs/architecture/
* docs/ai/
* docs/resolutions/

The user wanted to ensure the mini-governance doctrine was placed somewhere Cursor could read it and that `.cursorignore` would not hide it accidentally.

This produced a governance split:

* Heavy archaeology and historical material should be protected from routine AI ingestion.
* Active governance entry points should remain accessible.
* Cursor must not read active docs unless task-required or explicitly referenced.

This is subtle: accessibility is not permission.

The docs are available, but Cursor still needs discipline.

---

# 2. WORKFLOW DISCIPLINE EVOLUTION

## 2.1 Plan-first discipline

A repeated workflow doctrine was reinforced:

Do not code immediately.

Plan first.

Wait for approval.

This was especially important during:

* settings page revisions
* comparison page architecture
* city profile page architecture
* governance file creation
* new prototype files

The user reminded the system that the standard earlier workflow had been:

1. Don’t write.
2. Plan.
3. Tell me what you’re going to do.
4. Revise the plan two or three times if needed.
5. Only then code.

The user acknowledged this takes longer and can cost more, but it prevents expensive failures.

This became especially important when using expensive models like Opus or Composer/Sonnet in Cursor.

A key tension emerged:

* Planning costs money.
* Not planning can cost much more.

The working conclusion:

Use plan-first discipline for new surfaces and architecture.
Use smaller direct prompts for already-approved micro-corrections.

---

## 2.2 Versioning discipline: v1, v2, v3, v4

The user strongly prefers versioned prototype files rather than overwrites.

The assistant had sometimes suggested overwriting v1. The user corrected this:

Use v2, v3, v4 versions to preserve history.

This became a durable UI prototyping rule.

Applied examples:

* prototype_settings_v1.html
* prototype_settings_v2.html
* comparison_v2.html
* comparison_v3.html
* comparison_v4.html
* comparison_v5.html
* city_profile_v1.html
* city_profile_v2.html
* city_profile_v3.html
* city_profile_v4.html

Rationale:

* easy rollback
* compare iterations visually
* preserve design archaeology
* avoid losing useful old ideas
* reduce risk of AI overwriting a working prototype
* support plateau commits

This is especially important because many prototypes are exploratory. A “bad” version may contain a good idea. Versioned files protect that.

---

## 2.3 Whole-file and terminal-command preference

The user repeatedly emphasized:

I do not do document surgery.

Provide complete terminal commands.

Do not tell the user to manually edit a file.

This matters because the user is not a developer and because manual surgery creates errors. Commands should be copy-pasteable.

Examples:

* append governance section with `cat >> file <<'EOF'`
* immediately run `grep`
* paste output back
* commit with exact `git add` target list
* start server with exact `python3 -m http.server 8000`

The project already had a memory that terminal commands must include verification. This chat reinforced it.

The operational rule:

When giving commands, include verification commands and interpret the output before proceeding.

Echo messages are not enough.

---

## 2.4 One change type at a time

During the design phase, there was temptation to mix:

* UI polish
* data architecture
* backend connection
* Supabase
* API sourcing
* font/glyph system
* mobile adaptation
* profile architecture

The user repeatedly stepped back and asked what should be done next.

The discipline that emerged:

* Finish current surface enough to learn from it.
* Do not chase every design refinement forever.
* Get to a good plateau.
* Commit.
* Move to the next product surface.
* Return later with standards.

This became a design-stage adaptation of the earlier “one instability source” backend doctrine.

In UI terms:

Do not solve fonts, colors, glyphs, animations, Supabase, and mobile while still deciding layout.

---

# 3. AI REVIEW CHAIN EVOLUTION

## 3.1 Multi-model role separation

During this chat, multiple AI roles emerged:

* ChatGPT as governance/product architect.
* Cursor Composer as implementation interface.
* Sonnet as careful builder/reviser.
* Opus as deeper architecture reviewer.
* Composer 2.5 as a possible LLM inside Cursor, not the Composer interface itself.
* Cursor as coding agent requiring discipline.

There was confusion about “Composer” because the user clarified that Composer 2.5 is an LLM in Cursor, while the assistant had meant the Composer interface.

This clarified future prompts:

Specify both:

* model
* interface mode

Example:

Use Sonnet for architecture-sensitive build.
Use Composer interface for implementing file edits.
Use Composer 2.5 only for lighter or cleanup tasks if appropriate.

---

## 3.2 Opus vs Sonnet vs Composer

The chat produced practical model guidance.

For architecture review:

* Opus can be useful.
* It is expensive.
* It should be used for high-value reasoning, not repeated tiny fixes.

For building layout prototypes:

* Sonnet is generally strong.
* It can preserve constraints better than cheaper/looser models.
* It still needs plan-first discipline.

For small HTML/CSS cleanup:

* Composer 2.5 may be acceptable.
* It should not be trusted with large architecture unless tightly constrained.

For terminal commits:

* No LLM needed.
* Use direct commands.

This reduced unnecessary spending.

---

## 3.3 Cursor must report browser checks

The user explicitly required that Cursor report browser checks before accepting work.

This became part of prompts:

* open page
* verify render
* test interactions
* report failures
* report console errors
* state if browser could not access localhost
* do not claim success if manual verification is needed

The user added:

Make Cursor report browser checks before you accept the work.

This became important because Cursor repeatedly said things were working even when the user later found the page not loading or UI broken.

---

## 3.4 AI closeout reports

Cursor closeout reports became a recurring format:

* files created
* files touched
* files not touched
* validation run
* browser result
* git status
* known uncertainties
* rollback path

This aligned with the project’s governance doctrine.

However, a problem emerged:

Cursor sometimes claimed browser verification could not be performed because its IDE browser could not reach localhost.

This is acceptable only if reported clearly.

Then the user must manually verify.

The assistant repeatedly insisted that “validated” must distinguish:

* static validation
* HTTP 200
* manual browser verification
* automated browser screenshot verification

This precision matters.

---

# 4. APPROVAL CHAIN EVOLUTION

## 4.1 Plan approval before coding

The approval chain stabilized as:

1. Cursor reads authorized files only.
2. Cursor proposes plan.
3. User/assistant review.
4. User approves with amendments.
5. Cursor builds new versioned file.
6. Cursor validates.
7. User browser-reviews.
8. Small correction prompt.
9. New version.
10. Commit at plateau.

This chain was applied to:

* comparison pages
* city profile pages
* governance docs

The user sometimes said enough planning had already occurred and only final amendments were needed. This created a refinement:

Do not keep asking for full plan passes once architecture is already approved.

At that point use small correction prompts.

---

## 4.2 “Approved with amendments” pattern

Several build stages used:

Approved with amendments.

This allowed avoiding another full planning loop while preserving control.

Example:

City Profile v1 had several open decisions answered:

* 4+3 snapshot grid
* generic Back link
* EUR primary/USD secondary
* no CTAs
* orientation line
* Stable instead of High
* For Your Stated Intentions

The user wanted only those corrections passed to Cursor, not an entirely new build prompt.

This became a useful micro-approval pattern.

---

## 4.3 Human browser review remains decisive

Even when Cursor reported static checks passing, the user’s browser review revealed:

* not loading because server not running
* city hide behavior wrong
* columns misaligned
* info popup useless
* accordion jumping
* healthcare opening above
* formatting issues
* typography hierarchy issues
* population over-deemphasis
* currency selector in wrong place

Therefore browser review by the user remains a core approval gate.

Cursor’s closeout is not final acceptance.

It is a handoff for human QA.

---

# 5. COMMIT DISCIPLINE EVOLUTION

## 5.1 Local plateau commits

The user wanted commits at meaningful plateaus, not after every micro-change.

The earlier doctrine:

* commit after stable work
* do not crowd GitHub with every iteration
* local commit first
* push later at larger milestone

This was reaffirmed.

During this chat, commits included:

* settings/theme/overlay harness
* AI operator constitution
* comparison v5 prototype
* comparison and city profile prototypes

The latest confirmed log showed:

* `62e2222 Add comparison and city profile prototypes`
* `776a39a Add comparison page v5 prototype`
* `2408f24 Add AI operator constitution`
* `8aa659f Add settings prototypes and overlay color test harness`

This confirmed commit discipline was functioning, even though working tree remained dirty.

---

## 5.2 Scoped commits only

A major risk emerged when git status revealed:

* many modified files
* many deleted docs
* hundreds/thousands of untracked files

Cursor initially reported 46 deleted doctrine files.

This was alarming.

The project had moved or reorganized docs, but doctrine should not be blindly deleted.

The user asked if deleted docs could be recovered.

The response became:

Do not commit the whole tree.

Only commit explicitly approved files.

This led to narrow scoped commits.

Examples:

For settings/theme/overlay harness:

* prototype_settings_v1.html
* prototype_settings_v2.html
* theme/relocation_themes.css
* theme/relocation_theme.js
* map_SANDBOX_overlay_color_test.html
* fixtures/overlay_fixture_real.geojson

For AI constitution:

* ai_context/AI_OPERATOR_CONSTITUTION.md only

For comparison/city profile:

* comparison_v5.html
* city_profile_v1.html
* city_profile_v2.html
* city_profile_v3.html
* city_profile_v4.html

This protected the project from accidentally committing deleted doctrine or noisy artifacts.

---

## 5.3 Verification before commit

The commit prompts included:

* `git status --short | grep ...`
* `git add exact files`
* `git diff --cached --stat`
* `git diff --cached --name-status`
* `git commit -m "..."`
* `git status --short`

The purpose:

Ensure staged set exactly matches intended files.

Do not rely on Cursor’s internal staging.

Do not use broad `git add .`.

Do not use GitHub push button.

This was crucial because the working tree was huge and dirty.

---

## 5.4 Commit success verification

The user asked to confirm commits.

The assistant could not confirm from a screenshot alone. It requested Git output.

Eventually the user provided:

`git log --oneline -5`

showing:

* `62e2222 (HEAD -> checkpoint/pre-phase-2-3) Add comparison and city profile prototypes`
* `776a39a Add comparison page v5 prototype`
* `2408f24 Add AI operator constitution`
* `8aa659f Add settings prototypes and overlay color test harness`
* `3fcfa3d Add read-only chart record library truth panel`

This confirmed the commit succeeded.

Important distinction preserved:

Commit exists.

Working tree is still dirty.

These are separate facts.

---

# 6. BROWSER VALIDATION DISCIPLINE EVOLUTION

## 6.1 Server not running issue

A concrete browser validation failure occurred when the city profile page did not load.

Terminal output showed:

* file existed
* port 8000 had no server
* curl failed

The issue was not HTML.

The issue was:

No server running.

Command provided:

`python3 -m http.server 8000`

Then open:

`http://127.0.0.1:8000/city_profile_v1.html`

This reinforced an old lesson:

Do not confuse server/runtime state with code failure.

---

## 6.2 Cursor IDE browser limitation

Cursor repeatedly reported that the IDE browser could not access localhost or 127.0.0.1.

This created a validation classification:

* Static validation can be automated.
* HTTP 200 can be checked by curl.
* Browser visual verification may require user’s real browser.
* Cursor must not imply visual validation if it could not actually see the page.

This distinction became part of closeout reporting.

---

## 6.3 UI interaction validation

Several issues only appeared through manual clicking:

* Hide city did not realign columns.
* Hidden city stub appeared far right.
* Reorder worked but was too abrupt.
* Replace popup was unnecessary.
* Accordion opened wrong panel.
* Accordion jumped page down.
* Healthcare opened above.
* Currency selector was in wrong place.
* Dropdown animation caused disorientation.

These cannot be caught with `node --check`.

Therefore UI validation requires:

* load page
* click all interactive controls
* inspect layout after state changes
* verify alignment
* verify no unexpected scroll
* verify hidden/show state
* verify modals
* verify accordions
* verify tab/carousel behavior

This became especially important as prototypes became interaction-heavy.

---

## 6.4 Static checks are necessary but insufficient

Cursor repeatedly ran:

* node syntax check
* grep pattern checks
* HTTP 200
* file line count
* file touched list

These are useful.

But they do not validate design.

The chat reinforced the hierarchy:

1. Syntax check.
2. HTTP/server check.
3. Visual browser check.
4. Interaction check.
5. Human product review.

All five matter.

---

# 7. FINAL STATE OF GOVERNANCE AFTER CHAT 10

## 7.1 Active governance chain

The active chain established:

AI_OPERATOR_CONSTITUTION.md
↓
AI_WORK_PROTOCOL.md
↓
Task-specific doctrine

This is now a project artifact and must be included in future transfer.

---

## 7.2 Active workflow discipline

For significant work:

1. Read only required files.
2. Plan first.
3. Wait for approval.
4. Create new versioned file.
5. Validate syntax/server.
6. Browser-check if possible.
7. Report files changed.
8. Do not stage/commit unless asked.
9. Commit only exact files at plateau.
10. Preserve rollback.

---

## 7.3 Active commit discipline

Rules:

* no `git add .`
* no broad commits
* no committing docs deletions accidentally
* local commit at plateau
* no push unless explicitly requested
* staged diff must be inspected before commit
* commit success must be verified with `git log`

---

## 7.4 Active browser validation discipline

Rules:

* HTTP 200 is not visual validation
* static JS check is not interaction validation
* Cursor must report if browser cannot load localhost
* user’s browser review remains decisive
* manual QA notes are valid evidence
* UI bugs get small versioned correction passes

---

# 8. UNRESOLVED GOVERNANCE QUESTIONS

## 8.1 When to push to GitHub

Local commits exist.

Push strategy remains unresolved.

Likely:

* push at major plateau
* not every prototype
* not while working tree includes unresolved deletion/noise issues

## 8.2 Dirty tree cleanup

The working tree remains extremely dirty.

Open questions:

* which deleted docs are intentional moves?
* which should be restored?
* which untracked assets are real?
* which should be ignored?
* which should be committed later?
* should there be a cleanup branch?

This remains a major operational risk.

## 8.3 Cursor file access

The blue-dot / `.cursorignore` strategy exists, but final accessible set may need audit.

Open question:

* does Cursor reliably obey intended access boundaries?
* should active governance docs be duplicated in a smaller `ai_context/` folder?
* should there be a one-file Cursor entry point?

## 8.4 How much planning is enough?

The chat revealed tension:

* too little planning causes wasted work
* too much planning costs money and slows momentum

Current doctrine:

* full plan for new architecture/page
* small correction prompt for post-approval refinements

Still requires judgment.

## 8.5 Browser automation

Cursor’s IDE browser limitation means manual browser validation is still needed.

Future possibility:

* local Playwright script
* screenshot validation
* simple browser smoke scripts

Not implemented.

---

# 9. PASS 3A CONCLUSION

During Chat 10, governance matured from a backend/math safety protocol into a full product-building operating system.

The key evolution:

Governance is not only for calculation correctness.

Governance applies to:

* design
* UI prototypes
* HTML pages
* comparison systems
* city profiles
* documentation
* Cursor reading behavior
* commits
* browser validation
* cost control

The project now has a clearer operational chain:

* constrained reading
* plan first
* approve
* build new version
* validate
* human review
* scoped commit
* preserve archaeology

This chain emerged because the project is now large enough that uncontrolled AI behavior is not merely annoying; it is a structural risk.

The central governance lesson of Chat 10:

AI can still help build the project, but only inside a disciplined operating system that controls reading scope, implementation scope, validation, cost, commits, and truth claims.
</user_query>
