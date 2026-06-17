# AUDIT: 07_GITHUB_ACTIONS_VISIBILITY_AUDIT

Task: `07_GITHUB_ACTIONS_VISIBILITY_AUDIT`
Mode: read-only diagnosis, with requested audit/result outputs only
Result: **NOT VERIFIED**

## Inspection scope honored

Inspected only:

- `.github/workflows/relay.yml`
- `git branch -a`
- `git remote -v`

No production files were modified. No commit was created. No push was attempted.

## Evidence

### `.github/workflows/relay.yml`

The workflow file exists in the currently checked-out local branch and begins:

```yaml
name: two-agent-relay

on:
  workflow_dispatch:
    inputs:
      dry_run:
        description: "Dry run (no paid API calls, no changes)"
        type: boolean
        default: true
```

The workflow has a manual `workflow_dispatch` trigger and a `dry_run` boolean input.
The trigger is correctly formed for a manually runnable workflow once GitHub has discovered the workflow file.

### Branches

`git branch -a` reports:

```text
* checkpoint/pre-phase-2-3
  main
  remotes/origin/checkpoint/pre-phase-2-3
  remotes/origin/main
  remotes/origin/rendering-refactor
```

The currently checked-out branch is `checkpoint/pre-phase-2-3`.

### Remote

`git remote -v` reports:

```text
origin	https://github.com/IPARoger/relocation-backend.git (fetch)
origin	https://github.com/IPARoger/relocation-backend.git (push)
```

## Answers

### 1. Does `relay.yml` exist only on `checkpoint/pre-phase-2-3`?

**Locally, yes as observed from the current checkout:** `.github/workflows/relay.yml` exists while the active branch is `checkpoint/pre-phase-2-3`.

**Remote visibility is not verified in this audit** because the allowed inspection set did not include `git status`, `git log`, `git ls-tree`, `git show`, GitHub API, or a push. From the previous failed push state in this session, the likely situation is that the workflow commit exists locally only and is not present on GitHub yet.

### 2. Does `main` contain `relay.yml`?

**Not verified under the requested inspection limit.** Proving this directly would require inspecting the `main` tree, for example with `git ls-tree main -- .github/workflows/relay.yml` or `git show main:.github/workflows/relay.yml`, but those commands were outside the explicit inspection list.

Given the current checkout is `checkpoint/pre-phase-2-3` and the workflow was scaffolded there, the likely answer is **no, `main` does not contain `relay.yml` yet**.

### 3. Is `workflow_dispatch` present and correctly formed?

**Yes.** The workflow contains:

```yaml
on:
  workflow_dispatch:
    inputs:
      dry_run:
        description: "Dry run (no paid API calls, no changes)"
        type: boolean
        default: true
```

That is the correct shape for a manual GitHub Actions workflow trigger with one boolean input.

### 4. Could GitHub Actions visibility require the workflow to exist on the default branch before it appears in the Actions UI?

**Yes.** GitHub commonly discovers and lists workflows from the repository's default branch. A workflow that exists only on a non-default branch, or only in an unpushed local commit, may not appear in the Actions UI until the workflow file exists on GitHub in the default branch, or until GitHub has otherwise indexed the workflow from a pushed branch/PR context.

This is the most plausible reason the workflow is not visible: the file is not currently discoverable by GitHub's Actions UI from the default branch, and may not have been pushed to GitHub at all.

### 5. What is the minimum-risk path to run the first dry-run workflow?

Minimum-risk path:

1. Keep the workflow manual-only and dry-run-default exactly as written.
2. Push the existing relay automation commit to `checkpoint/pre-phase-2-3` once GitHub authentication is available.
3. Open a PR from `checkpoint/pre-phase-2-3` into `main` so GitHub can see the workflow diff without merging production code blindly.
4. Merge only the scoped relay scaffold into `main` after review, because GitHub Actions visibility is most reliable when `.github/workflows/relay.yml` exists on the default branch.
5. Run **Actions -> two-agent-relay -> Run workflow** with `dry_run = true` only.
6. Confirm the dry-run output calls only:
   - `relay_preflight.py --dry-run`
   - `relay_planner.py --dry-run`
   - `relay_executor.py --dry-run`

This path does not run live automation, does not spend API money, and does not create an agent PR. It only proves that GitHub can discover and execute the manual dry-run workflow.

## Production impact

- No production code inspected beyond the authorized workflow file.
- No production code changed.
- No commit created.
- No push attempted.
- No live automation run.
- No PR created.
- No secrets inspected or committed.

## Verification status

**NOT VERIFIED** because the strict inspection scope did not allow direct verification of whether `main` contains `.github/workflows/relay.yml`, nor whether the local workflow commit exists on the remote branch. The likely diagnosis is strong: GitHub Actions cannot show/run a workflow that is only local or not present on the default branch.
