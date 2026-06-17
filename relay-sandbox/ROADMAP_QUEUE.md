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

## Rules
1. First incomplete SB-* only.
2. Read-only — no code changes, no commits.
3. Closeout path: `relay-sandbox/results/<NN>_*.md` with `**Roadmap ID:** SB-N`
