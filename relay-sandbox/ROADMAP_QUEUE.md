# Sandbox relay queue (read-only — does not touch Chat 2)

Five S-sized audit steps to prove the relay loop. Write closeouts only under `relay-sandbox/results/`.
Do not modify application code except this sandbox tree.

| ID | Size | Item | Done when |
|----|------|------|-----------|
| SB-1 | S | Inventory: list every `relay_*.py` in `scripts/` with one-line purpose | closeout SB-1 |
| SB-2 | S | Grep `main_centerline` for `@app.post` / `@app.patch` / `@app.put` — count by path prefix | closeout SB-2 |
| SB-3 | S | Grep production JS (`map_CURRENT.html`, `app_shell.html`, `*.js` in repo root) for `fetch(` calls to port 8004 write methods (POST/PATCH/PUT) | closeout SB-3 |
| SB-4 | S | List smoke scripts under `smokes/` whose names contain `ownership` or `quarantine` | closeout SB-4 |
| SB-5 | S | Summarize SB-1..SB-4 findings in one consolidation closeout | closeout SB-5 |
| SB-6 | S | List relay env vars (keys only) from .env.local | closeout SB-6 |
| SB-7 | S | List files in relay-sandbox/results/ — names and sizes | closeout SB-7 |

## Rules
1. First incomplete SB-* only.
2. Read-only — no code changes, no commits.
3. Closeout path: `relay-sandbox/results/<NN>_*.md` with `**Roadmap ID:** SB-N`
| SB-8 | S | Count `*.md` files under `docs/architecture/` | closeout SB-8 |
| SB-9 | S | List top-level directories in repo root (names only) | closeout SB-9 |
| SB-10 | S | Grep `smokes/` for files referencing `port 8004` | closeout SB-10 |
| SB-11 | S | Count lines in `relay/CHAT_INSTRUCTIONS.md` | closeout SB-11 |
| SB-12 | S | List `validation/reports/*.json` filenames | closeout SB-12 |
| SB-13 | S | Count `.py` files in `scripts/` | closeout SB-13 |
| SB-14 | S | List all files in `relay-sandbox/tasks/` (names only) | closeout SB-14 |
| SB-15 | S | Count lines in `relay-sandbox/supervisor.py` | closeout SB-15 |
| SB-16 | S | List `.md` files in `relay/governance/` | closeout SB-16 |
| SB-17 | S | Count lines in `scripts/relay_planner.py` | closeout SB-17 |
| SB-18 | S | List `relay-sandbox/results/` files with line counts | closeout SB-18 |
| SB-19 | S | Count lines in `scripts/relay_executor.py` | closeout SB-19 |
| SB-20 | S | Summarize SB-13..SB-19 findings in one consolidation closeout | closeout SB-20 |
