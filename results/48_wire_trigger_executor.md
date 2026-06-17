# Task 48 — Wire trigger → executor + schedule

## 1. cursor_trigger.yml execute job

```yaml
  execute:
    needs: notify
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install cursor-sdk
        run: pip install cursor-sdk
      - name: Launch Cursor cloud agent
        run: python scripts/relay_executor.py
        env:
          CURSOR_API_KEY: ${{ secrets.CURSOR_API_KEY }}
          RELAY_BRANCH: main
```

Workflow-level `concurrency: group: relay-executor` added.

## 2. relay.yml schedule line

```yaml
  schedule:
    - cron: '0 * * * *'
```

Live-path steps use `(github.event_name == 'schedule' || inputs.dry_run == false)` so scheduled runs are not blocked by missing workflow_dispatch inputs.

Relay execute step disabled (`if: false`) so planning commit → cursor_trigger executes once (avoids double cloud-agent launch).

## 3. relay_executor.py interface

No `--task` / `--file` flags. Interface:

- `python scripts/relay_executor.py [--dry-run]`
- Env: `CURSOR_API_KEY` (required live), `GITHUB_REPOSITORY` (auto in Actions), `RELAY_BRANCH` (default checkout), `CURSOR_MODEL` (optional)

Auto-discovers newest `tasks/NN_*.md` without matching `results/NN_*.md`.

Draft task referenced nonexistent flags; workflow adjusted to match (executor not modified).

## 4. YAML validation

```
.github/workflows/cursor_trigger.yml valid
.github/workflows/relay.yml valid
```

## 5. Status

**VERIFIED**
